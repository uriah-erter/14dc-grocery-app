# Changelog

## [2.1.0] - 2026-01-01

### Added

- Introduced `@staticmethod` where appropriate across the codebase to clarify method intent and reduce unnecessary coupling to class instances.
- Added comprehensive docstrings and inline comments across all modules for improved readability and PEP 8 compliance.
- Added robust input handling for edit workflows, allowing users to press Enter to retain existing values.
- Added normalization logic when loading persisted JSON data to handle legacy keys (e.g. `_name` → `name`) and string boolean values.
- Added safer regex handling for search functionality using escaped user input.
- Added clearer separation of responsibilities between CLI (`app_launch.py`) and core logic (`app_core.py`).

### Changed

- Refactored `app_launch.py` input helper methods so that all methods not relying on instance state are static methods.
- Refactored `app_core.py` to improve validation logic and ensure booleans (`buy`) can correctly be set to `False`.
- Refactored `export_items` to write output to a dedicated export text file instead of overwriting the JSON persistence file.
- Refactored edit logic to use `None` as the sentinel value for “keep existing value” instead of string-based flags like `"skip"`.
- Refactored cost handling to preserve floating-point values instead of truncating to integers.
- Improved error handling and user feedback for invalid edits and missing item IDs.
- Standardized naming, formatting, and structure across all modules to align with PEP 8 best practices.

### Removed

- Removed unused imports and redundant logic discovered during refactoring.
- Removed implicit truthy checks that prevented valid boolean updates (e.g. explicitly setting `buy = False`).

---

## [2.0.0] - 2025-05-30

### Added

- Added export functionality to write grocery list data to disk.
- Added logging and basic persistence support.

---

## [1.1.0] - 2025-05-26

### Added

- Added `uuid` for unique item identification.
- Added `re` for flexible name-based search functionality.
- Refactored executable logic into discrete functions for improved maintainability.

---

## [1.0.0] - 2025-05-14

### Added

- `app_core.py`: Core functions to add, edit, list, search, and remove grocery list items.
- `app_launch.py`: Command-line interface to interact with grocery list functionality.

### Removed

- Removed `my_first_script.py` as functionality was consolidated into modular files.

---

## [0.3.0] - 2025-05-05

### Added

- Exercises focused on loops, conditional statements, and error handling.

---

## [0.2.0] - 2025-05-05

### Added

- Exercises for tuples, dictionaries, sets, and list slicing.

---

## [0.1.0] - 2025-05-04

### Initial Version

- Implemented core Python concepts including lists, tuples, dictionaries, and sets.
- Added initial changelog and versioning structure.
