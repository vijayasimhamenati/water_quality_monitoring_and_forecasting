"""
Main Streamlit App Entry Point
Multi-page application with custom header and horizontal navigation.
All default Streamlit UI elements hidden.
"""
import streamlit as st
from config import (
    PAGE_ICON, LAYOUT, CUSTOM_CSS, PRIMARY_COLOR, SECONDARY_COLOR
)

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Water Quality Management",
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="collapsed",
)

# ==========================================
# HIDE ALL DEFAULT STREAMLIT UI ELEMENTS
# ==========================================
hide_streamlit_ui = """
<style>
    /* Hide top header bar */
    header {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stAppHeader"] {
        display: none !important;
    }
    
    /* Hide Deploy button and menu */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Hide hamburger menu (3-dot menu) */
    button[kind="header"] {
        display: none !important;
    }
    
    /* Hide footer */
    footer {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide sidebar completely */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    [data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Remove sidebar margin from main container */
    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    /* Maximize main container width */
    [data-testid="stForm"] {
        max-width: 100% !important;
    }
    
    /* Hide vertical block border wrappers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        display: none !important;
    }
    
    /* Adjust main content area */
    .main {
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    
    /* Remove gaps from columns in header */
    [data-testid="column"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
</style>
"""
st.markdown(hide_streamlit_ui, unsafe_allow_html=True)

# Apply global custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# CUSTOM HEADER STYLING
# ==========================================
HEADER_CSS = f"""
<style>
    .custom-header {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, #003d6b 100%);
        padding: 24px 32px;
        margin: -80px -24px 0 -24px;
        border-bottom: 3px solid {SECONDARY_COLOR};
        box-shadow: 0 4px 12px rgba(0, 75, 135, 0.15);
    }}
    
    .header-title {{
        color: white;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin: 0;
        padding: 0;
    }}
    
    .header-subtitle {{
        color: rgba(255, 255, 255, 0.8);
        font-size: 12px;
        margin-top: 4px;
        padding: 0;
    }}
</style>
"""
st.markdown(HEADER_CSS, unsafe_allow_html=True)

# ==========================================
# INITIALIZE SESSION STATE
# ==========================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# ==========================================
# CUSTOM HEADER
# ==========================================
header_html = """
<div class="custom-header">
    <div class="header-title">💧 Water Quality Dashboard</div>
    <div class="header-subtitle">Real-time Digital Twin Analysis</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ==========================================
# HORIZONTAL NAVIGATION BAR
# ==========================================
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 4])

with nav_col1:
    if st.button(
        "🏠 Dashboard",
        use_container_width=True,
        key="nav_dashboard",
        help="View dashboard and run analysis"
    ):
        st.session_state.current_page = "Dashboard"
        st.rerun()

with nav_col2:
    if st.button(
        "📦 Bulk Analysis",
        use_container_width=True,
        key="nav_bulk",
        help="Analyze multiple samples at once"
    ):
        st.session_state.current_page = "Bulk Analysis"
        st.rerun()

st.divider()

# ==========================================
# IMPORT PAGE MODULES
# ==========================================
from pages import page_01_Dashboard, page_02_Bulk_Analysis

# Map pages to modules
pages = {
    "Dashboard": page_01_Dashboard,
    "Bulk Analysis": page_02_Bulk_Analysis,
}

# ==========================================
# RENDER SELECTED PAGE
# ==========================================
current_page = st.session_state.current_page

if current_page in pages:
    pages[current_page].render()
else:
    st.error(f"Page '{current_page}' not found.")

