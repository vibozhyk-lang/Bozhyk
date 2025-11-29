class CoffeeMachine:

    def __init__(self):
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550
        self.state = "action"

    def get_int(self, text):
        try:
            return int(text)
        except ValueError:
            print("❌ Please enter a valid number!")
            return None

    def process(self, user_input):
        if self.state == "action":
            self.process_action(user_input)
        elif self.state == "buy":
            self.process_buy(user_input)
        elif self.state.startswith("fill"):
            self.process_fill(user_input)

    def process_action(self, action):
        if action == "buy":
            self.state = "buy"
            print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back – to main menu:")
        elif action == "fill":
            self.state = "fill_water"
            print("Write how many ml of water do you want to add:")
        elif action == "take":
            print(f"I gave you ${self.money}")
            self.money = 0
        elif action == "remaining":
            self.print_remaining()
        elif action == "exit":
            self.state = "exit"
        else:
            print("❌ Unknown command. Choose: buy, fill, take, remaining, exit.")

    def process_buy(self, choice):
        if choice == "back":
            self.state = "action"
            return

        drinks = {
            "1": {"water": 250, "milk": 0, "beans": 16, "cost": 4},
            "2": {"water": 350, "milk": 75, "beans": 20, "cost": 7},
            "3": {"water": 200, "milk": 100, "beans": 12, "cost": 6},
        }

        drink = drinks.get(choice)
        if not drink:
            print("❌ Unknown option.")
            self.state = "action"
            return

        if self.water < drink["water"]:
            print("Sorry, not enough water!")
        elif self.milk < drink["milk"]:
            print("Sorry, not enough milk!")
        elif self.beans < drink["beans"]:
            print("Sorry, not enough coffee beans!")
        elif self.cups < 1:
            print("Sorry, not enough disposable cups!")
        else:
            self.water -= drink["water"]
            self.milk -= drink["milk"]
            self.beans -= drink["beans"]
            self.cups -= 1
            self.money += drink["cost"]
            print("I have enough resources, making you a coffee!")

        self.state = "action"

    def process_fill(self, amount):
        value = self.get_int(amount)
        if value is None:
            return

        if self.state == "fill_water":
            self.water += value
            self.state = "fill_milk"
            print("Write how many ml of milk do you want to add:")

        elif self.state == "fill_milk":
            self.milk += value
            self.state = "fill_beans"
            print("Write how many grams of coffee beans do you want to add:")

        elif self.state == "fill_beans":
            self.beans += value
            self.state = "fill_cups"
            print("Write how many disposable cups of coffee do you want to add:")

        elif self.state == "fill_cups":
            self.cups += value
            self.state = "action"

    def print_remaining(self):
        print("The coffee machine has:")
        print(f"{self.water} ml of water")
        print(f"{self.milk} ml of milk")
        print(f"{self.beans} g of coffee beans")
        print(f"{self.cups} disposable cups")
        print(f"${self.money} of money")


machine = CoffeeMachine()

while machine.state != "exit":
    if machine.state == "action":
        print("Write action (buy, fill, take, remaining, exit):")
    user_input = input("> ")
    machine.process(user_input)