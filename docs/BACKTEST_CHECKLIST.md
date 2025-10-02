# BACKTEST CHECKLIST - VP-CVD Confluence Strategy
## Complete Guide to Backtesting Before Live Trading

**Purpose:** Đảm bảo strategy hoạt động TRƯỚC KHI risking real money  
**Timeline:** Hoàn thành tất cả steps trong 2-4 tuần  
**Author:** Khogao, October 2025  
**Philosophy:** "Test everything, trust nothing until proven"

---

## 🎯 OVERVIEW - 3 Phases of Backtesting

```
PHASE 1: MANUAL BACKTEST (50 trades, scroll back chart)
    ↓ IF Win Rate > 50% + R:R > 1.5
PHASE 2: STRATEGY CODE BACKTEST (6-12 months data)
    ↓ IF Metrics match manual + Sortino > 1.0
PHASE 3: PAPER TRADING (50-100 trades, real-time)
    ↓ IF Discipline > 90% + Metrics hold
LIVE TRADING (start 0.5% position size)
```

**CRITICAL RULES:**
- ❌ **NO skipping phases** (each phase validates the previous)
- ❌ **NO cherry-picking setups** (must test ALL valid setups in timeframe)
- ❌ **NO moving goalposts** (define success criteria BEFORE testing)
- ✅ **YES to honesty** (log losses, mistakes, everything)
- ✅ **YES to patience** (rushing = blowing account later)

---

## 📋 PHASE 1: MANUAL BACKTEST (Week 1-2)

**Goal:** Validate entry rules work WITHOUT coding  
**Duration:** 1-2 weeks  
**Effort:** 5-10 hours total  
**Tools Needed:** TradingView with VPP5+ and CVPZero loaded

### Step 1.1: Setup Environment

**Checklist:**
- [ ] Open TradingView with target symbol (e.g., BTCUSDT)
- [ ] Load VPP5+ indicator (overlay)
- [ ] Load CVPZero indicator (lower pane)
- [ ] Set chart timeframe (15m, 1H, or 4H)
- [ ] Create Excel/Google Sheet for tracking

**Excel Template Columns:**
```
| Date | Time | Side | Entry | Stop | TP1 | TP2 | Conditions | Outcome | P&L% | R:R | Notes |
```

### Step 1.2: Define Backtest Period

**Recommended:**
- **Data Range:** Last 3 months (enough samples, recent market behavior)
- **Start Date:** Go back 90 days from today
- **Symbols:** Focus on 1-2 pairs initially (BTCUSDT, ETHUSDT)

**How to scroll back:**
1. Right-click chart → "Go to..."
2. Enter date 90 days ago
3. Click "Go"

### Step 1.3: Identify Valid Setups

**For EVERY bar, ask:**

#### 8-Point Checklist (LONG Example)

| # | Condition | How to Check on Chart |
|---|-----------|----------------------|
| 1️⃣ | Price at VAL? | Is price touching/near green VAL line from VPP5+? |
| 2️⃣ | HTF POC above? | Is orange HTF POC line above current price? |
| 3️⃣ | CVD rising? | Is CVD line (CVPZero) above its MA (blue line)? |
| 4️⃣ | VSA signal? | Are there "SP" (Spring) or "SV" labels on CVPZero? |
| 5️⃣ | Multi-TF aligned? | Check CVPZero multi-TF table: all green? |
| 6️⃣ | Volume quality? | Is volume bar on CVPZero colored (not gray)? |
| 7️⃣ | Divergence? | Are there bullish divergence lines on chart? |
| 8️⃣ | Not choppy? | Is price clearly trending or at extreme, not stuck mid-range? |

**COUNT conditions:**
- 6/8 → Mark as "Valid LONG"
- 7/8 → Mark as "Strong LONG"
- 8/8 → Mark as "Perfect LONG"
- <6/8 → Skip, not valid

**Repeat for SHORT (reverse conditions)**

### Step 1.4: Log Entry & Calculate Outcome

**For each valid setup:**

1. **Log Entry:**
   - Date/Time of entry bar
   - Entry price: Close of signal bar OR open of next bar
   - Stop loss: VAL - (1 * ATR) for LONG, VAH + (1 * ATR) for SHORT
   - TP1: POC
   - TP2: VAH for LONG, VAL for SHORT
   - Conditions met: X/8

2. **Simulate Outcome:**
   - Scroll forward bar by bar
   - IF stop hit first → LOSS (record loss %)
   - IF TP1 hit first → Partial WIN (close 50%, move stop to breakeven)
   - IF TP2 hit → Full WIN (record win %)
   - IF no TP/Stop after 16 bars → Time exit (record P&L)

3. **Calculate R:R:**
   - Risk: Entry - Stop (for LONG)
   - Reward: Exit - Entry
   - R:R = Reward / Risk

