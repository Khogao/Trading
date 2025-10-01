zscore_sweep helper

Purpose

- Run a quick parameter sweep for VSA z-score thresholds on OHLCV CSVs (BTC/ETH/SOL) to find reasonable sensitivity settings.

Requirements

- Python 3.8+
- Install requirements: pip install -r tools/requirements.txt

CSV format expected

- Columns: time, open, high, low, close, volume
- Optional: signed_volume (if present it's used directly; otherwise script approximates signed volume by sign(close-open)*volume)

Example runs

- python tools\zscore_sweep.py --csv data/BTC_15m.csv --symbol BTC --tf 15 --lookback 20
- python tools\zscore_sweep.py --csv data/ETH_1h.csv --symbol ETH --tf 60 --lookback 30 --thresholds 1.2,1.5,1.8,2.0,2.5

Outputs

- CSV per run: tools/out/sweep_results_{symbol}_{tf}m.csv
  Columns: symbol, tf_minutes, lookback, threshold, alerts_count, alerts_per_1000_bars, hits_up, hits_abs, precision_up, precision_abs, avg_wait_bars

Notes

- This is a quick, event-based evaluation: it checks whether z-score alerts precede a price move of pct_move within lookahead bars.
- For production/backtest you should integrate with your backtesting framework for P&L metrics.
