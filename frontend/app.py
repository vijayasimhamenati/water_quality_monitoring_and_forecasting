import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION (Light Mode Theme)
# ==========================================
st.set_page_config(
    page_title="Water Quality Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force Light Mode using Custom CSS
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] { background-color: #F8F9FA; color: #1E1E1E; }
        [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E0E0E0; }
        h1, h2, h3 { color: #004B87; } /* Deep Water Blue for headers */
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.title("💧 Water Quality Dashboard")
st.markdown("### Digital Twin Operations & Early Warning System")
st.divider()

# Backend API URL (Change to 8080 or 8000 if your FastAPI is running there)
API_URL = "http://127.0.0.1:9090/analyze"

# ==========================================
# SIDEBAR: RAW WATER INPUTS
# ==========================================
st.sidebar.header("🔬 Raw Water (RW) Metrics")
st.sidebar.markdown("Enter the latest sensor readings below:")

# We use forms so it doesn't predict on every single keystroke
with st.sidebar.form("input_form"):
    st.subheader("Key Parameters (Sliders)")
    # Sliders for standard intuitive ranges
    rw_ph = st.slider("RW pH", min_value=0.0, max_value=14.0, value=7.4, step=0.1)
    rw_tur = st.slider("RW Turbidity (NTU)", min_value=0.0, max_value=100.0, value=3.2, step=0.1)
    rw_colour = st.slider("RW Colour (PtCo)", min_value=0.0, max_value=100.0, value=15.0, step=1.0)
    rw_tds = st.slider("RW TDS (mg/L)", min_value=0.0, max_value=1000.0, value=245.5, step=1.0)
    
    st.subheader("Chemical Composition (Inputs)")
    # Number inputs for specific precise chemistry
    col1, col2 = st.columns(2)
    with col1:
        rw_iron = st.number_input("Iron", value=0.12, format="%.2f")
        rw_s_solids = st.number_input("S Solids", value=4.5, format="%.2f")
        rw_chloride = st.number_input("Chloride", value=35.0, format="%.2f")
        rw_calcium = st.number_input("Calcium", value=38.0, format="%.2f")
        rw_alkalinity = st.number_input("Alkalinity", value=95.0, format="%.2f")
    with col2:
        rw_hardness = st.number_input("Hardness", value=110.0, format="%.2f")
        rw_aluminium = st.number_input("Aluminium", value=0.02, format="%.2f")
        rw_manganese = st.number_input("Manganese", value=0.01, format="%.2f")
        rw_conductivity = st.number_input("Conduct.", value=410.0, format="%.2f")
        rw_magnesium = st.number_input("Magnesium", value=12.5, format="%.2f")
        
    rw_ammonia = st.number_input("Ammonia as N", value=0.05, format="%.2f")

    submitted = st.form_submit_button("🧪 Analyze Water", use_container_width=True)

# ==========================================
# MAIN DASHBOARD AREA
# ==========================================
if submitted:
    # 1. Prepare JSON Payload matching the FastAPI schema
    payload = {
        "RW pH": rw_ph, "RW Tur": rw_tur, "RW Colour": rw_colour, "RW TDS": rw_tds,
        "RW Iron": rw_iron, "RW Hardness": rw_hardness, "RW S Solids": rw_s_solids,
        "RW Aluminium": rw_aluminium, "RW Chloride": rw_chloride, "RW Manganese": rw_manganese,
        "RW Conductivity": rw_conductivity, "RW Calcium": rw_calcium, "RW Magnesium": rw_magnesium,
        "RW Alkalinity": rw_alkalinity, "RW Ammonia as N": rw_ammonia
    }

    with st.spinner("Analyzing water composition with Digital Twin..."):
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            
            classification = result["classification"]
            tw_preds = result["treated_water_predictions"]
            
            # --- ROW 1: CLASSIFICATION GAUGE ---
            st.markdown("### 🚨 Safety Classification")
            
            is_safe = classification["status_code"] == 1
            conf_safe = classification["confidence_safe_percent"]
            conf_toxic = classification["confidence_toxic_percent"]
            
            # Gauge Logic
            gauge_value = conf_safe if is_safe else conf_toxic
            gauge_title = "Confidence SAFE (%)" if is_safe else "Confidence TOXIC (%)"
            gauge_color = "#28A745" if is_safe else "#DC3545" # Green vs Red
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=gauge_value,
                title={'text': gauge_title, 'font': {'size': 24}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1},
                    'bar': {'color': gauge_color},
                    'steps': [
                        {'range': [0, 50], 'color': "#f0f2f6"},
                        {'range': [50, 80], 'color': "#e2e6ea"},
                        {'range': [80, 100], 'color': "#d6d8db"}
                    ]
                }
            ))
            fig_gauge.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
            
            # Display Status Banner & Gauge
            g_col1, g_col2 = st.columns([1, 2])
            with g_col1:
                st.write("") # Spacer
                if is_safe:
                    st.success(f"✅ **{classification['message']}**\n\nThe AI predicts this Raw Water is perfectly within operational bounds.")
                else:
                    st.error(f"⚠️ **{classification['message']}**\n\nThe AI has detected a catastrophic anomaly. Initiate emergency protocols.")
            with g_col2:
                st.plotly_chart(fig_gauge, use_container_width=True)

            st.divider()

            # --- ROW 2: PREDICTED TREATED WATER (METRIC CARDS WITH DELTAS) ---
            st.markdown("### 📊 Predicted Treated Water (TW) Metrics")
            st.caption("Arrows indicate change from Raw Water (Red = increase, Green = decrease)")
            
            # Create a 4x4 grid of metric cards
            m_cols = st.columns(4)
            
            # A dictionary mapping TW targets to their RW counterparts to calculate Deltas
            comparisons = {
                "TW pH": rw_ph, "TW Tur": rw_tur, "TW Colour": rw_colour, "TW TDS": rw_tds,
                "TW Iron": rw_iron, "TW Hardness": rw_hardness, "TW S Solids": rw_s_solids,
                "TW Aluminium": rw_aluminium, "TW Chloride": rw_chloride, "TW Manganese": rw_manganese,
                "TW Conductivity": rw_conductivity, "TW Calcium": rw_calcium, "TW Magnesium": rw_magnesium,
                "TW Alkalinity": rw_alkalinity, "TW Ammonia as N": rw_ammonia
            }
            
            idx = 0
            for tw_key, tw_val in tw_preds.items():
                if tw_key in comparisons:
                    delta_val = round(tw_val - comparisons[tw_key], 2)
                    # For things like Turbidity, a decrease (negative delta) is GOOD (normal behavior).
                    # Streamlit naturally colors negative deltas red. We reverse it so dropping toxins is Green!
                    m_cols[idx % 4].metric(
                        label=tw_key, 
                        value=f"{tw_val:.2f}", 
                        delta=f"{delta_val}",
                        delta_color="inverse" 
                    )
                else:
                    # For FRC (Free Residual Chlorine) which doesn't have an RW equivalent
                    m_cols[idx % 4].metric(label=tw_key, value=f"{tw_val:.2f}")
                idx += 1
                
            st.divider()

            # --- ROW 3: VISUAL COMPARISON CHART ---
            st.markdown("### 📈 Core Metrics: Intake vs. Predicted Output")
            # Select the most critical metrics to show in a bar chart
            chart_metrics = ["pH", "Turbidity", "Colour", "Hardness", "Alkalinity"]
            
            chart_data = {
                "Metric": chart_metrics,
                "Raw Water (Intake)": [rw_ph, rw_tur, rw_colour, rw_hardness, rw_alkalinity],
                "Treated Water (Predicted)": [
                    tw_preds.get("TW pH", 0), 
                    tw_preds.get("TW Tur", 0), 
                    tw_preds.get("TW Colour", 0), 
                    tw_preds.get("TW Hardness", 0), 
                    tw_preds.get("TW Alkalinity", 0)
                ]
            }
            df_chart = pd.DataFrame(chart_data).set_index("Metric")
            
            # Streamlit's native bar chart handles grouped bars beautifully
            st.bar_chart(df_chart, color=["#17a2b8", "#004B87"])

        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection Error: Cannot reach the Digital Twin API. Ensure your FastAPI server is running on port 9090.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
else:
    st.info("👈 Enter the Raw Water metrics in the sidebar and click **Analyze Water** to run the Digital Twin prediction.")