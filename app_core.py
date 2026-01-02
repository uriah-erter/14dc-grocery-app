"""
app_core.py

Core application logic for the Grocery List CLI app.

Responsibilities:
- Maintain an in-memory list of GroceryItem objects
- Provide CRUD operations (add/remove/edit/list/search)
- Persist the list to disk as JSON
- Export a filtered "buy list" to a text file
"""

import os
import re
import uuid

import constants
import utils
from grocery_item import GroceryItem


class GroceryList:
    """Primary application class that manages grocery list operations."""

    def __init__(self) -> None:
        """Initialize paths, load existing list from disk (or create a new one)."""
        self.grocery_list_path = os.path.join(
            constants.EXPORT_PATH,
            f"{constants.GROCERY_LIST}.json",
        )
        self.grocery_list: list[GroceryItem] = []
        self.set_grocery_list()

    def set_grocery_list(self) -> list[GroceryItem]:
        """
        Ensure export directory exists and load the grocery list from disk.

        If the grocery list file does not exist yet, create an empty list and save it.
        Returns the in-memory grocery list.
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

    def get_index_from_id(self, item_id: int) -> int | None:
        """Return the index of the item with the given unique ID, or None if not found."""
        for index, item in enumerate(self.grocery_list):
            if item.id == item_id:
                return index
        return None

    def get_index_from_name(self, name: str) -> int | None:
        """Return the index of the first item matching the given name exactly, or None."""
        for index, item in enumerate(self.grocery_list):
            if item.name == name:
                return index
        return None

    @staticmethod
    def calculate_total_cost(
        grocery_list: list[object],
        round_cost: bool = False,
        tax: float = 0.0825,
    ) -> float:
        """
        Calculate the total cost of items in a list.

        Args:
            grocery_list: Items to total.
            round_cost: If True, rounds the subtotal before applying tax.
            tax: Tax rate (e.g., 0.0825 for 8.25%). Use 0 to disable.

        Returns:
            Total cost including tax (if tax > 0).
        """
        total_cost = sum(item.amount * item.cost for item in grocery_list)

        if round_cost:
            total_cost = round(total_cost)

        if tax:
            total_cost += total_cost * tax

        return total_cost

    def add_item(self, name, store, cost, amount, priority, buy) -> None:
        """Create and append a new GroceryItem to the list and persist it."""
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
        """Edit an existing item by ID. None values mean 'keep current'."""
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

        # Boolean must check for None so False can be applied.
        if buy is not None:
            current_item.buy = buy

        self.save_data()

    def list_items(self, grocery_list: list[GroceryItem]) -> None:
        """Print a formatted list of items to the console."""
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

    def export_items(self, grocery_list: list[GroceryItem]) -> None:
        """Export items marked for purchase (buy is True) to a text file."""
        buy_list = [item for item in grocery_list if item.buy is True]

        if not buy_list:
            print("No items to export.")
            return

        exported_list_file = os.path.join(constants.EXPORT_PATH, constants.EXPORT_LIST)

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

    def search_item_name(self, search_item: str) -> list[GroceryItem]:
        """Return items whose names start with the provided search string (case-insensitive)."""
        matching_items: list[GroceryItem] = []
        pattern = rf"^{re.escape(search_item)}"

        for item in self.grocery_list:
            if re.match(pattern, item.name, re.IGNORECASE):
                matching_items.append(item)

        return matching_items

    def save_data(self) -> None:
        """
        Persist the current grocery list to JSON.

        Note:
            This writes internal fields (e.g. _name). A cleaner approach is to
            add GroceryItem.to_dict() and use that.
        """
        export_list = [vars(item) for item in self.grocery_list]
        utils.save_data(self.grocery_list_path, export_list)

    def load_data(self) -> list[GroceryItem]:
        """
        Load grocery list data from JSON and convert entries into GroceryItem objects.

        Normalizes:
        - legacy keys that start with "_" (e.g. "_buy" -> "buy")
        - string booleans for buy ("True"/"False") into real bools
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