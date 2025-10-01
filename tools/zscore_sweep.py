"""zscore_sweep.py

Quick parameter sweep helper to tune VSA z-score sensitivity on OHLCV CSVs.

Usage examples:
  python tools\zscore_sweep.py --csv data/BTC_15m.csv --symbol BTC --tf 15 --lookback 20
  python tools\zscore_sweep.py --csv data/BTC_1h.csv --symbol BTC --tf 60 --lookback 20 --thresholds 1.2,1.5,1.8,2.0

CSV expected columns: time, open, high, low, close, volume
Optional column: signed_volume - if present, used directly for zscore. Otherwise signed_volume is approximated as volume * sign(close - open).

Outputs a CSV `sweep_results_{symbol}_{tf}.csv` with metrics per threshold.
"""

import argparse
import os
from typing import List, Tuple

import numpy as np
import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    if 'time' in df.columns:
        try:
            df['time'] = pd.to_datetime(df['time'])
        except Exception:
            pass
    return df


def signed_volume(df: pd.DataFrame) -> pd.Series:
    if 'signed_volume' in df.columns:
        return df['signed_volume'].astype(float)
    # fallback: approximate signed volume by sign(close - open) * volume
    sign = np.sign(df['close'].astype(float) - df['open'].astype(float))
    # where price unchanged, use prior sign to avoid zeros
    sign_nozero = sign.replace(0, np.nan).ffill().fillna(0)
    return df['volume'].astype(float) * sign_nozero


def rolling_zscore(series: pd.Series, length: int) -> pd.Series:
    s = series.astype(float)
    mean = s.rolling(window=length, min_periods=1).mean()
    std = s.rolling(window=length, min_periods=1).std(ddof=0).replace(0, np.nan)
    z = (s - mean) / std
    z = z.fillna(0.0)
    return z


def detect_alerts(zseries: pd.Series, threshold: float) -> pd.Series:
    return (zseries >= threshold).astype(int)


def evaluate_alerts(df: pd.DataFrame, alerts: pd.Series, lookahead: int, pct_move: float) -> Tuple[int, int, float, float, float]:
    """Return (alerts_count, hits_up, hits_abs, precision_up, precision_abs, avg_wait_bars)
    """
    n = len(df)
    idxs = np.flatnonzero(alerts.values)
    alerts_count = len(idxs)
    if alerts_count == 0:
        return (0, 0, 0, 0.0, 0.0, 0.0)

    hits_up = 0
    hits_abs = 0
    waits = []
    closes = df['close'].values
    for i in idxs:
        start_price = closes[i]
        end_idx = min(i + lookahead, n - 1)
        future_window = closes[i+1:end_idx+1]
        if future_window.size == 0:
            waits.append(np.nan)
            continue
        # compute percent changes
        pct = (future_window - start_price) / start_price
        # check upward hit
        if np.any(pct >= pct_move):
            hits_up += 1
            # record wait bars to first hit
            first = np.argmax(pct >= pct_move) + 1
            waits.append(first)
        else:
            # if any downward large move qualifies as abs hit, treat accordingly
            if np.any(np.abs(pct) >= pct_move):
                hits_abs += 1
                first = np.argmax(np.abs(pct) >= pct_move) + 1
                waits.append(first)
            else:
                waits.append(np.nan)

    precision_up = hits_up / alerts_count if alerts_count > 0 else 0.0
    precision_abs = (hits_up + hits_abs) / alerts_count if alerts_count > 0 else 0.0
    avg_wait = float(np.nanmean(waits)) if len(waits) > 0 else 0.0
    return (alerts_count, hits_up, hits_abs, precision_up, precision_abs, avg_wait)


def run_sweep(csv_path: str, symbol: str, tf_minutes: int, lookback: int, thresholds: List[float],
              pct_move: float, lookahead: int, out_dir: str) -> pd.DataFrame:
    df = load_csv(csv_path)
    required = ['open', 'high', 'low', 'close', 'volume']
    for c in required:
        if c not in df.columns:
            raise SystemExit(f"CSV missing required column: {c}")
    sv = signed_volume(df)
    z = rolling_zscore(sv, lookback)
    results = []
    n = len(df)
    for thr in thresholds:
        alerts = detect_alerts(z, thr)
        alerts_count, hits_up, hits_abs, prec_up, prec_abs, avg_wait = evaluate_alerts(df, alerts, lookahead, pct_move)
        alerts_per_1000 = alerts_count / n * 1000 if n>0 else 0
        results.append({
            'symbol': symbol,
            'tf_minutes': tf_minutes,
            'lookback': lookback,
            'threshold': thr,
            'alerts_count': alerts_count,
            'alerts_per_1000_bars': alerts_per_1000,
            'hits_up': hits_up,
            'hits_abs': hits_abs,
            'precision_up': prec_up,
            'precision_abs': prec_abs,
            'avg_wait_bars': avg_wait,
        })
    out = pd.DataFrame(results)
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, f"sweep_results_{symbol}_{tf_minutes}m.csv")
    out.to_csv(out_csv, index=False)
    print(f"Wrote results to: {out_csv}")
    return out


def parse_thresholds(s: str) -> List[float]:
    parts = [p.strip() for p in s.split(',') if p.strip()]
    return [float(p) for p in parts]


def main(argv=None):
    p = argparse.ArgumentParser(description='Sweep z-score thresholds for VSA signals')
    p.add_argument('--csv', required=True, help='Path to OHLCV CSV')
    p.add_argument('--symbol', required=True)
    p.add_argument('--tf', type=int, required=True, help='Chart timeframe in minutes (e.g., 15, 60)')
    p.add_argument('--lookback', type=int, default=20)
    p.add_argument('--thresholds', default='1.2,1.5,1.8,2.0,2.5,3.0', help='Comma-separated thresholds')
    p.add_argument('--pct_move', type=float, default=0.008, help='Price move fraction to count as hit (default 0.8%%)')
    p.add_argument('--lookahead', type=int, default=6, help='Lookahead bars to check after an alert')
    p.add_argument('--out', default='tools/out', help='Output directory')
    args = p.parse_args(argv)

    thresholds = parse_thresholds(args.thresholds)
    run_sweep(args.csv, args.symbol, args.tf, args.lookback, thresholds, args.pct_move, args.lookahead, args.out)


if __name__ == '__main__':
    main()
    main()
