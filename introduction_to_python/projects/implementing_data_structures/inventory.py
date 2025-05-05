class Inventory:
    data: dict

    def __init__(self):
        self.data = {}

    def add(self, key: str, value: tuple[int, float]) -> None:
        # Adds key and value to the `data` dictionary
        if key in self.data.keys():
            # If the key already exists
            print(f"\n{key} already in inventory. Try updating inventory instead.")
            return

        self.data[key] = value

    def remove(self, key: str) -> None:
        # Removes a key-value pair from the `data` dictionary
        if key not in self.data.keys():
            # Item does not exist in inventory
            print(f"\n{key} does not exist in inventory.")
        else:
            # Item exists, so pop it off
            self.data.pop(key)

    def modify(self, key: str, value: tuple[int, float]) -> None:
        # Updates the two-tuple value of the key.
        # Adds to the dictionary if it doesn't already exist.
        if key in self.data.keys():
            self.data.update({key: value})
        else:
            self.data[key] = value

    def display(self, key: str) -> None:
         # Displays a single item from `data`
         if key in self.data.keys():
             print(f"Item: {key}, Quantity: {self.data[key][0]}, Price: ${self.data[key][1]:.2f}")
         else:
             print("\nItem not in inventory.")
             
    def display_all(self) -> None:
        # Displays all items in the inventory followed by the total value of all items
        if len(self.data) > 0:
            print("\n---------------[Inventory]---------------\n")
            # Loops through the dictionary and displays each item one by one
            for item in self.data:
                self.display(item)

            print(f"\nTotal inventory value: ${self.inventory_value():.2f}")
            print("\n-----------------------------------------")
        else:
            print("\nInventory is currently empty. Try adding some items!")

    def inventory_value(self) -> float:
        # Calcualtes the total value of the inventory and returns it as a float
        value = 0
        
        for item in self.data:
            value += self.data[item][0] * self.data[item][1]

        return value

def display_menu() -> None:
    print("\nSelect a number from the options below:")
    print("\n\t[1] - Add item to inventory")
    print("\t[2] - Remove item from dictionary")
    print("\t[3] - Update item in inventory")
    print("\t[4] - Display info about an item in the inventory")
    print("\t[5] - Display info for all items in inventory")
    print("\t[0] - Exit the program")
    
def main():
    # Main program logic loop
    # Init Inventory and display welcome message
    inventory = Inventory()
    print("Welcome to the Inventory Manager!")
    inventory.display_all()
    exit = False

    while not exit:
        display_menu()
        choice = input("\n> ")

        if choice.isdigit():
            match choice:
                case "1":
                    # Handle adding item to inventory
                    name = input("\nEnter the name of the item to be added: ")
                    amount = int(input(f"Enter the amount of {name}(s) to add: "))
                    price = float(input("Enter the price of the item: "))
                    inventory.add(name, (amount, price))

                case "2":
                    # Handle removing an item from inventory
                    if len(inventory.data) == 0:
                        print("\nThe inventory is currently empty! Try adding some items.")
                    else:
                        name = input("\nEnter the name of the item to remove: ")
                        inventory.remove(name)
                    
                case "3":
                    # Handle updating an item in the inventory
                    # NOTE: If item doesn't already exist a new entry in the inventory will be created
                    if len(inventory.data) == 0:
                        print("\nInventory is currently empty! Try adding some items first.")
                    else:
                        name = input("\nEnter the name of the item to be updated: ")
                        amount = int(input(f"Enter the amount of {name}(s) to add: "))
                        price = float(input("Enter the price of the item: "))
                        inventory.modify(name, (amount, price))

                case "4":
                    # Find an item in inventory and display info
                    if len(inventory.data) == 0:
                        print("\nThe inventory is currently empty! Try adding some items first.")
                    else:
                        name = input("\nSearch for an item: ")
                        inventory.display(name)

                case "5":
                    if len(inventory.data) == 0:
                        print("\nThe inventory is currently empty! Try adding some items first.")
                    inventory.display_all()

                case "0":
                    print("\nGoodbye!")
                    exit = True

                case _:
                    print("\nChoice not recognized. Please enter a single digit [0-5].")

if __name__ == "__main__":
    main()
