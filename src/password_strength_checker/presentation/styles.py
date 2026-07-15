"""Tkinter styling for the desktop application."""

from __future__ import annotations

from dataclasses import dataclass
from tkinter import Tk, ttk


@dataclass(frozen=True, slots=True)
class Theme:
    """Color and typography tokens used by the GUI."""

    background: str = "#111827"
    surface: str = "#1F2937"
    surface_alt: str = "#273244"
    border: str = "#374151"
    text: str = "#F9FAFB"
    muted_text: str = "#9CA3AF"
    accent: str = "#38BDF8"
    success: str = "#22C55E"
    warning: str = "#F59E0B"
    danger: str = "#EF4444"
    weak: str = "#F97316"
    moderate: str = "#EAB308"
    font_family: str = "Segoe UI"
    monospace_family: str = "Consolas"


THEME = Theme()


def strength_color(score: int) -> str:
    """Return the indicator color for a password score based on strength level."""
    # Very Weak (0-20) → Red
    if score < 20:
        return "#EF4444"  # Red
    # Weak (20-40) → Orange
    if score < 40:
        return "#F97316"  # Orange
    # Medium (40-60) → Yellow
    if score < 60:
        return "#EAB308"  # Yellow
    # Strong (60-80) → Blue
    if score < 80:
        return "#38BDF8"  # Blue
    # Very Strong (80-100) → Green
    return "#22C55E"  # Green


def configure_theme(root: Tk) -> None:
    """Configure global Tkinter and ttk styles for the dark theme."""
    root.configure(background=THEME.background)
    root.option_add("*Font", (THEME.font_family, 10))
    root.option_add("*Foreground", THEME.text)
    root.option_add("*Background", THEME.background)

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        ".",
        background=THEME.background,
        foreground=THEME.text,
        fieldbackground=THEME.surface_alt,
        bordercolor=THEME.border,
        lightcolor=THEME.border,
        darkcolor=THEME.border,
        troughcolor=THEME.surface_alt,
        font=(THEME.font_family, 10),
    )
    style.configure("TFrame", background=THEME.background)
    style.configure("Surface.TFrame", background=THEME.surface)
    style.configure(
        "TLabel",
        background=THEME.background,
        foreground=THEME.text,
    )
    style.configure(
        "Muted.TLabel",
        background=THEME.background,
        foreground=THEME.muted_text,
    )
    style.configure(
        "Surface.TLabel",
        background=THEME.surface,
        foreground=THEME.text,
    )
    style.configure(
        "Title.TLabel",
        background=THEME.background,
        foreground=THEME.text,
        font=(THEME.font_family, 20, "bold"),
    )
    style.configure(
        "Metric.TLabel",
        background=THEME.surface,
        foreground=THEME.text,
        font=(THEME.font_family, 16, "bold"),
    )
    style.configure(
        "Caption.TLabel",
        background=THEME.surface,
        foreground=THEME.muted_text,
        font=(THEME.font_family, 10),
    )
    style.configure(
        "Rule.TLabel",
        background=THEME.surface,
        foreground=THEME.text,
        font=(THEME.font_family, 10),
    )
    style.configure(
        "TButton",
        background=THEME.surface_alt,
        foreground=THEME.text,
        borderwidth=1,
        focusthickness=0,
        padding=(12, 8),
    )
    style.map(
        "TButton",
        background=[("active", THEME.border), ("pressed", THEME.accent)],
        foreground=[("disabled", THEME.muted_text)],
    )
    style.configure(
        "Accent.TButton",
        background=THEME.accent,
        foreground="#082F49",
        font=(THEME.font_family, 10, "bold"),
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#7DD3FC"), ("pressed", "#0284C7")],
    )
    style.configure(
        "TCheckbutton",
        background=THEME.surface,
        foreground=THEME.text,
        padding=(0, 4),
    )
    style.map("TCheckbutton", background=[("active", THEME.surface)])
    style.configure(
        "Horizontal.TProgressbar",
        background=THEME.accent,
        troughcolor=THEME.surface_alt,
        bordercolor=THEME.border,
        lightcolor=THEME.accent,
        darkcolor=THEME.accent,
    )
