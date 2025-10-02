# Trading Alert Receiver (PoC)

This small PoC receives TradingView Pine webhooks, normalizes the payload, calls an LLM (Claude/Gemini) to classify the signal, and optionally notifies via Telegram.

Files:

- `server.py` — FastAPI webhook receiver and LLM wrapper (PoC heuristic fallback if no API key)
- `requirements.txt` — Python dependencies
- `pine_alert_template.txt` — example JSON alert template to copy into Pine scripts
- `test_send.ps1` — PowerShell script to POST a sample webhook to the server

Quick start (Windows PowerShell):

1. Create and activate a virtual environment and install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables (optionally for LLM/Telegram):

```powershell
$env:CLAUDE_API_KEY="your_claude_key"
$env:GEMINI_API_KEY="your_gemini_key"
$env:TELEGRAM_BOT_TOKEN="bot_token"
$env:TELEGRAM_CHAT_ID="chat_id"
```

3. Run server:

```powershell
python server.py
```

4. Send a test webhook in a different PowerShell window:

```powershell
.\test_send.ps1
```

Notes:

- For TradingView use a public URL (ngrok or public VPS) as TradingView cannot reach localhost unless using a tunnel.
- The PoC attempts to call an LLM endpoint if keys are provided; those endpoints/URLS are placeholders and may need updating for your Claude/Gemini provider.
- I intentionally did not commit any API keys.
