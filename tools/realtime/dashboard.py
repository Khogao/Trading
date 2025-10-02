#!/usr/bin/env python3
"""
Real-time Trading Dashboard
Displays signals and AI analysis from your production indicators
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import asyncio
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import asdict
import queue

from signal_extractor import ProductionSignalExtractor
from ai_analyzer import AIAnalysisEngine, TradingOpportunity, TradingRisk

class RealTimeTradingDashboard:
    """
    Real-time dashboard for your production trading indicators
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 AI Trading Monitor - Production Indicators")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e1e")

        # Data queues for thread communication
        self.signal_queue = queue.Queue()
        self.analysis_queue = queue.Queue()

        # Components
        self.signal_extractor = None
        self.ai_engine = None
        self.is_running = False

        # UI Components
        self.create_ui()

        # Start background monitoring
        self.start_monitoring()

    def create_ui(self):
        """Create the main UI layout"""

        # Title
        title_frame = tk.Frame(self.root, bg="#1e1e1e")
        title_frame.pack(fill="x", padx=10, pady=5)

        title_label = tk.Label(
            title_frame,
            text="🚀 AI Trading Monitor - Production Indicators",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        title_label.pack()

        # Status bar
        self.status_frame = tk.Frame(self.root, bg="#2d2d2d")
        self.status_frame.pack(fill="x", padx=10, pady=2)

        self.status_label = tk.Label(
            self.status_frame,
            text="🟢 System Starting...",
            font=("Arial", 10),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        self.status_label.pack(side="left")

        self.time_label = tk.Label(
            self.status_frame,
            text="",
            font=("Arial", 10),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        self.time_label.pack(side="right")

        # Main content (3 panels)
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left panel - Opportunities
        self.create_opportunities_panel(main_frame)

        # Center panel - Signal Status
        self.create_signals_panel(main_frame)

        # Right panel - Risks & Analysis
        self.create_risks_panel(main_frame)

        # Bottom panel - Controls
        self.create_controls_panel()

    def create_opportunities_panel(self, parent):
        """Create opportunities panel"""
        opportunities_frame = tk.LabelFrame(
            parent,
            text="🎯 OPPORTUNITIES",
            font=("Arial", 12, "bold"),
            bg="#1e1e1e",
            fg="#00ff00",
            bd=2,
            relief="raised"
        )
        opportunities_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Opportunities listbox with scrollbar
        listbox_frame = tk.Frame(opportunities_frame, bg="#1e1e1e")
        listbox_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.opportunities_listbox = tk.Listbox(
            listbox_frame,
            bg="#2d2d2d",
            fg="#00ff00",
            selectbackground="#4d4d4d",
            font=("Consolas", 10),
            height=20
        )
        self.opportunities_listbox.pack(side="left", fill="both", expand=True)

        opp_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        opp_scrollbar.pack(side="right", fill="y")
        opp_scrollbar.config(command=self.opportunities_listbox.yview)
        self.opportunities_listbox.config(yscrollcommand=opp_scrollbar.set)

        # Opportunity details
        self.opp_details_text = tk.Text(
            opportunities_frame,
            height=8,
            bg="#2d2d2d",
            fg="#ffffff",
            font=("Consolas", 9),
            wrap="word"
        )
        self.opp_details_text.pack(fill="x", padx=5, pady=5)

        # Bind selection
        self.opportunities_listbox.bind("<<ListboxSelect>>", self.on_opportunity_select)

    def create_signals_panel(self, parent):
        """Create signals status panel"""
        signals_frame = tk.LabelFrame(
            parent,
            text="📊 SIGNAL STATUS",
            font=("Arial", 12, "bold"),
            bg="#1e1e1e",
            fg="#ffffff",
            bd=2,
            relief="raised"
        )
        signals_frame.pack(side="left", fill="both", expand=True, padx=5)

        # CVD Status
        cvd_frame = tk.LabelFrame(signals_frame, text="CVD Analysis", bg="#1e1e1e", fg="#ffffff")
        cvd_frame.pack(fill="x", padx=5, pady=2)

        self.cvd_status_label = tk.Label(
            cvd_frame,
            text="🔄 Waiting for CVD data...",
            bg="#1e1e1e",
            fg="#ffff00",
            font=("Arial", 10)
        )
        self.cvd_status_label.pack(pady=2)

        # Multi-TF CVD Table
        self.create_cvd_table(cvd_frame)

        # Volume Profile Status
        vp_frame = tk.LabelFrame(signals_frame, text="Volume Profile", bg="#1e1e1e", fg="#ffffff")
        vp_frame.pack(fill="x", padx=5, pady=2)

        self.vp_status_label = tk.Label(
            vp_frame,
            text="🔄 Waiting for VP data...",
            bg="#1e1e1e",
            fg="#ffff00",
            font=("Arial", 10)
        )
        self.vp_status_label.pack(pady=2)

        # Smart Money Status
        smc_frame = tk.LabelFrame(signals_frame, text="Smart Money", bg="#1e1e1e", fg="#ffffff")
        smc_frame.pack(fill="x", padx=5, pady=2)

        self.smc_status_label = tk.Label(
            smc_frame,
            text="🔄 Waiting for SMC data...",
            bg="#1e1e1e",
            fg="#ffff00",
            font=("Arial", 10)
        )
        self.smc_status_label.pack(pady=2)

        # AI Analysis Status
        ai_frame = tk.LabelFrame(signals_frame, text="AI Analysis", bg="#1e1e1e", fg="#ffffff")
        ai_frame.pack(fill="x", padx=5, pady=2)

        self.ai_status_label = tk.Label(
            ai_frame,
            text="🔄 AI Analysis pending...",
            bg="#1e1e1e",
            fg="#ffff00",
            font=("Arial", 10)
        )
        self.ai_status_label.pack(pady=2)

        self.confidence_label = tk.Label(
            ai_frame,
            text="Confidence: --",
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Arial", 10)
        )
        self.confidence_label.pack(pady=2)

    def create_cvd_table(self, parent):
        """Create CVD multi-timeframe table"""
        table_frame = tk.Frame(parent, bg="#1e1e1e")
        table_frame.pack(fill="x", padx=5, pady=5)

        # Headers
        tk.Label(table_frame, text="TF", bg="#2d2d2d", fg="#ffffff", width=6, relief="raised").grid(row=0, column=0)
        tk.Label(table_frame, text="CVD Status", bg="#2d2d2d", fg="#ffffff", width=15, relief="raised").grid(row=0, column=1)

        # CVD status labels
        self.cvd_tf_labels = {}
        timeframes = ["5m", "15m", "1H", "4H"]
        for i, tf in enumerate(timeframes):
            tk.Label(table_frame, text=tf, bg="#1e1e1e", fg="#ffffff", width=6, relief="sunken").grid(row=i+1, column=0)
            status_label = tk.Label(table_frame, text="--", bg="#1e1e1e", fg="#ffff00", width=15, relief="sunken")
            status_label.grid(row=i+1, column=1)
            self.cvd_tf_labels[tf] = status_label

    def create_risks_panel(self, parent):
        """Create risks and analysis panel"""
        risks_frame = tk.LabelFrame(
            parent,
            text="⚠️ RISKS & ANALYSIS",
            font=("Arial", 12, "bold"),
            bg="#1e1e1e",
            fg="#ff4444",
            bd=2,
            relief="raised"
        )
        risks_frame.pack(side="right", fill="both", expand=True, padx=5)

        # Risks listbox
        risks_list_frame = tk.Frame(risks_frame, bg="#1e1e1e")
        risks_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.risks_listbox = tk.Listbox(
            risks_list_frame,
            bg="#2d2d2d",
            fg="#ff4444",
            selectbackground="#4d4d4d",
            font=("Consolas", 10),
            height=12
        )
        self.risks_listbox.pack(side="left", fill="both", expand=True)

        risks_scrollbar = tk.Scrollbar(risks_list_frame, orient="vertical")
        risks_scrollbar.pack(side="right", fill="y")
        risks_scrollbar.config(command=self.risks_listbox.yview)
        self.risks_listbox.config(yscrollcommand=risks_scrollbar.set)

        # Analysis summary
        analysis_frame = tk.LabelFrame(risks_frame, text="Analysis Summary", bg="#1e1e1e", fg="#ffffff")
        analysis_frame.pack(fill="x", padx=5, pady=5)

        self.analysis_text = tk.Text(
            analysis_frame,
            height=10,
            bg="#2d2d2d",
            fg="#ffffff",
            font=("Consolas", 9),
            wrap="word"
        )
        self.analysis_text.pack(fill="both", padx=5, pady=5)

    def create_controls_panel(self):
        """Create controls panel"""
        controls_frame = tk.Frame(self.root, bg="#2d2d2d")
        controls_frame.pack(fill="x", padx=10, pady=5)

        # Start/Stop button
        self.start_stop_button = tk.Button(
            controls_frame,
            text="🟢 START MONITORING",
            font=("Arial", 12, "bold"),
            bg="#00aa00",
            fg="#ffffff",
            command=self.toggle_monitoring
        )
        self.start_stop_button.pack(side="left", padx=10)

        # Symbol selector
        tk.Label(controls_frame, text="Symbol:", bg="#2d2d2d", fg="#ffffff").pack(side="left", padx=5)
        self.symbol_var = tk.StringVar(value="BTCUSDT")
        symbol_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.symbol_var,
            values=["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT"],
            state="readonly",
            width=10
        )
        symbol_combo.pack(side="left", padx=5)

        # Timeframe selector
        tk.Label(controls_frame, text="TF:", bg="#2d2d2d", fg="#ffffff").pack(side="left", padx=5)
        self.timeframe_var = tk.StringVar(value="15")
        tf_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.timeframe_var,
            values=["1", "5", "15", "60", "240"],
            state="readonly",
            width=5
        )
        tf_combo.pack(side="left", padx=5)

        # Clear logs button
        tk.Button(
            controls_frame,
            text="Clear Logs",
            command=self.clear_logs
        ).pack(side="right", padx=10)

    def start_monitoring(self):
        """Start the monitoring system"""
        try:
            # Initialize components
            self.signal_extractor = ProductionSignalExtractor({"api_key": "your_api_key"})
            self.ai_engine = AIAnalysisEngine("claude_api_key", "gemini_api_key")

            # Start background thread
            self.is_running = True
            monitor_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
            monitor_thread.start()

            # Start UI update timer
            self.update_ui()

            self.update_status("🟢 System Online - Monitoring Started")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {e}")

    def monitoring_loop(self):
        """Background monitoring loop"""
        while self.is_running:
            try:
                symbol = self.symbol_var.get()
                timeframe = self.timeframe_var.get()

                # Extract signals
                signals = self.signal_extractor.get_all_signals(symbol, timeframe)
                self.signal_queue.put(signals)

                # AI analysis (async)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                analysis = loop.run_until_complete(self.ai_engine.analyze_signals(signals))
                loop.close()

                self.analysis_queue.put(analysis)

                # Wait before next update
                time.sleep(30)  # 30-second intervals

            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(10)

    def update_ui(self):
        """Update UI with latest data"""
        try:
            # Update time
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.config(text=f"Last Update: {current_time}")

            # Process signal queue
            while not self.signal_queue.empty():
                signals = self.signal_queue.get()
                self.update_signal_displays(signals)

            # Process analysis queue
            while not self.analysis_queue.empty():
                analysis = self.analysis_queue.get()
                self.update_analysis_displays(analysis)

        except Exception as e:
            print(f"UI update error: {e}")

        # Schedule next update
        self.root.after(1000, self.update_ui)  # Update every 1 second

    def update_signal_displays(self, signals):
        """Update signal status displays"""
        # CVD Status
        if signals.get('cvd'):
            cvd_signal = signals['cvd']
            if cvd_signal:
                self.cvd_status_label.config(
                    text=f"✅ CVD: {cvd_signal.divergence_type.upper()} ({cvd_signal.strength:.1f}%)",
                    fg="#00ff00"
                )

                # Update multi-TF table
                for tf, status in cvd_signal.multi_tf_status.items():
                    if tf in self.cvd_tf_labels:
                        color = "#00ff00" if "▲" in status else "#ff4444"
                        self.cvd_tf_labels[tf].config(text=status, fg=color)

        # Volume Profile Status
        if signals.get('volume_profile'):
            vp_signal = signals['volume_profile']
            if vp_signal:
                self.vp_status_label.config(
                    text=f"✅ VP: {vp_signal.current_price_position.upper()} (POC: {vp_signal.poc_price:.0f})",
                    fg="#00ff00"
                )

        # Smart Money Status
        if signals.get('smart_money'):
            smc_signal = signals['smart_money']
            if smc_signal:
                self.smc_status_label.config(
                    text=f"✅ SMC: {smc_signal.structure_break} ({smc_signal.current_trend.upper()})",
                    fg="#00ff00"
                )

    def update_analysis_displays(self, analysis):
        """Update AI analysis displays"""
        # AI Status
        confidence = analysis.confidence_score
        self.ai_status_label.config(
            text=f"🤖 AI Analysis Complete",
            fg="#00ff00"
        )
        self.confidence_label.config(
            text=f"Confidence: {confidence:.1f}%",
            fg="#00ff00" if confidence > 70 else "#ffff00" if confidence > 50 else "#ff4444"
        )

        # Update opportunities
        self.opportunities_listbox.delete(0, tk.END)
        for i, opp in enumerate(analysis.opportunities):
            display_text = f"{opp.opportunity_type}: {opp.description[:50]}..."
            self.opportunities_listbox.insert(tk.END, display_text)

        # Update risks
        self.risks_listbox.delete(0, tk.END)
        for risk in analysis.risks:
            display_text = f"{risk.severity}: {risk.description[:50]}..."
            self.risks_listbox.insert(tk.END, display_text)

        # Update analysis summary
        self.analysis_text.delete(1.0, tk.END)
        summary = f"""
Analysis Summary:
- Overall Bias: {analysis.combined_insights.get('overall_bias', 'N/A')}
- Pattern Strength: {analysis.combined_insights.get('pattern_strength', 'N/A')}
- Confluence Score: {analysis.combined_insights.get('confluence_score', 0):.1f}
- Success Probability: {analysis.combined_insights.get('success_probability', 0):.1f}%

Recent Analysis:
{json.dumps(analysis.claude_analysis.get('trade_logic', {}), indent=2)}
        """
        self.analysis_text.insert(tk.END, summary)

    def on_opportunity_select(self, event):
        """Handle opportunity selection"""
        try:
            selection = self.opportunities_listbox.curselection()
            if selection:
                # Show opportunity details
                details = "Opportunity details would go here..."
                self.opp_details_text.delete(1.0, tk.END)
                self.opp_details_text.insert(tk.END, details)
        except Exception as e:
            print(f"Opportunity selection error: {e}")

    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if self.is_running:
            self.is_running = False
            self.start_stop_button.config(
                text="🟢 START MONITORING",
                bg="#00aa00"
            )
            self.update_status("🔴 Monitoring Stopped")
        else:
            self.start_monitoring()
            self.start_stop_button.config(
                text="🔴 STOP MONITORING",
                bg="#aa0000"
            )

    def clear_logs(self):
        """Clear all displays"""
        self.opportunities_listbox.delete(0, tk.END)
        self.risks_listbox.delete(0, tk.END)
        self.analysis_text.delete(1.0, tk.END)
        self.opp_details_text.delete(1.0, tk.END)

    def update_status(self, message):
        """Update status message"""
        self.status_label.config(text=message)

    def run(self):
        """Start the dashboard"""
        print("🚀 Starting AI Trading Monitor Dashboard...")
        print("📊 Production Indicators: Better-CVD-Final, CVD-Pro, Pi-3.4-Professional, SMPA ORG, VPP5")
        print("🤖 AI Integration: Claude + Gemini Analysis")
        self.root.mainloop()

if __name__ == "__main__":
    dashboard = RealTimeTradingDashboard()
    dashboard.run()