### Step 1.5: Target Sample Size

**Minimum 50 trades:**
- Scroll until you find 50 valid setups (6+ conditions)
- This might take 60-90 days of chart data
- Mix of market conditions (trending, choppy, volatile)

**Why 50?**
- Statistical significance (30+ needed minimum)
- Enough to see patterns (which conditions matter most)
- Small enough to complete in 1-2 weeks

### Step 1.6: Calculate Metrics

**After 50 trades, calculate:**

| Metric | Formula | Target |
|--------|---------|--------|
| **Total Trades** | Count all entries | 50 |
| **Winners** | Count trades with P&L > 0 | -- |
| **Losers** | Count trades with P&L < 0 | -- |
| **Win Rate** | Winners / Total Trades | >50% |
| **Avg Win %** | Sum(win%) / Winners | -- |
| **Avg Loss %** | Sum(loss%) / Losers | -- |
| **Avg R:R** | Avg(Reward/Risk) | >1.5:1 |
| **Profit Factor** | Gross Profit / Gross Loss | >1.5 |
| **Max Consecutive Losses** | Longest losing streak | <5 |
| **Max Drawdown** | Largest peak-to-trough equity drop | <15% |

**Excel Formulas:**
```excel
Win Rate: =COUNTIF(P&L_column,">0")/COUNT(P&L_column)
Avg R:R: =AVERAGE(RR_column)
Profit Factor: =SUMIF(P&L_column,">0")/ABS(SUMIF(P&L_column,"<0"))
```

### Step 1.7: Decision Criteria

**PROCEED to Phase 2 IF:**
- ✅ Win Rate > 50% (preferably 55%+)
- ✅ Avg R:R > 1.5:1
- ✅ Profit Factor > 1.5
- ✅ Max Drawdown < 20%
- ✅ At least 15 winners in 50 trades

**STOP and REVISE IF:**
- ❌ Win Rate < 45%
- ❌ Avg R:R < 1.2:1
- ❌ Profit Factor < 1.2
- ❌ Max Consecutive Losses > 7

**REVISIONS to try:**
- Increase minimum conditions (7/8 instead of 6/8)
- Require divergence (makes it mandatory)
- Avoid choppy markets more strictly
- Adjust TP/SL (test TP1 at VAH instead of POC)

### Step 1.8: Pattern Analysis

**Analyze your 50 trades:**

**Winners Analysis:**
- What conditions were most common? (e.g., 90% had divergence)
- What regime? (70% were in trending markets)
- What timeframe? (1H trades did better than 15m)

**Losers Analysis:**
- What was missing? (e.g., 80% lacked multi-TF alignment)
- What regime? (60% were in choppy markets)
- What mistake? (Stop too tight? TP too greedy?)

**Create HEATMAP:**
```
Condition → Win Rate:
8/8 conditions → 85% win rate (but only 5 trades)
7/8 conditions → 70% win rate (15 trades)
6/8 conditions → 55% win rate (30 trades)

Divergence → Win Rate:
With divergence → 75% win rate (20 trades)
No divergence → 45% win rate (30 trades)

Regime → Win Rate:
Trending → 68% win rate
Mean-reverting → 58% win rate
Choppy → 30% win rate (AVOID!)
```

**INSIGHT:** This tells you which filters to tighten in Phase 2

---

## 📋 PHASE 2: STRATEGY CODE BACKTEST (Week 3)

**Goal:** Validate strategy in Pine Script over longer timeframe  
**Duration:** 3-5 days  
**Tools:** VP-CVD-Confluence-Strategy.pine (already created)

### Step 2.1: Load Strategy Script

**Checklist:**
- [ ] Open TradingView Pine Editor
- [ ] Copy VP-CVD-Confluence-Strategy.pine code
- [ ] Click "Add to Chart"
- [ ] Strategy Tester panel should appear at bottom

### Step 2.2: Configure Strategy Settings

**Based on Phase 1 learnings:**

| Setting | Recommended | Adjust if: |
|---------|-------------|------------|
| Min Conditions | 6 (from Phase 1) | Phase 1 showed 7/8 performed better → Set to 7 |
| Risk % | 1% | Conservative start |
| Require Divergence | False | Phase 1 showed divergence critical → Set to True |
| Allow Choppy Market | False | NEVER set to True (Phase 1 confirmed) |
| Use Time Exit | True | Prevents dead capital |
| Max Bars | 16 (4H on 15m) | Adjust based on avg hold time in Phase 1 |

**HTF/VP/CVD Settings:**
- Use SAME settings as manual backtest (e.g., VP lookback 200, CVD anchor D)
- Don't optimize yet (just validate first)

### Step 2.3: Set Backtest Period

