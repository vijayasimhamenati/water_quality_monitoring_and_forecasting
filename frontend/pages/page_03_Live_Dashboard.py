"""
Live Dashboard Page - Real-time sensor monitoring with live charts
"""
import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import CUSTOM_CSS, PRIMARY_COLOR, SECONDARY_COLOR
from utils.api_client import APIClient
from components.ui import header, section_divider, error_box


def render_live_dashboard():
    """Render the live dashboard with a simplified real-time status card."""

    api_client = APIClient()

    header("Live Dashboard", "Real-time water quality status", icon="📡")
    st.markdown("*This page shows one real-time reading with toxic/safe status and key RW values (pH, TDS).*")

    if "live_data" not in st.session_state:
        st.session_state.live_data = None

    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = None

    def get_status_card(data):
        if data is None:
            st.warning("No live data yet. Please wait or refresh.")
            return

        cr = data["current_reading"]
        cls = cr["classification"]
        rw = cr["raw_water_metrics"]

        status_text = "SAFE" if cls["status_code"] == 1 else "TOXIC"
        status_color = "#d4edda" if status_text == "SAFE" else "#f8d7da"
        border_color = "#28a745" if status_text == "SAFE" else "#dc3545"
        text_color = "#155724" if status_text == "SAFE" else "#721c24"

        st.markdown(f"""
        <div style='background: {status_color}; border: 2px solid {border_color}; border-radius: 12px; padding: 16px; margin-bottom: 16px;'>
            <h2 style='color: {text_color}; margin: 0;'>Status: {status_text}</h2>
            <p style='color: {text_color}; margin: 6px 0;'>
                Confidence Safe: {cls['confidence_safe_percent']:.1f}% | Confidence Toxic: {cls['confidence_toxic_percent']:.1f}%
            </p>
            <p style='color: {text_color}; margin: 6px 0;'>Primary values: pH={rw['RW pH']:.2f}, TDS={rw['RW TDS']:.0f}</p>
        </div>
        """, unsafe_allow_html=True)

    def refresh_data():
        try:
            live_data = api_client.get_live_dashboard_data()
            st.session_state.live_data = live_data
            st.session_state.last_refresh = datetime.now()
        except Exception as exc:
            error_box("Failed to fetch live data", str(exc))

    if st.button("🔄 Refresh Now", use_container_width=True):
        refresh_data()

    if st.session_state.live_data is None:
        refresh_data()

    get_status_card(st.session_state.live_data)

    if "live_history" not in st.session_state:
        st.session_state.live_history = []

    # Append current reading to history for graphing.
    if st.session_state.live_data is not None:
        cr = st.session_state.live_data["current_reading"]
        if not st.session_state.live_history or st.session_state.live_history[-1]["timestamp"] != cr["timestamp"]:
            st.session_state.live_history.append(cr)

    # Build and render graph of safe confidence over time.
    if st.session_state.live_history:
        history_df = pd.DataFrame([
            {
                "timestamp": datetime.fromisoformat(item["timestamp"]) if isinstance(item["timestamp"], str) else item["timestamp"],
                "safe_confidence": item["classification"]["confidence_safe_percent"],
                "status": "SAFE" if item["classification"]["status_code"] == 1 else "TOXIC"
            }
            for item in st.session_state.live_history
        ])

        threshold_value = 70.0
        status_color = ["#28a745" if v >= threshold_value else "#dc3545" for v in history_df["safe_confidence"]]

        fig = make_subplots(specs=[[{"secondary_y": False}]])
        fig.add_trace(
            go.Scatter(
                x=history_df["timestamp"],
                y=history_df["safe_confidence"],
                mode="lines+markers",
                name="Safe Confidence",
                line=dict(color="#007bff", width=2),
                marker=dict(color=status_color, size=8),
                hovertemplate="%{x}<br>Safe Confidence: %{y:.1f}%%<br>Status: %{customdata}",
                customdata=history_df[["status"]]
            )
        )

        fig.add_shape(
            type="line",
            x0=history_df["timestamp"].min(),
            x1=history_df["timestamp"].max(),
            y0=threshold_value,
            y1=threshold_value,
            line=dict(color="#dc3545", width=1, dash="dash"),
            name="Threshold"
        )

        fig.update_layout(
            title="Live Safe Confidence Trend",
            xaxis_title="Time",
            yaxis_title="Safe Confidence (%)",
            yaxis=dict(range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=60, b=30, l=30, r=30),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    if st.session_state.last_refresh:
        st.caption(f"Last updated: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")


def render():
    """Main render function for the live dashboard page"""
    render_live_dashboard()