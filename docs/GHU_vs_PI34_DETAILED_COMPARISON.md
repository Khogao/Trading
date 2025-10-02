# 📊 SO SÁNH CHI TIẾT: GHU vs PI34 Pro

## 🎯 TÓM TẮT NHANH (TL;DR)

| Tiêu chí | **GHU** (Greg+HiveScale Unified) | **PI34 Pro** (Pi 3.4 Professional) |
|----------|----------------------------------|-------------------------------------|
| **Triết lý** | WHAT → WHEN → HOW (Context first) | Volume Profile + VSA + CVD (Technical focus) |
| **Điểm mạnh** | Context detection, 7-level alerts | Advanced VP engine, 10 VSA signals |
| **Điểm yếu** | Basic VP calculation | No regime/phase detection |
| **Độ phức tạp** | Medium (632 lines) | High (939 lines) |
| **Win rate cao nhất** | LV7: 80-85% | LV5: 80-85% |
| **Phù hợp với** | Traders cần context (Wyckoff) | Traders focus vào orderflow |
| **Khuyến nghị** | Dùng làm MASTER indicator | Dùng làm CONFIRMATION indicator |

---

## 📏 SO SÁNH KỸ THUẬT CHI TIẾT

### **1️⃣ KIẾN TRÚC & TRIẾT LÝ**

#### **GHU (Greg+HiveScale Unified)**
```
Architecture: 3-Layer System
├─ LAYER 1: WHAT (Context Analysis)
│  ├─ Volume Profile (basic, 120 levels)
│  ├─ CVD (Cumulative Volume Delta)
│  ├─ Volume Z-Score
│  ├─ Regime Detection (Trend/Range/Choppy)
│  ├─ Phase Detection (Wyckoff: Accumulation/Distribution/Markup/Markdown)
│  ├─ Absorption Detection (Institutional activity at VAH/VAL)
│  └─ Context Synthesis (BULL/BEAR/NEUTRAL)
│
├─ LAYER 2: WHEN (Signal Generation)
│  ├─ Price at VP levels (VAL/VAH/POC)
│  ├─ CVD confirmation (rising/falling/divergence)
│  └─ Volume confirmation (spike detection)
│
└─ LAYER 3: HOW (Confluence Scoring)
   ├─ Buy/Sell Score (1-5 stars)
   ├─ Context aligned bonus
   ├─ Phase aligned bonus
   └─ High confidence threshold (4+ stars)
```

**Triết lý**: Context determines everything. Signal chỉ quan trọng khi context đúng.

**Ưu điểm**:
- ✅ **Regime Detection**: Biết được market đang Trend/Range/Choppy → trade theo đúng style
- ✅ **Phase Detection**: Wyckoff-inspired → biết được Accumulation (nên mua) hay Distribution (nên bán)
- ✅ **Absorption Detection**: Phát hiện institutional activity (volume spike + narrow range tại VAH/VAL)
- ✅ **Context Synthesis**: BULL/BEAR/NEUTRAL tổng hợp từ Regime + Phase + Absorption
- ✅ **7-Level Alert System**: Phân loại rõ ràng từ LV1 (50%) đến LV7 (85%)

**Nhược điểm**:
- ❌ **Basic VP**: Chỉ 120 levels, không có histogram visualization
- ❌ **No HTF Levels**: Không có Higher Timeframe VP (chỉ LTF)
- ❌ **No HVN/LVN**: Không có structure node detection
- ❌ **Simple CVD**: Chỉ có CVD rising/falling + simple divergence (RSI-based)

---

