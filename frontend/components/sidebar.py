"""
Sidebar Component - Navigation and input controls
"""
import streamlit as st
from frontend.config import PRIMARY_COLOR


def render_navigation():
    """Render sidebar navigation."""
    st.sidebar.markdown("### 📍 Navigation")
    page = st.sidebar.radio(
        label="Select Page",
        options=["Dashboard", "Bulk Analysis", "Settings", "About"],
        label_visibility="collapsed"
    )
    return page


def render_input_form() -> dict:
    """
    Render water quality input form.
    Returns dict with all RW metrics using dataset aliases.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔬 Raw Water (RW) Metrics")
    st.sidebar.markdown("*Enter sensor readings for analysis*")
    
    with st.sidebar.form("water_input_form", border=True):
        st.subheader("Key Parameters")
        
        # Sliders for intuitive ranges
        rw_ph = st.slider(
            "pH", min_value=0.0, max_value=14.0, value=7.4, step=0.1,
            help="Typical range: 6.5-8.5"
        )
        rw_tur = st.slider(
            "Turbidity (NTU)", min_value=0.0, max_value=100.0, value=3.2, step=0.1,
            help="Lower is better (< 5 NTU preferred)"
        )
        rw_colour = st.slider(
            "Colour (PtCo)", min_value=0.0, max_value=200.0, value=15.0, step=1.0,
            help="CPHEEO limit: 5 PtCo"
        )
        rw_tds = st.slider(
            "TDS (mg/L)", min_value=0.0, max_value=2000.0, value=245.5, step=10.0,
            help="CPHEEO limit: 500 mg/L"
        )
        
        st.subheader("Chemical Composition")
        
        col1, col2 = st.columns(2)
        with col1:
            rw_iron = st.number_input("Iron (mg/L)", value=0.12, step=0.01, format="%.2f")
            rw_s_solids = st.number_input("Suspended Solids (mg/L)", value=4.5, step=0.1, format="%.2f")
            rw_chloride = st.number_input("Chloride (mg/L)", value=35.0, step=1.0, format="%.1f")
            rw_calcium = st.number_input("Calcium (mg/L)", value=38.0, step=1.0, format="%.1f")
            rw_alkalinity = st.number_input("Alkalinity (mg/L)", value=95.0, step=1.0, format="%.1f")
        
        with col2:
            rw_hardness = st.number_input("Hardness (mg/L)", value=110.0, step=1.0, format="%.1f")
            rw_aluminium = st.number_input("Aluminium (mg/L)", value=0.02, step=0.01, format="%.2f")
            rw_manganese = st.number_input("Manganese (mg/L)", value=0.01, step=0.01, format="%.2f")
            rw_conductivity = st.number_input("Conductivity (µS/cm)", value=410.0, step=10.0, format="%.1f")
            rw_magnesium = st.number_input("Magnesium (mg/L)", value=12.5, step=0.1, format="%.2f")
        
        rw_ammonia = st.number_input("Ammonia as N (mg/L)", value=0.05, step=0.01, format="%.2f")
        
        submitted = st.form_submit_button(
            "🧪 Analyze Water", 
            use_container_width=True,
            type="primary"
        )
    
    # Return payload with dataset aliases (exact field names)
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
    
    return {"submitted": submitted, "payload": payload}
