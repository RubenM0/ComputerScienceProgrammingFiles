#Programming vending machine assignment by Ruben Mazziotta (s5706207) 

#Array for coin types
coin_types = [2, 1, 0.5, 0.2]

#Map coin types to these values for easier validation and allowing change to work
coin_map = {
    "2": 200,
    "1": 100,
    "0.5": 50,
    "0.2": 20
}

#Current balance of user
current_balance = 0

total_spent = 0
purchased_items = []
order_number = 1
discounts_applied_counter = 0

#Tracking number to find out how many items bought
track = len(purchased_items)

#Dictionary for the items in the vending machine, their prices and their stocks
items = {
    "Water" : [120, 5],
    "Soda" : [150, 5],
    "Chocolate" : [250, 10],
    "Crisps" : [140, 10],
    "Sandwich" : [380, 5]
}

#Function to reset all the values
def reset_values():
    global current_balance
    global total_spent
    global purchased_items
    global discounts_applied_counter

    current_balance = 0
    total_spent = 0
    purchased_items = []
    discounts_applied_counter = 0

#Bonus task: creating a function to calculate bonus change
def bonus_change(order_number, total_spent, remaining_balance):
    #Find out if the oder number is odd by using modulo and checking if the price is above the threshold
    if order_number % 2 == 1 and total_spent > 200:
        #Add £1
        remaining_balance += 100
        print("Bonus granted! +£1 added to your balance")
    return remaining_balance


#Format pence to pounds/pence
def format_money(pence):
    pounds = pence // 100
    #Find the remainder
    remaining_pence = pence % 100
    #Formatting
    return f"£{pounds}.{remaining_pence:02d}"


def add_coins_to_amount():
    global current_balance
    #Keep looping until the user types 'done'
    while True:
        print(f"Your current balance is: {format_money(current_balance)}")
        #String formatting
        input_coins_to_add = input(f"Insert coin ({', '.join(map(str, coin_types))}) or type 'done' to finish: ").strip()
        
        if input_coins_to_add.lower() == 'done':
            break

        #Check to see if a valid coin was put in and not a random character
        if input_coins_to_add in coin_map:
            current_balance += coin_map[input_coins_to_add]
            print(f"Added {format_money(coin_map[input_coins_to_add])}")
        else:
            print("Invalid coin")    

#Function to calculate change which takes the parameter "remaining_balance"
def give_change(remaining_balance):
    change = {}
    #Sort coins from largest first and conver to pence
    pence_coins = sorted(coin_map.values(), reverse=True)
    for pence_coin in pence_coins:
        count = remaining_balance // pence_coins
        if count > 0:
            #Map back for user display
            pound_coin = pence_coin / 100
            change[pound_coin] = count
            remaining_balance -= count * pence_coin
    return change


add_coins_to_amount()


#Create a reciept taking the items purchased, the total discounts applied, the total spent and the remaining money the user had
def generate_reciept(total_items_purchased, discounts_applied, total_spent, remaining_balance):
    global current_balance
    global order_number
    global discounts_applied_counter

    #Check how many discounts applied
    discounts_applied = discounts_applied_counter
    #Calculate the bonus change to add
    remaining_balance = bonus_change(order_number, total_spent, remaining_balance)

    #Print the reciept
    print("--- Reciept ---")
    print(f"Order number: {order_number}")
    print(f"Total items bought: {total_items_purchased}")
    print(f"Items bought: {', '.join(purchased_items)}")
    print(f"Total spent: {format_money(total_spent)}")
    print(f"Discounts applied: {discounts_applied}")
    print(f"Remaining balance: {format_money(remaining_balance)}")
    print("----------------------------")

    #Create the CSV file
    csv_filename = f"csv receipt {order_number}"

    #Write to the file
    with open(csv_filename, 'w') as file:
        file.write("--- Receipt ---\n")
        file.write(f"Order number: {order_number}\n")
        file.write(f"Total items bought: {total_items_purchased}\n")
        file.write(f"Items bought: {', '.join(purchased_items)}\n")
        file.write(f"Total spent: {format_money(total_spent)}\n")
        file.write(f"Discounts applied: {discounts_applied}\n")
        file.write(f"Remaining balance: {format_money(remaining_balance)}\n")
        file.write("----------------------------\n")

    #Reset values for next reciept
    reset_values()
    order_number += 1

    #Request if the user wants to start again
    while True:
        request_restart = input("Would you like to go again (y = yes, n = no)? ")
        if request_restart.lower() == "y":
            add_coins_to_amount()
            vending_machine_contents()
        elif request_restart.lower() == "n":
            print("Thank you for using this vending machine!")
            break
        else:
            print("Invalid input")


