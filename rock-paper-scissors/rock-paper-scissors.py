import random


class RockPaperScissorsPlus:
    DEFAULT_OPTIONS = ["rock", "paper", "scissors"]

    # Игровые статусы
    STATUS_SETUP = 0
    STATUS_PLAYING = 1
    STATUS_QUIT = 2

    def __init__(self, record_path: str = "rating.txt"):
        self.db_path = record_path
        self.player_name = ""
        self.score = 0
        self.variants = self.DEFAULT_OPTIONS.copy()
        self.state = self.STATUS_SETUP

    def _load_user_score(self) -> None:
        """Получение очков игрока из текстового файла базы."""
        try:
            with open(self.db_path, "r", encoding="utf-8") as storage:
                for line in storage:
                    name, value = line.strip().split()
                    if name == self.player_name:
                        self.score = int(value)
                        return
        except (FileNotFoundError, ValueError):
            pass
        self.score = 0

    def launch(self) -> None:
        self.player_name = input("Введите имя пользователя:\n> ").strip()
        print(f"Добро пожаловать, {self.player_name}!")
        self._load_user_score()
        self.show_controls()

    def show_controls(self):
        print("Команды управления:")
        print("!start  — переход к игре")
        print("!rating — посмотреть очки")
        print("!exit   — выход из приложения")
        print("Чтобы изменить список фигур, введите их через запятую (минимум 3 варианта) до начала игры.")

    def set_custom_variants(self, input_string: str) -> None:
        data = input_string.strip()

        # Если строка пустая — ставим дефолт
        if not data:
            self.variants = self.DEFAULT_OPTIONS.copy()
            print("Используются стандартные параметры.")
            return

        # Разбиваем и чистим список
        new_variants = [s.strip() for s in data.split(",") if s.strip()]

        # ПРОВЕРКА: Нужно минимум 3 символа для корректной логики
        if len(new_variants) < 3:
            print("Ошибка: для игры нужно минимум 3 различных символа!")
            print(f"Оставлен текущий набор: {', '.join(self.variants)}")
        else:
            self.variants = new_variants
            print(f"Параметры обновлены. Текущий набор: {', '.join(self.variants)}")

    def _check_computer_win(self, user_pick: str, comp_pick: str) -> bool:
        """Реализация круговой логики: бьет ли компьютерный выбор выбор игрока."""
        idx = self.variants.index(user_pick)
        # Перестраиваем список так, чтобы выбор пользователя был в начале
        rotated = self.variants[idx + 1:] + self.variants[:idx]
        # Половина элементов после выбора игрока считаются выигрышными для ПК
        half_len = len(rotated) // 2
        return comp_pick in rotated[:half_len]

    def play_turn(self, user_choice: str) -> None:
        cpu_choice = random.choice(self.variants)

        if cpu_choice == user_choice:
            print(f"Результат: ничья ({cpu_choice})")
            self.score += 50
        elif self._check_computer_win(user_choice, cpu_choice):
            print(f"Поражение. Компьютер выбрал {cpu_choice}")
        else:
            print(f"Победа! Вы обыграли {cpu_choice}")
            self.score += 100

    def _handle_input(self, entry: str):
        if entry == "!exit":
            print("Завершение программы. Всего доброго!")
            self.state = self.STATUS_QUIT
            return

        if entry == "!rating":
            print(f"Ваш текущий счет: {self.score}")
            return

        if self.state == self.STATUS_SETUP:
            if entry == "!help":
                self.show_controls()
            elif entry == "!start":
                print("Бой начался! Вводите выбранную фигуру.")
                self.state = self.STATUS_PLAYING
            else:
                self.set_custom_variants(entry)

        elif self.state == self.STATUS_PLAYING:
            if entry in self.variants:
                self.play_turn(entry)
            else:
                print(f"Неизвестный вариант. Доступны: {', '.join(self.variants)} или !exit.")

    def run(self):
        self.launch()

        while self.state != self.STATUS_QUIT:
            command = input("> ").strip()
            if not command:
                continue
            self._handle_input(command)


if __name__ == "__main__":
    app = RockPaperScissorsPlus()
    app.run()