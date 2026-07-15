"""Reusable Tkinter widgets for the password strength checker."""

from __future__ import annotations

from tkinter import Canvas, Text, ttk

from password_strength_checker.presentation.styles import THEME, strength_color


class SurfaceFrame(ttk.Frame):
    """A reusable dark surface container."""

    def __init__(self, parent: ttk.Widget, padding: int = 16) -> None:
        super().__init__(parent, style="Surface.TFrame", padding=padding)


class MetricCard(SurfaceFrame):
    """Small panel for displaying a single metric value."""

    def __init__(self, parent: ttk.Widget, title: str) -> None:
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self._value_var = ttk.Label(self, text="-", style="Metric.TLabel")
        self._title_label = ttk.Label(self, text=title, style="Caption.TLabel")

        self._value_var.grid(row=0, column=0, sticky="w")
        self._title_label.grid(row=1, column=0, sticky="w", pady=(6, 0))

    def set_value(self, value: str) -> None:
        """Update the displayed metric value."""
        self._value_var.configure(text=value)


class StrengthMeter(SurfaceFrame):
    """Progress bar and color indicator for password strength."""

    def __init__(self, parent: ttk.Widget) -> None:
        super().__init__(parent)
        self.columnconfigure(1, weight=1)

        self._indicator = Canvas(
            self,
            width=18,
            height=18,
            background=THEME.surface,
            borderwidth=0,
            highlightthickness=0,
        )
        self._indicator_oval = self._indicator.create_oval(
            2,
            2,
            16,
            16,
            fill=THEME.border,
            outline="",
        )
        self._progress = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            maximum=100,
        )
        self._label = ttk.Label(self, text="Not analyzed", style="Surface.TLabel")

        self._indicator.grid(row=0, column=0, padx=(0, 10), sticky="w")
        self._progress.grid(row=0, column=1, sticky="ew")
        self._label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def set_strength(self, score: int, level: str) -> None:
        """Update progress, text, and indicator color based on score."""
        color = strength_color(score)
        self._progress.configure(value=score)
        self._indicator.itemconfigure(self._indicator_oval, fill=color)
        self._label.configure(text=f"{level} strength ({score}/100)")

    def reset(self) -> None:
        """Return the strength meter to its initial state."""
        self._progress.configure(value=0)
        self._indicator.itemconfigure(self._indicator_oval, fill=THEME.border)
        self._label.configure(text="Not analyzed")


class SuggestionsPanel(SurfaceFrame):
    """Read-only panel for warnings and password suggestions."""

    def __init__(self, parent: ttk.Widget) -> None:
        super().__init__(parent)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="Requirements & Checks",
            style="Surface.TLabel",
            font=(THEME.font_family, 12, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))

        self._text = Text(
            self,
            height=10,
            wrap="word",
            background=THEME.surface_alt,
            foreground=THEME.text,
            insertbackground=THEME.text,
            relief="flat",
            padx=12,
            pady=10,
            font=(THEME.monospace_family, 9),
        )
        self._text.grid(row=1, column=0, sticky="nsew")
        self._text.configure(state="disabled")

        # Configure tags for pass/fail indicators
        self._text.tag_configure("pass", foreground="#22C55E", font=(THEME.monospace_family, 9, "bold"))
        self._text.tag_configure("fail", foreground="#EF4444", font=(THEME.monospace_family, 9, "bold"))
        self._text.tag_configure("advice", foreground=THEME.muted_text, font=(THEME.font_family, 9))

    def set_messages(self, messages: list[str]) -> None:
        """Display warning and recommendation messages."""
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")

        if messages:
            self._text.insert("end", "\n".join(f"• {message}" for message in messages))
        else:
            self._text.insert("end", "Enter or generate a password to see guidance.")

        self._text.configure(state="disabled")

    def set_rules_status(
        self,
        has_min_length: bool,
        has_acceptable_length: bool,
        has_uppercase: bool,
        has_lowercase: bool,
        has_number: bool,
        has_symbol: bool,
        has_no_repeated: bool,
        has_no_sequential: bool,
        has_no_keyboard_patterns: bool,
        has_no_dictionary_words: bool,
        is_not_common: bool,
    ) -> None:
        """Display rule pass/fail status."""
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")

        rules = [
            ("✔ Minimum 12 characters", has_min_length),
            ("✔ Maximum 128 characters", has_acceptable_length),
            ("✔ Uppercase letters (A-Z)", has_uppercase),
            ("✔ Lowercase letters (a-z)", has_lowercase),
            ("✔ Numbers (0-9)", has_number),
            ("✔ Symbols (!@#$%...)", has_symbol),
            ("✔ No repeated characters", has_no_repeated),
            ("✔ No sequential patterns", has_no_sequential),
            ("✔ No keyboard patterns", has_no_keyboard_patterns),
            ("✔ No dictionary words", has_no_dictionary_words),
            ("✔ Not a common password", is_not_common),
        ]

        for rule, passed in rules:
            if passed:
                self._text.insert("end", rule + "\n", "pass")
            else:
                display_rule = rule.replace("✔", "✖")
                self._text.insert("end", display_rule + "\n", "fail")

        self._text.configure(state="disabled")