**Recommended:**
- **Start Date:** 6-12 months ago
- **End Date:** Today (or 1 month ago if you want out-of-sample test)
- **Symbols:** Same as Phase 1 (BTCUSDT, ETHUSDT)
- **Timeframe:** Same as Phase 1 (15m, 1H, or 4H)

**Why 6-12 months?**
- Multiple market regimes (bull, bear, chop)
- More statistical confidence (200-500 trades)
- Reveals issues not visible in 50-trade manual test

### Step 2.4: Run Backtest & Review Results

**Strategy Tester Metrics:**

| Metric | Target | Red Flag |
|--------|--------|----------|
| Net Profit | Positive | Negative (obviously) |
| Total Trades | 100+ | <50 (not enough data) |
| Win Rate % | >55% | <50% |
| Profit Factor | >1.5 | <1.2 |
| Max Drawdown | <15% | >20% |
| Avg Trade | Positive | Negative |
| Sharpe Ratio | >1.0 | <0.5 |
| **Sortino Ratio** | **>1.0** | **<0.7** |

**Why Sortino > Sharpe?**
- Sortino only penalizes downside volatility (losses)
- Sharpe penalizes all volatility (even upside)
- For discretionary trading, Sortino is better measure

### Step 2.5: Compare with Manual Backtest

**CRITICAL CHECK:**

| Metric | Phase 1 (Manual) | Phase 2 (Code) | Acceptable Diff |
|--------|------------------|----------------|-----------------|
| Win Rate | 58% | 56% | ±5% OK |
| Avg R:R | 1.8:1 | 1.6:1 | ±20% OK |
| Profit Factor | 1.9 | 1.7 | ±15% OK |

**IF Phase 2 results MUCH WORSE than Phase 1:**
- 🔴 **Problem:** Code doesn't match manual rules
- 🔧 **Fix:** Review entry logic in Pine Script
- 🔍 **Debug:** Check 5-10 trades manually vs code execution

**IF Phase 2 results MUCH BETTER than Phase 1:**
- 🔴 **Problem:** Look-ahead bias or overfitting
- 🔧 **Fix:** Check `request.security` uses `lookahead=off`
- 🔍 **Debug:** Verify HTF POC not using future data

### Step 2.6: Equity Curve Analysis

**Look at equity curve chart:**

