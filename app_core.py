import os
import re
import uuid
import constants
import utils


def get_grocery_list():
    os.makedirs(constants.EXPORT_PATH, exist_ok=True)
    file_path = os.path.join(constants.EXPORT_PATH,
                             f'{constants.GROCERY_LIST}.json')

    if os.path.exists(file_path):
        grocery_list = utils.load_data(file_path)

    else:
        print('No JSON path found, creating JSON path.')
        grocery_list = []
        utils.save_data(file_path, grocery_list)

    return grocery_list


def get_index_from_id(id):
    index = 0
    grocery_list = get_grocery_list()

    for item in grocery_list:
        if item['id'] == id:
            return index
        else:
            index += 1


def calculate_total_cost(grocery_list, round_cost=False, tax=0.0825):
    """
    Calculates the total cost of items in the grocery list, including tax.

    Args:
        grocery_list (list): List of grocery items.
        round_cost (bool): Whether to round the total cost.
        tax (float): Tax rate to apply to the total cost.

    Returns:
        float: The total cost including tax.
    """
    total_cost = sum(item['amount'] * item['cost'] for item in grocery_list)

    if round_cost:
        total_cost = round(total_cost)

    if tax:
        total_cost += total_cost * tax

    return total_cost  # Ensure the function returns the calculated total cost


def get_index_from_name(name):
    """
    Returns the index of an item in the grocery list based on its name.

    Args:
        name (str)): Name of the item to search for.

    Returns:
        int or None: Index of the item if found, otherwise None.
    """
    index = 0
    grocery_list = get_grocery_list()

    for item in grocery_list:
        if item['name'] == name:
            return index
        else:
            index += 1


def add_item(name, store, cost, amount, priority, buy):
    """
    Adds a new item to the grocery list.

    Args:
        name (str): Name of the item.
        store (str): Store where the item is purchased.
        cost (float): Price of the item.
        amount (int): Quantity of the item.
        priority (int): Priority level (1-5).
        buy (bool): Whether the item is marked to buy.
        id (int): Automatically generated.
    """

    # Generate a random UUID
    unique_id = int(uuid.uuid4())

    item = {'name': name,
            'store': store,
            'cost': cost,
            'amount': amount,
            'priority': priority,
            'buy': buy,
            'id': unique_id
            }

    grocery_list = get_grocery_list()
    grocery_list.append(item)

    file_path = os.path.join(constants.EXPORT_PATH,
                             f'{constants.GROCERY_LIST}.json')
    utils.save_data(file_path, grocery_list)


def remove_item(name: str, id: int):
    """
    Removes an item from the grocery list by name.

    Args:
        id (int): Name of the item to remove.
    """
    index = get_index_from_id(id)
    grocery_list = get_grocery_list()
    grocery_list.pop(index)

    file_path = os.path.join(constants.EXPORT_PATH,
                             f'{constants.GROCERY_LIST}.json')
    utils.save_data(file_path, grocery_list)


def edit_item(
        name: str,
        store: str | None = None,
        cost: float | None = None,
        amount: int | None = None,
        priority: int | None = None,
        buy: bool | bool = "skip",
        id: int | None = None
) -> None:
    """
    Edits an existing item in the grocery list.

    Args:
        name (str): The name of the item to edit.
        store (str | None): Updated store name. Defaults to None.
        cost (float | None): Updated cost. Defaults to None.
        amount (int | None): Updated amount. Defaults to None.
        priority (int | None): Updated priority. Defaults to None.
        buy (str | bool): Updated buy status. Defaults to "skip".
        id (str | None): Updated id.
    """
    index = get_index_from_id(id)
    old_item = get_grocery_list()

    if not name:
        name = old_item['name']

    if not store:
        store = old_item["store"]

    if not cost:
        cost = old_item["cost"]

    if not amount:
        amount = old_item["amount"]

    if not priority:
        priority = old_item["priority"]

    if buy == "skip":
        buy = old_item["buy"]

    if not id:
        id = old_item["id"]

    item = {
        "name": name,
        "store": store,
        "cost": cost,
        "amount": amount,
        "priority": priority,
        "buy": buy,
        "id": id
    }

    grocery_list = get_grocery_list()
    grocery_list[index] = item

    file_path = os.path.join(constants.EXPORT_PATH,
                             f'{constants.GROCERY_LIST}.json')
    utils.save_data(file_path, grocery_list)


def list_items(grocery_list):
    """
    Prints all items in the grocery list.
    """

    for match_num, item in enumerate(grocery_list, start=1):
        match_string = (
            f"{match_num}. "
            f"Name: {item["name"]}, "
            f"Store: {item["store"]}, "
            f"Cost: {item["cost"]}, "
            f"Amount: {item["amount"]}, "
            f"Priority: {item["priority"]}, "
            f"Buy: {item["buy"]}"
        )
        print(match_string)


def export_items(grocery_list):
    """
    Exports items that need to be bought, saves them to a file, and prints details to the screen.
    """
    buy_list = [item for item in grocery_list if item['buy']]

    if not buy_list:
        print("No items to export.")
        return

    file_path = os.path.join(constants.EXPORT_PATH, "export_grocery_list.txt")

    # Check if file already exists
    if utils.check_file_exists(file_path):
        print(
            f"\nWarning: '{constants.EXPORT_LIST}' already exists and will be overwritten.\n")

    # Ask for user confirmation
    user_input = input("Do you want to proceed? (yes/no): ").strip().lower()
    print('')

    if user_input not in ("yes", "y"):
        print("Export canceled.\n")
        return  # Exit the function if the user does not confirm

    with open(file_path, "w") as file:
        file.write('\n** Grocery List Export ** \n\n')
        for match_num, item in enumerate(buy_list, start=1):
            match_string = (
                f"Item {match_num:<3} | Name: {item['name']:<10} | Store: {item['store']:<10} | "
                f"Cost: {item['cost']:<6} | Amount: {item['amount']:<3} | Priority: {item['priority']:<3}"
            )
            print(match_string)  # Print each item to the screen
            file.write(match_string + "\n")  # Write to the file

        total_cost = calculate_total_cost(buy_list, round_cost=True)
        # Print total cost to screen
        print(f"\nThe total cost is ${total_cost:.2f}\n")
        # Write total cost to file
        file.write(f"\nThe total cost is ${total_cost:.2f}\n")

    print(f"Grocery list exported to {file_path}")


def search_item_name(search_item):
    """Search for items in the grocery list based on a given keyword."""
    matching_items = []  # Initialize an empty list to store matches
    pattern = rf"^{search_item}"  # Create the search pattern

    grocery_list = get_grocery_list()

    for item in grocery_list:
        # Use re.match with case insensitivity
        if re.match(pattern, item['name'], re.IGNORECASE):
            matching_items.append(item)  # Add matching items to the list

    return matching_items
