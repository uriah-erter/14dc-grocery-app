#!/usr/bin/env python3
"""
app_launch.py

Command-line interface (CLI) for the Grocery List application.

This module is responsible for:
- Displaying the command prompt/menu
- Collecting and validating user input
- Printing user-facing messages

It delegates all business logic and persistence to `app_core.GroceryList`.
"""

import argparse

import app.app_core as app_core
import app.constants as constants
import app.utils as utils


class Launch:
    """CLI controller that routes user commands to the GroceryList core."""

    # -------------------------
    # Init / run modes
    # -------------------------

    def __init__(self) -> None:
        """Create the GroceryList core instance."""
        self.grocery_app = app_core.GroceryList()

    def launch(self, mode: str = "interactive") -> None:
        """Run the interactive CLI loop until the user quits."""
        if mode == "interactive":
            self.run_interactive()
        elif mode == "ui":
            # Placeholder for a future UI mode.
            pass
        else:
            print(f"Unknown mode: {mode}")

    def run_interactive(self) -> None:
        """Run the interactive prompt loop (input-driven mode)."""
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

    # -------------------------
    # Command handlers
    # -------------------------

    def handle_add_command(self, args: argparse.Namespace | None = None) -> None:
        """Prompt for item fields and add a new item."""
        if args:
            name = args.name
            store = args.store
            cost = args.cost
            amount = args.amount
            priority = args.priority

            buy = self._parse_buy_flag(str(args.buy))
            if buy is None:
                print("Invalid --buy value. Use yes/no/true/false (or y/n/1/0).")
                return
        else:
            name, store, cost, amount, priority, buy = self.get_inputs()

        self.grocery_app.add_item(
            name=name,
            store=store,
            cost=cost,
            amount=amount,
            priority=priority,
            buy=buy,
        )

        print(f"\n{name} was added to the grocery list.\n")
        utils.get_line_delimiter()

    def handle_remove_command(self, args: argparse.Namespace | None = None) -> None:
        """
        Remove an item by name prefix.

        If multiple items match, prompt the user to choose which one.
        """
        if args and getattr(args, "name", None):
            name = " ".join(args.name).strip() if isinstance(
                args.name, list) else str(args.name).strip()
        else:
            name = input("\nEnter the item name to remove: ").strip()

        print("")
        matches = self.grocery_app.search_item_name(name)

        if not matches:
            print(f"I'm sorry, I could not find a match for '{name}'.")
            return

        if len(matches) > 1:
            for match_num, match in enumerate(matches, start=1):
                print(
                    f"{match_num}. "
                    f"| Name: {match.name} "
                    f"| Store: {match.store} "
                    f"| Cost: {match.cost} "
                    f"| Amount: {match.amount} "
                    f"| Priority: {match.priority} "
                    f"| Buy: {match.buy}"
                )

            item_num = input(
                "\nPlease select the number you would like to remove: ").strip()
            match_item = matches[int(item_num) - 1]

            self.grocery_app.remove_item(name, id=match_item.id)
            print("\nSelected item has been removed.")
            return

        match_item = matches[0]
        self.grocery_app.remove_item(name, id=match_item.id)
        print("That item has been removed.\n")

    def handle_edit_command(self, args: argparse.Namespace | None = None) -> None:
        """
        Edit an existing item.

        Interactive mode:
        - Searches by name prefix
        - If multiple matches exist, prompts the user to choose one
        - Collects edit inputs (blank keeps existing values)

        CLI mode:
        - Accepts an item name (positional) and optional fields to update
        - If multiple items match, requires --id to disambiguate
        """
        # -----------------
        # CLI mode
        # -----------------
        if args is not None:
            raw_name = getattr(args, "name", None)
            if raw_name is None:
                print("Please provide an item name to edit.")
                return

            target_item = " ".join(raw_name).strip() if isinstance(
                raw_name, list) else str(raw_name).strip()
            matches = self.grocery_app.search_item_name(target_item)

            if not matches:
                print(
                    f"I'm sorry, I could not find a match for '{target_item}'.")
                return

            item_id = getattr(args, "id", None)
            if len(matches) > 1 and item_id is None:
                print(
                    f"Multiple items match '{target_item}'. Please rerun with --id to choose one:")
                for match_num, match in enumerate(matches, start=1):
                    print(
                        f"{match_num}. "
                        f"| id: {match.id} "
                        f"| name: {match.name} "
                        f"| store: {match.store} "
                        f"| cost: {match.cost} "
                        f"| amount: {match.amount} "
                        f"| priority: {match.priority} "
                        f"| buy: {match.buy}"
                    )
                return

            if item_id is not None:
                match_item = next(
                    (m for m in matches if m.id == item_id), None)
                if match_item is None:
                    print(
                        f"No match found for id={item_id} under '{target_item}'.")
                    return
            else:
                match_item = matches[0]

            name = getattr(args, "new_name", None)
            store = getattr(args, "store", None)
            cost = getattr(args, "cost", None)
            amount = getattr(args, "amount", None)
            priority = getattr(args, "priority", None)

            buy_raw = getattr(args, "buy", None)
            buy = None
            if buy_raw is not None:
                buy = self._parse_buy_flag(str(buy_raw))
                if buy is None:
                    print("Invalid --buy value. Use yes/no/true/false (or y/n/1/0).")
                    return

            self.grocery_app.edit_item(
                name=name,
                store=store,
                cost=cost,
                amount=amount,
                priority=priority,
                buy=buy,
                id=match_item.id,
            )
            print(f"\nUpdated item: {match_item.name} (id={match_item.id})\n")
            return

        # -----------------
        # Interactive mode
        # -----------------
        target_item = input("\nWhat item would you like to edit: ").strip()
        print("\nRetrieving your matching items...\n")

        matches = self.grocery_app.search_item_name(target_item)
        if not matches:
            print(
                f"\nI'm sorry, I could not find a match for '{target_item}'.\n")
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
                "\nPlease select the number you would like to edit: ").strip()
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

    def handle_list_command(self) -> None:
        """List all items currently in the grocery list."""
        self.grocery_app.list_items()

    def handle_search_command(self, args: argparse.Namespace | None = None) -> None:
        """Search for items by name prefix and print matching results."""
        if args and getattr(args, "query", None):
            search_keyword = " ".join(args.query).strip() if isinstance(
                args.query, list) else str(args.query).strip()
        else:
            search_keyword = input(
                "\nWhat is the name of the item you would like to search? ").strip()

        # Strip one pair of wrapping quotes (helpful in interactive mode)
        if (
            len(search_keyword) >= 2
            and (search_keyword[0] == search_keyword[-1])
            and search_keyword[0] in ('"', "'")
        ):
            search_keyword = search_keyword[1:-1].strip()

        matches = self.grocery_app.search_item_name(search_keyword)
        print("")

        if matches:
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
        else:
            print("No items match the provided search keyword.")

        print(utils.get_line_delimiter())

    # -------------------------
    # Small parsing helpers
    # -------------------------

    @staticmethod
    def _parse_buy_flag(value: str) -> bool | None:
        """Parse a buy flag string into a boolean (or None if invalid)."""
        if value is None:
            return None

        v = value.strip().lower()

        if v in constants.BUY_TRUE:
            return True
        if v in constants.BUY_FALSE:
            return False

        return None

    # ----------------------------
    # Input helpers (ADD workflow)
    # ----------------------------

    def get_inputs(self) -> tuple[str, str, float, int, int, bool]:
        """Collect add-workflow inputs (blank uses defaults)."""
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
        print("Enter a name for the item. (ex. Ice Cream)")
        name = input("Item name: ").strip()
        return name if name else constants.NAME_DEFAULT

    @staticmethod
    def get_store_input() -> str:
        print("Enter the name of the store for the item. (ex. Walmart)")
        store = input("Store name (or 'skip' to leave blank): ").strip()
        if store.lower() == "skip":
            return ""
        return store if store else constants.STORE_DEFAULT

    @staticmethod
    def get_cost_input() -> float:
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
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX

        print(
            f"Enter the priority for the item between {p_min}-{p_max}. (ex. 2)")
        while True:
            priority = input("Item priority: ").strip()
            if not priority:
                return constants.PRIORITY_DEFAULT
            try:
                priority_int = int(priority)
                if p_min <= priority_int <= p_max:
                    return priority_int
                print(
                    f"Invalid input. Please enter a number between {p_min}-{p_max}.")
            except ValueError:
                print(
                    f"Invalid input. Please enter a number between {p_min}-{p_max}.")

    @staticmethod
    def get_buy_input() -> bool:
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

    def get_inputs_edit(
        self,
    ) -> tuple[str | None, str | None, float | None, int | None, int | None, bool | None]:
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
    def get_name_input_edit() -> str | None:
        print("Enter a name for the item (press Enter to keep current).")
        name = input("Item name: ").strip()
        return None if name == "" else name

    @staticmethod
    def get_store_input_edit() -> str | None:
        print("Enter the store name (press Enter to keep current).")
        store = input("Store name: ").strip()
        return None if store == "" else store

    @staticmethod
    def get_cost_input_edit() -> float | None:
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
    def get_amount_input_edit() -> int | None:
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
    def get_priority_input_edit() -> int | None:
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
                print(
                    f"Invalid input. Please enter a number between {p_min}-{p_max}.")

    @staticmethod
    def get_buy_input_edit() -> bool | None:
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


