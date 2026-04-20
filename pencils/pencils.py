import random

def get_initial_pencils():
    while True:
        pencils = input("How many pencils would you like to use:\n> ")
        if not pencils.isdigit():
            print("The number of pencils should be numeric")
            continue

        pencils = int(pencils)
        if pencils == 0:
            print("The number of pencils should be positive")
            continue

        return pencils


def get_first_player(player_name, bot_name):
    while True:
        # Изменил имя переменной в input, чтобы не перекрывать аргументы
        choice = input(f"Who will be the first ({player_name}, {bot_name})?\nYou are {player_name}, and {bot_name} is the bot.\n> ").strip()
        if choice not in [player_name, bot_name]:
            print(f"Choose between '{player_name}' and '{bot_name}'")
            continue
        return choice


def bot_move(pencils_left):
    # Выигрышная стратегия: оставить противнику количество олимпиад, кратное 4, плюс 1
    # То есть позицию (4n + 1)
    target = (pencils_left - 1) % 4
    if target == 0:
        # Если бот в проигрышной позиции (уже 4n+1), берем 1 или рандом
        return 1 if pencils_left == 1 else random.randint(1, min(3, pencils_left))
    return target


def game():
    name_player = "John"
    name_bot = "Jack"

    pencils = get_initial_pencils()
    current_turn = get_first_player(name_player, name_bot)

    while pencils > 0:
        print("|" * pencils)
        print(f"{current_turn}'s turn!")

        if current_turn == name_player:
            move_input = input("> ")

            if not move_input.isdigit() or move_input not in ['1', '2', '3']:
                print("Possible values: '1', '2' or '3'")
                continue

            move = int(move_input)
            if move > pencils:
                print("Too many pencils were taken")
                continue
        else:
            # Ход бота
            move = bot_move(pencils)
            print(move)

        pencils -= move

        if pencils == 0:
            # Побеждает тот, кто НЕ брал последний карандаш
            winner = name_bot if current_turn == name_player else name_player
            print(f"{winner} won!")
            break

        # Смена хода: если был John, станет Jack, и наоборот
        current_turn = name_bot if current_turn == name_player else name_player

if __name__ == "__main__":
    game()