#### **PI34 Pro**
```
Architecture: Volume Profile-Centric
├─ VP ENGINE (VPP5 Enhanced, 120 levels)
│  ├─ Advanced VP calculation (age decay, session weight)
│  ├─ VP Histogram visualization (bars)
│  ├─ HTF VP levels (240/D POC/VAH/VAL)
│  ├─ HVN/LVN structure nodes
│  └─ Intraday session focus
│
├─ VSA ANALYSIS (10 signals)
│  ├─ Selling Climax (SC)
│  ├─ Buying Climax (BC)
│  ├─ No Demand (ND)
│  ├─ No Supply (NS)
│  ├─ Upthrust (UT)
│  ├─ Spring (SP)
│  ├─ Stopping Volume (SV)
│  ├─ Weakness (WK)
│  ├─ Strength (ST)
│  └─ Shakeout (SO)
│
├─ CVD LITE (Overlay markers)
│  ├─ CVD calculation (TradingView/ta/8)
│  ├─ Pivot-based divergence detection
│  ├─ Regular divergence (reversal)
│  ├─ Hidden divergence (continuation)
│  └─ Divergence line drawing
│
├─ VOLUME Z-SCORE
│  ├─ Adaptive classification (LTF vs HTF)
│  ├─ 4 tiers (Ultra/Very/High/Low)
│  └─ Volume coloring on chart
│
└─ 7-LEVEL ALERT SYSTEM
   ├─ LV1: Basic VSA/Divergence (50-55%)
   ├─ LV2: VSA @ VP / Div @ VP (65-70%)
   ├─ LV3: HTF Alignment (70-75%)
   ├─ LV4: Volume Extreme (75-80%)
   └─ LV5: Triple Confluence (80-85% - Holy Grail)
```

**Triết lý**: Order flow + Volume Profile = Truth. Price follows volume.

**Ưu điểm**:
- ✅ **Advanced VP Engine**: VPP5 production-grade, age decay, session weight
- ✅ **VP Histogram**: Visual volume distribution bars
- ✅ **HTF VP Levels**: 240/D POC/VAH/VAL cho institutional context
- ✅ **HVN/LVN Zones**: Consolidation (HVN) vs Breakout (LVN) areas
- ✅ **10 VSA Signals**: Complete VSA system (CVPZero engine)
- ✅ **CVD Lite**: Pivot-based divergence (regular + hidden)
- ✅ **Volume Z-Score**: Adaptive classification cho crypto
- ✅ **Intraday Mode**: Session focus (9-17h) cho day traders

**Nhược điểm**:
- ❌ **No Regime Detection**: Không biết market đang Trend/Range/Choppy
- ❌ **No Phase Detection**: Không có Wyckoff Accumulation/Distribution
- ❌ **No Context Synthesis**: Không có BULL/BEAR context tổng hợp
- ❌ **No Absorption Detection**: Không phát hiện institutional absorption
- ❌ **Complex Inputs**: 60+ inputs, overwhelming cho beginners

---

### **2️⃣ VOLUME PROFILE SO SÁNH**

| Feature | GHU | PI34 Pro |
|---------|-----|----------|
| **VP Levels** | 120 | 120 |
| **VP Lookback** | 200 bars | 200 bars (adaptive) |
| **VP Calculation** | Basic (uniform distribution) | Advanced (age decay, session weight, typical price) |
| **VP Visualization** | Lines only (POC/VAH/VAL) | Histogram bars + Lines |
| **HTF VP** | ❌ No | ✅ Yes (240/D POC/VAH/VAL) |
| **HVN/LVN Zones** | ❌ No | ✅ Yes (80%/20% thresholds) |
| **Intraday Mode** | ❌ No | ✅ Yes (session focus 9-17h) |
| **Volume Type Filter** | ❌ No | ✅ Yes (Both/Bullish/Bearish) |
| **Age Decay** | ❌ No | ✅ Yes (recent bars weighted higher) |
| **Session Weight** | ❌ No | ✅ Yes (1.2x for current session) |

**Kết luận VP**: PI34 Pro vượt trội hoàn toàn về VP engine.

---

### **3️⃣ CVD (CUMULATIVE VOLUME DELTA) SO SÁNH**

| Feature | GHU | PI34 Pro |
|---------|-----|----------|
| **CVD Source** | request.security() lower TF | tav6.requestVolumeDelta() |
| **CVD Accuracy** | Medium (estimated from close>open) | High (true delta from TradingView) |
| **CVD Reset** | Daily/Weekly anchor | Daily/Weekly anchor |
| **CVD Divergence** | ✅ Simple (RSI-based) | ✅ Advanced (Pivot-based) |
| **Divergence Types** | Bullish/Bearish only | Regular + Hidden (4 types) |
| **Divergence Lines** | ❌ No | ✅ Yes (visual connections) |
| **CVD Chart Display** | ❌ No (background only) | ❌ No (overlay markers only) |
| **CVD Confirmation** | CVD rising/falling vs MA | CVD pivot detection (5-bar left/right) |

