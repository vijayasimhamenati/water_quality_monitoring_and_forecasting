# Professional Frontend Architecture

## 🎨 New Structure (Industry Standard)

```
frontend/
├── __init__.py                    # Package marker
├── app.py                         # Main entry point (multi-page router)
├── config.py                      # Theme, colors, constants, API endpoints
│
├── utils/                         # Utility modules
│   ├── __init__.py
│   ├── api_client.py             # Centralized API communication
│   └── formatters.py             # Data formatting helpers
│
├── components/                    # Reusable UI components
│   ├── __init__.py
│   ├── ui.py                     # Basic UI components (headers, boxes, etc)
│   ├── sidebar.py                # Navigation + input form
│   └── dashboard.py              # Dashboard-specific components (gauges, charts)
│
├── pages/                         # Multi-page structure
│   ├── __init__.py
│   ├── page_01_dashboard.py      # Main analysis page
│   ├── page_02_bulk_analysis.py  # Batch processing
│   └── page_03_settings.py       # Configuration & system info
│
└── .streamlit/config.toml        # Streamlit theme configuration
```

## 🎯 Key Features

### 1. **Professional Color Scheme**

- **Primary**: Deep Water Blue (#004B87) - Trust, professional, science-focused
- **Secondary**: Teal (#17a2b8) - Energetic, complementary
- **Success**: Green (#28A745) - Safe, all-good
- **Danger**: Red (#DC3545) - Toxic, alert
- **Background**: White (#FFFFFF) - Clean, modern
- **Text**: Dark Gray (#1E1E1E) - High contrast, readable

### 2. **Centralized Configuration**

- Single `config.py` for all theme/color/API settings
- Easy to maintain and update globally
- `.streamlit/config.toml` for Streamlit's built-in theming

### 3. **API Client Layer**

- Centralized `api_client.py` for all backend requests
- Error handling and retry logic in one place
- Easy to extend with auth, logging, caching

### 4. **Reusable Components**

- `ui.py`: Generic UI building blocks (headers, boxes, dividers)
- `sidebar.py`: Navigation + water input form
- `dashboard.py`: Dashboard-specific visualizations (gauges, metrics, charts)
- Easy to add new components as app grows

### 5. **Multi-Page Structure**

- **Dashboard**: Main analysis interface
- **Bulk Analysis**: CSV upload and batch processing
- **Settings**: System info, API health check, configuration

## 🚀 How to Run

```bash
cd frontend

# Single page (old way - will fail)
streamlit run app.py                  # ❌ Won't work with new structure

# Correct way (multi-page detection automatic)
streamlit run app.py                  # ✅ Streamlit auto-detects pages/ folder
```

Streamlit **automatically discovers** multi-page apps when you have:

1. Main `app.py` as entry point
2. `pages/` folder with `*.py` files inside

## 🎨 Styling

All custom CSS is in `frontend/config.py` under `CUSTOM_CSS`:

- White background (`#FFFFFF`)
- Professional borders and shadows
- Responsive columns and spacing
- Color-coded status badges
- Clean form styling

## 💥 Scalability Roadmap

### Phase 1 ✅ (Current)

- Multi-page structure
- Professional theming
- API client layer
- Component reusability

### Phase 2 (Planned)

- Add **Reports** page (PDF export, charting)
- Add **Analytics** page (historical trends, dashboards)
- Add **Alerts** page (notification settings, rules engine)
- LocalStorage for user preferences

### Phase 3 (Future)

- Authentication (login/logout)
- User profiles and role-based access
- Real-time updates via WebSocket
- Advanced charting (Plotly dashboards)
- Mobile-responsive design

## 📝 Component Patterns

### Adding a New Page

1. Create `frontend/pages/page_04_NewFeature.py`
2. Implement `render()` function
3. Auto-discovered by Streamlit (no **init** changes needed)

### Adding a New Component

1. Add function to appropriate module in `frontend/components/`
2. Import in page modules as needed
3. Reuse across multiple pages

### Changing Theme

1. Update colors in `frontend/config.py`
2. Update `.streamlit/config.toml` for Streamlit defaults
3. Changes apply globally immediately

## ✨ Professional Features

- ✅ White background (modern, clean)
- ✅ Professional color scheme (science-focused)
- ✅ Consistent spacing and typography
- ✅ Error handling with UI feedback
- ✅ Loading states with spinners
- ✅ Responsive layout (wide mode)
- ✅ Accessible form controls
- ✅ API health monitoring
- ✅ Batch processing capability
- ✅ Metric cards with deltas
- ✅ Interactive gauges
- ✅ Comparison charts