def vending_machine_contents():
    global current_balance
    global total_spent
    global purchased_items
    global track
    global discounts_applied_counter 
    
    #Loop through dictionary and print the keys and values
    #Print the first value in the array, the price, first then the second, the stock
    #Keep looping until the user types 'exit'
    while True:
        print("--- Vending Machine Menu ---")
        for item_key, item_value in items.items():
            print(item_key,"-", format_money(item_value[0]), f"(Stock: {item_value[1]})")
        print("----------------------------")
        
        print(f"Current balance: {format_money(current_balance)}")
        input_purchase_item = input("Select an item by name or type 'exit' to quit: ")
        #Lower the input for case-insensitivity later
        lowered_input = input_purchase_item.lower()

        #Continue to the reciept if user is done
        if lowered_input == 'exit':
            generate_reciept(len(purchased_items), 0, total_spent, current_balance)
            break

        #Check to see if the inputted item matches what exists in the dictionary by iterating through it
        found_inputted_item = next((key for key in items if key.lower() == lowered_input), None)
        if found_inputted_item:
            #Get the values of the item purhcased and store it in separate variables
            return_items_dictionary = items[found_inputted_item]
            price = return_items_dictionary[0]
            stock = return_items_dictionary[1]
            #Check if the user has enough money or item is in stock before proceeding
            if current_balance < price:
                print("Not enough money!")
            elif stock <= 0:         
                print("Out of stock!")
            else:
                #Make the text clean
                input_purchase_item_capitalized = input_purchase_item.capitalize()
                track = len(purchased_items)

                #Check for discount by doing the maths and displaying original and new prices
                has_discount = False
                original_price = price
                if track == 2:
                    has_discount = True
                    discounted_amount = original_price * 5 // 100 #5%
                    price = original_price - discounted_amount
                    print(f"ORIGINAL PRICE: {format_money(original_price)}")
                    print(f"NEW PRICE: {format_money(price)}")
                elif track == 4:
                    has_discount = True
                    discounted_amount = original_price * 10 // 100 #10%
                    price = original_price - discounted_amount
                    print(f"ORIGINAL PRICE: {format_money(original_price)}")
                    print(f"NEW PRICE: {format_money(price)}")
                elif track == 6:
                    has_discount = True
                    discounted_amount = original_price * 15 // 100 #15%
                    price = original_price - discounted_amount
                    print(f"ORIGINAL PRICE: {format_money(original_price)}")
                    print(f"NEW PRICE: {format_money(price)}")

                #Display purchased item and for how much
                print(f"Purchased: {input_purchase_item_capitalized} for: {format_money(price)}")

                #Add/subtract values
                current_balance -= price
                return_items_dictionary[1] -= 1

                total_spent += price
                purchased_items.append(input_purchase_item_capitalized)

                if has_discount:
                    print(f"Total spent: {format_money(total_spent)} (Discount applied)")
                    discounts_applied_counter += 1
                else:
                    print(f"Total spent: {format_money(total_spent)} (No discount applied)")

                has_discount = False
                print(f"Remaining balance: {format_money(current_balance)}")
        else:
            print("Invalid input")


vending_machine_contents()