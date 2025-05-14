# Grocery list containing predefined items with attributes such as name, store, cost, amount, priority, and buy status.
grocery_list = [
    {'name': 'milk', 'store': 'H.E.B.', 'cost': 3.19, 'amount': 1, 'priority': 1, 'buy': True},
    {'name': 'eggs', 'store': 'H.E.B.', 'cost': 6.09, 'amount': 1, 'priority': 1, 'buy': True},
    {'name': 'cheese', 'store': 'H.E.B.', 'cost': 4.46, 'amount': 1, 'priority': 1, 'buy': True},
    {'name': 'steak', 'store': 'H.E.B.', 'cost': 12.79, 'amount': 1, 'priority': 1, 'buy': True},
    {'name': 'chicken', 'store': 'H.E.B.', 'cost': 13.59, 'amount': 1, 'priority': 1, 'buy': True},
    {'name': 'chips', 'store': 'H.E.B.', 'cost': 3.72, 'amount': 1, 'priority': 2, 'buy': False},
    {'name': 'soda', 'store': 'H.E.B.', 'cost': 7.99, 'amount': 1, 'priority': 2, 'buy': False},
    {'name': 'candy', 'store': 'H.E.B.', 'cost': 9.19, 'amount': 1, 'priority': 3, 'buy': False}
]

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
        name (str): Name of the item to search for.
    
    Returns:
        int or None: Index of the item if found, otherwise None.
    """
    for index, item in enumerate(grocery_list):
        if item['name'] == name:
            return index
    return None  # Handle cases where item is not found

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
    """
    item = {'name': name, 'store': store, 'cost': cost, 'amount': amount, 'priority': priority, 'buy': buy}
    grocery_list.append(item)

def remove_item(name):
    """
    Removes an item from the grocery list by name.
    
    Args:
        name (str): Name of the item to remove.
    """
    index = get_index_from_name(name)
    if index is not None:
        grocery_list.pop(index)
    else:
        print("Item not found.")

def edit_item(name, store=None, cost=None, amount=None, priority=None, buy="skip"):
    """
    Edits an existing item in the grocery list.
    
    Args:
        name (str): Name of the item to edit.
        store (str, optional): New store name.
        cost (float, optional): New cost.
        amount (int, optional): New quantity.
        priority (int, optional): New priority level.
        buy (bool or str, optional): Whether the item is marked to buy. Defaults to "skip".
    """
    index = get_index_from_name(name)
    if index is None:
        print("Item not found.")
        return  # Exit if item not found
    
    old_item = grocery_list[index]

    grocery_list[index] = {
        "name": name,
        "store": store if store else old_item['store'],
        "cost": cost if cost else old_item['cost'],
        "amount": amount if amount else old_item['amount'],
        "priority": priority if priority else old_item['priority'],
        "buy": old_item['buy'] if buy == "skip" else buy
    }

def list_items():
    """
    Prints all items in the grocery list.
    """
    for item in grocery_list:
        print(item)

def export_items():
    """
    Exports items that need to be bought and calculates the total cost.
    """
    buy_list = [item for item in grocery_list if item['buy']]

    if buy_list:
        for item in buy_list:
            print(f"name: {item['name']} - store: {item['store']} - cost: ${item['cost']} - amount: {item['amount']} - priority: {item['priority']}")
        
        total_cost = calculate_total_cost(buy_list, round_cost=True)
        print(f'Total cost: ${total_cost}')

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
