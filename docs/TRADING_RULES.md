
# Trading Rules — Supreme Rule (Repository-wide)

This document codifies the user's trading style and the mandatory engineering rules that every indicator, strategy, and template in this repository must follow.

Date: 2025-09-29

## Supreme Rule (one sentence)

Only trade when a top-down confirmation exists (W → D → 4H → 1H → 15m → 5m/1m) and when signals are "beautiful and sure"; indicators and strategies are tools — they must not force entries, SL/TP, or encourage overtrading; the trader is the final decision maker.

## Key Principles

- Indicators provide signals and optional suggestions only; they do NOT execute orders or place SL/TP unless the user explicitly opts in.

- Default mode for every script is conservative: no auto-ordering, and no SL/TP suggestions unless explicitly enabled.

## Indicator Behaviour Contract

- Indicators MUST NOT execute orders.
