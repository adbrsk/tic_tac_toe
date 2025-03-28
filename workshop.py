from math import ceil


class InvalidNumberError(Exception):
    pass


class InvalidValueNumberError(Exception):
    pass


class UnavailablePositionError(Exception):
    pass


def check_position_availability(position: int, board: list[list[str]]) -> tuple[int, int]:
    selected_row_index = ceil(position / 3) - 1
    selected_col_index = position % 3 - 1
    if board[selected_row_index][selected_col_index] != " ":
        raise UnavailablePositionError
    return selected_row_index, selected_col_index


def check_position_validity(position: str) -> int:
    try:
        position = int(position)
    except ValueError:
        raise InvalidNumberError

    if position < 1 or position > 9:
        raise InvalidValueNumberError

    return position


def define_signs(name: str) -> tuple[str, str]:
    while True:
        sign = input(f"{name} would tou like to play with X or O? ").upper()
        if sign in ("X", "O"):
            break

    other_player_sign = "0" if sign == "X" else "X"
    return sign, other_player_sign


def setup_players():
    player_one_name = input("Player one name: ")
    player_two_name = input("Player two name: ")
    player_one_sign, player_two_sign = define_signs(player_one_name)
    player_one = (player_one_name, player_one_sign)
    player_two = (player_two_name, player_two_sign)
    return player_one, player_two


def print_board(board):
    for row in board:
        print(f"|  {'  |  '.join([str(el) for el in row])}  |")


player_one, player_two = setup_players()

num_board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print_board(num_board)

board = [[" ", " ", " "] for _ in range(3)]
print(f"{player_one[0]} starts first!")
turns = 1
current_player = None

while True:
    turns += 1
    current_player = player_one if turns % 2 != 0 else player_two
    position = input(f"{current_player[0]} choose a free position [1-9]: ")

    try:
        position = check_position_validity(position)
        row_index, col_index = check_position_availability(position, board)
    except (InvalidNumberError, InvalidValueNumberError):
        print(f"position must be valid number between 1 and 9 (inclusive) and should be available")
    except UnavailablePositionError:
        print("You must select an empty position!")
    else:
        board[row_index][col_index] = current_player[1]
        print_board(board)

        if turns >= 6:
            first_row = all([el == current_player[1] for el in board[0]])
            second_row = all([el == current_player[1] for el in board[1]])
            third_row = all([el == current_player[1] for el in board[2]])

            first_column = all([el == current_player[1] for el in [board[0][0], board[1][0], board[2][0]]])
            second_column = all([el == current_player[1] for el in [board[0][1], board[1][1], board[2][1]]])
            third_column = all([el == current_player[1] for el in [board[0][2], board[1][2], board[2][2]]])

            first_diagonal = all([el == current_player[1] for el in [board[0][0], board[1][1], board[2][2]]])
            second_diagonal = all([el == current_player[1] for el in [board[0][2], board[1][1], board[2][0]]])

            if (first_row
                    or second_row
                    or third_row
                    or first_column
                    or second_column
                    or third_column
                    or first_diagonal
                    or second_diagonal
            ):
                print(f"{current_player[0]} won!")
                break

            if turns == 10:
                print("DRAW! No one wins!")
                break
