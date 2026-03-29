"""
UI Components - Reusable Streamlit components
"""
import streamlit as st
from frontend.config import PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, DANGER_COLOR


def header(title: str, subtitle: str = "", icon: str = "💧"):
    """Professional header with icon and subtitle."""
    st.markdown(f"# {icon} {title}")
    if subtitle:
        st.markdown(f"**{subtitle}**")
    st.divider()


def safety_indicator(is_safe: bool, confidence: float, message: str):
    """Display safety status with color-coded badge."""
    if is_safe:
        st.success(message)
    else:
        st.error(message)


def metric_card(label: str, value: str, delta: str = "", delta_color: str = "off"):
    """Display a metric card with optional delta."""
    cols = st.columns([3, 1])
    with cols[0]:
        st.metric(label=label, value=value, delta=delta, delta_color=delta_color)
    with cols[1]:
        pass  # Spacer for alignment


def info_box(title: str, content: str, icon: str = "ℹ️"):
    """Information box with icon."""
    st.info(f"**{icon} {title}**\n\n{content}")


def warning_box(title: str, content: str, icon: str = "⚠️"):
    """Warning box with icon."""
    st.warning(f"**{icon} {title}**\n\n{content}")


def error_box(title: str, content: str, icon: str = "❌"):
    """Error box with icon."""
    st.error(f"**{icon} {title}**\n\n{content}")


def section_divider(label: str = ""):
    """Visual section divider."""
    if label:
        st.markdown(f"### {label}")
    st.divider()
