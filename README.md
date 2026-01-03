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

```
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

### Clone the repository

```
git clone https://github.com/uriah-erter/14dc-grocery-app.git
cd 14dc-grocery-app
```

### Create and activate a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install the application

```
pip install -e .
```

This installs the `app` command as an executable entry point.

---

## Usage

### Interactive Mode (Default)

```
app
```

or:

```
app --mode interactive
```

Available commands:

```
add, remove, edit, list, search, export, quit
```

---

### CLI Mode (Non-interactive)

CLI mode allows direct execution of commands without prompts.

If `--mode cli` is provided without a subcommand, the help menu is displayed.

---

### Add an item

```
app --mode cli add   --name "Hot Dog"   --store "Costco"   --cost 1.50   --amount 2   --priority 1   --buy yes
```

Accepted values for `--buy`:

```
yes, no
true, false
y, n
1, 0
```

---

### List all items

```
app --mode cli list
```

---

### Search for items

```
app --mode cli search Ice Cream
```

---

### Remove an item

```
app --mode cli remove Hot Dog
```

---

### Edit an item

```
app --mode cli edit Chicken Breast --cost 5.99 --buy no
```

If multiple items match, the command will prompt for an `--id`.

---

## Multi-word Item Names

Multi-word item names work naturally in CLI commands:

```
app --mode cli remove Ice Cream
app --mode cli search Chicken Breast
app --mode cli edit Hot Dog --priority 2
```

Quoted strings are also supported.

---

## Environment Configuration

The application stores data in a configurable directory.

Set the location using an environment variable:

```
export GROCERY_APP_DATA_DIR="$HOME/.grocery_app"
```

This controls where:

- the grocery list JSON file is stored
- exported text files are written

---

## Data Persistence

- Grocery items are stored as JSON on disk
- Items marked with `buy = True` are exported to a text file
- Legacy data is normalized automatically:
  - Private keys (e.g. `_name`) are converted
  - String booleans are converted to real booleans

---

## Design Notes

- `app_core.py` contains all business logic and persistence
- `app_launch.py` handles CLI interaction and argument parsing
- `grocery_item.py` enforces validation via property setters
- Static methods are used where instance state is not required
- Edit workflows use `None` to retain existing values

---

## Development Status

This project is actively developed as a learning and portfolio project with a
focus on:

- clean architecture
- readability
- correctness
- real-world Python practices

---

## License

This project is intended for educational and personal development purposes.
