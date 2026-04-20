import random


class ArithmeticTrainer:
    def __init__(self):
        # Описание доступных режимов тренировки
        self.difficulties = {
            1: "базовые операции (числа 2-9)",
            2: "квадраты двузначных чисел (11-29)"
        }
        self.score = 0
        self.active_lv = None

    def ask_for_level(self):
        """Выбор сложности пользователем."""
        while True:
            print("Укажите желаемый уровень:")
            for key, desc in self.difficulties.items():
                print(f"{key} — {desc}")

            choice = input("> ").strip()
            if choice in ("1", "2"):
                self.active_lv = int(choice)
                break
            print("Неверный ввод. Выберите 1 или 2.")

    def generate_task(self):
        """Подготовка математического примера."""
        if self.active_lv == 1:
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            op = random.choice(["+", "-", "*"])
            task_str = f"{a} {op} {b}"
            # Вычисляем эталонный ответ
            return task_str, eval(task_str)
        else:
            base_num = random.randint(11, 29)
            return str(base_num), base_num ** 2

    def get_number_input(self):
        """Безопасное получение целого числа от пользователя."""
        while True:
            try:
                return int(input("> "))
            except ValueError:
                print("Ошибка: введите целое число.")

    def save_to_log(self):
        """Запись достижений в текстовый файл."""
        print("Сохранить результат сессии в файл? (yes/no)")
        confirm = input("> ").lower()
        if confirm in ("yes", "y", "да"):
            name = input("Введите имя для протокола: > ")
            # Сохраняем строку с результатами (дозапись в конец файла)
            with open("results.txt", "a", encoding="utf-8") as f:
                entry = (f"{name}: {self.score}/5 на уровне {self.active_lv} "
                         f"({self.difficulties[self.active_lv]}).\n")
                f.write(entry)
            print("Результат успешно экспортирован.")

    def run(self):
        """Запуск основного цикла программы."""
        while True:
            self.score = 0
            self.ask_for_level()

            for _ in range(5):
                expression, correct_answer = self.generate_task()
                print(expression)

                if self.get_number_input() == correct_answer:
                    print("Правильно!")
                    self.score += 1
                else:
                    print("Неверно.")

            print(f"Итоговый балл: {self.score} из 5.")
            self.save_to_log()

            print("\nЖелаете начать новую серию задач? (yes/no)")
            repeat = input("> ").lower()
            if repeat not in ("yes", "y", "да"):
                print("До встречи!")
                break


if __name__ == "__main__":
    trainer = ArithmeticTrainer()
    trainer.run()