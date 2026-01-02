import os
import re
import uuid

import constants
import utils

from grocery_item import GroceryItem

class GroceryList:

    def __init__(self):
        self.grocery_list_path = os.path.join(constants.EXPORT_PATH, f'{constants.GROCERY_LIST}.json')
        self.grocery_list = []
        self.set_grocery_list()

    def set_grocery_list(self):
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

    # def set_grocery_list(self):
    #     os.makedirs(constants.EXPORT_PATH, exist_ok=True)

    #     if os.path.exists(self.grocery_list_path):
    #         grocery_list = self.load_data()

    #     else:
    #         print("")
    #         print("** No JSON path found, creating JSON path **")
    #         grocery_list = []
    #         self.save_data()

    #     self.set_grocery_list = grocery_list


    def get_index_from_id(self, id):
        index = 0
        grocery_list = self.grocery_list

        for item in grocery_list:
            if item.id == id:
                return index
            else:
                index += 1

    def get_index_from_name(self, name):
        index = 0
        grocery_list = self.grocery_list

        for item in grocery_list:
            if item.name == name:
                return index
            else:
                index += 1


    def calculate_total_cost(self, grocery_list: list[object], round_cost: bool = False, tax: float = 0.0825) -> float:
        total_cost = sum(item.amount * item.cost for item in grocery_list)

        if round_cost:
            total_cost = round(total_cost)

        if tax:
            total_cost += total_cost * tax

        return total_cost



    def add_item(self, name, store, cost, amount, priority, buy):
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


    def remove_item(self, name: str, id: int):
        index = self.get_index_from_id(id)

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
        id: int | None = None
    ) -> None:
        index = self.get_index_from_id(id)
        current_item = self.grocery_list[index]

        if name:
            current_item.name = name

        if store:
            current_item.store = store

        if cost:
            current_item.cost = cost

        if amount:
            current_item.amount = amount

        if priority:
            current_item.priority = priority

        if buy is not None:
            current_item.buy = buy

        if id:
            current_item.id = id
        
        self.save_data()


    def list_items(self, grocery_list):
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


    def export_items(self, grocery_list):
        buy_list = [item for item in grocery_list if item.buy]

        if not buy_list:
            print("No items to export.")
            return

        # self.list_items(buy_list)

        exported_list_file = os.path.join(constants.EXPORT_PATH, constants.EXPORT_LIST)

        with open(exported_list_file, "w") as file:
            file.write('\n** Grocery List Export ** \n\n')
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


    def search_item_name(self, search_item):
        matching_items = []
        pattern = rf"^{search_item}"
        grocery_list = self.grocery_list

        for item in grocery_list:
            if re.match(pattern, item.name, re.IGNORECASE):
                matching_items.append(item)  # Add matching items to the list

        return matching_items

    def save_data(self):
            export_list = []

            for item in self.grocery_list:
                export_list.append(vars(item))

            utils.save_data(self.grocery_list_path, export_list)

    def load_data(self):
            grocery_list = []
            json_data = utils.load_data(self.grocery_list_path)

            for item in json_data:
                grocery_item = GroceryItem()
                for key, value in item.items():

                    # Ensure attribute exists
                    if hasattr(grocery_item, key):
                        setattr(grocery_item, key, value)

                grocery_list.append(grocery_item)

            return grocery_list
