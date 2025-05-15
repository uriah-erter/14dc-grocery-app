import app_core


def launch():
    """
    Launches the Grocery List app and handles user commands in a loop.

    The user can add, remove, edit, list, export, search for items, or quit
    the application.
    """
    print("\nWelcome to the Grocery List app! Let's make shopping easier.")

    while True:
        command = input(
            "\nEnter a command (add, remove, edit, list, export, " "search, quit): "
        )

        if command == "add":
            print(
                "\nEnter the following information. After entering the name, "
                'enter the rest of the information or type "skip" to skip '
                "any of the remaining fields."
            )
            name, store, cost, amount, priority, buy = get_inputs()
            app_core.add_item(
                name=name,
                store=store,
                cost=cost,
                amount=amount,
                priority=priority,
                buy=buy,
            )

        elif command == "remove":
            name = input("\nEnter the item name to remove: ")
            app_core.remove_item(name)

        elif command == "edit":
            print("\nEnter the name of the item you want to edit.")
            name, store, cost, amount, priority, buy = get_inputs()
            app_core.edit_item(name, store, cost, amount, priority, buy)

        elif command == "list":
            print("\nThese are the current items in the grocery list.\n")
            app_core.list_items()

        elif command == "export":
            print("\nThese are the current items marked to buy.")
            app_core.export_items()

        elif command == "search":
            name = input("\nEnter the item name to search: ")
            app_core.search_item(name)

        elif command == "quit":
            break


def get_inputs():
    """
    Collects user input for a grocery item, allowing optional skipping of fields.

    Returns:
        tuple: (name, store, cost, amount, priority, buy) where:
            - name (str): Name of the item (required).
            - store (str or None): Store name (optional).
            - cost (float or None): Price of the item (optional).
            - amount (int or None): Quantity of the item (optional).
            - priority (int or None): Priority level (1-5) (optional).
            - buy (bool or None): Whether the item is marked to buy (optional).
    """

    while True:
        name = input("item name: ")

        if name:
            break

        print("Invalid input. Please enter a valid item.")

    while True:
        store = input("store name: ")

        if store == "skip":
            store = None
            break

        elif store:
            break

        print('Invalid input. Please enter a valid item or enter "skip" to ' "skip.")

    while True:
        try:
            cost = input("item price: ")

            if cost == "skip":
                cost = None
                break

            elif cost:
                cost = float(cost)
                break
        except ValueError:
            print(
                'Invalid input. Please enter a valid price or enter "skip" ' "to skip."
            )

    while True:
        try:
            amount = input("item quantity: ")

            if amount == "skip":
                amount = None
                break

            elif int(amount) > 0:
                amount = int(amount)
                break

            else:
                print("Quantity must be a positive number.")

        except ValueError:
            print(
                'Invalid input. Please enter a valid quantity or enter "skip" '
                "to skip."
            )

    while True:
        try:
            priority = input("item priority (1-5): ")
            if priority == "skip":
                priority = None
                break

            elif 1 <= int(priority) <= 5:
                priority = int(priority)
                break

            else:
                print("Priority must be between 1 and 5.")

        except ValueError:
            print(
                'Invalid input. Please enter a valid priority or enter "skip" '
                "to skip."
            )

    while True:
        try:
            buy = input("buy (yes/no): ")

            if buy.lower() == "yes":
                buy = True
                break

            elif buy.lower() == "no":
                buy = False
                break

            elif buy == "skip":
                buy = None
                break

            else:
                print("Invalid input. Please enter yes or no.")

        except ValueError:
            print('Invalid input. Please enter yes or no or enter "skip" to ' "skip.")

    return name, store, cost, amount, priority, buy


if __name__ == "__main__":
    launch()