**Kết luận CVD**: PI34 Pro có CVD chính xác hơn (tav6) và divergence detection tốt hơn (pivot-based).

---

### **4️⃣ VSA (VOLUME SPREAD ANALYSIS) SO SÁNH**

| Feature | GHU | PI34 Pro |
|---------|-----|----------|
| **VSA Signals** | ❌ No dedicated VSA | ✅ 10 signals (SC/BC/ND/NS/UT/SP/SV/WK/ST/SO) |
| **Spring Detection** | ❌ No | ✅ Yes (low vol + narrow range + test low) |
| **Upthrust Detection** | ❌ No | ✅ Yes (high vol + test high + fail) |
| **Climax Detection** | ❌ No | ✅ Yes (SC: bearish climax, BC: bullish climax) |
| **No Demand/Supply** | ❌ No | ✅ Yes (low vol + weak close) |
| **Stopping Volume** | ❌ No | ✅ Yes (ultra high vol + narrow range) |
| **Weakness/Strength** | ❌ No | ✅ Yes (high vol + wide range + close position) |
| **Shakeout** | ❌ No | ✅ Yes (high vol + test low + strong close) |
| **VSA Score** | ❌ No | ✅ Yes (-3 to +3, aggregated) |
| **Volume Classifier** | Z-Score only | Ratio + Z-Score (adaptive) |
| **CVD Confirmation** | ❌ No | ✅ Optional (filter false VSA signals) |

**Kết luận VSA**: PI34 Pro có complete VSA system (10 signals), GHU hoàn toàn không có VSA.

---

### **5️⃣ CONTEXT DETECTION SO SÁNH**

| Feature | GHU | PI34 Pro |
|---------|-----|----------|
| **Regime Detection** | ✅ Yes (Trend Up/Down/Range/Choppy) | ❌ No |
| **Phase Detection** | ✅ Yes (Accumulation/Distribution/Markup/Markdown/Neutral) | ❌ No |
| **Absorption Detection** | ✅ Yes (Bull/Bear absorption at VAH/VAL) | ❌ No |
| **Context Synthesis** | ✅ Yes (BULL/BEAR/NEUTRAL) | ❌ No |
| **Trend Context** | ✅ Yes (via Regime) | ✅ Yes (via EMA 21/50/200 + Cloud) |
| **Wyckoff Analysis** | ✅ Yes (Phase detection) | ❌ No |
| **ATR Ratio Analysis** | ✅ Yes (Trend/Range threshold) | ✅ Yes (for VSA range analysis) |
| **POC Cross Count** | ✅ Yes (detect choppy market) | ❌ No |

**Kết luận Context**: GHU vượt trội hoàn toàn về context detection (Regime + Phase + Absorption).

---

### **6️⃣ ALERT SYSTEM SO SÁNH**

#### **GHU: 7-Level Alert System**
```
LV1A: VP Level Touch (Price at VAL/VAH)              ~50-55% WR
LV1B: CVD Signal (CVD rising/falling)                ~50-55% WR
───────────────────────────────────────────────────────────────
LV2A: VP + CVD (VAL + CVD rising / VAH + CVD falling) ~55-60% WR
LV2B: VP + Volume (VP level + Volume spike)          ~55-60% WR
───────────────────────────────────────────────────────────────
LV3:  Context Aligned (Signal + BULL/BEAR context)   ~60-65% WR
───────────────────────────────────────────────────────────────
LV4:  Phase Aligned (Context + Accumulation/Dist)    ~65-70% WR
───────────────────────────────────────────────────────────────
LV5:  Triple Confluence (VP + CVD + Volume)          ~70-75% WR
───────────────────────────────────────────────────────────────
LV6:  Absorption Detected (Institutions absorbing)   ~75-80% WR
───────────────────────────────────────────────────────────────
LV7:  HOLY GRAIL (All aligned: Context+Phase+VP+CVD  ~80-85% WR
      +Vol+NoAbsorption)
```

**Logic**: Confluence tăng dần → Win rate tăng dần.  
**Focus**: Context-first approach (Context → Phase → Signal → Confluence).

---

