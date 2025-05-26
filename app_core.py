import re
import uuid


# Grocery list containing predefined items with attributes such as name, store, cost, amount, priority, and buy status.
grocery_list = [
    {'name': 'milk',
     'store': 'H.E.B.',
     'cost': 3.19,
     'amount': 1,
     'priority': 1,
     'buy': True,
     'id': 324148079480209640266124969462437015018
     },
    {'name': 'eggs',
     'store': 'H.E.B.',
     'cost': 6.09,
     'amount': 1,
     'priority': 1,
     'buy': True,
     'id': 197309914455992414179216031361480414011
     },
    {'name': 'cheese',
     'store': 'H.E.B.',
     'cost': 4.46,
     'amount': 1,
     'priority': 1,
     'buy': True,
     'id': 9479391863861648278192224790194635018
     },
    {'name': 'steak',
     'store': 'H.E.B.',
     'cost': 12.79, 
     'amount': 1,
     'priority': 1, 
     'buy': True,
     'id': 48600721663948687578776355804601712073
    },
    {'name': 'chicken',
     'store': 'H.E.B.',
     'cost': 13.59,
     'amount': 1,
     'priority': 1,
     'buy': True,
     'id': 314903496015975209550637873193073339410 
     },
     {'name': 'milk',
     'store': 'H.E.B.',
     'cost': 3.19,
     'amount': 1,
     'priority': 1,
     'buy': True,
     'id': 324148079480209640266124969462437015019
     }
]

def get_index_from_id(id):
    index = 0
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
    
    grocery_list.append(item)

def remove_item(name: str, id: int):
    """
    Removes an item from the grocery list by name.
    
    Args:
        id (int): Name of the item to remove.
    """
    index = get_index_from_id(id)
    grocery_list.pop(index)

def edit_item(
        name: str,
        store: str | None=None,
        cost: float | None=None,
        amount: int | None=None,
        priority: int | None=None,
        buy: bool | bool="skip",
        id: int | None=None
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
    old_item = grocery_list[index]

    if not name:
        name = old_item['name']

    if not store:
        store= old_item["store"]

    if not cost:
        cost= old_item["cost"]

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

    grocery_list[index] = item

def list_items():
    """
    Prints all items in the grocery list.
    """
    for item in grocery_list:
        item_without_id = {key: value for key, value in item.items() if key != "id"}  # Remove "id"
        print(item_without_id)

def export_items():
    """
    Exports items that need to be bought and calculates the total cost.
    """
    buy_list = [item for item in grocery_list if item['buy']]

    if buy_list:
        for item in buy_list:
            print(f"name: {item['name']} - store: {item['store']} - cost: ${item['cost']} - amount: {item['amount']} - priority: {item['priority']}")
        
        total_cost = calculate_total_cost(buy_list, round_cost=True)
        print(f'Total cost: ${total_cost:.2f}')

def search_item(name):
    """
    Searches for an item in the grocery list by name and prints its details.
    
    Args:
        name (str): Name of the item to search for.
    """
    index = get_index_from_name(name)
    
    if index is not None:
        item = grocery_list[index]        
        print(f"name: {item['name']} - store: {item['store']} - cost: ${item['cost']} - amount: {item['amount']} - priority: {item['priority']}")
    else:
        print('Item not found.')

def search_item_name(search_item):
    """Search for items in the grocery list based on a given keyword."""
    matching_items = []  # Initialize an empty list to store matches
    pattern = rf"^{search_item}"  # Create the search pattern
    
    for item in grocery_list:
        if re.match(pattern, item['name'], re.IGNORECASE):  # Use re.match with case insensitivity
            matching_items.append(item)  # Add matching items to the list
    
    return matching_items