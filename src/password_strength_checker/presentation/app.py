"""Tkinter application bootstrap."""

from __future__ import annotations

from tkinter import Tk

from password_strength_checker.application.use_cases.analyze_password import (
    AnalyzePasswordUseCase,
)
from password_strength_checker.application.use_cases.generate_password import (
    GeneratePasswordUseCase,
)
from password_strength_checker.presentation.main_window import MainWindow
from password_strength_checker.presentation.styles import configure_theme


class PasswordStrengthCheckerApp:
    """Owns the Tk root window and starts the desktop application."""

    def __init__(
        self,
        analyze_password_use_case: AnalyzePasswordUseCase,
        generate_password_use_case: GeneratePasswordUseCase,
    ) -> None:
        self._root = Tk()
        configure_theme(self._root)
        self._main_window = MainWindow(
            root=self._root,
            analyze_password_use_case=analyze_password_use_case,
            generate_password_use_case=generate_password_use_case,
        )

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self._root.mainloop()
