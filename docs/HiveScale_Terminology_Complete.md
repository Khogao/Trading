# 📖 HiveScale Terminology Complete Guide

> **Source**: HiveScale's Reddit AMA "I just left an institutional trading desk"  
> **Context**: Institutional order flow trading vs Retail technical analysis  
> **User's Choice**: GHU + CVPZ (2 indicators maximum)

---

## ⚠️ CRITICAL: CVDRSI trong GHU là gì?

### **CVD RSI = Relative Strength Index của Cumulative Volume Delta**

```pine
// Code trong Greg_HiveScale_Unified.pine (dòng 159-161)
_cvd_rsi = ta.rsi(g_cvd_cumul, 14)
_cvd_div_bull = _cvd_rsi < 30 and g_cvd_cumul > g_cvd_cumul[1]
_cvd_div_bear = _cvd_rsi > 70 and g_cvd_cumul < g_cvd_cumul[1]
```

### **Ý nghĩa:**

1. **CVD RSI là oscillator đo momentum của buying/selling pressure**
   - `ta.rsi(g_cvd_cumul, 14)` = RSI của CVD cumulative (không phải RSI của price)
   - CVD RSI > 70 = **Buyers kiệt sức** (overbought pressure)
   - CVD RSI < 30 = **Sellers kiệt sức** (oversold pressure)

2. **Khác với RSI thường:**
   - RSI thường: `ta.rsi(close, 14)` → đo momentum của giá
   - CVD RSI: `ta.rsi(cvd_cumul, 14)` → đo momentum của volume delta
   - **CVD RSI chính xác hơn vì đo actual order flow, không phải giá**

3. **Divergence Detection trong GHU:**
   - **Bullish Divergence**: CVD RSI < 30 (oversold) + CVD đang tăng = Sellers kiệt sức, buyers vào
   - **Bearish Divergence**: CVD RSI > 70 (overbought) + CVD đang giảm = Buyers kiệt sức, sellers vào

4. **Tại sao GHU dùng CVD RSI thay vì divergence phức tạp?**
   - CVPZ đã có divergence engine phức tạp (C+P, C+V)
   - GHU chỉ cần simple divergence detection để kết hợp với VP + Context
   - Theo Greg's philosophy: Simple tools, mastered execution

---

## 🤖 RNN trong AMA của HiveScale là gì?

### **RNN = Recurrent Neural Network (Mạng Neural Hồi Quy)**

HiveScale quote (từ AMA):

> **"I only trade low touch, using a RNN model to predict price movements."**

> **"My strategy is not dependent on time as I am not using candlesticks to determine entries/exits. Instead I look at MBO (level 3 data) as well since I am directly getting CME market data in colo!"**

> **"I look at MBO market data to build a statistical model of where price, volume, and time is today and X days backwards. Then I take that into a data frame where a deep learning AI model which I wrote uses to calculate where price is most likely to be tomorrow. Then I trade those areas where price is likely to be."**

### **RNN trong Trading Context:**

1. **RNN là gì?**
   - Recurrent Neural Network = Deep Learning model có "memory"
   - Khác với Neural Network thường, RNN nhớ được sequence data (time series)
   - Dùng để predict future values dựa trên historical patterns

2. **HiveScale dùng RNN như thế nào?**
   - Input: MBO (Market by Order) level 3 data từ CME
   - Process: Build statistical model của price/volume/time hiện tại + X days backward
   - Output: Predict nơi price sẽ đi trong tương lai
   - Execution: Trade ở những zones predicted

3. **Tại sao HiveScale không dùng candlesticks?**
   - "There is 0% technical analysis. My model does not use charts, at all!"
   - RNN của anh ta feed bằng **raw order flow data**, không phải OHLC
   - Candlesticks = lagging indicator (đã xảy ra)
   - Order flow = leading indicator (đang xảy ra real-time)

4. **Hardware Requirements:**
   - "I have access to a H100 SXM farm which does help!" (NVIDIA H100 GPU cluster)
   - Colo data center (NY4/DC3) để latency thấp nhất
   - Không phải tools cho retail traders thông thường

