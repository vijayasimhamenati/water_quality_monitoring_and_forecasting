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

    auto_refresh = st.checkbox("Auto-refresh every 5 seconds", value=True)

    if st.session_state.live_data is None:
        refresh_data()

    get_status_card(st.session_state.live_data)

    if st.session_state.last_refresh:
        st.caption(f"Last updated: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")

    if auto_refresh:
        # Use st_autorefresh where available to avoid streamlit version mismatch
        try:
            from streamlit import st_autorefresh
            st_autorefresh(interval=5000, key="live_dashboard_autorefresh")
        except Exception:
            # Fallback: perform manual refresh button action only (no infinite rerun retries)
            st.info("Auto-refresh unavailable in this Streamlit version; use 'Refresh Now' button.")


def render():
    """Main render function for the live dashboard page"""
    render_live_dashboard()