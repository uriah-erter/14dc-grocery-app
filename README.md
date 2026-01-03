# Grocery List Application

A Python-based Grocery List manager that supports both **interactive** and
**command-line (CLI)** workflows. The application allows users to add, edit,
remove, search, list, and export grocery items with strong input validation and
persistent storage.

This project follows modern Python best practices, including a `src/` layout,
CLI entry points, and comprehensive documentation.

---

## Features

- Interactive menu-driven CLI
- Non-interactive CLI mode using arguments (`argparse`)
- Add, edit, remove, list, and search grocery items
- Export items marked for purchase to a formatted text file
- Persistent storage using JSON
- Input validation enforced via property-based data models
- Environment-variable configurable data directory
- Clear separation between CLI and core business logic
- Fully documented and PEP 8 / PEP 257 compliant

---

## Project Structure

```text
src/
└── app/
    ├── app_core.py       # Core business logic and persistence
    ├── app_launch.py     # CLI interface and argument parsing
    ├── grocery_item.py   # GroceryItem data model
    ├── constants.py      # Centralized configuration values
    ├── utils.py          # Shared utility functions
    ├── log_config.py     # Logging configuration
    └── __init__.py
```

---

## Installation

### Prerequisites

- Python 3.10+
- macOS or Linux (Windows should work with minor adjustments)

### 1. Clone the repository

```bash
git clone https://github.com/uriah-erter/14dc-grocery-app.git
cd 14dc-grocery-app
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the application in editable mode

```bash
pip install -e .
```

This installs the `app` command as an executable entry point.

---

## Usage

### Interactive Mode (Default)

```bash
app
```

or explicitly:

```bash
app --mode interactive
```

You will be prompted to enter commands such as:

```
add, remove, edit, list, search, export, quit
```

---

### CLI Mode (Non-interactive)

CLI mode allows commands to be executed directly without prompts.

#### Add an item

```bash
app --mode cli add \
  --name "Hot Dog" \
  --store "Costco" \
  --cost 1.50 \
  --amount 2 \
  --priority 1 \
  --buy yes
```

#### List all items

```bash
app --mode cli list
```

#### Export items marked for purchase

```bash
app --mode cli export
```

#### Search for items

```bash
app --mode cli search
```

---

## Environment Configuration

By default, data is stored in a local directory defined in `constants.py`.

You can override this location using an environment variable:

```bash
export GROCERY_APP_DATA_DIR="$HOME/.grocery_app"
```

This controls where:

- the grocery list JSON file is stored
- exported text files are written

---

## Data Persistence

- Grocery items are stored as JSON on disk
- Items marked with `buy = True` can be exported to a separate text file
- Legacy data formats are normalized automatically on load
  - Private keys (e.g. `_name`) are converted
  - String booleans are converted to real booleans

---

## Design Notes

- **`app_core.py`** contains all business logic and persistence
- **`app_launch.py`** handles user interaction and argument parsing
- **`grocery_item.py`** enforces validation via property setters
- Methods that do not rely on instance state are implemented as `@staticmethod`
- Edit workflows use `None` as a sentinel value to retain existing data

---

## Development Status

This project is actively developed as a learning and portfolio project, with an
emphasis on:

- clean architecture
- readability
- correctness
- real-world Python practices

---

## License

This project is intended for educational and personal development purposes.
