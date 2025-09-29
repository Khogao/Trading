
# Trading Rules — Supreme Rule (Repository-wide)

This document codifies the user's trading style and the mandatory engineering rules that every indicator, strategy, and template in this repository must follow.

Date: 2025-09-29


## Supreme Rule (one sentence)

Only trade when a top-down confirmation exists (W → D → 4H → 1H → 15m → 5m/1m) and when signals are "beautiful and sure"; indicators and strategies are tools — they must not force entries, SL/TP, or encourage overtrading; the trader is the final decision maker.


## Key Principles

- Top-down confirmation: HTF alignment required by default.

- Indicators provide signals and optional suggestions only; they do NOT execute orders or place SL/TP unless the user explicitly opts in.

- Default mode for every script is conservative: no auto-ordering, and no SL/TP suggestions unless explicitly enabled.

- Daily discipline: allow 0–5 trades/day, require cooldowns and a dopamine guard to prevent overtrading.


## Required Inputs (every new script/template)

- `mode` (display-only | signal-only | strategy) — default: `display-only`

- `require_htf_alignment` (bool) — default: `true`

- `enable_recommended_sl_tp` (bool) — default: `false` (no suggestions unless enabled)

- `auto_place_orders` (bool) — default: `false`

- `auto_manage_sl_tp` (bool) — default: `false`

- `confirm_auto_actions` (bool) — default: `false` (must be explicitly set to allow auto execution)

- `dry_run` (bool) — default: `true`

- `risk_pct_per_trade`, `max_daily_trades`, `cooldown_after_trade` — optional but recommended for strategy mode and only effective when auto execution is enabled.


## Indicator Behaviour Contract

- Indicators MUST NOT execute orders.

- Indicators MUST NOT expose `recommended_sl` or `recommended_tp` unless `enable_recommended_sl_tp == true`.

- When `enable_recommended_sl_tp == true`, indicators must document the method used (ATR, structural, VA node, etc.) and expose `suggestion_confidence` and `suggestion_method`.


## Strategy Behaviour Contract

- Strategies MAY provide execution pathways, but all automatic behaviors are gated behind explicit opt-ins:

  - `auto_place_orders` AND `confirm_auto_actions` must both be true, and `dry_run` must be false before any call to `strategy.entry` / `strategy.exit` / order placement.

  - `auto_manage_sl_tp` requires an additional explicit opt-in and must be documented in the PR.

  - By default a strategy should only compute and display signals when auto-execution is disabled.


## Dopamine / Overtrading Guards

- `max_daily_trades` default is 5. Implement persistent daily counters and block further entries when reached.

- Implement `cooldown_after_trade` (configurable) to avoid back-to-back entries.

- Implement `daily_loss_stop` or similar guard to disable trading for the day after a negative equity threshold is hit.


## SL/TP Policy (delta)

- By default, NO script provides or places SL/TP.

- `enable_recommended_sl_tp` must be explicitly set by the user to true before any recommended SL/TP values are computed or shown.

- Even when recommendations are shown, they are non-binding and scripts must not place SL/TP automatically unless `auto_manage_sl_tp` and `confirm_auto_actions` are explicitly enabled.


## Outputs required from indicators

- `signal_score` (float)

- `signal_type` (string: none|long|short)

- `signal_breakdown` (object/struct)

- `recommended_sl`, `recommended_tp` (only when enabled)

- `suggestion_confidence` and `suggestion_method` (only when enabled)


## PR Checklist (short)

- Default opt-ins must be conservative: `enable_recommended_sl_tp=false`, `auto_place_orders=false`, `auto_manage_sl_tp=false`, `confirm_auto_actions=false`, `dry_run=true`.

- If `enable_recommended_sl_tp==true`, the PR must document the computation method and attach sample screenshots.

- If auto-execution is enabled in code, PR must include a clear rationale and a manual test plan and screenshots of TradingView compile/backtest.


---

If you want this expanded with examples, or want me to implement enforcement (lint/check script) in CI, tell me and I will prepare the next steps.

