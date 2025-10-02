# ═══════════════════════════════════════════════════════════════════════
# CLAUDE SYSTEM INSTRUCTIONS - TRADING WORKSPACE
# Created: 2025-10-03
# Purpose: Enforce critical rules for Pine Script development
# ═══════════════════════════════════════════════════════════════════════

## 🔥 CRITICAL RULE #1: TIẾNG VIỆT BẮT BUỘC

**MANDATORY - NO EXCEPTIONS:**
- ALWAYS respond in Vietnamese (Tiếng Việt)
- English is FORBIDDEN except for:
  - Code comments
  - Technical variable names
  - Error messages from tools
- This rule is ABSOLUTE and NON-NEGOTIABLE
- Priority: HIGHEST (like preventing fake CVD bugs)

**Example:**
- ❌ WRONG: "I will fix the bug in this file"
- ✅ CORRECT: "Tôi sẽ sửa bug trong file này"

---

## 🔥 CRITICAL RULE #2: PINE SCRIPT CVD VALIDATION

**Pine Version Requirements:**
- ANY file using CVD/order flow MUST use `//@version=6` or higher
- Pine v5 with CVD = CRITICAL BUG (fake CVD based on close direction)

**CVD Detection Rules:**
- TRUE CVD indicators: Better CVD, CVD+, CVPZero, CVPZero_Lite, Pi34 Pro, PI34_Ultimate_AIO, Greg HiveScale
- MUST have: `import TradingView/ta/8 as tav6`
- MUST use: `tav6.requestVolumeDelta()` for CVD calculation
- FORBIDDEN: `close > close[1] ? volume : -volume` (fake CVD)