---

## 📚 Toàn bộ Terminology của HiveScale (A-Z)

### **A. Order Flow Concepts**

#### **1. CVD (Cumulative Volume Delta)**
- **Definition**: Tổng cộng dồn của (Buy Volume - Sell Volume) từ đầu session/anchor
- **Formula**: `CVD = Σ(Buy Volume - Sell Volume)`
- **Use**: Đo institutional buying/selling pressure tích lũy
- **HiveScale quote**: "CVD is the #1 tool I look at"

#### **2. MBO (Market by Order) / Level 3 Data**
- **Definition**: Raw order book data showing every individual order
- **Levels**:
  - Level 1: Best bid/ask (retail access)
  - Level 2: Full order book depth (advanced retail)
  - Level 3: Individual order IDs and fills (institutional only)
- **HiveScale quote**: "I look at MBO (level 3 data) as well since I am directly getting CME market data in colo!"
- **Data Source**: https://databento.com/ (historical MBO data)

#### **3. Volume Profile (VP)**
- **Definition**: Histogram showing volume distribution at each price level
- **Components**:
  - POC (Point of Control): Price level với volume cao nhất
  - VAH (Value Area High): Upper boundary của 70% volume
  - VAL (Value Area Low): Lower boundary của 70% volume
- **HiveScale's opinion**: "Volume Profile is the Rectangle in Greg's Year 5"

#### **4. VWAP (Volume Weighted Average Price)**
- **Definition**: Trung bình giá weighted by volume
- **Formula**: `VWAP = Σ(Price × Volume) / Σ(Volume)`
- **HiveScale quote**: "Is VWAP a core element of training models? — Yes, there are VWAP algos"
- **Context**: HiveScale's "Line" trong Greg's Rectangle + Line có thể là VWAP hoặc CVD

---

### **B. Institutional Trading Concepts**

#### **5. Sell Side vs Buy Side**
- **Sell Side**: Banks, brokerages creating/selling securities to public
- **Buy Side**: Hedge funds, asset managers buying securities
- **HiveScale's role**: Worked on sell side execution desk

#### **6. Gateway**
- **Definition**: Application where clients enter orders
- **Process**: Client → Gateway → Risk Engine → Exchange
- **HiveScale's job**: Optimize this flow for speed & price

#### **7. Execution Algorithms**
- **Types**:
  - VWAP algo: Execute at volume-weighted average price
  - TWAP algo: Time-weighted average price
  - Iceberg orders: Hide large orders, show small slices
  - Smart Order Router (SOR): Route to best exchange
- **Goal**: Get 500k+ orders filled without moving market

#### **8. Colo (Colocation)**
- **Definition**: Placing servers physically next to exchange servers
- **Benefit**: Reduce latency from milliseconds to microseconds
- **HiveScale quote**: "Currently setting up infra in NY4/DC3 for new fund"
- **NY4**: Equinix data center in New Jersey (near NYSE)
- **DC3**: CME data center in Chicago

---

### **C. Machine Learning & Quant Concepts**

#### **9. RNN (Recurrent Neural Network)**
- **Already explained above** ⬆️

#### **10. Deep Learning AI Model**
- **HiveScale's architecture**:
  1. Collect MBO data (price, volume, time) for today + X days back
  2. Build statistical model in dataframe
  3. Feed to deep learning AI (RNN)
  4. Output: Predicted price zones for tomorrow
  5. Trade those zones
- **Key**: Not predicting exact price, predicting **zones** where institutions likely to be active

#### **11. Statistical Arbitrage (Stat Arb)**
- **Definition**: Exploit temporary mispricings between correlated assets
- **HiveScale quote**: "Professionally I have worked on stat arb models exploiting options greeks"

#### **12. Sortino Ratio**
- **Definition**: Risk-adjusted return metric (only penalizes downside volatility)
- **HiveScale quote**: "Sortino mattered a lot more than Sharpe ratios"
- **Why**: Sharpe penalizes both upside and downside volatility, Sortino only downside