#### **PI34 Pro: 7-Level Alert System**
```
CẤP 1A: Basic VSA (Spring/Upthrust/Climax/etc)       ~50-55% WR
CẤP 1B: Basic Divergence (CVD+Price divergence)      ~50-55% WR
───────────────────────────────────────────────────────────────
CẤP 2A: VSA @ VP (VSA signal AT POC/VA)              ~65-70% WR
CẤP 2B: Divergence @ VP (CVD div AT POC/VA)          ~65-70% WR
───────────────────────────────────────────────────────────────
CẤP 3:  HTF Alignment (Signal AT HTF POC/VA)         ~70-75% WR
───────────────────────────────────────────────────────────────
CẤP 4:  Volume Extreme (Ultra high vol + VSA/Div     ~75-80% WR
        + VP level)
───────────────────────────────────────────────────────────────
CẤP 5:  TRIPLE CONFLUENCE - HOLY GRAIL               ~80-85% WR
        (VSA + Divergence + VP level)
        🔥 Setup hiếm, 1-3 lần/tháng!
```

**Logic**: Location + Volume + Signal → Win rate tăng.  
**Focus**: Order flow-first approach (VSA/Div → VP → HTF → Volume).

---

### **7️⃣ ĐIỂM MẠNH & ĐIỂM YẾU**

#### **GHU (Greg+HiveScale Unified)**

**✅ ĐIỂM MẠNH:**
1. **Context Detection**: Regime + Phase + Absorption → biết được WHAT (market structure)
2. **Wyckoff Philosophy**: Accumulation/Distribution phases → institutional thinking
3. **Context Synthesis**: BULL/BEAR/NEUTRAL tổng hợp từ nhiều yếu tố
4. **Absorption Detection**: Phát hiện institutional activity (volume spike + narrow range tại VAH/VAL)
5. **7-Level Alerts**: Phân loại rõ ràng từ 50% (LV1) đến 85% (LV7)
6. **Clean Interface**: 9 input groups, easy to understand
7. **Greg's Philosophy**: WHAT → WHEN → HOW (context-first trading)

**❌ ĐIỂM YẾU:**
1. **Basic VP**: Chỉ 120 levels, không có histogram visualization
2. **No HTF Levels**: Không có Higher Timeframe VP (240/D)
3. **No HVN/LVN**: Không có structure node detection
4. **Simple CVD**: request.security() (estimated delta, không chính xác bằng tav6)
5. **No VSA Signals**: Không có 10 VSA signals (Spring/Upthrust/Climax/etc)
6. **No Divergence Lines**: Chỉ có divergence detection, không có visual lines

---

#### **PI34 Pro**

**✅ ĐIỂM MẠNH:**
1. **Advanced VP Engine**: VPP5 production-grade (age decay, session weight, typical price distribution)
2. **VP Histogram**: Visual volume distribution bars (clear institutional zones)
3. **HTF VP Levels**: 240/D POC/VAH/VAL → institutional context
4. **HVN/LVN Zones**: Consolidation (HVN 80%) vs Breakout (LVN 20%) areas
5. **10 VSA Signals**: Complete VSA system (SC/BC/ND/NS/UT/SP/SV/WK/ST/SO)
6. **Accurate CVD**: tav6.requestVolumeDelta() (true delta from TradingView)
7. **Pivot Divergence**: Advanced divergence detection (regular + hidden)
8. **Volume Z-Score**: Adaptive classification (LTF 2.5 / HTF 1.6 sensitivity)
9. **Intraday Mode**: Session focus (9-17h) cho day traders
10. **7-Level Alerts**: From basic (50%) to Triple Confluence (85%)

**❌ ĐIỂM YẾU:**
1. **No Regime Detection**: Không biết market đang Trend/Range/Choppy
2. **No Phase Detection**: Không có Wyckoff Accumulation/Distribution
3. **No Context Synthesis**: Không có BULL/BEAR context tổng hợp
4. **No Absorption Detection**: Không phát hiện institutional absorption
5. **Complex Inputs**: 60+ inputs, overwhelming cho beginners
6. **No Context Dashboard**: Chỉ có Info Panel (Trend/Volume/VSA Score)
7. **No Confluence Scoring**: Không có 1-5 stars scoring system

---

### **8️⃣ USE CASES & KHUYẾN NGHỊ**

#### **Khi nào dùng GHU?**