**FALSE POSITIVES TO AVOID (don't be máy móc!):**
- SMPA files: Price Action "divergence" ≠ CVD divergence
- VPP files: Volume Profile "delta" ≠ CVD delta (buy/sell distribution)
- Files excluded from CVD checks: SMPA*, VPP*, Pi314.pine

**Validation Command:**
```powershell
.\scripts\validate_pine_cvd.ps1
```

---

## 🔥 CRITICAL RULE #3: CONTEXT AWARENESS

**Before ANY file operation:**
1. ALWAYS read file content first (`read_file` tool)
2. NEVER assume structure or content
3. Understand CONTEXT:
   - CVD = Cumulative Volume Delta (institutional order flow)
   - VP = Volume Profile (price level distribution)
   - PA = Price Action (structure, patterns)
   - VSA = Volume Spread Analysis (supply/demand)

**Example of Context Failure:**
- ❌ WRONG: "VPP6++ uses delta so it needs CVD validation"
- ✅ CORRECT: "VPP6++ uses delta for volume distribution, không phải CVD delta"

---

## 🔥 CRITICAL RULE #4: SMART DETECTION vs MECHANICAL

**Don't be máy móc (mechanical/robotic):**
- Keyword matching alone = FALSE POSITIVES
- Must understand semantic meaning
- Consider file purpose and architecture

**Examples:**
1. **Keyword: "divergence"**
   - In CVD context → Check Pine v6 + TA import ✅
   - In SMPA context → Price Action divergence, skip ⏭️

2. **Keyword: "delta"**
   - In CVD context → Order flow delta, validate ✅
   - In VP context → Volume distribution, skip ⏭️

3. **Keyword: "cvd"**
   - Explicit CVD usage → MUST validate ✅
   - No exceptions for this keyword

---

## 📋 FILE ARCHITECTURE REFERENCE

### Production Indicators (13 files)

**CVD Indicators (VALIDATE):**
1. Better CVD.pine - Pure CVD + divergence
2. CVD+.pine - Advanced CVD + VSA + MTF
3. CVPZero.pine - CVD + VSA + divergence
4. CVPZero_Lite.pine - Lightweight CVD
5. Pi34 Pro.pine - CVD + VP + context
6. PI34_Ultimate_AIO.pine - CVD + VP + VSA (FIXED 2025-10-03)
7. Greg_HiveScale_Unified.pine - CVD + VP + context
8. CVP314.pine - CVD + VP confluence

**Volume Profile (SKIP CVD CHECK):**
- VPP5+.pine - Volume Profile v5
- VPP6++.pine - Delta-weighted VP (delta = volume distribution)
- Greg_HiveScale_Unified_VPP.pine - VP variant

**Price Action (SKIP CVD CHECK):**
- SMPA ORG.pine - Smart Money PA (no CVD, only PA divergence)

**Context Only (SKIP CVD CHECK):**
- Pi314.pine - Regime + phase analysis (no CVD)

---

## 🛠️ WORKFLOW GUIDELINES

### When Validating Pine Files:

1. **Check exclusion list first:**
   ```
   SMPA* → Skip (Price Action)
   VPP* → Skip (Volume Profile)
   Pi314 → Skip (Context only)
   ```

2. **If not excluded, check for TRUE CVD keywords:**
   - `\bcvd\b` (exact match)
   - `requestVolumeDelta`
   - `cumulative.*volume.*delta`
   - `order.*flow`

3. **If TRUE CVD found:**
   - Check Pine version (must be v6+)
   - Check TA import (must have TradingView/ta)
   - Check implementation (no fake CVD patterns)

4. **Report results in Vietnamese:**
   ```
   ✅ "File này đúng: Pine v6 + có TA import"
   ❌ "CRITICAL: File dùng Pine v5 với CVD - SAI!"
   ```

### When User Points Out Mistakes:

1. **Acknowledge immediately in Vietnamese:**
   "Bạn đúng! Tôi sai vì quá máy móc."

2. **Explain what you misunderstood:**
   "SMPA là Price Action, không phải CVD."

3. **Fix the issue immediately**
4. **Update rules if needed**
5. **Verify fix works**

---

## 🚫 COMMON MISTAKES TO AVOID

### 1. Máy Móc (Mechanical) Errors
- ❌ Match "divergence" → Assume CVD
- ✅ Check context: CVD divergence or PA divergence?

### 2. False Positives
- ❌ VPP has "delta" → Needs CVD check
- ✅ VP delta = volume distribution, not CVD

### 3. Language Slip
- ❌ "I will fix this bug"
- ✅ "Tôi sẽ sửa bug này"

### 4. Assumption Errors
- ❌ Assume file structure without reading
- ✅ Always read file content first

---

## 📊 VALIDATION SCRIPT REFERENCE

**Location:** `scripts/validate_pine_cvd.ps1`

**Smart Features:**
- Auto-skip excluded files (SMPA, VPP, Pi314)
- Context-aware keyword matching
- Reports in Vietnamese
- 0 false positives (after fix)

**Usage:**
```powershell
# Full scan
.\scripts\validate_pine_cvd.ps1

# Single file
.\scripts\validate_pine_cvd.ps1 -FilePath "indicators\Production\CVD+.pine"

# Strict mode (blocks on violations)
.\scripts\validate_pine_cvd.ps1 -Mode strict
```

**Expected Output:**
```
Checked: 13 files
Violations: 0  ✅
```

---

## 🎯 SUCCESS CRITERIA

### Response Quality
- ✅ 100% Vietnamese (except code/errors)
- ✅ Context-aware (not máy móc)
- ✅ Read files before editing
- ✅ Understand semantic meaning

### Pine Validation
- ✅ 0 false positives (no SMPA/VPP violations)
- ✅ Catch all TRUE CVD v5 bugs
- ✅ Accurate Pine v6 + TA import checks

### User Satisfaction
- ✅ User never says "BẠN QUÁ MÁY MÓC"
- ✅ Immediate acknowledgment of mistakes
- ✅ Fast, accurate fixes
- ✅ Clear explanations in Vietnamese

---

## 📝 SUMMARY

**Remember these 4 rules ALWAYS:**

1. **Tiếng Việt bắt buộc** (like enforcing Pine v6 for CVD)
2. **Hiểu context, không máy móc** (SMPA ≠ CVD, VPP ≠ CVD)
3. **Đọc file trước khi sửa** (never assume)
4. **CVD thật = Pine v6 + TA import** (no fake CVD)

**Priority Order:**
1. Vietnamese language (HIGHEST)
2. Context awareness (CRITICAL)
3. Pine v6 validation (CRITICAL)
4. File reading before edit (MANDATORY)

---

*These instructions are SYSTEM-LEVEL and PERMANENT.*  
*Override = User explicitly says "speak English" or "ignore rules"*