---

### **D. Market Structure Concepts**

#### **13. Market Regime**
- **Definition**: Current state of market behavior
- **Types**:
  - Trend: Directional, ATR expanding, price moving away from POC
  - Range: Sideways, ATR contracting, price oscillating around POC
  - Choppy: Random, high ATR but no direction
- **HiveScale quote**: "Identify different market regimes... find or create a trading strategy that can be profitable [in each regime]"

#### **14. Wyckoff Phases**
- **Definition**: 4 phases of institutional accumulation/distribution
- **Phases**:
  - Accumulation: Institutions buying (low volume, range-bound)
  - Markup: Price rising (high volume, trend up)
  - Distribution: Institutions selling (low volume, range-bound)
  - Markdown: Price falling (high volume, trend down)
- **GHU Implementation**: `f_detect_phase()` function

#### **15. Absorption**
- **Definition**: Large volume at a price level WITHOUT price movement
- **Meaning**: Institutions absorbing all retail orders at that level
- **Signal**: Strong support/resistance, potential reversal zone
- **GHU Implementation**: `f_detect_absorption()` function

---

### **E. Retail vs Institutional Concepts**

#### **16. Technical Analysis (TA)**
- **HiveScale's opinion**: "There is 0% technical analysis. My model does not use charts, at all!"
- **Why TA fails**:
  - Lagging indicators (RSI, MACD, EMA)
  - Based on past price (not current order flow)
  - Everyone sees same patterns → overcrowded trades
- **What institutions use instead**: Order flow data (CVD, VP, MBO)

#### **17. Candlestick Patterns**
- **HiveScale quote**: "Candlestick patterns are nonsense"
- **Why**: Arbitrary patterns with no statistical edge
- **What works instead**: "Standard deviation is actually telling you something about how **people** and **price** BEHAVED"

#### **18. Stop Hunting Myth**
- **HiveScale quote**: "The mentality that institutions are taking the stops of retail traders is just not founded in reality. Retail orders are too small to matter."
- **Reality**: Institutions don't care about retail stops
- **Exception**: Meme stocks (collective retail becomes institutional-size)

---

### **F. HiveScale's 10/30/60 Formula**

#### **19. 10% Signal**
- **Definition**: Trading edge/strategy
- **Examples**: RNN model, CVD divergence, VP levels
- **HiveScale's approach**: Library of 10 strategies, fire on different days/weeks/months

#### **20. 30% Risk Management**
- **Definition**: Position sizing, stop loss, risk per trade
- **Key**: Protect capital, survive to trade another day

#### **21. 60% Psychology**
- **Definition**: Discipline, emotion control, consistency
- **HiveScale quote**: "I have given my signals/RNN output to many retail traders and even though the system has a 75%+ win rate they couldn't follow it because of emotions"
- **Implication**: Perfect signals ≠ Profitable trader if psychology fails

---

### **G. Trading Infrastructure**

#### **22. FPGA (Field-Programmable Gate Array)**
- **Definition**: Hardware chip programmed for ultra-low latency
- **Use**: Process market data & send orders faster than CPU
- **HiveScale quote**: Worked with FPGAs for HFT (High Frequency Trading)

#### **23. CME (Chicago Mercantile Exchange)**
- **Definition**: Largest futures exchange (ES, NQ, GC, CL)
- **HiveScale's markets**: /ES, /NQ, /GC, /CL futures

#### **24. H100 SXM Farm**
- **Definition**: NVIDIA H100 GPU cluster (latest AI hardware)
- **Use**: Train deep learning models (RNN) on massive datasets
- **Cost**: ~$30k per GPU, needs farm of dozens for HiveScale's models

---

## 🎯 Key Takeaways for YOUR System (GHU + CVPZ)

