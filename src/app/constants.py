"""
constants.py

Centralized configuration values for the Grocery List application.

This module contains:
- File paths and filenames
- Default values for GroceryItem fields
- Validation boundaries
- Accepted user input values
"""

import os

# -------------------------
# File system configuration
# -------------------------

# Directory where all grocery list data and exports are stored
EXPORT_PATH = os.environ.get(
    "GROCERY_APP_DATA_DIR",
    "/Users/uriah.erter/14dc_dev/grocery_app_list",
)

# Filename for the exported (buy-only) grocery list
EXPORT_LIST = "export_grocery_list.txt"

# Base filename (without extension) for the persistent grocery list JSON
GROCERY_LIST = "grocery_list"


# -------------------------
# GroceryItem default values
# -------------------------

# Default item name when user input is blank
NAME_DEFAULT = "unnamed item"

# Default store name when user input is blank
STORE_DEFAULT = "Kroger"

# Default item cost
COST_DEFAULT = 0.00

# Default quantity
AMOUNT_DEFAULT = 1

# Default priority value
PRIORITY_DEFAULT = 1


# -------------------------
# Validation constraints
# -------------------------

# Allowed priority range (inclusive)
PRIORITY_MIN = 1
PRIORITY_MAX = 5


# -------------------------
# Buy flag configuration
# -------------------------

# Default buy flag when user presses Enter
BUY_DEFAULT = True

# Accepted truthy user input (lowercase comparison)
BUY_TRUE = ("yes", "true")

# Accepted falsy user input (lowercase comparison)
BUY_FALSE = ("no", "false")


# -------------------------
# ID defaults
# -------------------------

# Default ID before a UUID-based ID is assigned
ID_DEFAULT = 0