"""
Formatters - Data formatting utilities
"""
from typing import Dict


def format_value(value: float, unit: str = "", decimals: int = 2) -> str:
    """Format numeric value with unit."""
    return f"{value:.{decimals}f} {unit}".strip()


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format as percentage."""
    return f"{value:.{decimals}f}%"


def get_safety_message(is_safe: bool, confidence: float) -> tuple[str, str]:
    """
    Generate safety message and icon.
    
    Returns:
        (message: str, icon: str)
    """
    if is_safe:
        return (
            f"✅ SAFE - Water is within operational bounds (Confidence: {confidence:.1f}%)",
            "success"
        )
    else:
        return (
            f"⚠️ TOXIC - Potential quality issues detected (Confidence: {confidence:.1f}%)",
            "error"
        )


def get_delta_interpretation(delta: float, param_name: str) -> str:
    """Interpret delta changes - most params improve (decrease) naturally."""
    metric_lower = param_name.lower()
    
    # For toxicity indicators, decrease is good
    toxins = ["tur", "colour", "iron", "manganese", "hardness", "tds"]
    for toxin in toxins:
        if toxin in metric_lower:
            if delta < 0:
                return "✓ Improved"
            elif delta > 0:
                return "⚠️ Worsened"
            return "No change"
    
    return "No change"
