"""
Streamlit Configuration - Theme, Colors, and Constants
Professional color scheme with white background and good contrast.
"""

# ==========================================
# PROFESSIONAL COLOR PALETTE
# ==========================================
# Primary: Deep Water Blue (trust, professional, science-focused)
PRIMARY_COLOR = "#004B87"
# Secondary: Accent Teal (complementary, energetic)
SECONDARY_COLOR = "#17a2b8"
# Success: Green (safe, all-good)
SUCCESS_COLOR = "#28A745"
# Danger: Red (toxic, alert)
DANGER_COLOR = "#DC3545"
# Warning: Orange
WARNING_COLOR = "#FF6B35"
# Neutral: Gray shades
DARK_GRAY = "#1E1E1E"
LIGHT_GRAY = "#F8F9FA"
BORDER_GRAY = "#E0E0E0"

# ==========================================
# CUSTOM CSS FOR PROFESSIONAL THEME
# ==========================================
CUSTOM_CSS = """
<style>
    /* Overall app background: WHITE */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
        color: #1E1E1E;
    }
    
    /* Sidebar: Subtle gray/white */
    [data-testid="stSidebar"] {
        background-color: #F5F7FA;
        border-right: 1px solid #E0E0E0;
    }
    
    /* Headers: Professional deep blue */
    h1, h2 {
        color: #004B87;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    
    h3 {
        color: #004B87;
        font-weight: 500;
    }
    
    /* Body text: Dark gray for readability */
    p, span, label {
        color: #1E1E1E;
    }
    
    /* Metric boxes border */
    [data-testid="metric-container"] {
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 16px;
        background: linear-gradient(135deg, #FAFBFC 0%, #FFFFFF 100%);
    }
    
    /* Cards/containers: Subtle shadow */
    .card-container {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    }
    
    /* Divider */
    hr {
        border: 1px solid #E0E0E0;
    }
    
    /* Buttons */
    button {
        border-radius: 6px;
        font-weight: 500;
        background-color: #004B87 !important;
        color: white !important;
    }
    
    button:hover {
        background-color: #003056 !important;
    }
    
    /* Sidebar input labels */
    [data-testid="stSidebar"] label {
        color: #004B87;
        font-weight: 500;
    }
</style>
"""

# ==========================================
# APP METADATA
# ==========================================
APP_NAME = "💧 Water Quality Digital Twin"
APP_VERSION = "1.0.0"
API_VERSION = "v1"

# ==========================================
# PAGE CONFIG
# ==========================================
PAGE_ICON = "💧"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# ==========================================
# API ENDPOINTS
# ==========================================
import os

API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:9090")
API_HEALTH = f"{API_BASE_URL}/api/{API_VERSION}/health"
API_ANALYZE = f"{API_BASE_URL}/api/{API_VERSION}/analyze"