def main() -> None:
    """Parse CLI arguments and route commands to the application."""
    parser = argparse.ArgumentParser(description="Grocery App List Manager")
    parser.add_argument(
        "--mode",
        choices=["cli", "ui", "interactive"],
        default="interactive",
        help="Choose how to run the app: cli, ui, or interactive (default).",
    )

    subparser = parser.add_subparsers(dest="command")

    add_parser = subparser.add_parser("add", help="Add new item")
    add_parser.add_argument("--name", required=True, help="Item name")
    add_parser.add_argument(
        "--store", default=constants.STORE_DEFAULT, help="Store name")
    add_parser.add_argument("--cost", type=float,
                            default=constants.COST_DEFAULT, help="Item cost")
    add_parser.add_argument("--amount", type=int,
                            default=constants.AMOUNT_DEFAULT, help="Quantity")
    add_parser.add_argument(
        "--priority", type=int, default=constants.PRIORITY_DEFAULT, help="Priority (1-5)")
    add_parser.add_argument(
        "--buy",
        default="yes" if constants.BUY_DEFAULT else "no",
        choices=(*constants.BUY_TRUE, *constants.BUY_FALSE),
        help="Buy flag (yes/no/true/false or y/n/1/0).",
    )

    remove_parser = subparser.add_parser("remove", help="Remove an item")
    remove_parser.add_argument(
        "name", nargs="+", help="Item name (or prefix) to remove")

    edit_parser = subparser.add_parser("edit", help="Edit an item")
    edit_parser.add_argument(
        "name", nargs="+", help="Item name (or prefix) to edit")
    edit_parser.add_argument("--id", type=int, default=None,
                             help="Item id to disambiguate when multiple items match")
    edit_parser.add_argument("--new-name", dest="new_name",
                             default=None, help="New name for the item (optional)")
    edit_parser.add_argument("--store", default=None,
                             help="New store name (optional)")
    edit_parser.add_argument("--cost", type=float,
                             default=None, help="New cost (optional)")
    edit_parser.add_argument("--amount", type=int,
                             default=None, help="New quantity (optional)")
    edit_parser.add_argument("--priority", type=int,
                             default=None, help="New priority 1-5 (optional)")
    edit_parser.add_argument(
        "--buy",
        default=None,
        choices=(*constants.BUY_TRUE, *constants.BUY_FALSE),
        help="Set buy flag (yes/no/true/false or y/n/1/0). Omit to keep current.",
    )

    subparser.add_parser("list", help="List all items")
    subparser.add_parser("export", help="Export 'buy' items")

    search_parser = subparser.add_parser("search", help="Search an item")
    search_parser.add_argument(
        "query",
        nargs="+",
        help="Search prefix for item name (positional). Use quotes for multi-word searches.",
    )

    args = parser.parse_args()
    app = Launch()

    # If user asked for CLI mode but didn't provide a subcommand, show help and quit.
    if args.mode == "cli" and not args.command:
        parser.print_help()
        return

    # If no subcommand was provided, run the selected app mode.
    if not args.command:
        app.launch(mode=args.mode)
        return

    # Otherwise, run the subcommand (CLI execution path).
    match args.command:
        case "add":
            app.handle_add_command(args)
        case "remove":
            app.handle_remove_command(args)
        case "edit":
            app.handle_edit_command(args)
        case "list":
            app.grocery_app.list_items()
        case "export":
            app.grocery_app.export_items()
        case "search":
            app.handle_search_command(args)


if __name__ == "__main__":
    main()
