"""
Settings Page - Configuration and preferences
"""
import streamlit as st
from frontend.config import CUSTOM_CSS, APP_NAME, APP_VERSION, API_ANALYZE
from frontend.utils.api_client import APIClient
from frontend.components.ui import header


def render():
    """Render settings page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    header(title="Settings", subtitle="Configuration & System Info", icon="⚙️")
    
    # System Information
    with st.expander("📋 System Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("App Name", APP_NAME)
            st.metric("Version", APP_VERSION)
        with col2:
            api_alive = APIClient.check_health()
            st.metric("API Status", "🟢 Online" if api_alive else "🔴 Offline")
            st.metric("API Endpoint", API_ANALYZE)
    
    st.divider()
    
    # Analysis Settings
    with st.expander("🔧 Analysis Settings", expanded=False):
        st.markdown("**Safety Confidence Threshold**")
        threshold = st.slider(
            "Minimum confidence required to declare water SAFE (%)",
            min_value=50,
            max_value=100,
            value=80,
            step=5,
            help="Default: 80%"
        )
        st.info(f"Current setting: Water is safe if confidence > {threshold}%")
    
    st.divider()
    
    # API Configuration
    with st.expander("🌐 API Configuration", expanded=False):
        st.markdown("**Backend API Settings**")
        st.text(f"Base URL: {API_ANALYZE}")
        
        if st.button("🔄 Test API Connection"):
            if APIClient.check_health():
                st.success("✅ API is reachable and healthy")
            else:
                st.error("❌ Cannot reach API. Check if backend is running.")
    
    st.divider()
    
    # About
    with st.expander("ℹ️ About", expanded=False):
        st.markdown("""
        ### Water Quality Digital Twin
        
        A modern ML-based system for water quality monitoring and forecasting.
        
        **Features:**
        - Real-time water quality assessment
        - AI-powered classification (Safe/Toxic)
        - Treated water metric predictions
        - Bulk sample analysis
        - RESTful API backend
        
        **Technology Stack:**
        - Frontend: Streamlit
        - Backend: FastAPI
        - ML: scikit-learn
        - Data: pandas, numpy
        """)
        
        st.markdown("---")
        st.markdown("*© 2026 Water Quality Monitoring & Forecasting System*")
