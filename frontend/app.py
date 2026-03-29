"""
Main Streamlit App Entry Point
Multi-page application with professional theming.
"""
import streamlit as st
from config import (
    APP_NAME, APP_VERSION, PAGE_ICON, LAYOUT,
    INITIAL_SIDEBAR_STATE, CUSTOM_CSS
)

# Configure page
st.set_page_config(
    page_title="Water Quality Digital Twin",
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE,
)

# Apply global custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Import page modules
# from pages import page_01_dashboard, page_02_bulk_analysis, page_03_settings
from pages import page_01_Dashboard, page_02_Bulk_Analysis, page_03_Settings

# Map pages
pages = {
    "🏠 Dashboard": page_01_Dashboard,
    "📦 Bulk Analysis": page_02_Bulk_Analysis,
    "⚙️ Settings": page_03_Settings,
}

# Sidebar header and navigation
st.sidebar.markdown(f"### {APP_NAME}")
st.sidebar.markdown(f"*v{APP_VERSION}*")
st.sidebar.divider()

selected_page_name = st.sidebar.radio(
    "Navigation",
    pages.keys(),
    label_visibility="collapsed"
)

# Render selected page
pages[selected_page_name].render()

