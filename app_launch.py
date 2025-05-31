import app_core
import log_config
import constants
import utils


def launch():
    """
    Launches the Grocery List app and handles user commands in a loop.

    The user can add, remove, edit, list, export, search for items, or quit
    the application.
    """
    print('')
    print(utils.get_line_delimiter())
    print("Welcome to the Grocery List app! Let's make shopping easier.")
    print(utils.get_line_delimiter())

    while True:
        command = input("\nEnter a command (add, remove, edit, list, export, search, or quit): ")


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
            grocery_list = app_core.get_grocery_list()
            app_core.list_items(grocery_list)
            print(utils.get_line_delimiter())

        elif command == "export":
            grocery_list = app_core.get_grocery_list()      
            app_core.export_items(grocery_list)
            print(utils.get_line_delimiter())

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
    print('')
    print(utils.get_line_delimiter())
    print("Enter the following information:\n")
    
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
    print(f'\nItem was added to the grocery list.')

def handle_remove_command():
    name = input("\nEnter the item name to remove: ")
    print('')
    matches = app_core.search_item_name(name)

    if not matches:
        print(f'I\'m sorry, I could not find a match for \'{name}.\'')

    elif len(matches) > 1:
        for match_num, match in enumerate(matches, start=1):
            match_string = (
                f"{match_num}. "
                f"| Name: {match["name"]} "
                f"| Store: {match["store"]} "
                f"| Cost: {match["cost"]} "
                f"| Amount: {match["amount"]} "
                f"| Priority: {match["priority"]} "
                f"| Buy: {match["buy"]} |"
            )
            print(match_string)
    
        item_num = input('\nPlease select the number you would lke to remove: ')
        match_item = matches[int(item_num) - 1]
        app_core.remove_item(name, id=match_item['id'])
        print(f'\nItem {match_num} has been removed.')

    else:
        match_item = matches[0]
        app_core.remove_item(name, id=match_item['id'])
        print(f'That item has been removed.')

def handle_edit_command():
    target_item = input('\nWhat item would you like to edit: ')
    print("\nRetrieving your matching items...\n")
    matches = app_core.search_item_name(target_item)

    if not matches:
        print(f'\nI\'m sorry, I could not find a match for \'{target_item}.\'\n')

    elif len(matches) > 1:
        for match_num, match in enumerate(matches, start=1):
            match_string = (
                f"{match_num}. "
                f"| name: {match["name"]} "
                f"| store: {match["store"]} "
                f"| cost: {match["cost"]} "
                f"| amount: {match["amount"]} "
                f"| priority: {match["priority"]} "
                f"| buy: {match["buy"]}"
            )
            print(match_string)

        item_num = input('\nPlease select the number you would like to edit: ')
        match_item = matches[int(item_num) - 1]
        name, store, cost, amount, priority, buy = get_inputs()
        app_core.edit_item(name, store, cost, amount, priority, buy, id=match_item['id'])
    
    else:
        match_item = matches[0]
        name, store, cost, amount, priority, buy = get_inputs()
        app_core.edit_item(name, store, cost, amount, priority, buy, id=match_item['id'])

def handle_search_command():
    """Prompt user for a search keyword and display matching items."""

    search_keyword = input("\nWhat is the name of the item you would like to search? ")
    matches = app_core.search_item_name(search_keyword)  # Call search function
    print('')

    if matches:
        for match_num, match in enumerate(matches, start=1):
            match_string = (
                f"{match_num}. "
                f"| name: {match["name"]} "
                f"| store: {match["store"]} "
                f"| cost: {match["cost"]} "
                f"| amount: {match["amount"]} "
                f"| priority: {match["priority"]} "
                f"| buy: {match["buy"]}"
            )
            print(match_string)

    else:
        print("No items match the provided search keyword.")

    print(utils.get_line_delimiter())

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
    name = get_name_input()
    print(utils.get_line_delimiter())
    print('')

    store = get_store_input()
    print(utils.get_line_delimiter())
    print('')
    
    cost = get_cost_input()
    print(utils.get_line_delimiter())
    print('')
    
    amount = get_amount_input()
    print(utils.get_line_delimiter())
    print('')
    
    priority = get_priority_input()
    print(utils.get_line_delimiter())
    print('')
    
    buy = get_buy_input()
    print(utils.get_line_delimiter())
    print('')
    

    return name, store, cost, amount, priority, buy

