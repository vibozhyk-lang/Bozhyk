class MarkdownEditor:
    def __init__(self):
        # Накопитель для итогового текста
        self.content_storage = ""
        # Список поддерживаемых стилей форматирования
        self.tags = {
            "plain", "bold", "italic", "header", "link",
            "inline-code", "ordered-list", "unordered-list", "new-line"
        }
        # Служебные команды управления
        self.control_cmds = {"!help", "!done", "exit"}

    def display_help(self):
        print("Доступные форматы: " + ", ".join(self.tags))
        print("Команды: !help (справка), !done (сохранить результат)")

    def _get_row_quantity(self):
        while True:
            try:
                n = int(input("Введите число строк: > "))
                if n > 0:
                    return n
                print("Ошибка: требуется число больше нуля.")
            except ValueError:
                print("Ошибка: некорректный ввод, нужно целое число.")

    def run(self):
        print("Редактор Markdown активен.")
        print("Введите !help для списка команд или exit для выхода.")

        while True:
            user_choice = input("Тип разметки или команда:\n> ").strip().lower()

            if user_choice in self.control_cmds:
                if user_choice == "!help":
                    self.display_help()
                elif user_choice == "!done":
                    with open("output.md", "w", encoding="utf-8") as out_file:
                        out_file.write(self.content_storage)
                    print("Файл output.md сохранен. Работа завершена.")
                    break
                elif user_choice == "exit":
                    print("Завершение без сохранения.")
                    break
                continue

            if user_choice not in self.tags:
                print("Ошибка: такой опции не существует.")
                continue

            # Секция обработки текстовых элементов
            if user_choice == "plain":
                txt = input("Введите текст: > ")
                self.content_storage += txt

            elif user_choice == "bold":
                txt = input("Текст для жирного выделения: > ")
                self.content_storage += f"**{txt}**"

            elif user_choice == "italic":
                txt = input("Текст для курсива: > ")
                self.content_storage += f"*{txt}*"

            elif user_choice == "inline-code":
                txt = input("Код: > ")
                self.content_storage += f"`{txt}`"

            elif user_choice == "header":
                while True:
                    try:
                        h_lvl = int(input("Уровень (1-6): > "))
                        if 1 <= h_lvl <= 6:
                            break
                        print("Диапазон уровней: от 1 до 6.")
                    except ValueError:
                        print("Нужна цифра от 1 до 6.")
                txt = input("Заголовок: > ")
                self.content_storage += f"{'#' * h_lvl} {txt}\n"

            elif user_choice == "link":
                label = input("Текст ссылки: > ")
                url = input("URL: > ")
                self.content_storage += f"[{label}]({url})"

            elif user_choice == "new-line":
                if self.content_storage.endswith("\n\n"):
                    pass
                elif self.content_storage.endswith("\n"):
                    self.content_storage += "\n"
                else:
                    self.content_storage += "\n\n"

            elif user_choice in ("ordered-list", "unordered-list"):
                rows = self._get_row_quantity()
                if self.content_storage and not self.content_storage.endswith("\n"):
                    self.content_storage += "\n"

                for i in range(1, rows + 1):
                    item_text = input(f"Строка #{i}: > ")
                    if user_choice == "ordered-list":
                        self.content_storage += f"{i}. {item_text}\n"
                    else:
                        self.content_storage += f"* {item_text}\n"
                self.content_storage += "\n"

            # Мониторинг текущего прогресса
            print("--- Предпросмотр ---")
            print(self.content_storage)
            print("--------------------")


if __name__ == "__main__":
    app = MarkdownEditor()
    app.run()