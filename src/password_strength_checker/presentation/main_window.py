"""Main Tkinter window for the password strength checker."""

from __future__ import annotations

from pathlib import Path
from tkinter import BooleanVar, IntVar, StringVar, Tk, filedialog, messagebox, ttk

from password_strength_checker.application.dto.password_analysis_dto import (
    PasswordAnalysisDTO,
)
from password_strength_checker.application.reports.report_exporter import (
    ReportExporter,
)
from password_strength_checker.application.use_cases.analyze_password import (
    AnalyzePasswordUseCase,
)
from password_strength_checker.application.use_cases.generate_password import (
    GeneratePasswordUseCase,
)
from password_strength_checker.presentation.styles import THEME
from password_strength_checker.presentation.widgets import (
    MetricCard,
    StrengthMeter,
    SuggestionsPanel,
    SurfaceFrame,
)
from password_strength_checker.shared.constants import (
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
)
from password_strength_checker.shared.exceptions import (
    PasswordStrengthCheckerError,
)


class MainWindow:
    """Professional desktop interface for password analysis and generation."""

    def __init__(
        self,
        root: Tk,
        analyze_password_use_case: AnalyzePasswordUseCase,
        generate_password_use_case: GeneratePasswordUseCase,
    ) -> None:
        self._root = root
        self._analyze_password_use_case = analyze_password_use_case
        self._generate_password_use_case = generate_password_use_case
        self._password_var = StringVar()
        self._show_password_var = BooleanVar(value=False)
        self._length_var = IntVar(value=20)
        self._uppercase_var = BooleanVar(value=True)
        self._lowercase_var = BooleanVar(value=True)
        self._numbers_var = BooleanVar(value=True)
        self._symbols_var = BooleanVar(value=True)
        self._latest_analysis: PasswordAnalysisDTO | None = None
        self._report_exporter = ReportExporter()

        self._configure_window()
        self._build_layout()
        self._bind_keyboard_shortcuts()
        self._reset_results()

    def _configure_window(self) -> None:
        """Configure title, size, and responsive root grid."""
        self._root.title("Password Strength Checker")
        self._root.minsize(960, 680)
        self._root.geometry("1120x780")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

    def _bind_keyboard_shortcuts(self) -> None:
        """Bind keyboard shortcuts for common actions."""
        self._root.bind("<Return>", lambda _: self._analyze_password())
        self._root.bind("<Control-c>", lambda _: self._copy_password())
        self._root.bind("<Control-g>", lambda _: self._generate_password())

    def _build_layout(self) -> None:
        """Create all visual sections in the main window."""
        container = ttk.Frame(self._root, padding=28)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(2, weight=1)

        self._build_header(container)
        self._build_password_section(container)
        self._build_results_section(container)
        self._build_generator_section(container)
        self._build_suggestions_section(container)

    def _build_header(self, parent: ttk.Frame) -> None:
        """Create application title and subtitle."""
        ttk.Label(
            parent,
            text="Password Strength Checker",
            style="Title.TLabel",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))
        ttk.Label(
            parent,
            text="Analyze password strength and generate secure passwords with confidence",
            style="Muted.TLabel",
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 24))

    def _build_password_section(self, parent: ttk.Frame) -> None:
        """Create password input and primary actions."""
        panel = SurfaceFrame(parent)
        panel.grid(row=2, column=0, sticky="nsew", padx=(0, 14))
        panel.columnconfigure(0, weight=1)

        ttk.Label(
            panel,
            text="Password",
            style="Surface.TLabel",
            font=(THEME.font_family, 12, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self._password_entry = ttk.Entry(
            panel,
            textvariable=self._password_var,
            show="*",
            font=(THEME.monospace_family, 13),
        )
        self._password_entry.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        self._password_entry.bind("<KeyRelease>", self._handle_password_change)

        controls = ttk.Frame(panel, style="Surface.TFrame")
        controls.grid(row=2, column=0, sticky="ew", pady=(0, 18))
        controls.columnconfigure(5, weight=1)

        ttk.Checkbutton(
            controls,
            text="Show password",
            variable=self._show_password_var,
            command=self._toggle_password_visibility,
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(
            controls,
            text="Analyze",
            style="Accent.TButton",
            command=self._analyze_password,
        ).grid(row=0, column=1, padx=(14, 0))
        ttk.Button(
            controls,
            text="Copy",
            command=self._copy_password,
        ).grid(row=0, column=2, padx=(8, 0))
        ttk.Button(
            controls,
            text="Clear",
            command=self._clear_password,
        ).grid(row=0, column=3, padx=(8, 0))
        ttk.Button(
            controls,
            text="Export",
            command=self._export_report,
        ).grid(row=0, column=4, padx=(8, 0))

        self._strength_meter = StrengthMeter(panel)
        self._strength_meter.grid(row=3, column=0, sticky="ew")

    def _build_results_section(self, parent: ttk.Frame) -> None:
        """Create metric cards for score, entropy, and crack time."""
        metrics = ttk.Frame(parent)
        metrics.grid(row=3, column=0, sticky="ew", padx=(0, 14), pady=(16, 0))
        for column in range(3):
            metrics.columnconfigure(column, weight=1)

        self._score_card = MetricCard(metrics, "Password Score")
        self._entropy_card = MetricCard(metrics, "Password Entropy")
        self._crack_time_card = MetricCard(metrics, "Estimated Crack Time")

        self._score_card.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self._entropy_card.grid(row=0, column=1, sticky="ew", padx=5)
        self._crack_time_card.grid(row=0, column=2, sticky="ew", padx=(10, 0))

    def _build_generator_section(self, parent: ttk.Frame) -> None:
        """Create secure password generation controls."""
        panel = SurfaceFrame(parent)
        panel.grid(row=2, column=1, sticky="nsew", padx=(14, 0))
        panel.columnconfigure(0, weight=1)

        ttk.Label(
            panel,
            text="Generator",
            style="Surface.TLabel",
            font=(THEME.font_family, 12, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 12))

        length_row = ttk.Frame(panel, style="Surface.TFrame")
        length_row.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        length_row.columnconfigure(1, weight=1)

        ttk.Label(
            length_row,
            text="Length",
            style="Surface.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Spinbox(
            length_row,
            from_=MIN_PASSWORD_LENGTH,
            to=MAX_PASSWORD_LENGTH,
            textvariable=self._length_var,
            width=8,
        ).grid(row=0, column=1, sticky="e")

        self._add_generator_checkbox(
            panel,
            row=2,
            text="Uppercase letters",
            variable=self._uppercase_var,
        )
        self._add_generator_checkbox(
            panel,
            row=3,
            text="Lowercase letters",
            variable=self._lowercase_var,
        )
        self._add_generator_checkbox(
            panel,
            row=4,
            text="Numbers",
            variable=self._numbers_var,
        )
        self._add_generator_checkbox(
            panel,
            row=5,
            text="Symbols",
            variable=self._symbols_var,
        )

        ttk.Button(
            panel,
            text="Generate Password",
            style="Accent.TButton",
            command=self._generate_password,
        ).grid(row=6, column=0, sticky="ew", pady=(16, 0))

    def _build_suggestions_section(self, parent: ttk.Frame) -> None:
        """Create the suggestions and warnings panel."""
        self._suggestions_panel = SuggestionsPanel(parent)
        self._suggestions_panel.grid(
            row=3,
            column=1,
            sticky="nsew",
            padx=(14, 0),
            pady=(16, 0),
        )

    def _add_generator_checkbox(
        self,
        parent: ttk.Frame,
        row: int,
        text: str,
        variable: BooleanVar,
    ) -> None:
        """Add one generator option checkbox."""
        ttk.Checkbutton(
            parent,
            text=text,
            variable=variable,
        ).grid(row=row, column=0, sticky="w")

    def _handle_password_change(self, _event: object) -> None:
        """Analyze typed passwords and reset empty input."""
        if self._password_var.get():
            self._analyze_password()
        else:
            self._reset_results()

    def _toggle_password_visibility(self) -> None:
        """Switch the password field between hidden and visible text."""
        show_character = "" if self._show_password_var.get() else "*"
        self._password_entry.configure(show=show_character)

    def _analyze_password(self) -> None:
        """Analyze the current password and update the dashboard."""
        password = self._password_var.get()
        if not password:
            self._reset_results()
            return

        try:
            analysis = self._analyze_password_use_case.execute(password)
        except PasswordStrengthCheckerError as exc:
            messagebox.showerror("Analysis Error", str(exc))
            return

        self._display_analysis(analysis)

    def _display_analysis(self, analysis: PasswordAnalysisDTO) -> None:
        """Render password analysis values in the interface."""
        self._strength_meter.set_strength(analysis.score, analysis.strength_level)
        self._latest_analysis = analysis
        self._score_card.set_value(f"{analysis.score}/100")
        self._entropy_card.set_value(f"{analysis.entropy_bits:.2f} bits")
        
        # Format crack time with better text
        crack_time = self._format_crack_time_display(analysis.estimated_crack_time)
        self._crack_time_card.set_value(crack_time)

        # Display rules status
        self._suggestions_panel.set_rules_status(
            has_min_length=analysis.has_minimum_length,
            has_acceptable_length=analysis.has_acceptable_length,
            has_uppercase=analysis.has_uppercase,
            has_lowercase=analysis.has_lowercase,
            has_number=analysis.has_number,
            has_symbol=analysis.has_symbol,
            has_no_repeated=not analysis.has_repeated_characters,
            has_no_sequential=not analysis.has_sequential_characters,
            has_no_keyboard_patterns=not analysis.has_keyboard_patterns,
            has_no_dictionary_words=not analysis.has_dictionary_words,
            is_not_common=not analysis.is_common_password,
        )

    def _format_crack_time_display(self, crack_time: str) -> str:
        """Format crack time display with professional formatting."""
        if "years" in crack_time.lower():
            if "million" in crack_time.lower():
                parts = crack_time.split()
                if len(parts) >= 2:
                    try:
                        num = float(parts[0].replace(">", "").replace("≈", "").replace("+", "").strip())
                        return f"≈ {num} million yrs"
                    except ValueError:
                        pass
            elif "billion" in crack_time.lower():
                return "> 1 billion yrs"
        return crack_time

    def _generate_password(self) -> None:
        """Generate, display, and analyze a secure password."""
        try:
            generated = self._generate_password_use_case.execute(
                length=self._length_var.get(),
                include_uppercase=self._uppercase_var.get(),
                include_lowercase=self._lowercase_var.get(),
                include_numbers=self._numbers_var.get(),
                include_symbols=self._symbols_var.get(),
            )
        except PasswordStrengthCheckerError as exc:
            messagebox.showerror("Generation Error", str(exc))
            return

        self._password_var.set(generated.password)
        self._analyze_password()

    def _copy_password(self) -> None:
        """Copy the current password to the system clipboard and show feedback."""
        password = self._password_var.get()
        if not password:
            messagebox.showinfo("Copy Password", "No password to copy.")
            return

        self._root.clipboard_clear()
        self._root.clipboard_append(password)
        self._root.update_idletasks()
        
        # Show confirmation message
        messagebox.showinfo("Copy Password", "✓ Password copied to clipboard")

    def _export_report(self) -> None:
        """Export the latest password analysis as TXT, JSON, or CSV."""
        if self._latest_analysis is None:
            messagebox.showinfo("Export Report", "Analyze a password first.")
            return

        file_name = filedialog.asksaveasfilename(
            title="Export Password Analysis",
            defaultextension=".txt",
            filetypes=[
                ("Text report", "*.txt"),
                ("JSON report", "*.json"),
                ("CSV report", "*.csv"),
            ],
        )
        if not file_name:
            return

        try:
            self._report_exporter.export(self._latest_analysis, Path(file_name))
        except (OSError, ValueError) as exc:
            messagebox.showerror("Export Error", str(exc))
            return

        messagebox.showinfo("Export Report", "Report exported successfully.")

    def _clear_password(self) -> None:
        """Clear the password textbox and reset displayed results."""
        self._password_var.set("")
        self._reset_results()
        self._password_entry.focus_set()

    def _reset_results(self) -> None:
        """Reset all metric and suggestion widgets to their default state."""
        self._strength_meter.reset()
        self._score_card.set_value("-")
        self._entropy_card.set_value("-")
        self._crack_time_card.set_value("-")
        self._latest_analysis = None
        self._suggestions_panel.set_messages([])
