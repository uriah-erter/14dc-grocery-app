import os
import re
import uuid

import constants
import utils


def get_grocery_list():
    os.makedirs(constants.EXPORT_PATH, exist_ok=True)
    file_path = os.path.join(constants.EXPORT_PATH, f'{constants.GROCERY_LIST}.json')

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
    total_cost = sum(item['amount'] * item['cost'] for item in grocery_list)

    if round_cost:
        total_cost = round(total_cost)

    if tax:
        total_cost += total_cost * tax

    return total_cost


def get_index_from_name(name):
    index = 0
    grocery_list = get_grocery_list()

    for item in grocery_list:
        if item['name'] == name:
            return index
        else:
            index += 1


def add_item(name, store, cost, amount, priority, buy):
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
    file_path = os.path.join(constants.EXPORT_PATH, f'{constants.GROCERY_LIST}.json')

    utils.save_data(file_path, grocery_list)


def remove_item(name: str, id: int):
    index = get_index_from_id(id)
    grocery_list = get_grocery_list()
    grocery_list.pop(index)
    file_path = os.path.join(constants.EXPORT_PATH, f'{constants.GROCERY_LIST}.json')

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
    file_path = os.path.join(constants.EXPORT_PATH, f'{constants.GROCERY_LIST}.json')
    
    utils.save_data(file_path, grocery_list)


def list_items(grocery_list):
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
    buy_list = [item for item in grocery_list if item['buy']]

    if not buy_list:
        print("No items to export.")
        return

    file_path = os.path.join(constants.EXPORT_PATH, "export_grocery_list.txt")

    if utils.check_file_exists(file_path):
        print(
            f"\nWarning: '{constants.EXPORT_LIST}' already exists and will be overwritten.\n")

    user_input = input("Do you want to proceed? (yes/no): ").strip().lower()
    print('')

    if user_input not in ("yes", "y"):
        print("Export canceled.\n")
        return

    with open(file_path, "w") as file:
        file.write('\n** Grocery List Export ** \n\n')
        for match_num, item in enumerate(buy_list, start=1):
            match_string = (
                f"Item {match_num:<3} | Name: {item['name']:<10} | Store: {item['store']:<10} | "
                f"Cost: {item['cost']:<6} | Amount: {item['amount']:<3} | Priority: {item['priority']:<3}"
            )
            print(match_string)
            file.write(match_string + "\n")

        total_cost = calculate_total_cost(buy_list, round_cost=True)
        print(f"\nThe total cost is ${total_cost:.2f}\n")
        file.write(f"\nThe total cost is ${total_cost:.2f}\n")

    print(f"Grocery list exported to {file_path}")


def search_item_name(search_item):
    matching_items = []
    pattern = rf"^{search_item}"
    grocery_list = get_grocery_list()

    for item in grocery_list:
        if re.match(pattern, item['name'], re.IGNORECASE):
            matching_items.append(item)  # Add matching items to the list

    return matching_items
