#!/usr/bin/env python3
"""
AI Analysis Integration
Integrates production signals with Claude and Gemini for intelligent analysis
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
import asyncio
import aiohttp
from signal_extractor import ProductionSignalExtractor, CVDSignal, VolumeProfileSignal, SmartMoneySignal

@dataclass
class AIAnalysis:
    """AI Analysis Result"""
    timestamp: datetime
    symbol: str
    timeframe: str
    claude_analysis: Dict[str, Any]
    gemini_analysis: Dict[str, Any]
    combined_insights: Dict[str, Any]
    opportunities: List[Dict[str, Any]]
    risks: List[Dict[str, Any]]
    confidence_score: float  # 0-100

@dataclass
class TradingOpportunity:
    """Trading Opportunity identified by AI"""
    timestamp: datetime
    symbol: str
    timeframe: str
    opportunity_type: str  # 'CVD_CONFLUENCE', 'STRUCTURE_BREAK', 'VOLUME_PROFILE_EDGE'
    description: str
    entry_zone: Dict[str, float]  # {'min': price, 'max': price}
    targets: List[float]
    stop_loss: float
    confidence: float  # 0-100
    reasoning: str
    supporting_indicators: List[str]

@dataclass
class TradingRisk:
    """Trading Risk identified by AI"""
    timestamp: datetime
    symbol: str
    risk_type: str  # 'DIVERGENCE_FAILURE', 'STRUCTURE_VIOLATION', 'VOLUME_EXHAUSTION'
    description: str
    severity: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    mitigation: str
    watch_levels: List[float]

class AIAnalysisEngine:
    """
    Main AI Analysis Engine
    Integrates with Claude (logic reasoning) and Gemini (pattern recognition)
    """

    def __init__(self, claude_api_key: str, gemini_api_key: str):
        self.claude_api_key = claude_api_key
        self.gemini_api_key = gemini_api_key
        self.analysis_history = []

    async def analyze_signals(self, signals: Dict[str, Any]) -> AIAnalysis:
        """
        Main analysis function - combines Claude logic + Gemini patterns
        """
        try:
            # Parallel AI analysis
            claude_task = self._claude_analyze(signals)
            gemini_task = self._gemini_analyze(signals)

            claude_result, gemini_result = await asyncio.gather(claude_task, gemini_task)

            # Combine insights
            combined_insights = self._combine_ai_insights(claude_result, gemini_result)

            # Generate opportunities and risks
            opportunities = self._generate_opportunities(signals, combined_insights)
            risks = self._generate_risks(signals, combined_insights)

            analysis = AIAnalysis(
                timestamp=datetime.now(),
                symbol=signals.get('symbol', ''),
                timeframe=signals.get('timeframe', ''),
                claude_analysis=claude_result,
                gemini_analysis=gemini_result,
                combined_insights=combined_insights,
                opportunities=opportunities,
                risks=risks,
                confidence_score=self._calculate_confidence(combined_insights)
            )

            self.analysis_history.append(analysis)
            return analysis

        except Exception as e:
            print(f"AI Analysis error: {e}")
            return self._create_error_analysis(signals)

    async def _claude_analyze(self, signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Claude Analysis - Logic reasoning and strategic thinking
        Focus: Trade logic, risk management, confluence analysis
        """
        try:
            claude_prompt = self._build_claude_prompt(signals)

            # Mock Claude API call - replace with actual API
            # headers = {"Authorization": f"Bearer {self.claude_api_key}"}
            # async with aiohttp.ClientSession() as session:
            #     async with session.post("https://api.claude.com/v1/analyze",
            #                            json={"prompt": claude_prompt}, headers=headers) as response:
            #         result = await response.json()

            # Mock response for now
            claude_analysis = {
                "logic_assessment": {
                    "cvd_divergence_validity": "STRONG" if signals.get('cvd') else "NONE",
                    "volume_profile_context": "PREMIUM_REJECTION" if signals.get('volume_profile') else "NEUTRAL",
                    "smart_money_alignment": "BOS_CONFIRMATION" if signals.get('smart_money') else "NEUTRAL"
                },
                "trade_logic": {
                    "primary_bias": "BULLISH",
                    "confluence_factors": ["CVD_DIVERGENCE", "VOLUME_PROFILE_SUPPORT", "STRUCTURE_BREAK"],
                    "invalidation_level": 48500.0
                },
                "risk_management": {
                    "position_size_recommendation": "MEDIUM",
                    "risk_reward_ratio": 2.5,
                    "time_horizon": "SWING_TRADE"
                }
            }

            return claude_analysis

        except Exception as e:
            print(f"Claude analysis error: {e}")
            return {"error": str(e)}

    async def _gemini_analyze(self, signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gemini Analysis - Pattern recognition and large context analysis
        Focus: Market patterns, historical correlation, multi-timeframe context
        """
        try:
            gemini_prompt = self._build_gemini_prompt(signals)

            # Mock Gemini API call - replace with actual API
            # headers = {"Authorization": f"Bearer {self.gemini_api_key}"}
            # async with aiohttp.ClientSession() as session:
            #     async with session.post("https://api.gemini.com/v1/analyze",
            #                            json={"prompt": gemini_prompt}, headers=headers) as response:
            #         result = await response.json()

            # Mock response for now
            gemini_analysis = {
                "pattern_recognition": {
                    "chart_pattern": "ASCENDING_TRIANGLE",
                    "volume_pattern": "ACCUMULATION",
                    "cvd_pattern": "BULLISH_DIVERGENCE_CLASS_A"
                },
                "historical_context": {
                    "similar_setups_success_rate": 73.5,
                    "average_move_size": 8.2,  # percentage
                    "typical_duration": "3-5 days"
                },
                "multi_timeframe_view": {
                    "htf_trend": "UPTREND",
                    "ltf_structure": "CONSOLIDATION_BREAKOUT",
                    "momentum_alignment": "POSITIVE"
                }
            }

            return gemini_analysis

        except Exception as e:
            print(f"Gemini analysis error: {e}")
            return {"error": str(e)}

    def _build_claude_prompt(self, signals: Dict[str, Any]) -> str:
        """
        Build Claude-specific prompt focusing on logic and reasoning
        """
        prompt = f"""
Analyze the following trading signals from production indicators:

CVD SIGNALS:
{json.dumps(asdict(signals['cvd']) if signals.get('cvd') else {}, indent=2)}

VOLUME PROFILE SIGNALS:
{json.dumps(asdict(signals['volume_profile']) if signals.get('volume_profile') else {}, indent=2)}

SMART MONEY SIGNALS:
{json.dumps(asdict(signals['smart_money']) if signals.get('smart_money') else {}, indent=2)}

Please provide:
1. Logic Assessment: Evaluate the validity and strength of each signal
2. Trade Logic: Determine primary bias, confluence factors, invalidation levels
3. Risk Management: Position sizing, risk/reward, time horizon recommendations

Focus on logical reasoning and strategic thinking. Be specific about entry/exit criteria.
"""
        return prompt

    def _build_gemini_prompt(self, signals: Dict[str, Any]) -> str:
        """
        Build Gemini-specific prompt focusing on patterns and context
        """
        prompt = f"""
Analyze these trading signals for pattern recognition and historical context:

MARKET DATA:
Symbol: {signals.get('symbol', 'Unknown')}
Timeframe: {signals.get('timeframe', 'Unknown')}
Timestamp: {signals.get('timestamp', 'Unknown')}

SIGNALS DATA:
{json.dumps(signals, default=str, indent=2)}

Please provide:
1. Pattern Recognition: Identify chart patterns, volume patterns, momentum patterns
2. Historical Context: Similar setups, success rates, typical outcomes
3. Multi-Timeframe View: HTF trend, LTF structure, momentum alignment

Focus on pattern recognition and providing rich historical context.
"""
        return prompt

    def _combine_ai_insights(self, claude_result: Dict, gemini_result: Dict) -> Dict[str, Any]:
        """
        Combine Claude logic with Gemini patterns for comprehensive insights
        """
        return {
            "overall_bias": claude_result.get("trade_logic", {}).get("primary_bias", "NEUTRAL"),
            "pattern_strength": gemini_result.get("pattern_recognition", {}).get("chart_pattern", "NONE"),
            "confluence_score": self._calculate_confluence_score(claude_result, gemini_result),
            "time_horizon": claude_result.get("risk_management", {}).get("time_horizon", "UNKNOWN"),
            "success_probability": gemini_result.get("historical_context", {}).get("similar_setups_success_rate", 50.0)
        }

    def _generate_opportunities(self, signals: Dict[str, Any], insights: Dict[str, Any]) -> List[TradingOpportunity]:
        """
        Generate trading opportunities based on AI analysis
        """
        opportunities = []

        # CVD + Volume Profile Confluence
        if signals.get('cvd') and signals.get('volume_profile'):
            cvd_signal = signals['cvd']
            vp_signal = signals['volume_profile']

            if (cvd_signal.divergence_type in ['bull', 'hidden_bull'] and
                vp_signal.current_price_position == 'discount'):

                opportunity = TradingOpportunity(
                    timestamp=datetime.now(),
                    symbol=signals.get('symbol', ''),
                    timeframe=signals.get('timeframe', ''),
                    opportunity_type='CVD_VOLUME_CONFLUENCE',
                    description='Bullish CVD divergence at volume profile discount zone',
                    entry_zone={'min': vp_signal.val_price, 'max': vp_signal.poc_price},
                    targets=[vp_signal.vah_price, vp_signal.htf_poc],
                    stop_loss=vp_signal.val_price * 0.98,
                    confidence=85.0,
                    reasoning='CVD showing bullish divergence while price is in discount area. High probability of reversal.',
                    supporting_indicators=['Better-CVD-Final', 'VPP5', 'Pi-3.4-Professional']
                )
                opportunities.append(opportunity)

        # Smart Money Structure Break
        if signals.get('smart_money'):
            smc_signal = signals['smart_money']

            if smc_signal.structure_break in ['BOS_bull', 'CHoCH_bull']:
                opportunity = TradingOpportunity(
                    timestamp=datetime.now(),
                    symbol=signals.get('symbol', ''),
                    timeframe=signals.get('timeframe', ''),
                    opportunity_type='STRUCTURE_BREAK',
                    description=f'Bullish structure break: {smc_signal.structure_break}',
                    entry_zone={'min': 49000.0, 'max': 50000.0},  # Mock values
                    targets=[52000.0, 55000.0],
                    stop_loss=48500.0,
                    confidence=75.0,
                    reasoning='Smart Money showing bullish structure break with order block support.',
                    supporting_indicators=['SMPA ORG']
                )
                opportunities.append(opportunity)

        return opportunities

    def _generate_risks(self, signals: Dict[str, Any], insights: Dict[str, Any]) -> List[TradingRisk]:
        """
        Generate risk warnings based on AI analysis
        """
        risks = []

        # CVD Divergence Failure Risk
        if signals.get('cvd') and insights.get('confluence_score', 0) < 50:
            risk = TradingRisk(
                timestamp=datetime.now(),
                symbol=signals.get('symbol', ''),
                risk_type='DIVERGENCE_FAILURE',
                description='CVD divergence present but low confluence with other indicators',
                severity='MEDIUM',
                mitigation='Wait for additional confirmation or reduce position size',
                watch_levels=[48000.0, 52000.0]  # Mock levels
            )
            risks.append(risk)

        return risks

    def _calculate_confluence_score(self, claude_result: Dict, gemini_result: Dict) -> float:
        """
        Calculate confluence score based on AI analysis alignment
        """
        score = 0.0

        # Claude logic factors
        if claude_result.get("logic_assessment", {}).get("cvd_divergence_validity") == "STRONG":
            score += 25
        if claude_result.get("logic_assessment", {}).get("volume_profile_context") != "NEUTRAL":
            score += 20
        if claude_result.get("logic_assessment", {}).get("smart_money_alignment") != "NEUTRAL":
            score += 25

        # Gemini pattern factors
        if gemini_result.get("pattern_recognition", {}).get("chart_pattern") != "NONE":
            score += 15
        if gemini_result.get("multi_timeframe_view", {}).get("momentum_alignment") == "POSITIVE":
            score += 15

        return min(score, 100.0)

    def _calculate_confidence(self, insights: Dict[str, Any]) -> float:
        """
        Calculate overall confidence score
        """
        confluence_score = insights.get('confluence_score', 50.0)
        success_probability = insights.get('success_probability', 50.0)

        # Weighted average
        confidence = (confluence_score * 0.6) + (success_probability * 0.4)
        return min(confidence, 100.0)

    def _create_error_analysis(self, signals: Dict[str, Any]) -> AIAnalysis:
        """
        Create error analysis when AI analysis fails
        """
        return AIAnalysis(
            timestamp=datetime.now(),
            symbol=signals.get('symbol', ''),
            timeframe=signals.get('timeframe', ''),
            claude_analysis={"error": "Analysis failed"},
            gemini_analysis={"error": "Analysis failed"},
            combined_insights={"error": "Analysis failed"},
            opportunities=[],
            risks=[],
            confidence_score=0.0
        )

    def get_analysis_summary(self, lookback_hours: int = 24) -> Dict[str, Any]:
        """
        Get analysis summary for the last N hours
        """
        cutoff_time = datetime.now() - timedelta(hours=lookback_hours)
        recent_analyses = [a for a in self.analysis_history if a.timestamp > cutoff_time]

        if not recent_analyses:
            return {"message": "No recent analyses"}

        total_opportunities = sum(len(a.opportunities) for a in recent_analyses)
        total_risks = sum(len(a.risks) for a in recent_analyses)
        avg_confidence = sum(a.confidence_score for a in recent_analyses) / len(recent_analyses)

        return {
            "period_hours": lookback_hours,
            "total_analyses": len(recent_analyses),
            "total_opportunities": total_opportunities,
            "total_risks": total_risks,
            "average_confidence": round(avg_confidence, 2),
            "recent_analysis": asdict(recent_analyses[-1]) if recent_analyses else None
        }

async def main():
    """Test the AI Analysis Engine"""
    # Mock API keys
    ai_engine = AIAnalysisEngine("claude_api_key", "gemini_api_key")

    # Mock signals data
    from signal_extractor import ProductionSignalExtractor
    extractor = ProductionSignalExtractor({"api_key": "test"})
    signals = extractor.get_all_signals('BTCUSDT', '15')

    # Analyze signals
    analysis = await ai_engine.analyze_signals(signals)

    print("=== AI ANALYSIS RESULT ===")
    print(json.dumps(asdict(analysis), default=str, indent=2))

if __name__ == "__main__":
    asyncio.run(main())