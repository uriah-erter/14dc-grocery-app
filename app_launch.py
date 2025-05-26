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
            "\nEnter a command (add, remove, edit, list, export, search, or quit): "
        )

        if command == "add":

            # Add an item to the grocery list
            handle_add_command()

        elif command == "remove":

            # Remove an item from the grocery list
            handle_remove_command()

        elif command == "edit":
            
            # Edit an item in the grocery list
            handle_edit_command()

        elif command == "list":

            # Prints all the items in the grocery list
            handle_list_command()

        elif command == "export":

            # Prints items marked for 'buy' in the grocery list
            handle_export_command()

        elif command == "search":

            # Searches for items in the grocery list
            handle_search_command()

        elif command == "quit":
            break

def  handle_add_command():
    """
    Handles the logic triggered by the add command in command line mode.
    Adds an item to the grocery list.
    """
    print("\nEnter the following information:")
    
    # Get the inputs from the user
    name, store, cost, amount, priority, buy = get_inputs()

    # Add the item to the grocery list
    app_core.add_item(
        name=name,
        store=store,
        cost=cost,
        amount=amount,
        priority=priority,
        buy=buy    
    )
    print(f'Item was added to the grocery list.')

def handle_remove_command():
    name = input("\nEnter the item name to remove: ")
    matches = app_core.search_item_name(name)

    if not matches:
        print(f'\nI\'m sorry, I could not find a match for \'{name}.\'')

    elif len(matches) > 1:
        match_number = 1  

        for item in matches:
            item_without_id = {key: value for key, value in item.items() if key != 'id'}
            print(
                f"{match_number}: Name: {item_without_id['name']}, "
                f"Store: {item_without_id['store']}, Cost: ${item_without_id['cost']}, "
                f"Amount: {item_without_id['amount']}, Priority: {item_without_id['priority']}"
            )
            match_number += 1

        item_num = input('\nPlease select the number you would lke to remove: ')
        match_item = matches[int(item_num) - 1]

        index = app_core.get_index_from_id(id)  
        app_core.remove_item(name, id=match_item['id'])
        print('That item has been removed.\n')
        

    else:
        match_item = matches[0]
        index = app_core.get_index_from_id(id)
        app_core.remove_item(name, id=match_item['id'])
        print('That item has been removed.\n')

def handle_edit_command():
    target_item = input('\nWhat item would you like to edit: ')
    print("\nRetrieving your matching items...\n")
    matches = app_core.search_item_name(target_item)

    if not matches:
        print(f'\nI\'m sorry, I could not find a match for \'{edit_keyword}.\'\n')

    elif len(matches) > 1:
        match_number = 1

        for item in matches:
            item_without_id = {key: value for key, value in item.items() if key != 'id'}
            print(
                f"{match_number}: Name: {item_without_id['name']}, "
                f"Store: {item_without_id['store']}, Cost: ${item_without_id['cost']}, "
                f"Amount: {item_without_id['amount']}, Priority: {item_without_id['priority']}"
            )
            match_number += 1

        item_num = input('\nPlease select the number you would lke to edit: ')
        match_item = matches[int(item_num) - 1]

        name, store, cost, amount, priority, buy = get_inputs()
        index = app_core.get_index_from_id(id)
        app_core.edit_item(name, store, cost, amount, priority, buy, id=match_item['id'])
    
    else:
        match_item = matches[0]
        name, store, cost, amount, priority, buy = get_inputs()
        index = app_core.get_index_from_id(id)
        app_core.edit_item(name, store, cost, amount, priority, buy, id=match_item['id'])

def handle_list_command():
    print("\nThese are the current items in the grocery list.\n")
    print("Generating your list of items...\n")
    app_core.list_items()


def handle_export_command():
    print("\nThese are the current items marked to buy.")
    app_core.export_items()

def handle_search_command():
    """Prompt user for a search keyword and display matching items."""

    search_keyword = input("What is the name of the item you would like to search? ")
    print("\nSearching for matching items...\n")
    
    matches = app_core.search_item_name(search_keyword)  # Call search function

    if matches:
        print("These items match your search:\n")
        for item in matches:
            print(f"Name: {item['name']}")
            print(f"Store: {item['store']}")
            print(f"Cost: ${item['cost']:.2f}")
            print(f"Amount: {item['amount']}")
            print(f"Priority: {item['priority']}")
            print(f"Buy: {'Yes' if item['buy'] else 'No'}")
            print("-" * 30)  # Separator for readability
    else:
        print("No items match the provided search keyword.")


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
        name = input("item name: ").strip()

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
