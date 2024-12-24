"""
Vending Machine - Assessment 2
This Python program simulates a vending machine, allowing users to:
-Check out a list of products with their code numbers, the price and the quantity in stock.
-Pay for items by placing money and the amount returned if any into the till.
-Through using a secured password, administrators can restock items.
"""

import pyttsx3  #To add text to speech functionality we first import the pyttsx3 library.


engine = pyttsx3.init() #Start the text-speech system

#Welcome message using text-to-speech
engine.say("Welcome to Marc's Vending Machine!")
engine.runAndWait()

# Dictionary containing items in the vending machine with their properties
items = {
    1: {
        "name": "Royal",         #Orange-flavored soft drink
        "price": 5.50,           #Price in AED
        "category": "Drink",     #Categorized as a beverage
        "stock": 5               #Units currently in stock
    },
    2: {
        "name": "Pocari Sweat",  #A refreshing isotonic drink for rehydration
        "price": 5.50,           #Price in AED
        "category": "Drink",     #Categorized as a beverage
        "stock": 2               #Units currently in stock
    },
    3: {
        "name": "Water",         #Plain bottled water, essential for hydration
        "price": 3.50,           #Price in AED
        "category": "Drink",     #Categorized as a beverage
        "stock": 10              #Units currently in stock
    },
    4: {
        "name": "Fudgee Bar",    #A chocolate-flavored snack bar
        "price": 7.50,           #Price in AED
        "category": "Snack",     #Categorized as a snack
        "stock": 2               #Units currently in stock
    },
    5: {
        "name": "Piatos",        #Crispy cheese-flavored potato chips
        "price": 4.50,           #Price in AED
        "category": "Snack",     #Categorized as a snack
        "stock": 7               #units currently in stock
    },
}


#Administrator password for accessing restocking functionality
admin_password = "pogi123" #password for the admin mode

def show_menu():
    """
    Displays the menu, including item codes, names, prices, categories, and stock levels.
    """
    print("\n{***** Welcome to Marc's Vending Machine *****}")
    print("Code   Item                  Price      Category      Stock")
    print("=" * 70)

    # Loop through each item in the items dictionary and display its details
    for code, item in items.items():
        print(
            f"{code:<5} {item['name']:<22} AED {item['price']:<7.2f} {item['category']:<12} {item['stock']}"
        )
    print("=" * 70)

def restock():
    """
    Administrator mode for restocking items in the vending machine.
    Allows the admin to add stock to items by providing item codes and quantities.
    """
    print("** Administrator Mode **")
    while True:
        show_menu()  # Display the menu for reference
        add_stock = input("Enter the item code to restock (or 0 to exit): ").strip()
        if add_stock == "0":  # Exit admin mode
            print("Exiting Administrator mode.")
            break
        if not add_stock.isdigit() or int(add_stock) not in items:  # Validate the entered code
            print("Invalid code. Try again.")
            continue
        itm_code = int(add_stock)
        try:
            # Ask for the quantity to restock
            qty = int(input(f"How many units to add for {items[itm_code]['name']}? "))
            if qty <= 0:  # Ensure quantity is positive
                print("Quantity must be positive!")
            else:
                items[itm_code]["stock"] += qty  # Add the quantity to the item's stock
                print(f"{items[itm_code]['name']} now has {items[itm_code]['stock']} units in stock.")
        except ValueError:
            print("Please enter a valid number.")  # Handle invalid input

def buy_itm():
    """
    Handles the purchasing process:
    –Enables users to choose items, pay for commodities and receive change.
    -Confirms the existence of the stocks and users’ inputs.
    """
    balance = 0  #Initialize user balance
    while True:
        show_menu()  #Display the menu
        if balance > 0:
            print(f"Your remaining balance: AED {balance:.2f}")  #Show current balance

        choice = input("Enter item code to buy (or 0 to exit): ").strip()
        if choice == "0":  #Exit purchasing mode
            print("Thank you for using the vending machine! See you again later!")
            break
        if choice == "999":  #A secret code to enter admin mode
            password = input("Enter the admin password: ").strip()
            if password == admin_password:
                restock()  #Access restocking functionality
            else:
                print("Incorrect password.")  #Handle incorrect admin password
            continue
        if not choice.isdigit() or int(choice) not in items:  #Validate item code
            print("Invalid code. Try again.")
            continue

        itm_code = int(choice)
        item = items[itm_code]
        if item["stock"] <= 0:  #Check if the selected item is in stock
            print(f"{item['name']} is out of stock, come back again later!")
            continue

        print(f"You selected {item['name']}. It costs AED {item['price']:.2f}.")  #Show selected item details

        if balance >= item["price"]:  #Check if balance is sufficient
            balance -= item["price"]  #Deduct item price from balance
            item["stock"] -= 1  #Reduce stock by 1
            print(f"Dispensing {item['name']}... Enjoy your item!")
            print(f"Remaining balance is: AED {balance:.2f}")
        else:
            while True:  #Handle payment process
                try:
                    #Ask user to insert money
                    payment = float(input(f"Insert AED {item['price'] - balance:.2f} to pay: "))
                    if payment < item["price"] - balance:  #Insufficient funds
                        print(f"Not enough money. You still need AED {item['price'] - balance - payment:.2f}.")
                        continue
                    else:
                        #Calculate change and dispense the item
                        change = payment + balance - item["price"]
                        item["stock"] -= 1
                        print(f"Dispensing {item['name']}... Enjoy your item!")
                        if change > 0:
                            print(f"Here's your change: AED {change:.2f}")  #Return change
                        balance = change  #Update balance
                        break
                except ValueError:
                    print("Invalid input. Please insert a valid amount.")  #Handle invalid input

        #Ask user if they want to buy another item
        more = input("Would you like to buy another item? (yes/no): ").strip().lower()
        if more != "yes":
            if balance > 0:
                print(f"Returning your remaining balance: AED {balance:.2f}")  #Returning the remaining balance
            print("Thank you for your purchase! Have a nice day!")
            break

def start_vm():
    """
    Starts the vending machine application.
    """
    print("Marc's vending machine is starting...")  #Startup message
    engine.say("Here's the menu")  #Text-to-speech output
    engine.runAndWait()
    buy_itm()  #Start the purchasing process

#Main program execution starts here
start_vm()

#Final text-to-speech message before program ends
engine.say("Dispensing item")
engine.runAndWait()

engine.say("Thank you for using the vending machine, see you again later!!")
engine.runAndWait()
