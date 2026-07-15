# Password Strength Checker

A professional Python 3.13+ Tkinter desktop application for analyzing password strength with entropy estimation, pattern detection, real-time feedback, and secure password generation.

## Overview

Password Strength Checker is a secure, offline password analysis tool built with clean architecture principles. It provides instant strength assessment, actionable feedback, and export options without logging or transmitting passwords.

## Features

### Password Analysis
- **Score:** 0-100 strength rating with five strength levels
- **Entropy calculation:** Estimates password randomness in bits
- **Crack time estimation:** Practical time-to-break guidance
- **Pattern detection:** Repeated sequences, sequential characters, keyboard walks, dictionary word detection, and common passwords
- **Rule feedback:** Clear pass/fail indicators for password requirements

### Password Generation
- **Configurable character sets:** Uppercase, lowercase, numbers, symbols
- **Length range:** 12-128 characters
- **Secure randomness:** Uses Python's `secrets` module
- **Auto-analysis:** Generated passwords are evaluated immediately

### User Experience
- **Real-time results:** Updates as you type
- **Visual strength bar:** Color-coded progress indicator
- **Clipboard support:** Copy with one click
- **Keyboard shortcuts:** Analyze, generate, and navigate quickly
- **Responsive layout:** Adjusts to the window size

### Export & Reporting
- **Multi-format exports:** TXT, JSON, CSV
- **Privacy-first:** Exports exclude the password unless explicitly chosen

## Screenshots

> [Screenshots would be displayed here in a real published version]

The interface includes:
- Password input and analysis panel
- Strength score and entropy cards
- Crack time estimate
- Password generator controls
- Rule-by-rule feedback list

## Project Structure

```
password-strength-checker/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── docs/
│   ├── architecture.md
│   ├── threat_model.md
│   └── screenshots/
├── src/
│   └── password_strength_checker/
├── tests/
│   ├── unit/
│   └── integration/
└── resources/
    └── common_passwords.txt
```

## Installation

### Prerequisites
- Python 3.13+ ([Download](https://www.python.org/downloads/))
- pip (included with Python)

### Setup

1. Clone the repository:
   ```bash
   cd password-strength-checker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the application in editable mode:
   ```bash
   pip install -e .
   ```

4. Install development dependencies (optional):
   ```bash
   pip install -r requirements-dev.txt
   ```

## Usage

### Start the application

```bash
python -m password_strength_checker.main
```

### Basic workflow

1. Enter a password in the input field
2. Press `Enter` or click **Analyze**
3. Review the strength score, entropy, and crack time
4. Generate a secure password with character options
5. Export the analysis as TXT, JSON, or CSV

### Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Analyze current password |
| `Ctrl+C` | Copy password to clipboard |
| `Ctrl+G` | Generate new password |
| `Tab` | Navigate between controls |

## Technologies Used

- Python 3.13
- Tkinter
- pytest
- ruff
- mypy
- Python standard library modules: `pathlib`, `dataclasses`, `typing`, `logging`, `csv`, `json`

## Future Improvements

- Multi-language UI
- Theme customization
- Password policy templates
- Advanced export workflows
- Additional pattern analysis rules

## License

MIT License - see [LICENSE](LICENSE) for details.
