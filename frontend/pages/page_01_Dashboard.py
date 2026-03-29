"""
Dashboard Page - Main analysis interface
"""
import streamlit as st
import pandas as pd
from frontend.config import CUSTOM_CSS, PRIMARY_COLOR, SECONDARY_COLOR, APP_NAME
from frontend.utils.api_client import APIClient
from frontend.components.sidebar import render_navigation, render_input_form
from frontend.components.dashboard import (
    render_classification_gauge,
    render_treated_water_metrics,
    render_comparison_chart,
)
from components.ui import header, safety_indicator, section_divider, error_box


def render():
    """Render dashboard page."""
    # Apply custom theme
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Header
    header(title="Water Quality Dashboard", subtitle="Real-time Digital Twin Analysis", icon="💧")
    
    # Sidebar
    page = render_navigation()
    form_data = render_input_form()
    
    # Main content
    if form_data["submitted"]:
        payload = form_data["payload"]
        
        with st.spinner("🔄 Analyzing water composition with Digital Twin..."):
            try:
                # Call API
                result = APIClient.analyze_water(payload)
                
                if result:
                    classification = result["classification"]
                    tw_preds = result["treated_water_predictions"]
                    
                    # --- SECTION 1: SAFETY CLASSIFICATION ---
                    section_divider("🚨 Safety Classification")
                    
                    is_safe = classification["status_code"] == 1
                    conf_safe = classification["confidence_safe_percent"]
                    conf_toxic = classification["confidence_toxic_percent"]
                    message = classification["message"]
                    
                    # Display safety status
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if is_safe:
                            st.success(
                                f"✅ **SAFE**\n\n"
                                f"Water is within operational bounds.\n\n"
                                f"Confidence: {conf_safe:.1f}%"
                            )
                        else:
                            st.error(
                                f"⚠️ **TOXIC**\n\n"
                                f"Action required - anomaly detected.\n\n"
                                f"Confidence: {conf_toxic:.1f}%"
                            )
                    
                    with col2:
                        render_classification_gauge(is_safe, conf_safe if is_safe else conf_toxic)
                    
                    st.divider()
                    
                    # --- SECTION 2: TREATED WATER METRICS ---
                    section_divider("📊 Predicted Output")
                    render_treated_water_metrics(tw_preds, payload)
                    
                    st.divider()
                    
                    # --- SECTION 3: COMPARISON ---
                    section_divider("📈 Comparison")
                    render_comparison_chart(payload, tw_preds)
                    
                    # --- SECTION 4: SUMMARY TABLE ---
                    st.divider()
                    section_divider("📋 Detailed Summary")
                    
                    summary_data = {
                        "Parameter": list(tw_preds.keys()),
                        "Predicted Value": [f"{v:.2f}" for v in tw_preds.values()],
                    }
                    df_summary = pd.DataFrame(summary_data)
                    st.dataframe(df_summary, use_container_width=True)
                    
            except ConnectionError as e:
                error_box(
                    "Connection Error",
                    f"Cannot reach the API server.\n\n{str(e)}",
                    icon="🔌"
                )
            except ValueError as e:
                error_box(
                    "Validation Error",
                    f"The backend returned an error.\n\n{str(e)}",
                    icon="❌"
                )
            except Exception as e:
                error_box(
                    "Unexpected Error",
                    f"Something went wrong.\n\n{str(e)}",
                    icon="⚡"
                )
    else:
        st.info(
            "👈 **Getting Started**\n\n"
            "1. Enter Raw Water (RW) metrics in the sidebar\n"
            "2. Click **Analyze Water** to run the Digital Twin\n"
            "3. View predictions, classifications, and insights below"
        )
