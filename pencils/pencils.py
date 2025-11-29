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


def get_first_player(player, bot):
    while True:
        player = input(f"Who will be the first ({player}, {bot})?\nYou are {player}, and {bot} is the bot.\n> ")
        if player not in [player, bot]:
            print(f"Choose between '{player}' and '{bot}'")
            continue
        return player


def bot_move(pencils_left):
    # Виграшна стратегія:
    if pencils_left % 4 == 0:
        return 3
    elif pencils_left % 4 == 3:
        return 2
    elif pencils_left % 4 == 2:
        return 1
    else:
        # Програшна позиція → бот вибирає випадкове число
        return random.randint(1, 3)


def game():
    player = "John"
    bot = "Jack"

    pencils = get_initial_pencils()
    player = get_first_player(player, bot)

    print("|" * pencils)
    print(f"{player}'s turn!")

    while pencils > 0:
        if player == player:
            move = input("> ")

            # Перевіряємо коректність ходу
            if not move.isdigit() or move not in ['1', '2', '3']:
                print("Possible values: '1', '2' or '3'")
                continue

            move = int(move)
            if move > pencils:
                print("Too many pencils were taken")
                continue

        else:  # Ход бота
            move = bot_move(pencils)
            print(move)

        # Зменшуємо кількість олівців
        pencils -= move

        if pencils == 0:
            # Перемагає інший гравець
            winner = bot if player == player else player
            print(f"{winner} won!")
            break

        print("|" * pencils)

        # Змінюємо чергу
        player = bot if player == player else player
        print(f"{player}'s turn!")


if __name__ == "__main__":
    game()