Владислав, [09.12.2025 9:40]
class CoffeeMachine:
    """
    Класс, имитирующий работу кофемашины.
    Управляется через состояние (state).
    """

    def init(self):
        # Инициализация начальных ресурсов
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550
        # Начальное состояние машины
        self.state = "action"

    def _safe_int_conversion(self, text):
        """Вспомогательный метод: пробует превратить текст в число."""
        try:
            return int(text)
        except ValueError:
            print(" Пожалуйста, введите корректное число!")
            return None

    def handle_input(self, user_input):
        """
        Главный распределитель команд.
        В зависимости от текущего состояния (self.state) вызывает нужный метод.
        """
        if self.state == "action":
            self.main_menu_handler(user_input)
        elif self.state == "buy":
            self.buy_coffee(user_input)
        elif self.state.startswith("fill"):
            self.fill_resources(user_input)

    def main_menu_handler(self, action):
        """Обрабатывает основные команды главного меню."""
        if action == "buy":
            self.state = "buy"
            print("Что хотите купить? 1 - эспрессо, 2 - латте, 3 - капучино, back – назад:")

        elif action == "fill":
            self.state = "fill_water"
            print("Сколько мл воды вы хотите добавить:")

        elif action == "take":
            print(f"Я выдала вам ${self.money}")
            self.money = 0

        elif action == "remaining":
            self.display_status()

        elif action == "exit":
            self.state = "exit"

        else:
            print(" Неизвестная команда. Выберите: buy, fill, take, remaining, exit.")

    def buy_coffee(self, choice):
        """Логика покупки и приготовления кофе."""
        if choice == "back":
            self.state = "action"
            return

        # Рецепты напитков
        recipes = {
            "1": {"water": 250, "milk": 0, "beans": 16, "cost": 4},  # Эспрессо
            "2": {"water": 350, "milk": 75, "beans": 20, "cost": 7},  # Латте
            "3": {"water": 200, "milk": 100, "beans": 12, "cost": 6},  # Капучино
        }

        drink = recipes.get(choice)
        if not drink:
            print(" Нет такого варианта.")
            self.state = "action"
            return

        # Проверка ресурсов перед приготовлением
        if self.water < drink["water"]:
            print("Извините, не хватает воды!")
        elif self.milk < drink["milk"]:
            print("Извините, не хватает молока!")
        elif self.beans < drink["beans"]:
            print("Извините, не хватает зерен!")
        elif self.cups < 1:
            print("Извините, закончились стаканчики!")
        else:
            # Списываем ресурсы и добавляем деньги
            self.water -= drink["water"]
            self.milk -= drink["milk"]
            self.beans -= drink["beans"]
            self.cups -= 1
            self.money += drink["cost"]
            print("Ресурсов достаточно, готовлю ваш кофе!")

        # Возвращаемся в главное меню
        self.state = "action"

    def fill_resources(self, amount):
        """
        Пошаговое пополнение запасов.
        Состояние меняется по цепочке: вода -> молоко -> зерна -> стаканчики.
        """
        value = self._safe_int_conversion(amount)
        if value is None:
            return

        if self.state == "fill_water":
            self.water += value
            self.state = "fill_milk"
            print("Сколько мл молока добавить:")

        elif self.state == "fill_milk":
            self.milk += value
            self.state = "fill_beans"
            print("Сколько грамм зерен добавить:")

        elif self.state == "fill_beans":
            self.beans += value
            self.state = "fill_cups"
            print("Сколько стаканчиков добавить:")

Владислав, [09.12.2025 9:40]
elif self.state == "fill_cups":
            self.cups += value
            self.state = "action"  # Завершили пополнение, возврат в меню

    def display_status(self):
        """Вывод текущих запасов машины."""
        print("\nСостояние кофемашины:")
        print(f"{self.water} мл воды")
        print(f"{self.milk} мл молока")
        print(f"{self.beans} г кофейных зерен")
        print(f"{self.cups} одноразовых стаканчиков")
        print(f"${self.money} денег внутри\n")


# --- Запуск программы ---
machine = CoffeeMachine()

while machine.state != "exit":
    if machine.state == "action":
        print("Выберите действие (buy, fill, take, remaining, exit):")

    user_input = input("> ")
    machine.handle_input(user_input)