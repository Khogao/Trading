import os
import time
import hmac
import hashlib
import json
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

load_dotenv()

APP = FastAPI(title="Trading Alert Receiver (PoC)")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto")  # 'claude' | 'gemini' | 'auto'
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Simple in-memory dedupe store (bar_time keyed)
seen_alerts = {}
DEDUP_TTL = int(os.getenv("DEDUP_TTL_SECONDS", "30"))


class NormalizedAlert(BaseModel):
    symbol: str
    timeframe: Optional[str]
    source: Optional[str]
    signal: Optional[str]
    price: Optional[float]
    volume: Optional[float]
    cvd: Optional[float]
    raw: Optional[dict]


def dedupe_key(a: NormalizedAlert) -> str:
    # create a simple key
    return f"{a.source}|{a.symbol}|{a.timeframe}|{a.signal}|{a.price}".lower()


async def call_llm_classify(alert: NormalizedAlert) -> dict:
    # If no API key, fallback to a lightweight heuristic
    if (LLM_PROVIDER in ("claude", "auto") and CLAUDE_API_KEY) or (LLM_PROVIDER in ("gemini", "auto") and GEMINI_API_KEY):
        # call appropriate provider; this PoC uses a tiny POST shape for either
        prompt = {
            "task": "classify",
            "payload": alert.dict()
        }
        headers = {"Content-Type": "application/json"}
        if CLAUDE_API_KEY and (LLM_PROVIDER in ("claude", "auto")):
            headers["Authorization"] = f"Bearer {CLAUDE_API_KEY}"
            url = os.getenv("CLAUDE_API_URL", "https://api.anthropic.com/v1/claude-invoke")
        elif GEMINI_API_KEY and (LLM_PROVIDER in ("gemini", "auto")):
            headers["Authorization"] = f"Bearer {GEMINI_API_KEY}"
            url = os.getenv("GEMINI_API_URL", "https://api.google.com/v1/gemini-invoke")
        else:
            url = None

        if url:
            try:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    r = await client.post(url, headers=headers, json=prompt)
                    r.raise_for_status()
                    return r.json()
            except Exception as e:
                return {"error": "llm_call_failed", "message": str(e)}

    # Heuristic fallback
    score = 50
    tags = []
    reason = []
    if alert.cvd is not None:
        if alert.cvd > 0:
            score += 10
            tags.append("cvd_bull")
        else:
            score -= 10
            tags.append("cvd_bear")
    if alert.volume is not None:
        if alert.volume > 1.5:  # arbitrary multiplier; Pine should send relative volume
            score += 15
            tags.append("volume_spike")
    if alert.signal:
        s = alert.signal.lower()
        if "buy" in s or "bull" in s:
            score += 10
            tags.append("price_action_bull")
        if "sell" in s or "bear" in s:
            score -= 10
            tags.append("price_action_bear")

    classification = "opportunity" if score >= 60 else ("risk" if score <= 40 else "neutral")
    return {
        "classification": classification,
        "score": max(0, min(100, score)),
        "tags": tags,
        "reason": ", ".join(tags) or "heuristic",
    }


async def notify_telegram(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text})


def normalize_tradingview(payload: dict) -> NormalizedAlert:
    # Many Pine scripts send a plain string in 'alert_message' or 'message'
    # Try common fields first
    symbol = payload.get("symbol") or payload.get("ticker") or payload.get("exchange")
    timeframe = payload.get("timeframe") or payload.get("tf")
    source = payload.get("source") or payload.get("script") or payload.get("indicator")
    raw_msg = payload.get("alert_message") or payload.get("message") or payload.get("text") or payload

    # attempt to parse JSON message embedded
    signal = None
    price = None
    volume = None
    cvd = None
    if isinstance(raw_msg, str):
        try:
            parsed = json.loads(raw_msg)
            signal = parsed.get("signal") or parsed.get("type")
            price = parsed.get("price")
            volume = parsed.get("volume")
            cvd = parsed.get("cvd")
        except Exception:
            # fallback: simple heuristics
            if "buy" in raw_msg.lower():
                signal = "buy"
            if "sell" in raw_msg.lower():
                signal = "sell"
    elif isinstance(raw_msg, dict):
        signal = raw_msg.get("signal") or raw_msg.get("type")
        price = raw_msg.get("price")
        volume = raw_msg.get("volume")
        cvd = raw_msg.get("cvd")

    return NormalizedAlert(
        symbol=symbol or "",
        timeframe=timeframe,
        source=source,
        signal=signal,
        price=float(price) if price is not None else None,
        volume=float(volume) if volume is not None else None,
        cvd=float(cvd) if cvd is not None else None,
        raw=payload,
    )


@APP.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    try:
        payload = await request.json()
    except Exception:
        try:
            payload = json.loads(body.decode('utf-8'))
        except Exception:
            payload = {"raw": body.decode('utf-8')}

    alert = normalize_tradingview(payload)
    key = dedupe_key(alert)
    now = time.time()
    # dedupe
    if key in seen_alerts and now - seen_alerts[key] < DEDUP_TTL:
        return {"status": "deduped"}
    seen_alerts[key] = now

    llm_result = await call_llm_classify(alert)

    out = {"alert": alert.dict(), "llm": llm_result}

    # fire notification (telegram) asynchronously
    try:
        text = f"{alert.symbol} {alert.timeframe} {alert.signal} => {llm_result.get('classification')} ({llm_result.get('score')})"
        await notify_telegram(text)
    except Exception:
        pass

    return out


@APP.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(APP, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
