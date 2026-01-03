"""
utils.py

Small utility functions used by the Grocery List application.
"""

import json
import os


def save_data(file_path: str, data: list) -> None:
    """
    Save a Python list to a JSON file.

    Args:
        file_path: Full path to the file to write.
        data: List of JSON-serializable objects.
    """
    # Ensure we always write a list to disk.
    if not data:
        data = []

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except (OSError, TypeError) as exc:
        print(f"Error saving data: {exc}")


def load_data(file_path: str) -> list:
    """
    Load JSON data from disk.

    Args:
        file_path: Full path to the file to read.

    Returns:
        A list loaded from JSON, or an empty list if loading fails.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error loading data: {exc}")
        return []


def check_file_exists(file_path: str) -> bool:
    """
    Check if a file exists at the given path.

    Args:
        file_path: Full path to the file.

    Returns:
        True if the file exists, otherwise False.
    """
    return os.path.isfile(file_path)


def get_line_delimiter(length: int = 69) -> str:
    """
    Return a horizontal line delimiter for CLI output.

    Args:
        length: Number of dashes to print.

    Returns:
        A string of '-' characters.
    """
    return "-" * length