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

# # ** day_4 Exercise 1: Grocery Item Categorization Using Conditional Statements
# food_items = ['apple', 'bread', 'milk']
# non_food_items = ['soap', 'detergent', 'paper towel']

# grocery_item = input('Please add an item: ')

# if grocery_item in food_items:
#     print('Food item')

# elif grocery_item in non_food_items:
#     print('Non-food Item')

# else:
#     print('Unknown Item')

# **************************************************************
# **************************************************************

# # ** day_4 Exercise 2: GMaking a Burger with a While Loop
# items_list = [
#     {'name':'fries', 'cost':6.25, 'amount':1},
#     {'name':'burger patties', 'cost':13.50, 'amount':1},
#     {'name':'burger buns', 'cost':3.50, 'amount':2},
#     {'name':'tomato', 'cost':1.50, 'amount':2},
#     {'name':'lettuce', 'cost':5, 'amount':1},
#     {'name':'Ketchup', 'cost':3.47, 'amount':1},
#     {'name':'pickles', 'cost':4.25, 'amount':1}
# ]

# shopping_list = []

# budget = 27.50
# total_cost = 0
# index = 0

# while total_cost <= budget:
#     item = items_list[index]
#     shopping_list.append(item['name'])
#     total_cost += item['cost'] * item['amount']
#     index += 1
        
# print(f'\nExpected output: {shopping_list}\n')

# **************************************************************
# **************************************************************

# # ** day_4 Exercise 3: Extending Logic with Nesting
# items_list = [
#     {'name':'fries', 'cost':6.25, 'amount':1},
#     {'name':'burger patties', 'cost':13.50, 'amount':1},
#     {'name':'burger buns', 'cost':3.50, 'amount':2},
#     {'name':'tomato', 'cost':1.50, 'amount':2},
#     {'name':'lettuce', 'cost':5, 'amount':1},
#     {'name':'Ketchup', 'cost':3.47, 'amount':1},
#     {'name':'pickles', 'cost':4.25, 'amount':1}
# ]

# shopping_list = []

# budget = 27.50
# total_cost = 0
# index = 0

# print('\n')
# while total_cost <= budget:
#     item = items_list[index]
#     shopping_list.append(item['name'])
#     total_cost += item['cost'] * item['amount']
#     index += 1
    
#     for i in shopping_list:
#         print(i)
        
#     print('----------') 
        
    
# print(f'{shopping_list}\n')

# **************************************************************
# **************************************************************

# # ** day_4 Exercise 4: Breaking the Loop
# items_list = [
#     {'name':'fries', 'cost':6.25, 'amount':1},
#     {'name':'burger patties', 'cost':13.50, 'amount':1},
#     {'name':'burger buns', 'cost':3.50, 'amount':2},
#     {'name':'tomato', 'cost':1.50, 'amount':2},
#     {'name':'lettuce', 'cost':5, 'amount':1},
#     {'name':'Ketchup', 'cost':3.47, 'amount':1},
#     {'name':'pickles', 'cost':4.25, 'amount':1}
# ]

# shopping_list = []

# budget = 27.50
# total_cost = 0
# index = 0

# print('\n')
# while total_cost <= budget:
#     item = items_list[index]
#     shopping_list.append(item['name'])
#     total_cost += item['cost'] * item['amount']
#     index += 1
    
#     for i in shopping_list:
#         print(i)
        
#     print('----------')
    
#     if 'fries' in shopping_list and 'burger patties' in shopping_list and 'burger buns' in shopping_list:
#         print(f'We can make burgers and fries for ${total_cost}!')
#         break
    
# print(f'{shopping_list}\n')

# **************************************************************
# **************************************************************

# # ** day_4 Exercise 5: Error Handling with Try-Except
# items_list = [
#     {'name':'fries', 'cost':6.25, 'amount':1},
#     {'name':'burger patties', 'cost':13.50, 'amount':1},
#     {'name':'burger buns', 'cost':3.50, 'amount':2},
#     {'name':'tomato', 'cost':1.50, 'amount':2},
#     {'name':'lettuce', 'cost':5, 'amount':1},
#     {'name':'Ketchup', 'cost':3.47, 'amount':1},
#     {'name':'pickles', 'cost':4.25, 'amount':1}
# ]

# shopping_list = []

# budget = 27.50
# total_cost = 0
# index = 0

# print('\n')
# while total_cost <= budget:
#     try:
#         item = items_list[index]
#         shopping_list.append(item['name'])
#         total_cost += item['cost'] * item['amount']
#         index += 1
        
#         for i in shopping_list:
#             print(i)
            
#         print('----------')
        
#         if 'fries' in shopping_list and 'burger patties' in shopping_list and 'burger buns' in shopping_list:
#             print(f'We can make burgers and fries for ${total_cost}!')
#             break
    
#     except:
#         print(f'ERROR: The index must be an integer.')
        
# print(f'{shopping_list}\n')

# **************************************************************
# **************************************************************

# ** day_4 Exercise 6: Customize Your Script
items_list = [
    {'name':'top sirloin', 'cost':14.29, 'amount':1},
    {'name':'egg noodles', 'cost':4.26, 'amount':1},
    {'name':'seasoning mix', 'cost':2.07, 'amount':1},
    {'name':'tomato', 'cost':1.50, 'amount':2},
    {'name':'lettuce', 'cost':5, 'amount':1},
    {'name':'Ketchup', 'cost':3.47, 'amount':1},
    {'name':'pickles', 'cost':4.25, 'amount':1}
]

shopping_list = []

budget = 27.50
total_cost = 0
index = 0

print('\n')
while total_cost <= budget:
    try:
        item = items_list[index]
        shopping_list.append(item['name'])
        total_cost += item['cost'] * item['amount']
        index += 1
        
        for i in shopping_list:
            print(i)
            
        print('----------')
        
        if 'top sirloin' in shopping_list and 'egg noodles' in shopping_list and 'seasoning mix' in shopping_list:
            print(f'We can make beef stroganoff for ${total_cost:.2f}!')
            break
    
    except IndexError:
        print(f'ERROR: The index must be an integer.')
        
print(f'{shopping_list}\n')