✅ **Phù hợp với:**
- Traders ưu tiên **context** (Wyckoff, Regime, Phase)
- Traders trade theo **market structure** (Accumulation → Markup, Distribution → Markdown)
- Traders muốn biết **WHAT** (market regime) trước khi vào lệnh
- Traders cần **absorption detection** (institutional activity)
- Traders muốn **clean interface** (9 input groups, không overwhelming)
- Swing traders (focus on LV6-7 alerts, ~10-20 signals/month)

✅ **Ví dụ trading workflow với GHU:**
```
1. Check Context Dashboard: BULL or BEAR?
   → If NEUTRAL/CHOPPY, skip trading (wait for clear regime)

2. Check Phase: Accumulation or Distribution?
   → If Accumulation in BULL context, prepare to BUY
   → If Distribution in BEAR context, prepare to SELL

3. Wait for LV5+ alert (Triple Confluence):
   → Price at VAL + CVD rising + Volume spike

4. Check Absorption:
   → If "Bull (VAH)" absorption, wait for breakout
   → If "Clear", safe to enter

5. Enter trade:
   → Entry: VAL
   → Stop: Below VAL
   → Target: POC → VAH
```

---

#### **Khi nào dùng PI34 Pro?**

✅ **Phù hợp với:**
- Traders ưu tiên **order flow** (VSA + CVD divergence)
- Traders focus vào **volume distribution** (VP histogram, HVN/LVN)
- Traders cần **HTF context** (240/D POC/VAH/VAL)
- Day traders (intraday mode, session focus 9-17h)
- Traders thích **visual confirmation** (VP histogram, divergence lines, HVN/LVN zones)
- Scalpers/Day traders (focus on LV2-4 alerts, ~40-60 signals/month)

✅ **Ví dụ trading workflow với PI34 Pro:**
```
1. Check VP Histogram:
   → HVN zone = consolidation, wait for breakout
   → LVN zone = potential breakout area

2. Check HTF POC/VAH/VAL (240/D):
   → Price near HTF POC = high probability bounce/rejection

3. Wait for VSA signal (10 types):
   → Spring at VAL = bullish reversal
   → Upthrust at VAH = bearish reversal

4. Check CVD divergence:
   → Regular divergence = reversal signal
   → Hidden divergence = continuation signal

5. Wait for LV3+ alert (HTF Alignment or higher):
   → VSA/Div AT HTF POC/VA + Volume extreme

6. Enter trade:
   → Entry: HTF VAL (for long) / HTF VAH (for short)
   → Stop: Tight (0.5R if LV4 Volume Extreme)
   → Target: 2-3R
```

---

### **9️⃣ KHUYẾN NGHỊ SỬ DỤNG 2 INDICATORS CÙNG LÚC**

#### **🎯 Cấu hình lý tưởng: GHU (Master) + PI34 Pro (Confirmation)**

**Lý do:**
- GHU cung cấp **CONTEXT** (Regime + Phase + Absorption) → biết WHAT & WHERE
- PI34 Pro cung cấp **CONFIRMATION** (VSA + CVD divergence + HTF VP) → biết WHEN & HOW STRONG

**Workflow kết hợp:**
```
STEP 1: Check GHU Context Dashboard
├─ Regime: Trend Up/Down/Range/Choppy?
├─ Phase: Accumulation/Distribution/Markup/Markdown?
├─ Absorption: Clear or Absorbing?
└─ Context: BULL/BEAR/NEUTRAL?

STEP 2: If Context is BULL/BEAR (not NEUTRAL/CHOPPY), proceed
└─ If NEUTRAL/CHOPPY, SKIP trading (wait for clear trend)

STEP 3: Check PI34 Pro VP Histogram
├─ Is price near HVN (consolidation) or LVN (breakout)?
├─ Is price near HTF POC/VAH/VAL (240/D)?
└─ Is VP histogram showing accumulation at current level?

STEP 4: Wait for CONFLUENCE of alerts
├─ GHU Alert: LV5+ (Triple Confluence or higher)
│  └─ VP + CVD + Volume + Context + Phase aligned
│
└─ PI34 Alert: CẤP 3+ (HTF Alignment or higher)
   └─ VSA signal AT HTF VP level + Volume extreme

STEP 5: Enter trade when BOTH indicators confirm
├─ Entry: VP level (VAL for long, VAH for short)
├─ Stop: GHU gives context (below VAL if Accumulation phase)
├─ Target: PI34 gives targets (HTF POC → HTF VAH)
└─ Risk: 2% if both LV7 (GHU) + CẤP 5 (PI34) → HOLY GRAIL setup!
```

