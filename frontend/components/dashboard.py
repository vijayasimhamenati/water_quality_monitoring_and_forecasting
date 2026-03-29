"""
Dashboard Cards Component - Analysis results display
"""
import streamlit as st
import plotly.graph_objects as go
from frontend.config import SUCCESS_COLOR, DANGER_COLOR


def render_classification_gauge(is_safe: bool, confidence: float):
    """Render safety classification gauge chart."""
    gauge_color = SUCCESS_COLOR if is_safe else DANGER_COLOR
    gauge_title = "Confidence SAFE" if is_safe else "Confidence TOXIC"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=confidence,
        title={'text': gauge_title, 'font': {'size': 20}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#CCCCCC"},
            'bar': {'color': gauge_color, 'thickness': 0.7},
            'bgcolor': "#F0F0F0",
            'borderwidth': 1,
            'bordercolor': "#E0E0E0",
            'steps': [
                {'range': [0, 33], 'color': "#FFE6E6"},
                {'range': [33, 66], 'color': "#FFFBEA"},
                {'range': [66, 100], 'color': "#E6F5E6"},
            ],
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", color="#1E1E1E")
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_treated_water_metrics(tw_predictions: dict, rw_inputs: dict):
    """Render treated water metrics in a grid."""
    st.markdown("### 📊 Predicted Treated Water (TW) Metrics")
    st.caption("*Arrows indicate change from Raw Water input. Green = improvement, Red = increase*")
    
    # Create 4-column grid
    cols = st.columns(4)
    
    comparisons = {
        "TW pH": rw_inputs.get("RW pH", 0),
        "TW Tur": rw_inputs.get("RW Tur", 0),
        "TW Colour": rw_inputs.get("RW Colour", 0),
        "TW TDS": rw_inputs.get("RW TDS", 0),
        "TW Iron": rw_inputs.get("RW Iron", 0),
        "TW Hardness": rw_inputs.get("RW Hardness", 0),
        "TW S Solids": rw_inputs.get("RW S Solids", 0),
        "TW Aluminium": rw_inputs.get("RW Aluminium", 0),
        "TW Chloride": rw_inputs.get("RW Chloride", 0),
        "TW Manganese": rw_inputs.get("RW Manganese", 0),
        "TW Conductivity": rw_inputs.get("RW Conductivity", 0),
        "TW Calcium": rw_inputs.get("RW Calcium", 0),
        "TW Magnesium": rw_inputs.get("RW Magnesium", 0),
        "TW Alkalinity": rw_inputs.get("RW Alkalinity", 0),
    }
    
    idx = 0
    for tw_key, tw_val in tw_predictions.items():
        if tw_key in comparisons:
            delta_val = round(tw_val - comparisons[tw_key], 2)
            cols[idx % 4].metric(
                label=tw_key,
                value=f"{tw_val:.2f}",
                delta=f"{delta_val:+.2f}",
                delta_color="inverse"  # Invert so decrease shows green
            )
        else:
            # FRC doesn't have RW counterpart
            cols[idx % 4].metric(label=tw_key, value=f"{tw_val:.2f}")
        idx += 1


def render_comparison_chart(rw_inputs: dict, tw_predictions: dict):
    """Render intake vs predicted output comparison."""
    st.markdown("### 📈 Core Metrics: Intake vs. Predicted Output")
    
    chart_metrics = ["pH", "Tur", "Colour", "Hardness", "Alkalinity"]
    chart_data = {
        "Metric": chart_metrics,
        "Raw Water (Intake)": [
            rw_inputs.get("RW pH", 0),
            rw_inputs.get("RW Tur", 0),
            rw_inputs.get("RW Colour", 0),
            rw_inputs.get("RW Hardness", 0),
            rw_inputs.get("RW Alkalinity", 0),
        ],
        "Treated Water (Predicted)": [
            tw_predictions.get("TW pH", 0),
            tw_predictions.get("TW Tur", 0),
            tw_predictions.get("TW Colour", 0),
            tw_predictions.get("TW Hardness", 0),
            tw_predictions.get("TW Alkalinity", 0),
        ]
    }
    
    import pandas as pd
    df = pd.DataFrame(chart_data).set_index("Metric")
    st.bar_chart(df, color=["#004B87", "#17a2b8"])
