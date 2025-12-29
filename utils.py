import json
import os


def save_data(file_path: str, data: list) -> None:
    if not data:
        data = []

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    except (IOError, TypeError) as e:
        print(f"Error saving data: {e}")


def load_data(file_path: str) -> list:
    data = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading data: {e}")
        return []


def check_file_exists(file_path):
    """
    Checks if a file exists at the given path.
    """
    return os.path.isfile(file_path)


def get_line_delimiter():
    delimiter = '-' * 69

    return delimiter
