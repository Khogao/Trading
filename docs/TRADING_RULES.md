
# Trading Rules — Supreme Rule (Repository-wide)

This document codifies the user's trading style and the mandatory engineering rules that every indicator, strategy, and template in this repository must follow.

Date: 2025-09-29

## Supreme Rule (one sentence)

# 🔥 SUPREME TRADING RULE (Greg + HiveScale Integrated)

> **"Only trade when (1) REGIME is identified, (2) Top-down confirmation exists (W → D → 4H → 1H → 15m → 5m/1m), (3) Signals are 'beautiful and sure' (Triple Confluence: VP + Trend + Order Flow), and (4) Risk is defined BEFORE entry. Indicators are tools (10% Signal) — Risk Management (30%) and Psychology (60%) are the real edge. Trader is final decision maker. **Adapt or Die.**"**

---

## 🎯 PART 1: GREG'S 7 RULES (Foundation)

### **Rule #1: BẢO VỆ VỐN LÀ ƯU TIÊN SỐ 1**
> *"Không có stop loss = Không có quyền trade."*

**Mandatory Requirements:**
- ✅ **Stop loss ALWAYS** (no exceptions, even on "sure" trades)
- ✅ **Risk 1-2% max per trade** (Greg: "Even 5 losers in a row won't hurt you")
- ✅ **Position sizing calculation BEFORE entry:**
  ```
  Position Size = (Account * 0.01) / (Entry - Stop Loss)
  Example: $10,000 account, 1% risk, Entry $50, Stop $48
  → Position Size = ($10,000 * 0.01) / ($50 - $48) = $50 / $2 = 25 shares
  ```
