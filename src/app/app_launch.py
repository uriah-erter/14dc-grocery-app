#!/usr/bin/env python3

"""
app_launch.py

Command-line interface (CLI) entry point for the Grocery List application.

This module is responsible for:
- Displaying the main menu
- Collecting user input for add/remove/edit/search/export actions
- Delegating all data operations to app_core.GroceryList
"""

import argparse

from . import app_core
from . import constants
from . import utils


class Launch:
    """CLI controller for interacting with the GroceryList application."""

    def __init__(self) -> None:
        """Initialize the CLI and create the GroceryList application instance."""
        self.grocery_app = app_core.GroceryList()

    def launch(self, mode="interactive") -> None:
        """
        Start the main CLI loop.

        The loop continues until the user enters the "quit" command.
        """
        if mode == "interactive":
            self.run_interactive()
        elif mode == "cli":
            print("Use CLI mode from main()")
        elif mode == "ui":
            pass
        else:
            print(f"Unknown mode: {mode}")

    def run_interactive(self):        
        print("")
        print(utils.get_line_delimiter())
        print("Welcome to the Grocery App List Manager!")
        print(utils.get_line_delimiter())

        while True:
            command = input(
                "\nEnter a command (add, remove, edit, list, export, search, or quit): "
            ).strip().lower()

            if command == "add":
                self.handle_add_command()
            elif command == "remove":
                self.handle_remove_command()
            elif command == "edit":
                self.handle_edit_command()
            elif command == "list":
                self.handle_list_command()
            elif command == "export":
                self.grocery_app.export_items()
            elif command == "search":
                self.handle_search_command()
            elif command == "quit":
                break
            else:
                print("Invalid command. Please try again.")

    def handle_add_command(self, args=None) -> None:
        if args:
            name = args.name
            store = args.store
            cost = args.cost
            amount = args.amount
            priority = args.priority
            buy = args.buy.lower() in constants.BUY_TRUE
        else:
            name, store, cost, amount, priority, buy = self.get_inputs()

        self.grocery_app.add_item(name=name, store=store, cost=cost, amount=amount, priority=priority, buy=buy)

        print(f"{name} was added to the grocery list.")
        utils.get_line_delimiter()


    def handle_remove_command(self) -> None:
        """
        Remove an item by name prefix.

        If multiple items match, prompt the user to choose which one.
        """
        name = input("\nEnter the item name to remove: ").strip()
        print("")

        matches = self.grocery_app.search_item_name(name)

        if not matches:
            print(f"I'm sorry, I could not find a match for '{name}'.")
            return

        if len(matches) > 1:
            for match_num, match in enumerate(matches, start=1):
                match_string = (
                    f"{match_num}. "
                    f"| Name: {match.name} "
                    f"| Store: {match.store} "
                    f"| Cost: {match.cost} "
                    f"| Amount: {match.amount} "
                    f"| Priority: {match.priority} "
                    f"| Buy: {match.buy}"
                )
                print(match_string)

            item_num = input(
                "\nPlease select the number you would like to remove: "
            ).strip()
            match_item = matches[int(item_num) - 1]

            self.grocery_app.remove_item(name, id=match_item.id)
            print("\nSelected item has been removed.")
            return

        match_item = matches[0]
        self.grocery_app.remove_item(name, id=match_item.id)
        print("That item has been removed.")

    def handle_edit_command(self) -> None:
        """
        Edit an existing item.

        - Searches by name prefix
        - If multiple matches exist, prompts the user to choose one
        - Collects edit inputs (blank keeps existing values)
        """
        target_item = input("\nWhat item would you like to edit: ").strip()
        print("\nRetrieving your matching items...\n")

        matches = self.grocery_app.search_item_name(target_item)

        if not matches:
            print(f"\nI'm sorry, I could not find a match for '{target_item}'.\n")
            return

        if len(matches) > 1:
            for match_num, match in enumerate(matches, start=1):
                print(
                    f"{match_num}. "
                    f"| name: {match.name} "
                    f"| store: {match.store} "
                    f"| cost: {match.cost} "
                    f"| amount: {match.amount} "
                    f"| priority: {match.priority} "
                    f"| buy: {match.buy}"
                )

            item_num = input(
                "\nPlease select the number you would like to edit: "
            ).strip()
            match_item = matches[int(item_num) - 1]
        else:
            match_item = matches[0]

        name, store, cost, amount, priority, buy = self.get_inputs_edit()

        self.grocery_app.edit_item(
            name,
            store,
            cost,
            amount,
            priority,
            buy,
            id=match_item.id,
        )
    def handle_list_command(self):
        self.grocery_app.list_items(self.grocery_app.grocery_list)

    def handle_search_command(self) -> None:
        """Search for items by name prefix and print matching results."""
        search_keyword = input(
            "\nWhat is the name of the item you would like to search? "
        ).strip()
        matches = self.grocery_app.search_item_name(search_keyword)
        print("")

        if matches:
            for match_num, match in enumerate(matches, start=1):
                match_string = (
                    f"{match_num}. "
                    f"| name: {match.name} "
                    f"| store: {match.store} "
                    f"| cost: {match.cost} "
                    f"| amount: {match.amount} "
                    f"| priority: {match.priority} "
                    f"| buy: {match.buy}"
                )
                print(match_string)
        else:
            print("No items match the provided search keyword.")

        print(utils.get_line_delimiter())

    # ----------------------------
    # Input helpers (ADD workflow)
    # ----------------------------

    def get_inputs(self):
        """
        Collect inputs for adding a new item.

        This method applies defaults when the user leaves a field blank.
        """
        name = self.get_name_input()
        print(utils.get_line_delimiter())
        print("")

        store = self.get_store_input()
        print(utils.get_line_delimiter())
        print("")

        cost = self.get_cost_input()
        print(utils.get_line_delimiter())
        print("")

        amount = self.get_amount_input()
        print(utils.get_line_delimiter())
        print("")

        priority = self.get_priority_input()
        print(utils.get_line_delimiter())
        print("")

        buy = self.get_buy_input()
        print(utils.get_line_delimiter())
        print("")

        return name, store, cost, amount, priority, buy

    @staticmethod
    def get_name_input() -> str:
        """Get item name for ADD. Blank input uses NAME_DEFAULT."""
        print("Enter a name for the item. (ex. Ice Cream)")
        name = input("Item name: ").strip()
        return name if name else constants.NAME_DEFAULT

    @staticmethod
    def get_store_input() -> str:
        """
        Get store name for ADD.

        - 'skip' returns an empty string
        - blank input uses STORE_DEFAULT
        """
        print("Enter the name of the store for the item. (ex. Walmart)")
        store = input("Store name (or 'skip' to leave blank): ").strip()

        if store.lower() == "skip":
            return ""

        return store if store else constants.STORE_DEFAULT

    @staticmethod
    def get_cost_input() -> float:
        """Get item cost for ADD. Blank input uses COST_DEFAULT."""
        print("Enter the cost of the item. (ex. 5.25)")
        while True:
            cost = input("Item price: ").strip()

            if not cost:
                return constants.COST_DEFAULT

            try:
                return float(cost)
            except ValueError:
                print("Invalid input. Please enter a valid price.")

    @staticmethod
    def get_amount_input() -> int:
        """Get item amount for ADD. Blank input uses AMOUNT_DEFAULT."""
        print("Enter the amount you need to get. (ex. 5)")
        while True:
            amount = input("Item quantity: ").strip()

            if not amount:
                return constants.AMOUNT_DEFAULT

            try:
                amount_int = int(amount)
                if amount_int > 0:
                    return amount_int
                print("Quantity must be a positive number.")
            except ValueError:
                print("Invalid input. Please enter a valid quantity.")

    @staticmethod
    def get_priority_input() -> int:
        """Get priority for ADD. Blank input uses PRIORITY_DEFAULT."""
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX

        print(f"Enter the priority for the item between {p_min}-{p_max}. (ex. 2)")
        while True:
            priority = input("Item priority: ").strip()

            if not priority:
                return constants.PRIORITY_DEFAULT

            try:
                priority_int = int(priority)
                if p_min <= priority_int <= p_max:
                    return priority_int
                print(f"Invalid input. Please enter a number between {p_min}-{p_max}.")
            except ValueError:
                print(f"Invalid input. Please enter a number between {p_min}-{p_max}.")

    @staticmethod
    def get_buy_input() -> bool:
        """Get buy flag for ADD. Blank input uses BUY_DEFAULT."""
        print("Enter if this item should be purchased now. (ex. yes)")
        while True:
            buy = input("Buy: ").strip().lower()

            if buy == "":
                return constants.BUY_DEFAULT
            if buy in constants.BUY_TRUE:
                return True
            if buy in constants.BUY_FALSE:
                return False

            print("Invalid input. Please enter true|yes OR false|no")

    # -----------------------------
    # Input helpers (EDIT workflow)
    # -----------------------------

    def get_inputs_edit(self):
        """
        Collect inputs for editing an existing item.

        Blank input returns None, which signals "keep the current value".
        """
        name = self.get_name_input_edit()
        print(utils.get_line_delimiter())
        print("")

        store = self.get_store_input_edit()
        print(utils.get_line_delimiter())
        print("")

        cost = self.get_cost_input_edit()
        print(utils.get_line_delimiter())
        print("")

        amount = self.get_amount_input_edit()
        print(utils.get_line_delimiter())
        print("")

        priority = self.get_priority_input_edit()
        print(utils.get_line_delimiter())
        print("")

        buy = self.get_buy_input_edit()
        print(utils.get_line_delimiter())
        print("")

        return name, store, cost, amount, priority, buy

    @staticmethod
    def get_name_input_edit():
        """Get item name for EDIT. Blank returns None (keep current)."""
        print("Enter a name for the item (press Enter to keep current).")
        name = input("Item name: ").strip()
        return None if name == "" else name

    @staticmethod
    def get_store_input_edit():
        """Get store name for EDIT. Blank returns None (keep current)."""
        print("Enter the store name (press Enter to keep current).")
        store = input("Store name: ").strip()
        return None if store == "" else store

    @staticmethod
    def get_cost_input_edit():
        """Get item cost for EDIT. Blank returns None (keep current)."""
        print("Enter the cost (press Enter to keep current).")
        while True:
            cost = input("Item price: ").strip()
            if cost == "":
                return None
            try:
                return float(cost)
            except ValueError:
                print("Invalid input. Please enter a valid price.")

    @staticmethod
    def get_amount_input_edit():
        """Get item amount for EDIT. Blank returns None (keep current)."""
        print("Enter the quantity (press Enter to keep current).")
        while True:
            amount = input("Item quantity: ").strip()
            if amount == "":
                return None
            try:
                amount_int = int(amount)
                if amount_int > 0:
                    return amount_int
                print("Quantity must be a positive number.")
            except ValueError:
                print("Invalid input. Please enter a valid quantity.")

    @staticmethod
    def get_priority_input_edit():
        """Get item priority for EDIT. Blank returns None (keep current)."""
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX
        print(f"Enter priority {p_min}-{p_max} (press Enter to keep current).")

        while True:
            priority = input("Item priority: ").strip()
            if priority == "":
                return None
            try:
                priority_int = int(priority)
                if p_min <= priority_int <= p_max:
                    return priority_int
                print(f"Must be between {p_min}-{p_max}.")
            except ValueError:
                print(f"Invalid input. Please enter a number between {p_min}-{p_max}.")

    @staticmethod
    def get_buy_input_edit():
        """Get buy flag for EDIT. Blank returns None (keep current)."""
        print("Enter buy yes/no (press Enter to keep current).")
        while True:
            buy = input("Buy: ").strip().lower()
            if buy == "":
                return None
            if buy in constants.BUY_TRUE:
                return True
            if buy in constants.BUY_FALSE:
                return False
            print("Invalid input. Please enter true|yes OR false|no")

