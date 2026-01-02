import app_core
import constants
import utils

class Launch:
    def __init__(self):
        self.grocery_app = app_core.GroceryList()

    def launch(self):
        print('')
        print(utils.get_line_delimiter())
        print("Welcome to the Grocery List app! Let's make shopping easier.")
        print(utils.get_line_delimiter())

        while True:
            command = input(
                "\nEnter a command (add, remove, edit, list, export, search, or quit): ")

            if command == "add":
                self.handle_add_command()

            elif command == "remove":
                self.handle_remove_command()

            elif command == "edit":
                self.handle_edit_command()

            elif command == "list":
                self.grocery_app.list_items(self.grocery_app.grocery_list)

            elif command == "export":
                self.grocery_app.export_items(self.grocery_app.grocery_list)

            elif command == "search":
                self.handle_search_command()

            elif command == "quit":
                break


    def handle_add_command(self):
        print('')
        print(utils.get_line_delimiter())
        print("Enter the following information:\n")

        name, store, cost, amount, priority, buy = self.get_inputs()

        self.grocery_app.add_item(name=name, store=store, cost=cost, amount=amount,  priority=priority, buy=buy)
        print(f'\nItem was added to the grocery list.')


    def handle_remove_command(self):
        name = input("\nEnter the item name to remove: ")
        print('')
        matches = self.grocery_app.search_item_name(name)

        if not matches:
            print(f'I\'m sorry, I could not find a match for \'{name}.\'')

        elif len(matches) > 1:
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

            item_num = input('\nPlease select the number you would lke to remove: ')
            match_item = matches[int(item_num) - 1]
            
            self.grocery_app.remove_item(name, id=match_item.id)
            print(f'\nItem {match_num} has been removed.')

        else:
            match_item = matches[0]
            
            self.grocery_app.remove_item(name, id=match_item.id)
            print('That item has been removed.')


    def handle_edit_command(self):
        target_item = input('\nWhat item would you like to edit: ')
        print("\nRetrieving your matching items...\n")
        matches = self.grocery_app.search_item_name(target_item)

        if not matches:
            print(f'\nI\'m sorry, I could not find a match for \'{target_item}.\'\n')

        elif len(matches) > 1:
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

            item_num = input('\nPlease select the number you would like to edit: ')
            match_item = matches[int(item_num) - 1]

            name, store, cost, amount, priority, buy = self.get_inputs_edit()
            self.grocery_app.edit_item(name, store, cost, amount, priority, buy, id=match_item.id)

        else:
            match_item = matches[0]
            name, store, cost, amount, priority, buy = self.get_inputs_edit()
            self.grocery_app.edit_item(name, store, cost, amount, priority, buy, id=match_item.id)


    def handle_search_command(self):
        search_keyword = input("\nWhat is the name of the item you would like to search? ")
        matches = self.grocery_app.search_item_name(search_keyword)
        print('')

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


    def get_inputs(self):
        name = self.get_name_input()
        print(utils.get_line_delimiter())
        print('')

        store = self.get_store_input()
        print(utils.get_line_delimiter())
        print('')

        cost = self.get_cost_input()
        print(utils.get_line_delimiter())
        print('')

        amount = self.get_amount_input()
        print(utils.get_line_delimiter())
        print('')

        priority = self.get_priority_input()
        print(utils.get_line_delimiter())
        print('')

        buy = self.get_buy_input()
        print(utils.get_line_delimiter())
        print('')

        return name, store, cost, amount, priority, buy


    def get_name_input(self):
        print("Enter a name for the item. (ex. Ice Cream)")
        name = input("Item name: ").strip()
        
        if not name:
            name = constants.NAME_DEFAULT

        return name


    def get_store_input(self):
        print("Enter the name of the store for the item. (ex. Walmart)")
        store = input("Store name (or 'skip' to leave blank): ").strip()

        if not store:
            store = constants.STORE_DEFAULT

        return store


    def get_cost_input(self):
        print("Enter the cost of the item. (ex. 5.25)")

        while True:
            cost = input("Item price: ").strip()

            if not cost:
                cost = constants.COST_DEFAULT
                break

            try:
                cost = float(cost)
                break

            except ValueError:
                print("Invalid input. Please enter a valid price.")

        return cost


    def get_amount_input(self):
        print("Enter the amount you need to get. (ex. 5)")
        while True:
            amount = input("Item quantity: ").strip()

            if not amount:
                amount = constants.AMOUNT_DEFAULT
                break

            try:
                amount = int(amount)

                if amount > 0:
                    break

                print("Quantity must be a positive number.")

            except ValueError:
                print("Invalid input. Please enter a valid quantity.")

        return amount


    def get_priority_input(self):
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
                print(
                    f'Invalid input. Please enter a number between {p_min}-{p_max}.')

        return priority


    def get_buy_input(self):
        print("Enter if this item should be purchased now. (ex. yes)")

        while True:
            buy = input("Buy: ").strip().lower()

            if buy == "":
                return "skip"

            if buy in constants.BUY_TRUE:
                return True

            if buy in constants.BUY_FALSE:
                return False

            print("Invalid input. Please enter true|yes OR false|no")


    def get_inputs_edit(self):
        name = self.get_name_input_edit()
        print(utils.get_line_delimiter()); print("")

        store = self.get_store_input_edit()
        print(utils.get_line_delimiter()); print("")

        cost = self.get_cost_input_edit()
        print(utils.get_line_delimiter()); print("")

        amount = self.get_amount_input_edit()
        print(utils.get_line_delimiter()); print("")

        priority = self.get_priority_input_edit()
        print(utils.get_line_delimiter()); print("")

        buy = self.get_buy_input_edit()
        print(utils.get_line_delimiter()); print("")

        return name, store, cost, amount, priority, buy


    def get_name_input_edit(self):
        print("Enter a name for the item (press Enter to keep current).")
        name = input("Item name: ").strip()
        return None if name == "" else name


    def get_store_input_edit(self):
        print("Enter the store name (press Enter to keep current).")
        store = input("Store name: ").strip()
        return None if store == "" else store


    def get_cost_input_edit(self):
        print("Enter the cost (press Enter to keep current).")
        while True:
            cost = input("Item price: ").strip()
            if cost == "":
                return None
            try:
                return float(cost)
            except ValueError:
                print("Invalid input. Please enter a valid price.")


    def get_amount_input_edit(self):
        print("Enter the quantity (press Enter to keep current).")
        while True:
            amount = input("Item quantity: ").strip()
            if amount == "":
                return None
            try:
                amount = int(amount)
                if amount > 0:
                    return amount
                print("Quantity must be a positive number.")
            except ValueError:
                print("Invalid input. Please enter a valid quantity.")


    def get_priority_input_edit(self):
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX
        print(f"Enter priority {p_min}-{p_max} (press Enter to keep current).")

        while True:
            priority = input("Item priority: ").strip()
            if priority == "":
                return None
            try:
                priority = int(priority)
                if p_min <= priority <= p_max:
                    return priority
                print(f"Must be between {p_min}-{p_max}.")
            except ValueError:
                print(f"Invalid input. Please enter a number between {p_min}-{p_max}.")


    def get_buy_input_edit(self):
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

if __name__ == "__main__":
    app = Launch()
    app.launch()