**GOOD signs:**
- ✅ Smooth upward trend (not straight line, that's suspicious)
- ✅ Drawdowns recover within 10-20 trades
- ✅ No catastrophic drops (>20% in few trades)
- ✅ Profit consistent across different months

**BAD signs:**
- 🔴 All profit from 1-2 trades (luck, not system)
- 🔴 Long flat periods (50+ trades no progress)
- 🔴 Recent drawdown not recovering (regime change?)
- 🔴 Profit only in bull market (not robust)

### Step 2.7: Trade Distribution Analysis

**Check trade outcomes:**

```
Win Distribution:
Small wins (<1% gain): ___% of winners
Medium wins (1-3% gain): ___% of winners
Large wins (>3% gain): ___% of winners

Loss Distribution:
Small losses (<1% loss): ___% of losers
Medium losses (1-2% loss): ___% of losers  
Large losses (>2% loss): ___% of losers
```

**IDEAL:**
- Many small/medium wins (consistent system)
- Few medium losses (stops working)
- Almost NO large losses (risk management good)
- Some large wins (letting winners run)

**RED FLAG:**
- Most wins are tiny (<0.5%)
- Most losses are large (>2%)
- This = negative expectancy despite "good" win rate

### Step 2.8: Parameter Sensitivity Test

**DON'T optimize aggressively, BUT test robustness:**

**Test 1: Min Conditions**
- Run backtest with minConditions = 5, 6, 7, 8
- Record win rate for each
- IF 6 and 7 have similar results → Robust
- IF huge difference (60% vs 45%) → Overfitted to one value

**Test 2: Risk %**
- Run with 0.5%, 1%, 2% risk
- Record Sortino ratio for each
- IF similar Sortino → Good risk management
- IF huge difference → Position sizing problematic

**Test 3: TP Levels**
- Run with TP1 at POC vs VAH/VAL
- Record R:R and win rate
- IF POC better → Use POC
- IF VAH better → Adjust code

**GOAL:** Find robust settings that work across ranges, not one perfect value

### Step 2.9: Out-of-Sample Test (CRITICAL)

**Split backtest data:**
- **In-Sample:** First 9 months (for optimization)
- **Out-of-Sample:** Last 3 months (for validation)

**Process:**
1. Optimize parameters on in-sample data (first 9 months)
2. Lock parameters (don't touch again)
3. Run on out-of-sample data (last 3 months)
4. Compare metrics

**PASS CRITERIA:**
- Out-of-sample metrics within 80-120% of in-sample
- Example: In-sample win rate 58% → Out-of-sample 50-66% OK
- IF out-of-sample < 70% of in-sample → Overfitted

**WHY THIS MATTERS:**
- Most traders optimize on ALL data → looks great
- Then goes live → fails immediately (overfitted to past)
- Out-of-sample = simulates going live

### Step 2.10: Decision Criteria

**PROCEED to Phase 3 IF:**
- ✅ Win Rate > 55% (across full 6-12 months)
- ✅ Sortino Ratio > 1.0
- ✅ Max Drawdown < 15%
- ✅ 100+ trades in sample
- ✅ Equity curve healthy (smooth upward)
- ✅ Out-of-sample within 80-120% of in-sample
- ✅ Results match Phase 1 manual backtest (±20%)

**STOP and REVISE IF:**
- ❌ Win Rate < 50%
- ❌ Sortino < 0.7
- ❌ Max Drawdown > 20%
- ❌ Equity curve erratic (huge swings)
- ❌ Out-of-sample < 70% of in-sample (overfitted)
- ❌ Results don't match Phase 1 (code is wrong)

---

## 📋 PHASE 3: PAPER TRADING (Week 4-8)

**Goal:** Validate YOU can execute strategy in real-time  
**Duration:** 4-8 weeks (50-100 trades)  
**Tools:** TradingView alerts + Manual execution + Trade journal

### Step 3.1: Setup Paper Trading Environment

**Checklist:**
- [ ] Keep VPP5+ and CVPZero on chart (visual confirmation)
- [ ] Load VP-CVD-Confluence-Strategy script (for alerts)
- [ ] Create alerts for Long Entry and Short Entry
- [ ] Setup Trade Journal spreadsheet (use TRADE_JOURNAL_TEMPLATE.md)
- [ ] NO real money yet (use demo account or just track)

**Alert Settings:**
```
Alert Name: "VP-CVD Long Entry"
Condition: VP-CVD-Confluence-Strategy → "Long Entry"
Message: "BTCUSDT LONG setup - Conditions: {{plot("Conditions Met")}}/8"
Frequency: Once Per Bar Close
```

### Step 3.2: Execution Protocol (CRITICAL)

**When alert fires:**

#### Step 1: Screenshot IMMEDIATELY (within 30 seconds)
- Full chart with VPP5+ levels visible
- CVPZero pane showing CVD, VSA, multi-TF table
- Current price, time, symbol
- Save as: `YYYY-MM-DD_HH-MM_SYMBOL_LONG.png`

#### Step 2: Fill Pre-Trade Checklist (2-3 minutes)
- Use template from TRADE_JOURNAL_TEMPLATE.md
- Verify all 8 conditions manually (don't trust alert blindly)
- Rate psychology 1-10 (if <5, SKIP trade)
- Calculate position size and stops

#### Step 3: Execute Entry (if >6 conditions + psych OK)
- Log "entry time" in journal
- Record entry price (use current market or limit order)
- Set stop loss IMMEDIATELY (non-negotiable)
- Set TP1 and TP2 levels

#### Step 4: Monitor (Passive, not active)
- Check 1-2x per hour (not every minute)
- Update journal if significant event (TP hit, stop moved, etc.)
- Do NOT interfere (no stop moving, no early exit unless planned)

#### Step 5: Post-Trade Review (within 1 hour of close)
- Log final outcome
- Screenshot exit
- Fill post-trade review section
- Rate execution quality 1-10
- Identify lesson learned

**TIME INVESTMENT:** ~10 minutes per trade (setup + journal)

### Step 3.3: Common Paper Trading Pitfalls

**Problem 1: "I would have entered earlier"**
- 🔴 **Reality:** No you wouldn't have, you only see it in hindsight
- 🔧 **Fix:** Use alerts ONLY, no manual hunting
- ✅ **Rule:** If no alert fired, no entry (period)

**Problem 2: "I would have exited at the perfect top"**
- 🔴 **Reality:** No one exits at top in live trading
- 🔧 **Fix:** Follow TP plan exactly (TP1 at POC, TP2 at VAH/VAL)
- ✅ **Rule:** No TP level changes after entry

**Problem 3: "Stop loss hit by 1 pip then reversed"**
- 🔴 **Reality:** This happens in live too (slippage)
- 🔧 **Fix:** Accept losses, don't say "I would have held"
- ✅ **Rule:** Stop hit = loss recorded, no exceptions

**Problem 4: "I'm executing perfectly, 90% win rate"**
- 🔴 **Reality:** You're cheating (hindsight bias)
- 🔧 **Fix:** Only count trades from alert firing forward
- ✅ **Rule:** No backtesting within paper trading period

### Step 3.4: Discipline Tracking (THE MOST IMPORTANT METRIC)

**For EVERY trade, calculate Discipline Score:**

| Question | Yes = 1 pt | No = 0 pt |
|----------|-----------|----------|
| Did I wait for alert? | | |
| Did I fill checklist before entry? | | |
| Did I verify 6+ conditions? | | |
| Did I check psychology score? | | |
| Did I calculate position size correctly? | | |
| Did I place stop immediately? | | |
| Did I follow TP plan exactly? | | |
| Did I journal within 1 hour of close? | | |

**Discipline Score = Sum / 8 * 100%**

**Target: 90%+ discipline across all trades**

**Why this matters MORE than win rate:**
- OP said: "I gave signals, they still failed" → Execution problem
- Phase 1-2 proved strategy works → Phase 3 proves YOU can execute it
- If discipline < 80% → You'll fail live regardless of strategy

### Step 3.5: Weekly Check-Ins

**Every Sunday (or end of trading week):**

**Metrics Check:**
- Win Rate: ___% (target: >55%)
- Discipline: ___% (target: >90%)
- Trades: ___ (target: 10-15/week)
- Journal Compliance: ___% (target: 100%)

**Questions:**
1. Am I following alerts only? (Yes/No)
2. Am I checking all conditions? (Yes/No)
3. Am I placing stops immediately? (Yes/No)
4. Am I letting TP plan execute? (Yes/No)
5. Am I journaling every trade? (Yes/No)

**IF 3+ "No" answers:**
- 🔴 **Problem:** Discipline breaking down
- 🔧 **Fix:** Reduce trade frequency, focus on quality
- ⏸️ **Consider:** Pause paper trading for 1 week, review all journal entries

### Step 3.6: Psychological Patterns

**Track emotion score over time:**

```
Week 1: Avg Psychology Score: __/10
Week 2: Avg Psychology Score: __/10
Week 3: Avg Psychology Score: __/10
Week 4: Avg Psychology Score: __/10
```

**Correlate with trade outcomes:**
```
Trades when Psych > 7: Win Rate ____%
Trades when Psych 5-7: Win Rate ____%
Trades when Psych < 5: Win Rate ____%
```

**COMMON PATTERNS:**
- After 2 wins → Overconfident → Psych 9/10 → Sloppy trade → Loss
- After 2 losses → Fearful → Psych 3/10 → Skip good setup → Regret

**SOLUTION:**
- Implement circuit breakers (from TRADE_JOURNAL_TEMPLATE.md)
- 2 wins → SLOW DOWN, double-check next entry
- 2 losses → PAUSE, review mistakes, breathe

### Step 3.7: Compare Phase 2 vs Phase 3

**CRITICAL COMPARISON:**

| Metric | Phase 2 (Code) | Phase 3 (Paper) | Acceptable? |
|--------|----------------|-----------------|-------------|
| Win Rate | 58% | 55% | ✅ (within 5%) |
| Avg R:R | 1.7:1 | 1.6:1 | ✅ (within 10%) |
| Sortino | 1.2 | 1.1 | ✅ (within 10%) |
| Discipline | N/A | 92% | ✅ (>90%) |

**IF Paper Trading WORSE than Code Backtest by >20%:**
- 🔴 **Problem:** Execution issues (YOU, not strategy)
- 🔧 **Fix:** Review journal for patterns
  - Entering too early? (Before alert confirmation)
  - Exiting too early? (Fear of giving back profit)
  - Moving stops? (Hoping trade will recover)
  - Ignoring conditions? (FOMO entries)

**DO NOT PROCEED TO LIVE if:**
- Paper trading win rate < 50%
- Discipline < 85%
- Emotion score consistently < 5/10
- Can't explain why losses happened

### Step 3.8: Sample Size Requirements

**Minimum 50 trades, ideally 100:**

**Why 50 minimum?**
- Statistical significance (30+ needed)
- Experience different market conditions
- Build muscle memory for execution

**Why 100 ideal?**
- More confident in win rate (±5% margin of error)
- See rare edge cases (extreme volatility, gaps, news)
- Discipline habits solidify after 100 reps

**HOW LONG?**
- If 3-5 trades/day → 10-20 trading days (2-4 weeks)
- If 1-2 trades/day → 25-50 trading days (5-10 weeks)
- Don't rush! Quality > speed

### Step 3.9: Decision Criteria for Going Live

**PROCEED to Live Trading IF:**
- ✅ 50+ paper trades completed (100+ ideal)
- ✅ Win Rate > 55%
- ✅ Sortino Ratio > 1.0
- ✅ **Discipline Score > 90%** (MOST IMPORTANT)
- ✅ Journal compliance 100% (every trade logged)
- ✅ Emotion score avg > 6/10
- ✅ No circuit breakers triggered in last 2 weeks
- ✅ Metrics within 80-120% of Phase 2 code backtest
- ✅ Can explain every loss (not "bad luck")
- ✅ Comfortable with position sizing math
- ✅ Stops placed automatically (habit formed)

**DO NOT GO LIVE IF:**
- ❌ Win Rate < 50%
- ❌ Discipline < 85%
- ❌ Cherry-picking entries (not following alerts)
- ❌ Moving stops frequently
- ❌ Revenge trading after losses
- ❌ Emotion score avg < 5/10
- ❌ Can't keep up with journaling
- ❌ Impatient (wanting to trade more than 5 setups/day)

**IF NOT READY:**
- Option 1: Continue paper trading (another 50 trades)
- Option 2: Reduce to 1 trade every 2 days (focus on quality)
- Option 3: Go back to Phase 1 (maybe strategy needs adjustment)

---

## 📋 PHASE 4: LIVE TRADING (Month 3+)

**Goal:** Scale from 0.5% to full 1-2% position size gradually  
**Duration:** 3-6 months to full size  
**Mental shift:** Real money = real emotions

### Step 4.1: Starting Live (First 20 Trades)

**Settings:**
- Position size: **0.5% risk** (half of target)
- Trade frequency: Max 2-3/day (conservative)
- Focus: **Discipline > profit**

**Why 0.5% risk?**
- Emotions will spike even with small size
- Need to build confidence gradually
- Better to win small than lose big while learning

**First 20 Trades Checklist:**
- [ ] Every trade journaled (no exceptions)
- [ ] Every stop placed immediately
- [ ] No stop moving (even if tempted)
- [ ] No revenge trades (if loss, wait 30 min)
- [ ] No overtrading (max 3/day)

### Step 4.2: Scaling Position Size

**Gradual increase based on performance:**

| Milestone | Increase to | Conditions Required |
|-----------|-------------|---------------------|
| Trades 1-20 | 0.5% risk | Starting point |
| Trades 21-50 | 0.75% risk | IF: Win rate >50%, Discipline >90%, No circuit breakers |
| Trades 51-100 | 1.0% risk | IF: Win rate >55%, Sortino >1.0, Max DD <10% |
| Trades 101+ | 1.5-2% risk | IF: Win rate >58%, Sortino >1.2, Consistent 3+ months |

**NEVER increase if:**
- Current drawdown > 10%
- 3 losses in a row
- Discipline slipping (<85%)
- Emotion score dropping (<5/10)

**ALWAYS decrease if:**
- Max drawdown > 15% (cut to 0.5%)
- 5 losses in a row (cut to 0.5%)
- Discipline < 80% (cut to 0.5% or pause)

### Step 4.3: Monthly Review (Live Trading)

**Metrics to Track:**

| Metric | Month 1 | Month 2 | Month 3 | Target |
|--------|---------|---------|---------|--------|
| Total Trades | | | | 30-60 |
| Win Rate | | | | >55% |
| Sortino Ratio | | | | >1.0 |
| Max Drawdown | | | | <15% |
| Discipline Score | | | | >90% |
| Avg Hold Time | | | | Matches Phase 2 |
| Profit Factor | | | | >1.5 |

**Questions:**
1. Are live metrics within 80-120% of paper trading? (Yes/No)
2. Am I following the same rules? (Yes/No)
3. Is emotion interfering with execution? (Yes/No)
4. Am I overtrading (>5 setups/day)? (Yes/No)
5. Am I journaling 100%? (Yes/No)

**IF 3+ concerning answers:**
- Reduce position size by 50%
- Review last 20 trades in detail
- Identify root cause (emotion? Fatigue? Overconfidence?)
- Consider 1-week break to reset

### Step 4.4: Regime Adaptation

**After 3 months live trading, analyze:**

```
TRENDING MARKETS:
- Trades: ___ | Win Rate: ___% | Avg R:R: ___
- Best setups: _______________________________

MEAN-REVERTING MARKETS:
- Trades: ___ | Win Rate: ___% | Avg R:R: ___
- Best setups: _______________________________

CHOPPY MARKETS:
- Trades: ___ | Win Rate: ___% | Avg R:R: ___
- Action: AVOID (if win rate <40%)
```

**Strategy Adjustments:**
- IF trending markets = 70% win rate → Trade more aggressively in trends
- IF choppy markets = 30% win rate → Require 7/8 conditions in chop
- IF certain VSA signal = 80% win rate → Increase size on that signal

**KAIZEN (Continuous Improvement):**
- Every quarter: Review 100 trades
- Identify top 10 best setups → What made them "beautiful"?
- Identify top 10 worst setups → What to avoid?
- Refine rules (tighten filters, not loosen)

---

## 📊 BACKTEST METRICS SUMMARY

### Phase 1: Manual Backtest

| Metric | Formula | Target | Decision |
|--------|---------|--------|----------|
| Sample Size | Count | 50 trades | Minimum |
| Win Rate | Winners/Total | >50% | Proceed |
| Avg R:R | Avg(Reward/Risk) | >1.5 | Proceed |
| Profit Factor | Gross Win / Gross Loss | >1.5 | Proceed |
| Max Drawdown | Peak-to-trough equity | <20% | Proceed |

**Decision:** IF all targets met → Phase 2

### Phase 2: Code Backtest

| Metric | Source | Target | Decision |
|--------|--------|--------|----------|
| Win Rate | Strategy Tester | >55% | Proceed |
| Sortino Ratio | Strategy Tester | >1.0 | Proceed |
| Max Drawdown | Strategy Tester | <15% | Proceed |
| Total Trades | Strategy Tester | 100+ | Proceed |
| Out-of-Sample | Manual calc | 80-120% of in-sample | Proceed |

**Decision:** IF all targets met → Phase 3

### Phase 3: Paper Trading

| Metric | Source | Target | Decision |
|--------|--------|--------|----------|
| Sample Size | Journal | 50-100 trades | Minimum |
| Win Rate | Journal | >55% | Proceed |
| Discipline | Journal | >90% | CRITICAL |
| Emotion Score | Journal | >6/10 avg | Proceed |
| Journal Compliance | Journal | 100% | Proceed |

**Decision:** IF all targets met → Phase 4 (Live, 0.5% size)

### Phase 4: Live Trading

| Metric | Period | Target | Action |
|--------|--------|--------|--------|
| Win Rate | Monthly | >55% | Scale if met |
| Sortino | Monthly | >1.0 | Scale if met |
| Discipline | Weekly | >90% | Critical to maintain |
| Max Drawdown | Real-time | <15% | Reduce size if breached |

**Scaling:** 0.5% → 0.75% → 1.0% → 1.5% → 2.0% (over 6 months)

---

## 🚨 RED FLAGS - When to STOP and REASSESS

### During Manual Backtest (Phase 1)

❌ **Stop IF:**
- Win rate < 40% after 30 trades
- Losing 8+ trades in a row
- Can't find 50 valid setups in 90 days (strategy too strict)
- Profit factor < 1.0 (losing money on average)

🔧 **Action:**
- Revisit entry rules (too strict? Too loose?)
- Test different TP/SL ratios
- Analyze losing trades for common thread
- Consider different timeframe (15m vs 1H vs 4H)

### During Code Backtest (Phase 2)

❌ **Stop IF:**
- Out-of-sample < 70% of in-sample (overfitted)
- Equity curve shows all profit from 1 month (luck)
- Max drawdown > 25% (too risky)
- Win rate dropping every month (strategy decay)

🔧 **Action:**
- Check for look-ahead bias (HTF data using future info?)
- Verify position sizing (might be too aggressive)
- Test on different symbols (is it BTC-specific?)
- Consider regime filters (avoid trading in choppy)

### During Paper Trading (Phase 3)

❌ **Stop IF:**
- Discipline < 80% after 30 trades (can't follow rules)
- Win rate < 45% (significantly worse than Phase 2)
- Overtrading (10+ entries/day, FOMO)
- Moving stops frequently (fear of losses)
- Not journaling (lack of discipline)

🔧 **Action:**
- Reduce trade frequency (1 trade/day max)
- Use bigger timeframe (4H instead of 15m)
- Take 1 week break (reset psychology)
- Review journal for patterns (when do you break rules?)
- Consider accountability partner (someone checks your journal)

### During Live Trading (Phase 4)

❌ **Stop IF:**
- Max drawdown > 20% (risk of ruin)
- 3 months of declining equity (strategy stopped working)
- Discipline < 80% (real money breaking your rules)
- Emotion score < 4/10 consistently (burnout)
- Revenge trading after losses (tilt)

🔧 **Action:**
- IMMEDIATELY reduce size to 0.5% or pause trading
- Review last 50 trades (what changed?)
- Check if market regime changed (strategy fits regime?)
- Consider taking 1 month break (seriously, walk away)
- Seek peer review (show journal to experienced trader)
- Possibly return to paper trading (rebuild confidence)

---

## ✅ SUCCESS CRITERIA - Final Checklist

### Before Going Live, I have:

**PHASE 1: MANUAL BACKTEST**
- [ ] Completed 50+ manual backtests
- [ ] Achieved >50% win rate
- [ ] Achieved >1.5 avg R:R
- [ ] Analyzed winners/losers for patterns
- [ ] Documented findings in spreadsheet

**PHASE 2: CODE BACKTEST**
- [ ] Coded strategy in Pine Script
- [ ] Backtested 6-12 months of data
- [ ] Achieved >55% win rate
- [ ] Achieved >1.0 Sortino ratio
- [ ] Achieved <15% max drawdown
- [ ] Out-of-sample test passed (80-120% of in-sample)
- [ ] Results match Phase 1 (within 20%)

**PHASE 3: PAPER TRADING**
- [ ] Executed 50-100 paper trades
- [ ] Maintained >90% discipline score
- [ ] Achieved >55% win rate
- [ ] Journaled 100% of trades
- [ ] Avg emotion score >6/10
- [ ] No circuit breakers triggered in last 2 weeks
- [ ] Results match Phase 2 (within 20%)

**PHASE 4: LIVE READY**
- [ ] Understand position sizing math
- [ ] Comfortable placing stops immediately
- [ ] Can calculate R:R quickly
- [ ] Know circuit breaker rules by heart
- [ ] Have 6 months of living expenses saved (don't need trading income immediately)
- [ ] Account size appropriate (not risking rent money)
- [ ] Mentally prepared for losing streaks (5-7 losses in a row)
- [ ] Support system in place (journal, mentor, community)

---

## 📚 APPENDIX - Tools & Resources

### Recommended Tools

**For Manual Backtesting:**
- TradingView (Pro plan for alerts)
- Excel or Google Sheets
- Screenshot tool (Windows Snipping Tool, macOS Shift+Cmd+4)

**For Code Backtesting:**
- TradingView Pine Editor
- Strategy Tester (built-in)
- Export data to CSV for deeper analysis (Python/Excel)

**For Paper Trading:**
- TradingView Alerts
- Trade Journal (use TRADE_JOURNAL_TEMPLATE.md)
- Demo account (Binance Testnet, Bybit Demo)

**For Analysis:**
- Excel/Google Sheets (basic metrics)
- Python (pandas, numpy) for advanced analysis
- TradingView Strategy Tester (auto-calculates Sortino, Sharpe, etc.)

### Metrics Calculators

**Win Rate:**
```
Win Rate = (Number of Winning Trades / Total Trades) * 100
```

**Sortino Ratio:**
```
Sortino = (Avg Return - Risk-Free Rate) / Downside Deviation
```
(TradingView calculates this automatically in Strategy Tester)

**Max Drawdown:**
```
Max DD = (Trough Value - Peak Value) / Peak Value * 100
```
(Lowest point from highest point in equity curve)

**Profit Factor:**
```
Profit Factor = Gross Profit / Gross Loss
```
(2.0 = you make $2 for every $1 lost)

---

## 🎯 FINAL WORDS

### Backtest is NOT Optional

**OP from AMA:** "Write your own algo. Set goals, design solutions."

**Translation:**
- Test BEFORE risking money (obvious but ignored by 90% of traders)
- Define success criteria BEFORE testing (win rate, Sortino, DD)
- If fails backtest → don't trade it (no matter how "sure" you feel)

### Backtest Protects You From:

1. **Bad Strategies:** 80% of "great ideas" fail backtest
2. **Overfitting:** "Works on 2023 data" ≠ "Works on 2025 data"
3. **Execution Illusions:** "I would have exited there" (no you wouldn't)
4. **Emotional Trading:** "I feel this setup" (feelings ≠ edge)

### Backtest Gives You:

1. **Confidence:** "I know this works, I tested it 200+ times"
2. **Patience:** "I can wait, I know good setup will come"
3. **Discipline:** "I follow rules because I KNOW they work"
4. **Realistic Expectations:** "I expect 55% win rate, not 90%"

### The 90-Day Reality

**If you rush (skip Phase 1-3):**
- Week 1 live: Exciting! First win!
- Week 2 live: Losing streak, panic
- Week 3 live: Revenge trading, bigger losses
- Week 4 live: Account down 20%, quit trading

**If you follow this checklist:**
- Week 1-2: Manual backtest (boring but enlightening)
- Week 3: Code backtest (confidence building)
- Week 4-8: Paper trading (habit forming)
- Month 3+: Live trading (calm, prepared, profitable)

### Which path do you choose?

**Path A:** Rush → Blow account → Quit → "Trading doesn't work"  
**Path B:** Test → Validate → Execute → Profit → "Trading is a skill"

**This checklist = Path B**

**START TODAY:** Open TradingView, scroll back 90 days, find first valid setup, begin Phase 1.

---

**VERSION:** 1.0  
**DATE:** October 2025  
**AUTHOR:** Khogao  
**STRATEGY:** VP-CVD Confluence

*"Everybody wants to make money. Nobody wants to do the work. Backtest is the work." - Every profitable trader who survived past year 1*
