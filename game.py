import copy

# Cписок всех выигрышных комбинаций игры
WINNING_COMBINATIONS = [
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]


def display_rules() -> None:
    """
    Выводит правила и описния игры в консоль
    :return: None
    """
    print("""
    Игроки по очереди ставят на свободные клетки поля 3×3 знаки (один всегда крестики, другой всегда нолики).
    Первый, выстроивший в ряд 3 своих фигуры по вертикали, горизонтали или диагонали, выигрывает.
    Первый ход делает игрок, ставящий крестики. Для того чтобы сделать код,
     укажите через пробел номер ячейки по горизонтали (от 0 до 2) и затем номер ячейки по вертикали (от 0 до 2):

        0 |  1 | 2 |
    ----------------
    0 | - |  - | - |
    ________________
    1 | - |  - | - |
    ________________
    2 | - |  - | - |
    ________________
   
    """)


def check_yes_no_answer(answer: str) -> str:
    """
    Задаем пользователя вопрос и
    валидируем чтобы он дал ответ "Да" или "Нет"
    :param answer: Вопрос для проверки
    :return: Ожидаемый ответ: Да или Нет
    """
    while True:
        res = input(answer).lower()
        if any([res == "да", res == "нет"]):
            break
        print("Неправильный ответ. Введите ответ 'Да' или 'Нет'")
    return res


def choosing_first_move() -> tuple:
    """
    Определяет кто будет делать первый ход,
     и какими знаками играет игрок и компьютер
    :return: знаки комьютера и игрока
    """
    res = check_yes_no_answer("Будете ли вы делать первый ход? (Да/Нет): ")
    computer, player = (" O ", " X ") if res == "да" else (" X ", " O ")
    return computer, player


def make_move_for_player(sign: str, field: list, acceptable_moves: list) -> None:
    """
    Заправшиваем и валидируем ход игрока
    :param player_sign: знак игрока
    :param field: текущие состояние игрового поля :param acceptable_moves: список допустимых ходов
    :return:
    """
    while True:
        cords = (input("Введите координаты клетки (два числа от 0 до 3 через пробел): ").split())

        if len(cords) != 2:
            print("Введите два числа от 0 до 2 через пробел.")
            continue

        if not cords[0].isdigit() or not cords[1].isdigit():
            print("Введенные значения не являются числами.")
            continue

        x, y = map(int, cords)
        if not all([0 <= x <= 2, 0 <= y <= 2]):
            print("Вы ввели неверные координаты клетки. Числа должны быть от 0 до 2.")
            continue

        if (x, y) in acceptable_moves:
            field[x][y] = sign
            break
        print("Клетка уже занята.")
    print("Вы сделали свой ход!")


def display_game_field(current_field: list) -> None:
    """
    Вывдит в консоль текущие игровое поле
    :param current_field: лист с текущим расположение знаков игроков
    :return:
    """
    print()
    print("      0  |  1  |  2  |")
    print("-" * 21)
    for i, row in enumerate(current_field):
        print(f" {str(i)} | {' | '.join(row)} |")
        print("_" * 21)


def checking_winnings(current_field: list, sign: str) -> bool:
    """
    Проверка выиграша для текущего состояния поля и переданного знака
    :param current_field: лист с текущим расположение знаков игроков
    :param sign: знак ('X' или 'O')
    :return:
    """
    for combination in WINNING_COMBINATIONS:
        y_cords = list(map(lambda x: x[0], combination))
        x_cords = list(map(lambda x: x[1], combination))

        if current_field[y_cords[0]][x_cords[0]] == \
                current_field[y_cords[1]][x_cords[1]] == \
                current_field[y_cords[2]][x_cords[2]] == sign:
            return True
    return False


def get_empty_cells(current_field: list) -> list:
    """
    Возвращает список доступных ходов на поле
    :param current_field: текущее игровое поле
    :return: список достпуных ходов
    """
    list_empty_cells = []
    for i in range(len(current_field)):
        for j in range(len(current_field[i])):
            if current_field[i][j] == " - ":
                list_empty_cells.append((i, j))
    return list_empty_cells


def checking_winning_move(current_field: list, acceptable_moves: list, sign: str):
    """
    Проверка возможности выиграть игру для текущего состояния поля.
    :param current_field: текущее игровое поле
    :param acceptable_moves: список достпуных ходов
    :param sign: игровой знак ("X" или "O")
    :return:
    """
    for y_cord, x_cord in acceptable_moves:
        copy_field = copy.deepcopy(current_field)
        copy_field[y_cord][x_cord] = sign
        if checking_winnings(copy_field, sign):
            return y_cord, x_cord

    return None


def computer_moves(current_field: list, acceptable_moves: list, computer_sign: str, player_sign: str) -> tuple:
    """
    Лолигка ходов компьютера
    :param current_field: текущие расположение знаков на поле
    :param acceptable_moves: список пустых клеток на поле
    :param computer_sign: знак компьютера
    :param player_sign: знак игрока
    :return:
    """

    cords = checking_winning_move(current_field, acceptable_moves, computer_sign) or \
            checking_winning_move(current_field, acceptable_moves, player_sign)

    if cords:
        return cords
    elif current_field[1][1] == " - ":
        return 1, 1
    else:
        list_moves = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for cords in list_empty_cells:
            if cords in list_moves:
                return cords
        return list_empty_cells[0]


if __name__ == '__main__':
    display_rules()

    # Выбираем кто делает первый ход и какими знаками играет
    computer_sign, player_sign = choosing_first_move()
    move_selection_flag = 1 if player_sign == " X " else 0

    # Инициализируем  и выводим в консоль игровое поле
    # init_filed = [[" - " for j in range(3)] for i in range(3)]
    init_filed = [[" - "] * 3 for i in range(3)]
    display_game_field(init_filed)

    game_status = True

    while game_status:
        # Получаем список доступных ходов после каждого раунда игры
        list_empty_cells = get_empty_cells(current_field=init_filed)
        if list_empty_cells:
            if move_selection_flag:
                make_move_for_player(sign=player_sign, field=init_filed, acceptable_moves=list_empty_cells)
                if checking_winnings(current_field=init_filed, sign=player_sign):
                    print("Игра окончена. Вы победили!")
                    game_status = False
                else:
                    move_selection_flag = 0
            else:
                cords = computer_moves(init_filed, list_empty_cells, computer_sign, player_sign)
                init_filed[cords[0]][cords[1]] = computer_sign

                if checking_winnings(current_field=init_filed, sign=computer_sign):
                    print("Игра окончена. Вы проиграли!")
                    game_status = False
                else:
                    move_selection_flag = 1

            display_game_field(init_filed)

        else:
            game_status = False
            print("Игра окончена! Ничья.")