def get_name_input():
    """
    Get the user input for the name attribute

    Returns:
        name (str): The name of the item
    """
    print("Enter a name for the item. (ex. Ice Cream)")

    # Get the name input
    name = input("Item name: ").strip()

    # No name provided, set to default
    if not name:
        name = constants.NAME_DEFAULT

    return name

def get_store_input():
    print("Enter the name of the store for the item. (ex. Walmart)")

    # Get the store input
    store = input("Store name (or 'skip' to leave blank): ").strip()

    # No store provided, set to default
    if not store:
        store = constants.STORE_DEFAULT

    return store

def get_cost_input():
    print("Enter the cost of the item. (ex. 5.25)")

    while True:
        # Get the cost input
        cost = input("Item price: ").strip()

        # No cost input provided, set to default
        if not cost:
            cost = constants.COST_DEFAULT
            break

        try:
            # Convert the cost to a float
            cost = float(cost)
            break

        # Unable to convert the cost to a float
        except ValueError:
            print("Invalid input. Please enter a valid price.")

    return cost

def get_amount_input():
    print("Enter the amount you need to get. (ex. 5)")
    while True:

        # Get the amount input
        amount = input(
            "Item quantity: "
            ).strip()
        
        # Amount not provided, set to default
        if not amount:
            amount = constants.AMOUNT_DEFAULT
            break

        try:
            # Convert the amount to an int
            amount = int(amount)

            # Amount must be at least 1
            if amount > 0:
                break

            print("Quantity must be a positive number.")

        # Unable to convert amount to an int
        except ValueError:
            print("Invalid input. Please enter a valid quantity.")

    return amount

def get_priority_input():
    p_min = constants.PRIORITY_MIN
    p_max = constants.PRIORITY_MAX

    print(f'Enter the priority for the item between {p_min}-{p_max}. (ex. 2)')

    while True:
        priority = input('Item priority: ').strip()

        if not priority:
            constants.PRIORITY_DEFAULT
            break
        try:
            priority = int(priority)

            if p_min <= priority <= p_max:
                break

        except ValueError:
            print(f'Invalid input. Please enter a number between {p_min}-{p_max}.')

    return priority

def get_priority_input():
    p_min = constants.PRIORITY_MIN
    p_max = constants.PRIORITY_MAX
    
    print(
        f"Enter the priority for the item between "
        f"{p_min}-{p_max}. (ex. 2)"
        )

    while True:
        # Get the priority input
        priority = input("Priority: ").strip()
        
        # No input provided, set to default
        if not priority:
            constants.PRIORITY_DEFAULT
            break

        try:
            # Convert the priority to an int
            priority = int(priority)

            # Check priority is within min to max
            if p_min <= priority <= p_max:
                break

        # Failed to convert priority to an int
        except ValueError:
            print(
                f"Invalid input. Please enter a number between "
                f"{p_min} and {p_max}."
                )

    return priority

def get_buy_input():
    print("Enter if this item should be purchased now. (ex. yes)")

    while True:
        # Get the buy input
        buy = input("Buy: ").strip().lower()

        # No buy input provided
        if not buy:
            buy = constants.BUY_DEFAULT
            break

        # Buy input is true
        if buy in constants.BUY_TRUE:
            buy = True
            break

        # Buy input is false
        elif buy in constants.BUY_FALSE:
            buy = False
            break

        # Buy input was not valid
        else:
            print(
                "Invalid input. Please enter true|yes OR false|no")

    return buy

if __name__ == "__main__":
    launch()