**Ví dụ setup hoàn hảo:**
```
GHU shows:
✅ Regime: Trend Up
✅ Phase: Accumulation
✅ Context: BULL
✅ Absorption: Clear
✅ Alert: LV7 HOLY GRAIL (Price at VAL + CVD rising + Volume spike)

PI34 Pro shows:
✅ VP Histogram: Accumulation at current VAL
✅ HTF POC (240): Price near HTF VAL (institutional support)
✅ HVN Zone: Price exiting HVN (consolidation ending)
✅ VSA Signal: Spring (low vol + test low + strong close)
✅ CVD Divergence: Regular bullish (price LL, CVD HL)
✅ Alert: CẤP 5 TRIPLE CONFLUENCE (VSA + Div + VP)

→ ENTER LONG IMMEDIATELY!
→ Entry: Current VAL
→ Stop: Below VAL (0.5-1 ATR)
→ Target: POC (50%) → HTF POC (30%) → HTF VAH (20% trailing)
→ Risk: 2% vốn (setup hiếm, 1-3 lần/tháng)
→ Expected Win Rate: 85-90% (both LV7 + CẤP 5)
```

---

### **🔟 KẾT LUẬN CUỐI CÙNG**

#### **So sánh tổng quan:**

| Tiêu chí | GHU | PI34 Pro | Winner |
|----------|-----|----------|--------|
| **Context Detection** | ⭐⭐⭐⭐⭐ (Regime+Phase+Absorption) | ⭐⭐ (Only EMA trend) | 🏆 **GHU** |
| **Volume Profile** | ⭐⭐ (Basic, lines only) | ⭐⭐⭐⭐⭐ (Advanced, histogram, HTF) | 🏆 **PI34** |
| **VSA Signals** | ⭐ (No dedicated VSA) | ⭐⭐⭐⭐⭐ (10 signals complete) | 🏆 **PI34** |
| **CVD Accuracy** | ⭐⭐⭐ (request.security) | ⭐⭐⭐⭐⭐ (tav6 true delta) | 🏆 **PI34** |
| **Divergence Detection** | ⭐⭐⭐ (Simple RSI-based) | ⭐⭐⭐⭐⭐ (Pivot-based, 4 types) | 🏆 **PI34** |
| **Alert System** | ⭐⭐⭐⭐⭐ (7 levels, 50-85%) | ⭐⭐⭐⭐⭐ (7 levels, 50-85%) | 🤝 **TIE** |
| **Ease of Use** | ⭐⭐⭐⭐ (9 groups, clean) | ⭐⭐⭐ (60+ inputs, complex) | 🏆 **GHU** |
| **Wyckoff Analysis** | ⭐⭐⭐⭐⭐ (Phase detection) | ⭐ (No phase detection) | 🏆 **GHU** |
| **Institutional Tracking** | ⭐⭐⭐⭐ (Absorption detection) | ⭐⭐⭐⭐⭐ (HVN/LVN, HTF VP) | 🏆 **PI34** |
| **Visual Clarity** | ⭐⭐⭐⭐ (Dashboard clean) | ⭐⭐⭐⭐⭐ (Histogram, lines, zones) | 🏆 **PI34** |

---

#### **🎯 KHUYẾN NGHỊ CUỐI CÙNG:**

**1. Nếu chỉ dùng 1 indicator:**
- **Swing Traders / Position Traders**: Dùng **GHU** (context detection quan trọng hơn)
- **Day Traders / Scalpers**: Dùng **PI34 Pro** (orderflow + HTF VP quan trọng hơn)

**2. Nếu dùng 2 indicators (KHUYẾN NGHỊ):**
- **Master Indicator**: **GHU** (provides WHAT & WHERE via Context)
- **Confirmation Indicator**: **PI34 Pro** (provides WHEN & HOW STRONG via VSA+CVD+HTF)

**3. Nếu dùng 3 indicators (Maximum limit):**
- **Indicator 1**: **GHU** (Context: Regime + Phase + Absorption)
- **Indicator 2**: **PI34 Pro** (Orderflow: VSA + CVD + HTF VP)
- **Indicator 3**: **CVPZ** (Multi-TF CVD table + Advanced divergences)

