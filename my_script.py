# ** day_1 script_1 **
# print('Hello, world!')

# # ** day_2 Exercise 1: Calculation **
# milk = 3.19
# bread = 2.58
# eggs = 4.53

# total = milk + bread + eggs
# print(f'Your total is: ${total:.2f}')

# **************************************************************
# **************************************************************

# # ** day_2 Exercise 2: String Manipulation **
# store_name = input('What is your favorite grocery store? ')
# print(f'Welcome to {store_name}!')

# # ** day_2 Exercise 3: Common Errors
# milk = 3
# bread = 2.50
# total = milk + bread
# formatted_total = f'{total:.2f}'
# print("The total cost is: $" + str(formatted_total))

# **************************************************************
# **************************************************************

# # ** day_3 Exercise 1: Creating a Grocery List with Tuples
# apple_tuple = ('apples', 0.50, 5)
# orange_tuple = ('oranges', 0.35, 3)
# banana_tuple = ('bananas', 0.45, 6)

# grocery_list = []

# grocery_list.append(apple_tuple)
# grocery_list.append(orange_tuple)
# grocery_list.append(banana_tuple)

# for item in grocery_list:
#     total_cost = item[1] * item[2]
#     print(f'Total cost of {item[0]}: ${total_cost:.2f}')

# # ** day_3 Exercise 2: Working with Dictionaries
# grocery_list = [
#     {"name": "apples", "price": 0.50, "quantity": 5},
#     {"name": "oranges", "price": 0.35, "quantity": 3},
#     {"name": "bananas", "price": 0.45, "quantity": 6},
# ]

# for item in grocery_list:
#     total_cost = item['price'] * item['quantity']
#     item['total_cost'] = f'{total_cost:.2f}'
#     print(f'Total cost of {item['name']}: ${total_cost:.2f}')

# # ** day_3 Exercise 3: Slicing and Sorting a List
# num_list = [16, 47, 1, 3, 5, 9, 15, 2]

# print(num_list[2:])
# print(num_list[:4])
# print(num_list[-3])

# print(sorted(num_list))
# print(len(num_list))

# # ** day_3 Exercise 4: Sets Operations
# dairy = {'milk', 'butter', 'cream', 'yogurt', 'cheese'}
# deserts = {'jello', 'chocolate', 'candy', 'cookies', 'muffins'}

# dairy.add('ice_cream')
# deserts.add('ice_cream')

# print(f'\n{dairy}')
# print(f'{deserts}\n')

# dairy.remove('milk')
# deserts.remove('jello')

# print(f'\n{dairy}')
# print(f'{deserts}\n')

# print(dairy.intersection(deserts))

# **************************************************************
# **************************************************************

