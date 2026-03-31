"""
Dashboard Page - Main analysis interface with modular input cards
"""
import streamlit as st
import pandas as pd
from config import CUSTOM_CSS, PRIMARY_COLOR, SECONDARY_COLOR
from utils.api_client import APIClient
from components.dashboard import (
    render_classification_gauge,
    render_treated_water_metrics,
    render_comparison_chart,
)
from components.ui import header, section_divider, error_box


def render_input_cards() -> dict:
    """
    Render modular input cards for water quality parameters.
    Returns dict with all RW metrics.
    """
    st.markdown("### 🔬 Raw Water (RW) Parameters")
    st.markdown("*Enter sensor readings for analysis*")
    
    # Card 1: RW Key Sensor Readings
    with st.container(border=True):
        st.markdown("#### 📊 RW Key Sensor Readings")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            rw_ph = st.slider(
                "pH", min_value=0.0, max_value=14.0, value=7.4, step=0.1,
                help="Typical range: 6.5-8.5"
            )
        
        with col2:
            rw_tur = st.slider(
                "Turbidity (NTU)", min_value=0.0, max_value=100.0, value=3.2, step=0.1,
                help="Lower is better (< 5 NTU preferred)"
            )
        
        with col3:
            rw_colour = st.slider(
                "Colour (PtCo)", min_value=0.0, max_value=200.0, value=15.0, step=1.0,
                help="CPHEEO limit: 5 PtCo"
            )
        
        with col4:
            rw_tds = st.slider(
                "TDS (mg/L)", min_value=0.0, max_value=2000.0, value=245.5, step=10.0,
                help="CPHEEO limit: 500 mg/L"
            )
    
    # Card 2: Chemical Properties Analysis
    with st.container(border=True):
        st.markdown("#### 🧪 Chemical Properties Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            rw_iron = st.number_input("Iron (mg/L)", value=0.12, step=0.01, format="%.2f")
            rw_hardness = st.number_input("Hardness (mg/L)", value=110.0, step=1.0, format="%.1f")
            rw_s_solids = st.number_input("Suspended Solids (mg/L)", value=4.5, step=0.1, format="%.2f")
            rw_aluminium = st.number_input("Aluminium (mg/L)", value=0.02, step=0.01, format="%.2f")
            rw_chloride = st.number_input("Chloride (mg/L)", value=35.0, step=1.0, format="%.1f")
        
        with col2:
            rw_manganese = st.number_input("Manganese (mg/L)", value=0.01, step=0.01, format="%.2f")
            rw_conductivity = st.number_input("Conductivity (µS/cm)", value=410.0, step=10.0, format="%.1f")
            rw_calcium = st.number_input("Calcium (mg/L)", value=38.0, step=1.0, format="%.1f")
            rw_magnesium = st.number_input("Magnesium (mg/L)", value=12.5, step=0.1, format="%.2f")
            rw_alkalinity = st.number_input("Alkalinity (mg/L)", value=95.0, step=1.0, format="%.1f")
        
        rw_ammonia = st.number_input("Ammonia as N (mg/L)", value=0.05, step=0.01, format="%.2f")
    
    # Return payload with dataset aliases
    payload = {
        "RW pH": rw_ph,
        "RW Tur": rw_tur,
        "RW Colour": rw_colour,
        "RW TDS": rw_tds,
        "RW Iron": rw_iron,
        "RW Hardness": rw_hardness,
        "RW S Solids": rw_s_solids,
        "RW Aluminium": rw_aluminium,
        "RW Chloride": rw_chloride,
        "RW Manganese": rw_manganese,
        "RW Conductivity": rw_conductivity,
        "RW Calcium": rw_calcium,
        "RW Magnesium": rw_magnesium,
        "RW Alkalinity": rw_alkalinity,
        "RW Ammonia as N": rw_ammonia,
    }
    
    return payload


def render():
    """Render dashboard page."""
    # Apply custom theme
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # Header
    header(title="Water Quality Dashboard", subtitle="Real-time Digital Twin Analysis", icon="💧")
    
    # Getting Started Info
    st.info(
        "👋 **Getting Started**\n\n"
        "1. Enter Raw Water (RW) metrics in the cards below\n"
        "2. Click **Analyze Water** to run the Digital Twin analysis\n"
        "3. View predictions, classifications, and insights in the results area below"
    )
    
    # Input cards
    payload = render_input_cards()
    
    # Analyze button
    col_btn, col_spacer = st.columns([1, 4])
    with col_btn:
        submitted = st.button("🧪 Analyze Water", type="primary", use_container_width=True)
    
    if submitted:
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
        # Results placeholder when not submitted
        with st.container(border=True):
            st.markdown("### 📊 Real-time Digital Insights")
            st.info("Results will appear here after analysis")