**Lý do cấu hình 3 indicators:**
```
GHU answers:
- WHAT: Market regime (Trend/Range/Choppy)
- WHERE: Phase (Accumulation/Distribution/etc)
- CONTEXT: BULL/BEAR/NEUTRAL synthesis

PI34 Pro answers:
- WHEN: VP levels (LTF + HTF POC/VAH/VAL)
- HOW: VSA signals (10 types) + Volume extreme
- WHERE: HVN/LVN structure nodes

CVPZ answers:
- WHY: Advanced divergences (C+P, C+V, P+V)
- HOW STRONG: Multi-TF CVD table (1m → Daily alignment)
- CONFIRMATION: VSA signals (10 types) + Multi-TF context
```

**Kết luận**:
- **GHU** và **PI34 Pro** KHÔNG duplicate, chúng COMPLEMENT nhau
- GHU = Context (WHAT/WHERE)
- PI34 = Orderflow (WHEN/HOW)
- Combined = Complete trading system

---

## 📌 CHEAT SHEET

### **GHU Alert Priorities:**
```
LV7 (Holy Grail) → TAKE IMMEDIATELY (80-85% WR)
LV6 (Absorption) → WAIT for breakout confirmation (75-80% WR)
LV5 (Triple) → TAKE if context aligned (70-75% WR)
LV4 (Phase) → TAKE if phase = Accum/Dist (65-70% WR)
LV3 (Context) → TAKE if context = BULL/BEAR (60-65% WR)
LV2 (Confluence) → WAIT for more confirmation (55-60% WR)
LV1 (Basic) → SKIP, too low WR (50-55% WR)
```

### **PI34 Pro Alert Priorities:**
```
CẤP 5 (Triple Confluence) → ALL-IN MINDSET (80-85% WR, 1-3 lần/tháng)
CẤP 4 (Volume Extreme) → VÀO NGAY (75-80% WR, institutional activity)
CẤP 3 (HTF Alignment) → VÀO NGAY (70-75% WR, HTF support/resistance)
CẤP 2 (VSA/Div @ VP) → CÓ THỂ VÀO (65-70% WR, wait for close confirmation)
CẤP 1 (Basic) → SKIP (50-55% WR, wait for confluence)
```

### **Combined Alert Strategy:**
```
🔥 HOLY GRAIL SETUP (Risk 2% vốn):
├─ GHU: LV7 (All aligned: Context+Phase+VP+CVD+Vol+Clear)
└─ PI34: CẤP 5 (VSA + Divergence + VP level)
   → WIN RATE: 85-90%
   → FREQUENCY: 1-3 lần/tháng
   → ACTION: VÀO NGAY không chờ!

🎯 HIGH CONFIDENCE SETUP (Risk 1.5% vốn):
├─ GHU: LV6 (Absorption) OR LV5 (Triple)
└─ PI34: CẤP 4 (Volume Extreme) OR CẤP 3 (HTF Alignment)
   → WIN RATE: 75-80%
   → FREQUENCY: ~5-10 lần/tháng
   → ACTION: Vào sau khi confirm breakout (if LV6)

⭐ DECENT SETUP (Risk 1% vốn):
├─ GHU: LV4 (Phase Aligned) OR LV3 (Context Aligned)
└─ PI34: CẤP 2 (VSA/Div @ VP)
   → WIN RATE: 65-70%
   → FREQUENCY: ~20-30 lần/tháng
   → ACTION: Có thể vào, nhưng TP sớm hơn (2R thay vì 3R)

🚫 SKIP SETUPS:
├─ GHU shows: NEUTRAL/CHOPPY context → SKIP
├─ GHU shows: Absorption + No breakout → SKIP
├─ PI34 shows: Only CẤP 1 without context → SKIP
└─ Both show LV1-2 only → SKIP (too low WR)
```

---

## 🏁 TÓM TẮT 1 DÒNG

**GHU = Context King (WHAT/WHERE), PI34 Pro = Orderflow King (WHEN/HOW).**  
**Dùng cả 2 = Complete System. Greg's Year 5: Rectangle (VP) + Line (Context). ✅**

---

**© 2025 Trading Analysis - GHU vs PI34 Pro Comparison**