- ❌ **NEVER average down on losing position** (that's gambling, not trading)
- ❌ **NEVER move stop loss further away** (accept loss, move on)

**Penalty for breaking Rule #1:** 
- First violation: No trading for 1 week
- Second violation: Reduce position size to 0.5% for 1 month
- Third violation: Stop trading, back to paper trading

---

### **Rule #2: THỊ TRƯỜNG KHÔNG BIẾT BẠN TỒN TẠI**
> *"Ego = Enemy. Thị trường không quan tâm bạn mất bao nhiêu hôm qua."*

**Mandatory Mindset:**
- ✅ **No revenge trading** (lost yesterday? Today is NEW day)
- ✅ **No "making back losses" mindset** (that's how you blow account)
- ✅ **Accept losses FAST** (if stop hit, close immediately, don't hope)
- ✅ **No attachment to positions** ("My analysis was wrong" → OK, exit)
- ❌ **No "I KNOW this will bounce"** (you don't know, market decides)
- ❌ **No "I deserve to win after 5 losses"** (market doesn't owe you)

**Penalty for breaking Rule #2:**
- If catch yourself revenge trading → STOP, close platform, walk away for 24 hours
- Journal: "Why did I feel I deserved to win? What emotion drove this trade?"

---

### **Rule #3: TRADE THEO KẾ HOẠCH, KHÔNG PHẢI CẢM XÚC**
> *"Kỷ luật > Lợi nhuận. Nếu bạn không thể follow kế hoạch, đừng trade."*

**Mandatory Workflow:**
1. ✅ **Pre-market plan (9:00 AM daily):**
   - Check RegimeRadar: Which regime today? (Trending? Ranging? Choppy?)
   - Check CVPGreg on 4H: Where is POC/VAH/VAL? Where is 50 EMA?
   - Define: "If X happens, I do Y. If Z happens, I do nothing."
   
2. ✅ **During market:**
   - Execute ONLY pre-defined setups (no improvisation)
   - If confusion → Close platform, don't trade
   - If FOMO → Remember: "Cash is a position" (Greg Rule #4)

3. ✅ **Post-market review (5:00 PM daily):**
   - Did I follow plan? (Yes/No)
   - If No: Why? What emotion? How to prevent tomorrow?
   - If Yes: Did plan work? Should I adjust for tomorrow?

**Penalty for breaking Rule #3:**
- If traded without plan → That trade doesn't count (even if profit)
- Write 100 times: "I will not trade without a plan"

---

### **Rule #4: KIÊN NHẪN LÀ MỘT VỊ THẾ**
> *"Greg trade 1-3 lần/ngày, không phải 20+. Chờ đợi = Công việc của trader."*

**Mandatory Patience:**
- ✅ **Wait for A+ setup ONLY** (Greg: "70% win rate from PATIENCE, not signals")
- ✅ **"Beautiful and Sure" checklist:**
  ```
  ☑ Regime matches my strategy? (Trending → Trend-following OK)
  ☑ Price at key VP level? (VAL/POC/VAH)
  ☑ Trend confirmed? (Close > 50 EMA for long)
  ☑ Order flow confirmed? (CVD rising for long)
  ☑ VSA signal? (Spring/Upthrust at key level)
  
  If ALL 5 checked → Trade
  If 4 or less → WAIT
  ```
- ✅ **Cash is a position** (0 trades today = OK if no A+ setup)
- ❌ **No "I need to trade today"** (that's gambler mindset)
- ❌ **No "It's close enough"** (close ≠ perfect, WAIT)

**Greg's Quote:**
> *"Year 1: I thought I had to trade every day. Year 5: I realize some weeks I trade 0 times. Those weeks I make no losses = Best weeks."*

---

### **Rule #5: NGHĨ RỦI RO TRƯỚC, LỢI NHUẬN SAU**
> *"Biết exit trước khi biết entry. Stop loss trước, target sau."*

**Mandatory Risk-First Thinking:**
1. ✅ **Define stop loss BEFORE entry:**
   - Long: Stop below VAL or POC (whichever is support)
   - Short: Stop above VAH or POC (whichever is resistance)
   
2. ✅ **Calculate R:R (Risk:Reward) BEFORE entry:**
   - Minimum 1:2 (Greg: "1:1.5 acceptable if win rate >70%")
   - Ideal 1:3 (Greg's default)
   - Refuse trade if R:R < 1:2 (not worth it)

3. ✅ **Ask: "If this goes wrong, can I afford it?"**
   - If answer is "No" → Position size too large
   - If answer is "Yes, but it hurts" → Still too large
   - If answer is "Yes, and I won't lose sleep" → Correct size

**Example:**
```
Entry: $100
Stop: $98 (risk = $2)
Target: $106 (reward = $6)
R:R = $6 / $2 = 3:1 ✅ GOOD

If $2 loss = 1% of $10,000 account → Position size = $50 loss / $2 = 25 shares
```

---

### **Rule #6: THỊ TRƯỜNG LÀ THẦY GIÁO**
> *"Journal mỗi trade. Review mỗi tuần. Nếu không học từ lỗi, bạn sẽ lặp lại mãi."*

**Mandatory Journaling:**
- ✅ **After EVERY trade (win or loss):**
  ```
  Date/Time:
  Pair:
  Entry: $X | Stop: $Y | Target: $Z
  Regime: (Trending/Ranging/Choppy)
  Setup: (Spring at VAL | Upthrust at VAH | ...)
  Result: +X% or -Y%
  
  Emotion BEFORE trade: (Confident? Fearful? FOMO?)
  Emotion DURING trade: (Calm? Anxious? Moved stop?)
  Emotion AFTER trade: (Happy? Regret? Revenge?)
  
  What worked:
  What didn't work:
  What to improve:
  ```

- ✅ **Weekly review (Sunday night):**
  - How many trades? Win rate this week?
  - Which regime performed best? Which worst?
  - Any pattern in losses? (e.g., "All losses were revenge trades")
  - What to keep? What to kill?

**Greg's Wisdom:**
> *"My journal taught me: I lose most money on Fridays (tired), I win most on Tuesdays (fresh). Now I don't trade Fridays. Simple."*

---

### **Rule #7: THÍCH NGHI HOẶC BỊ ĐÀO THẢI** ⭐
> *"Thị trường luôn thay đổi. Hệ thống của bạn cũng phải vậy. Đừng kết hôn với một ý tưởng. Hãy là nước, không phải đá."*

**Mandatory Adaptability:**

1. ✅ **Identify Regime BEFORE trading (daily, 9:30 AM):**
   - Use RegimeRadar.pine: "High Vol Trend? Low Vol Range? Choppy?"
   - Match strategy to regime:
     ```
     IF Regime = "High Vol Uptrend"
       → Use CVPGreg (Trend-Following mode: Buy VAL, Sell VAH+)
     
     IF Regime = "Low Vol Range"
       → Use CVPGreg (Mean-Reversion mode: Buy VAL, Sell VAH, repeat)
     
     IF Regime = "High Vol Choppy"
       → NO TRADE (wait for regime change)
     
     IF Regime = "Neutral"
       → Scalp POC only (tight stop, 1R target)
     ```

2. ✅ **Review strategy performance per regime (monthly):**
   - "Trend-Following worked in Jan (trending month) → 70% WR"
   - "Mean-Reversion failed in Jan (no ranging days) → 40% WR"
   - "Feb looks choppy (VIX rising) → Reduce size, wait for clarity"

3. ✅ **Kill underperforming strategies:**
   - If strategy X loses 3 months straight → STOP using it
   - Don't marry your ideas (Greg: "I killed 10+ strategies in Year 3")

4. ✅ **Backtest on MULTIPLE market conditions:**
   - Does strategy work in uptrend? Downtrend? Sideways?
   - Does it work in high vol? Low vol?
   - If "Only works in X condition" → You have 1 strategy, need 2-3 more

**Greg's Checklist (Strategy Viability):**
```
✅ Strategy works in uptrend?
✅ Strategy works in downtrend?
✅ Strategy works in sideways market?
✅ How does it perform in high volatility?
✅ How does it perform in low volatility?
✅ Have I reviewed this strategy in last 6 months?
✅ Do I have backup strategy if this stops working?
```

**HiveScale's Regime Concept (Institutional Perspective):**
> *"Market tomorrow ≠ Market today. Retailers fail because they only profit in **certain regimes**. I have library of strategies (10+). At 9:29 decision engine picks which to fire."*

**Retail Adaptation (Greg + HiveScale Hybrid):**
- **Greg's approach:** Human discretionary (notice regime change weekly, switch strategy manually)
- **HiveScale's approach:** Algorithmic systematic (RNN model detects regime daily at 9:29, auto-switches)
- **Our approach (Retail Hybrid):**
  1. Use RegimeRadar.pine for **automatic regime detection** (like HiveScale)
  2. Use CVPGreg.pine for **clear signals per regime** (VP + Trend + Order Flow)
  3. Human makes **final decision** (like Greg) based on regime + signals + context
  4. Balance: Speed of automation + Flexibility of discretion

**Key Insight:**
> **Greg Rule #7 + HiveScale Regime = SAME IDEA, different execution.**
> 
> **Both say:** "One strategy won't work forever. Adapt or die."
> 
> **Difference:** Greg = Manual adaptation (human switches), HiveScale = Automatic adaptation (algo switches)
> 
> **Retail solution:** RegimeRadar (auto-detect) + Human (final decision) = Best of both worlds

---

## 🎯 PART 2: HIVESCALE'S INSTITUTIONAL WISDOM (10/30/60 Formula)

### **The 10/30/60 Formula:**
> *"Even with perfect signals (10%), they still fail. Missing: Risk Management (30%) + Psychology (60%)."*

```
100% Trading Success = 10% Signal Generation
                     + 30% Risk Management
                     + 60% Psychology/Discipline

Most retailers: 90% focus on signals, 10% on rest = Recipe for failure
Institutions: 10% signals (good enough), 90% execution = Consistent profit
```

---

### **10% = SIGNAL GENERATION (Order Flow > Lagging Indicators)**

**HiveScale's Priority:**
1. ✅ **Order Flow (CVD, Volume Profile)** = Real-time institutional footprints
2. ✅ **Market Profile (POC/VAH/VAL)** = Where institutions accepted price
3. ⚠️ **Price Action (Support/Resistance)** = Lagging, but valid
4. ❌ **Technical Indicators (RSI, MACD, Stoch)** = Lagging, institutions don't use

**Why Order Flow > TA?**
> *"My model does 0% technical analysis. It does not use charts. It's purely order flow and statistical-driven." — HiveScale*

**Retail Application:**
- CVPGreg.pine uses: **CVD (order flow) + Volume Profile (institutional levels) + 2 VSA (smart money patterns)**
- RegimeRadar.pine uses: **ATR + Trend (regime classification) → NOT lagging indicators**
- NO RSI, NO MACD, NO Stochastic (Greg: "Year 5 = Rectangle + Line, not oscillators")

---

### **30% = RISK MANAGEMENT (This is Where Retail Dies)**

**HiveScale's Risk Rules:**
1. ✅ **Position Sizing = CRITICAL** (1-2% risk per trade, scale based on conviction)
2. ✅ **Stop Loss = NON-NEGOTIABLE** (if hit, close immediately, no hoping)
3. ✅ **Risk:Reward = 1:2 minimum** (if <1:2, don't take trade)
4. ✅ **Correlation Risk** (don't trade BTC + ETH simultaneously = 2x correlated risk)
5. ✅ **Portfolio Heat** (max 6% total risk across all open positions)

**Position Sizing Formula (Conviction-Based):**
```
Base Risk: 1% per trade

IF RegimeRadar = "High Vol Trend" (clear regime)
AND CVPGreg = Triple Confluence (Spring + CVD rising + Price at VAL)
AND HTF aligned (4H POC support)
  → Increase to 2% risk (High conviction)

IF RegimeRadar = "Neutral" (unclear regime)
OR CVPGreg = Only 2/3 conditions met
  → Reduce to 0.5% risk (Low conviction)

IF RegimeRadar = "Choppy" (dangerous regime)
  → 0% risk (NO TRADE, cash is position)
```

**Portfolio Heat Calculation:**
```
Open positions:
- BTC Long: 2% risk
- ETH Long: 2% risk (correlated with BTC!)
- SPY Short: 1% risk

Total Portfolio Heat = 2% + 2% + 1% = 5% ✅ (under 6% limit)

If want to add 4th position:
- Max allowed = 6% - 5% = 1% risk only
- If 4th position needs 2% risk → WAIT for one of first 3 to close
```

---

### **60% = PSYCHOLOGY/DISCIPLINE (The Real Edge)**

**HiveScale's Truth:**
> *"I have given my signals/RNN output to many retail traders for free... they will still fail. They allow scarcity mindset, greed, FOMO, fear, revenge trading take over. **Signals alone won't save you.**"*

**Mandatory Psychological Rules:**

1. ✅ **Scarcity Mindset = Killer**
   - "I need to make money TODAY" → Leads to forcing trades
   - "I missed that move, must catch next one" → Leads to FOMO
   - **Antidote:** "Market is open 250 days/year. If I miss today, 249 more chances."

2. ✅ **Greed = Killer**
   - "This is going to moon, let me add more" → Overleveraging
   - "Why take 2R when I can get 10R?" → Refusing to take profit
   - **Antidote:** "Follow plan. 2R target = close 50%, trail rest. NO exceptions."

3. ✅ **FOMO = Killer**
   - "Everyone is buying, I must too" → Buy at top
   - "It's running without me" → Chase price
   - **Antidote:** "If I missed it, it's gone. Wait for next A+ setup."

4. ✅ **Fear = Killer**
   - "This will reverse, let me close early" → Exit at 0.5R instead of 2R
   - "Stop is too tight, let me widen it" → Turn 1% loss into 5% loss
   - **Antidote:** "Trust the plan. Trust the stop. Trust the target."

5. ✅ **Revenge Trading = Killer**
   - "Lost $500, must make it back NOW" → Overtrading
   - "Market took my money, I'll take it back" → Emotional trading
   - **Antidote:** "3 losses in row = STOP trading for 24 hours. Walk away."

**Daily Psychological Checklist (Pre-Market):**
```
Before opening platform, ask yourself:

☑ Am I calm and focused? (Yes → Continue. No → Don't trade today.)
☑ Am I trading to follow plan, or to make back yesterday's loss? (Plan → OK. Loss recovery → STOP.)
☑ Do I feel FOMO from missing recent move? (Yes → WAIT 24 hours. No → OK.)
☑ Am I hungry, tired, or emotional? (Yes → Don't trade. No → OK.)
☑ Have I reviewed my rules today? (Yes → OK. No → Read this document first.)
```

**If 1 or more answers are RED FLAGS → Don't trade today. Cash is a position.**

---

## 🎯 PART 3: ANTI-OVERWHELM & ANALYSIS PARALYSIS PREVENTION

### **The Problem:**
> *"Các chiến lược code tổ hợp indicators phức tạp làm tôi cảm giác **overwhelm** và chắc chắn đưa tới cảnh **Analysis Paralysis**."* — You (2025)

**Root Cause:**
- ❌ Too many indicators (CVD+ 4 variants, CVPZero 16 VSA, VPP6++ delta-weighted, SMPA BOS/CHoCH/OB/FVG)
- ❌ Too many signals (20+ signals, 7 alert levels, 8 divergence types)
- ❌ No clear decision framework ("Which signal to follow? When to ignore?")
- ❌ No regime awareness (Same strategy for trending vs ranging = confusion)

**Solution: Greg's Minimalism + HiveScale's Regime Awareness**

---

### **🔥 ANTI-OVERWHELM MANDATE (Effective Immediately)**

**Rule:** **If you need >3 indicators to make a decision, you don't have a system. You have confusion.**

**Allowed Setup (2 indicators ONLY):**
1. **CVPGreg.pine** (Rectangle + Line + Order Flow + 2 VSA)
   - VP (POC/VAH/VAL)
   - 50 EMA (Trend)
   - CVD (Order Flow context)
   - Spring/Upthrust (2 VSA signals)

2. **RegimeRadar.pine** (Regime Detection + Strategy Recommendation)
   - Automatic regime classification (Trending/Ranging/Choppy)
   - Strategy recommendation per regime
   - Regime change alert

**Decision Framework (NO GUESSWORK):**
```
Step 1: Check RegimeRadar (9:30 AM daily)
  → "High Vol Uptrend" → Proceed to Step 2
  → "Choppy" → STOP (no trade today)

Step 2: Check CVPGreg on 4H chart
  → Is price at VAL? (Yes → Continue. No → Wait.)
  → Is trend UP (close > 50 EMA)? (Yes → Continue. No → Wait.)
  → Is CVD rising OR Spring pattern? (Yes → Continue. No → Wait.)

Step 3: If ALL 3 conditions met → Trade
  → Entry: Market order at VAL
  → Stop: Below VAL (1% risk)
  → Target: VAH (2R)

Step 4: If <3 conditions met → WAIT (cash is position)
```

**NO MORE:**
- ❌ "Should I wait for HTF confirmation?"
- ❌ "Should I wait for divergence?"
- ❌ "Should I wait for Multi-TF alignment?"
- ❌ "Which alert level to follow? LV3 or LV5?"

**ANSWER:** If 3 conditions (VP level + Trend + Order Flow) met → Trade. Else → Wait. **SIMPLE.**

---

### **🔥 ANALYSIS PARALYSIS PREVENTION CLAUSE**

**Symptom Check:**
- Do you stare at chart for 2+ hours without taking trade? ✅ Analysis Paralysis
- Do you see 5+ signals but can't decide which to follow? ✅ Analysis Paralysis
- Do you close winning trade at 0.3R because "what if it reverses"? ✅ Analysis Paralysis
- Do you add 10th indicator hoping it will clarify? ✅ Analysis Paralysis

**Cure:**
1. **Reduce indicators to 2 (CVPGreg + RegimeRadar)**
2. **Use checklist (3 conditions: VP + Trend + Order Flow)**
3. **If confused after checklist → Don't trade (cash is position)**
4. **Set timer: 15 minutes to decide. If no decision → Close platform.**

**Greg's Quote:**
> *"Year 2: I spent 8 hours/day watching charts, made 20 trades, lost money. Year 5: I spend 30 minutes/day, make 1-3 trades, consistently profitable. **Difference? I stopped analyzing, started executing.**"*

---

## 🎯 PART 4: CODE ENFORCEMENT (For All Future Indicators/Strategies)

### **ALL indicators/strategies created from now on MUST comply:**

1. ✅ **Line Count Limit: <250 lines** (exceptions need written justification)
   - Why? Greg's Year 5 target = ~200 lines
   - If >250 lines → Too complex, will cause overwhelm
   - **Penalty:** Indicator will be rejected, must simplify

2. ✅ **Clear Decision Framework** (No guesswork)
   - Must have: "If X and Y and Z → Trade, else WAIT"
   - No vague signals: "RSI oversold" (oversold at 30? 20? 10?)
   - **Penalty:** Indicator unusable, must add clear rules

3. ✅ **Regime-Aware** (Or explicitly state limitations)
   - Either: Auto-detect regime (like RegimeRadar)
   - Or: State clearly: "This strategy works ONLY in trending markets"
   - **Penalty:** Will fail in wrong regime, user will blame indicator

4. ✅ **Reduce Overwhelm (Not Increase It)**
   - Test: "Does this make trading EASIER or MORE CONFUSING?"
   - If more confusing → Scrap it
   - **Penalty:** Contributes to Analysis Paralysis

5. ✅ **Follow Greg's Principles**
   - Rectangle (Volume Profile = institutional levels)
   - Line (Trend EMA = directional bias)
   - Eliminate 95% of features (keep only essentials)
   - **Penalty:** Year 2-3 indicator, not Year 5

6. ✅ **Apply HiveScale's Wisdom**
   - Order flow priority (CVD, VP > RSI, MACD)
   - 10/30/60 formula (signals alone won't save you)
   - Regime awareness (one strategy ≠ all conditions)
   - **Penalty:** Retail-grade indicator, not institutional-grade

---

### **✅ APPROVED TEMPLATE: CVPGreg.pine (~250 lines)**

**Complies with all 6 rules:**
1. ✅ ~250 lines (within limit)
2. ✅ Clear decision: "If price at VAL + trend UP + CVD rising → BUY"
3. ✅ Regime-aware: Use with RegimeRadar (trending → trend-following, ranging → mean-reversion)
4. ✅ Reduces overwhelm: 2 alerts (BUY/SELL), 1 decision tree
5. ✅ Greg's principles: Rectangle (VP) + Line (50 EMA) + 2 VSA (Spring/Upthrust)
6. ✅ HiveScale's wisdom: CVD (order flow) + VP (institutional levels) + No lagging indicators

**This is the standard. All future code must match or exceed this quality.**

---

## 🎯 FINAL WORDS: SIMPLICITY = SURVIVAL

### **Greg's Journey:**
- **Year 1:** 100 indicators → Confused, losing
- **Year 2:** 50 indicators → Still confused, still losing
- **Year 3:** 10 indicators → Less confused, break-even
- **Year 4:** 3 indicators → Clarity, starting to win
- **Year 5:** Rectangle + Line → Freedom (70% WR, 30 min/day, consistent profit)

### **HiveScale's Warning:**
> *"Retailers fail in **certain regimes** because they don't adapt. One strategy won't work forever. You need library of strategies + decision engine to pick which to fire."*

### **Our Path (Greg + HiveScale Synthesis):**
1. **Minimalism:** 2 indicators (CVPGreg + RegimeRadar)
2. **Clarity:** Clear decision trees (no guesswork)
3. **Adaptability:** Regime-aware (match strategy to market condition)
4. **Discipline:** 10% Signal + 30% Risk + 60% Psychology = 100% Trading
5. **Execution:** If confused → Don't trade (cash is position)

---

## 🔥 COMMIT TO MEMORY:

> **"Đơn giản ≠ Dễ dàng. Đơn giản = Có thể thực hiện được. Phức tạp = Tê liệt."**
> 
> **"Simple ≠ Easy. Simple = Executable. Complex = Paralysis."**

**If you can't explain your strategy in 3 sentences, you don't have a strategy. You have confusion.**

**Trade less. Think more. Execute better.**

**Adapt or Die.**

---

**END OF SUPREME RULE**

**Last Updated:** 2025-01-XX (Greg + HiveScale Integration)  
**Next Review:** Weekly (Sunday night)  
**Mandatory Compliance:** All traders, All indicators, All strategies, Forever.

## Key Principles

- Indicators provide signals and optional suggestions only; they do NOT execute orders or place SL/TP unless the user explicitly opts in.

- Default mode for every script is conservative: no auto-ordering, and no SL/TP suggestions unless explicitly enabled.

## Indicator Behaviour Contract

- Indicators MUST NOT execute orders.
