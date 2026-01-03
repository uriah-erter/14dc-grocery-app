"""
app_core.py

Core application logic for the Grocery List application.

This module contains the `GroceryList` class which is responsible for:
- Maintaining the in-memory list of `GroceryItem` objects
- CRUD operations (add, edit, remove, list, search)
- Persisting the list to disk as JSON
- Exporting a filtered "buy list" to a text file

Design note:
The CLI layer (user prompts/printing) should live in `app_launch.py`. This module
should focus on business logic and persistence.
"""

import os
import re
import uuid

import app.constants as constants
import app.utils as utils
from app.grocery_item import GroceryItem


class GroceryList:
    """Manage grocery list items, persistence, search, and export operations."""

    # -------------------------
    # Init / load
    # -------------------------

    def __init__(self) -> None:
        """Initialize paths, load the grocery list from disk (or create a new file)."""
        self.grocery_list_path = os.path.join(
            constants.EXPORT_PATH,
            f"{constants.GROCERY_LIST}.json",
        )
        self.grocery_list: list[GroceryItem] = []
        self.set_grocery_list()

    def set_grocery_list(self) -> list[GroceryItem]:
        """Load the grocery list from disk into memory.

        Creates the export directory if needed. If the JSON file does not exist,
        initializes an empty list and writes it to disk.

        Returns:
            The in-memory grocery list.
        """
        os.makedirs(constants.EXPORT_PATH, exist_ok=True)

        if os.path.exists(self.grocery_list_path):
            grocery_list = self.load_data()
        else:
            print("")
            print("** No JSON path found, creating JSON path **")
            grocery_list = []
            self.grocery_list = []
            self.save_data()

        self.grocery_list = grocery_list
        return self.grocery_list

    # -------------------------
    # Lookup helpers
    # -------------------------

    def get_index_from_id(self, item_id: int) -> int | None:
        """Return the index for a given item ID, or None if not found."""
        for index, item in enumerate(self.grocery_list):
            if item.id == item_id:
                return index
        return None

    def get_index_from_name(self, name: str) -> int | None:
        """Return the index of the first item with an exact matching name, or None."""
        for index, item in enumerate(self.grocery_list):
            if item.name == name:
                return index
        return None

    # -------------------------
    # CRUD
    # -------------------------

    def add_item(
        self,
        name: str,
        store: str,
        cost: float,
        amount: int,
        priority: int,
        buy: bool,
    ) -> None:
        """Create a new GroceryItem, append it to the list, and persist to disk."""
        unique_id = int(uuid.uuid4())

        grocery_item = GroceryItem()
        grocery_item.name = name
        grocery_item.store = store
        grocery_item.cost = cost
        grocery_item.amount = amount
        grocery_item.priority = priority
        grocery_item.buy = buy
        grocery_item.id = unique_id

        self.grocery_list.append(grocery_item)
        self.save_data()

    def remove_item(self, name: str, id: int) -> None:
        """Remove an item by its unique ID and persist changes."""
        # Note: removal is performed by `id`; `name` is only used for user-friendly messaging.
        index = self.get_index_from_id(id)
        if index is None:
            print(f"Could not remove '{name}': ID not found.")
            return

        self.grocery_list.pop(index)
        self.save_data()

    def edit_item(
        self,
        name: str | None = None,
        store: str | None = None,
        cost: float | None = None,
        amount: int | None = None,
        priority: int | None = None,
        buy: bool | None = None,
        id: int | None = None,
    ) -> None:
        """Update an existing item by ID.

        Any argument set to None means "keep the current value".
        """
        if id is None:
            print("Cannot edit item: missing id.")
            return

        index = self.get_index_from_id(id)
        if index is None:
            print("Cannot edit item: ID not found.")
            return

        current_item = self.grocery_list[index]

        if name is not None:
            current_item.name = name
        if store is not None:
            current_item.store = store
        if cost is not None:
            current_item.cost = cost
        if amount is not None:
            current_item.amount = amount
        if priority is not None:
            current_item.priority = priority

        # Use `is not None` so `False` is treated as a real update.
        if buy is not None:
            current_item.buy = buy

        self.save_data()

    # -------------------------
    # Search
    # -------------------------

    def search_item_name(self, search_item: str) -> list[GroceryItem]:
        """Return items whose names start with the search string (case-insensitive)."""
        matching_items: list[GroceryItem] = []
        pattern = rf"^{re.escape(search_item)}"

        for item in self.grocery_list:
            if re.match(pattern, item.name, re.IGNORECASE):
                matching_items.append(item)

        return matching_items

    # -------------------------
    # Display / export
    # -------------------------

    def list_items(self, grocery_list: list[GroceryItem] | None = None) -> None:
        """Print a formatted list of items to stdout."""
        if grocery_list is None:
            grocery_list = self.grocery_list

        print("")
        for match_num, item in enumerate(grocery_list, start=1):
            match_string = (
                f"{match_num}. "
                f"Name: {item.name}, "
                f"Store: {item.store}, "
                f"Cost: {item.cost}, "
                f"Amount: {item.amount}, "
                f"Priority: {item.priority}, "
                f"Buy: {item.buy}"
            )
            print(match_string)
        print("")

    def export_items(self, grocery_list: list[GroceryItem] | None = None) -> None:
        """Write items marked for purchase (buy=True) to the export text file."""
        if grocery_list is None:
            grocery_list = self.grocery_list

        buy_list = [item for item in grocery_list if item.buy is True]

        if not buy_list:
            print("No items to export.")
            return

        exported_list_file = os.path.join(
            constants.EXPORT_PATH, constants.EXPORT_LIST)

        with open(exported_list_file, "w") as file:
            file.write("\n** Grocery List Export ** \n\n")

            for match_num, item in enumerate(buy_list, start=1):
                match_string = (
                    f"Item {match_num} "
                    f"| Name: {item.name} "
                    f"| Store: {item.store} "
                    f"| Cost: {item.cost} "
                    f"| Amount: {item.amount} "
                    f"| Priority: {item.priority} "
                    f"| Buy: {item.buy}"
                )
                print(match_string)
                file.write(match_string + "\n")

            total_cost = self.calculate_total_cost(buy_list, round_cost=True)
            print(f"\nThe total cost is ${total_cost:.2f}\n")
            file.write(f"\nThe total cost is ${total_cost:.2f}\n")

        print(f"Grocery list exported to {exported_list_file}")

    # -------------------------
    # Persistence
    # -------------------------

    def save_data(self) -> None:
        """Persist the current grocery list to JSON.

        Note:
            This writes the internal/private fields produced by `vars(item)`.
            A future improvement is to add `GroceryItem.to_dict()`.
        """
        export_list = [vars(item) for item in self.grocery_list]
        utils.save_data(self.grocery_list_path, export_list)

    def load_data(self) -> list[GroceryItem]:
        """Load grocery list data from JSON and return GroceryItem objects.

        Normalizes legacy data:
        - Keys that start with an underscore (e.g. "_buy" -> "buy")
        - String booleans for buy ("True"/"False") into real bool values
        """
        grocery_list: list[GroceryItem] = []
        json_data = utils.load_data(self.grocery_list_path)

        for item_dict in json_data:
            grocery_item = GroceryItem()

            for key, value in item_dict.items():
                if isinstance(key, str) and key.startswith("_"):
                    key = key[1:]

                if key == "buy" and isinstance(value, str):
                    v = value.strip().lower()
                    if v in ("true", "yes", "y", "1"):
                        value = True
                    elif v in ("false", "no", "n", "0"):
                        value = False

                if hasattr(grocery_item, key):
                    setattr(grocery_item, key, value)

            grocery_list.append(grocery_item)

        return grocery_list

    # -------------------------
    # Utilities
    # -------------------------

    @staticmethod
    def calculate_total_cost(
        grocery_list: list[GroceryItem],
        round_cost: bool = False,
        tax: float = 0.0825,
    ) -> float:
        """Calculate total cost for a list of items."""
        total_cost = sum(item.amount * item.cost for item in grocery_list)

        if round_cost:
            total_cost = round(total_cost)

        if tax:
            total_cost += total_cost * tax

        return total_cost