### **What HiveScale Uses (Institutional Level):**
1. ✅ CVD (you have this in both GHU & CVPZ)
2. ✅ Volume Profile (you have this in GHU via VPP5+/VPP6++ upgrade)
3. ❌ RNN/Deep Learning (requires H100 farm, MBO data, colo infrastructure)
4. ❌ Level 3 MBO data (institutional only, ~$10k/month subscription)
5. ❌ Colo servers (NY4/DC3, ~$5k-20k/month)

### **What YOU Can Replicate (Retail Level):**
1. ✅ CVD analysis (GHU + CVPZ both have this)
2. ✅ Volume Profile (GHU will have VPP5+/VPP6++ engine)
3. ✅ Divergence detection (CVPZ has C+P, C+V; GHU has CVD RSI)
4. ✅ Context analysis (GHU has Regime/Phase/Absorption)
5. ✅ Confluence scoring (GHU's 1-5 star system)

### **CVD RSI trong GHU:**
- **Simple but effective** divergence detector
- Complements CVPZ's advanced C+P and C+V divergences
- GHU (simple divergence + context) + CVPZ (advanced divergence + VSA) = Complete system

### **Why You Don't Need RNN:**
- RNN requires: H100 farm, MBO data, colo, PhD-level ML knowledge
- Your edge = **Context-aware order flow analysis** (GHU) + **Divergence hunting** (CVPZ)
- Greg's Year 5 wisdom: Master simple tools, not accumulate complex ones

---

## 📊 Decision Validation: GHU + CVPZ

### **Why This Combo Works:**

| Component | GHU Role | CVPZ Role |
|-----------|----------|-----------|
| **Context** | ✅ Regime/Phase/Absorption | ❌ No context |
| **VP** | ✅ Full histogram + HTF levels | ❌ No VP |
| **CVD** | ✅ Basic CVD confirmation | ✅ Multi-TF CVD table |
| **Divergence** | ✅ Simple (CVD RSI) | ✅ Advanced (C+P, C+V) |
| **VSA** | ❌ No VSA | ✅ 10 VSA signals |
| **Alerts** | ✅ 7-level confluence | ✅ 5-type alerts |

### **How They Complement:**

1. **GHU answers "WHAT" and "WHEN"**:
   - WHAT: Market regime (Trend/Range/Choppy)
   - WHAT: Wyckoff phase (Accumulation/Distribution/etc)
   - WHEN: Price at VP level (POC/VAH/VAL)
   - WHEN: CVD confirming direction

2. **CVPZ answers "WHY" and "HOW STRONG"**:
   - WHY: Divergence (institutions accumulating/distributing)
   - HOW STRONG: VSA signals (volume spike types)
   - HOW STRONG: Multi-TF CVD alignment

3. **Together = Complete Order Flow System:**
   - GHU: "We're in Accumulation phase at VAL with CVD rising" → Setup forming
   - CVPZ: "C+P bullish divergence + No Demand signal" → Entry confirmed
   - Combined alert: LV7 (Holy Grail) → Take the trade

---

## 🚀 Next Steps: Upgrade GHU VP Engine

Now that you understand all terminology, I'll:

1. **Upgrade GHU's `f_calculate_vp()` function**:
   - Import full VP histogram engine from VPP5+ or VPP6++
   - Add HTF levels (240/D POC/VAH/VAL) via `request.security()`
   - Keep same output interface for GHU's existing logic

2. **Keep GHU's CVD RSI as-is**:
   - It's intentionally simple (complements CVPZ's advanced divergence)
   - Focus is on context detection, not divergence complexity

3. **Final system**:
   - **GHU**: Context (Regime/Phase/Absorption) + VP + CVD + Confluence alerts
   - **CVPZ**: Divergence (C+P, C+V) + VSA + Multi-TF CVD table
   - **Maximum 2 indicators** = Clean chart, clear system

**Ready to upgrade? Should I proceed with VPP5+ or VPP6++ VP engine integration?**

VPP5+ (668 lines) = Stable, production-proven  
VPP6++ = Has HTF VP levels built-in (might be cleaner integration)

Bạn chọn nào?
