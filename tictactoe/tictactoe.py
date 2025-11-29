def print_board(board):
    """Виводить ігрове поле на екран"""
    print("---------")
    for row in board:
        print(f"| {' '.join(row)} |")
    print("---------")



def check_state(board):
    """Перевіряє поточний стан гри"""
    lines = [
        # рядки
        board[0], board[1], board[2],
        # стовпці
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        # діагоналі
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]

    x_wins = any(line == ["X", "X", "X"] for line in lines)
    o_wins = any(line == ["O", "O", "O"] for line in lines)
    empty = any("_" in row for row in board)

    if x_wins and o_wins:
        return "Impossible"
    elif x_wins:
        return "X wins"
    elif o_wins:
        return "O wins"
    elif empty:
        return "Game not finished"
    else:
        return "Draw"


def valid_coordinates(coord):
    """Перевіряє, що координати — це два числа від 1 до 3"""
    if not coord.replace(" ", "").strip():
        return False
    try:
        x, y = map(int, coord.split())
        return 1 <= x <= 3 and 1 <= y <= 3
    except ValueError:
        return False


def make_move(board, player):
    """Зчитує координати від гравця і робить хід"""
    while True:
        print(f"\nХід гравця: {player}")
        coords = input("Введіть координати:\n> ").split()

        # Перевірка: чи введено саме числа
        if len(coords) != 2 or not all(c.isdigit() for c in coords):
            print("Потрібно вводити числа!")
            continue

        x, y = map(int, coords)

        # Перевірка: чи в діапазоні від 1 до 3
        if not (1 <= x <= 3 and 1 <= y <= 3):
            print("Координати повинні бути від 1 до 3!")
            continue

        # Перетворення координат на індекси списку
        row = x - 1
        col = y - 1

        # Перевірка: чи клітинка вільна
        if board[row][col] != "_":
            print("Ця клітинка вже зайнята! Оберіть іншу!")
            continue

        # Якщо все добре — робимо хід
        board[row][col] = player
        break


def main():
    # Створення поля
    board = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]

    print_board(board)
    current_player = "X"

    while True:
        make_move(board, current_player)
        print_board(board)

        state = check_state(board)
        if state in ["X wins", "O wins", "Draw"]:
            print(state)
            break

        # Зміна гравця
        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    main()