def main():
    parser = argparse.ArgumentParser(description="Grocery App List Manager")
    parser.add_argument("--mode", choices=["cli", "ui", "interactive"], default="interactive", help="Choose how to run the app: cli, ui, or interactive (default).")

    subparser = parser.add_subparsers(dest="command")
    add_parser = subparser.add_parser("add", help="Add new item")
    add_parser.add_argument("--name", required=True, help="Item name")
    add_parser.add_argument("--store", default=constants.STORE_DEFAULT, help="Store name")
    add_parser.add_argument("--cost", type=float, default=constants.COST_DEFAULT, help="Item cost")
    add_parser.add_argument("--amount", type=int, default=constants.AMOUNT_DEFAULT, help="Quantity")
    add_parser.add_argument("--priority", type=int, default=constants.PRIORITY_DEFAULT, help="Priority (1-5)")
    add_parser.add_argument("--buy", type=str, default=str(constants.BUY_DEFAULT), help="Buy now? (yes/no)")
       
    add_parser = subparser.add_parser("remove", help="Remove an item")
    add_parser = subparser.add_parser("edit", help="Edit an item")
    add_parser = subparser.add_parser("list", help="List all items")
    add_parser = subparser.add_parser("export", help="Export 'buy' items")
    add_parser = subparser.add_parser("search", help="Search am item")

    args = parser.parse_args()
    app = Launch()

    if args.mode == "interactive":
        app.launch(mode="interactive")
    elif args.mode == "ui":
        app.launch(mode="ui")
    elif args.mode == "cli":
        if not args.command:
            print("Please provide a command (Like 'add', 'remove', 'edit', 'list', 'export', or 'search')")

    match args.command:
        case "add":
            app.handle_add_command(args)
        case "remove":
            app.handle_remove_command()
        case "edit":
            app.handle_edit_command()
        case "list":
            app.grocery_app.list_items(app.grocery_app.grocery_list)
        case "export":
            app.grocery_app.export_items()
        case "search":
            app.handle_search_command()


if __name__ == "__main__":
    main()