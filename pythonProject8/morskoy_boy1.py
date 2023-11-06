# def clear_screen():
#     os.system('clear')
class Cell(object):
    empty_cell = '\033[1;35m___|\033[0m'
    ship_cell = '\033[0;34m_■_|\033[0m'
    killed_cell = '\033[1;93m_X_|\033[0m'
    damaged_cell = '\033[1;93m_□_|\033[0m'
    miss_cell = '\033[0;37m_•_|\033[0m'


class Field:
    def __init__(self, size=6):
        self.size = size
        self.player = [[Cell.empty_cell for i in range(size)] for j in range(size)]
        self.ai_show = [[Cell.empty_cell for i in range(size)] for j in range(size)]
        self.ai_hidden = [[Cell.empty_cell for i in range(size)] for j in range(size)]

    @staticmethod
    def dostal(mistake):
        if mistake < 2:
            print('Не влезает так')
        elif 2 <= mistake <= 3:
            print('\033[1;33mНе глупи, разобьешь наши корабли\033[0m')
        else:
            print('\033[1;31mНе выдумывай... ТАК НЕ ДЕЛАЕТСЯ!...\033[0m')

    def get_field_type(self, field_type):
        # print(field_type)
        if field_type == 'User':
            return self.player
        elif field_type == 'AI show':
            return self.ai_show
        elif field_type == 'AI hidden':
            return self.ai_hidden
        else:
            print('Unknown type of a field')

    def check_ship_position(self, ship, orientation):
        x, y = ship.x, ship.y
        vert, gor = 1, 1
        field = user_field  # switch then

        if orientation == '-':
            gor = ship.ship_size
        elif orientation == '+' or orientation == '/':
            vert = ship.ship_size
        for p_x in range(x - 1, x + vert + 1):
            for p_y in range(y - 1, y + gor + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                if str(field[p_x][p_y]) != Cell.empty_cell:
                    # in (Cell.ship_cell, Cell.killed_cell):
                    return False
        return True

    def print_field(self, printed_field):
        # field = self.get_field_type(field_type)
        # print('field')
        row = 1
        print('   ', *list(f" {i}  " for i in range(1, (self.size) + 1)))
        row = 0
        for line in printed_field:
            print(f"{row + 1}\t|", end='')
            print(*line, end='\n')
            row += 1


class Player:
    def __init__(self, name, is_ai):
        self.name = name
        self.is_ai = is_ai
        self.fleet_auto = True
        self.message = []
        self.player_ship = []
        self.ai_ship = []
        self.field = None

    def make_shoot(self, aimed_cell):
        pass

    def receive_shoot(self, shoot):
        pass


def battlefield_size():
    print(
        '\033[34mВэлком на поля сражений!!!\nПо умолчанию- поле размером 9x9. На каком размере поля будем таки поиграть?',
        end='')
    print("\033[0m")
    while True:
        try:
            f_size = (input('введи одну цифру: '))
            if f_size == '':
                return 9

            elif int(f_size) < 8:
                print('В такой маленькой луже не поиграешь. Размахнись пошире.')

                # continue
            elif int(f_size) > 12:
                print('Нуу, в океане ты точно пропадешь. Поменьше выбери..')
                # continue
            else:
                print(f'Значит играем на поле: {f_size}х{f_size}')
                return int(f_size)
        except (TypeError, ValueError):
            print("\033[31mА это вообще не число. Давай, попробуй по-новой\033[0m")


class Ship:

    def __init__(self, ship_size, quantity, shut_parts=0, position='', x=0, y=0):
        self.ship_size = ship_size
        self.ship_hp = ship_size
        self.quantity = quantity
        self.shut_parts = shut_parts
        self.position = position
        self.x = x
        self.y = y

    def shoot_check(self):
        # if ??? :
        #     self.ship_hp-=1
        pass


def set_vessels():
    field.print_field(user_field)

    # for player
    for ship in fleet:
        count = 1
        mistake = 0

        orientation = '+'
        for i in range(ship.quantity):
            print(f'Введите положение и координаты {ship.ship_size}-трубного корабля.'
                  f' {count}-го из {ship.quantity}')
            if ship.ship_size > 1:
                while True:
                    try:
                        orientation = input(
                            'Положение корабля: - (минус) горизонтально, / (делить) вертикально:  ')
                        if orientation == '-' or orientation == '/':
                            break
                        else:
                            print('\033[1;33mНе понял, как поставить корабль.\033[0m')
                            mistake += 1
                            Field.dostal(mistake)
                            raise ValueError
                    except:
                        field.print_field(user_field)
                        print('Давай еще раз.\nНапоминаю- ', end='')
            mistake = 0
            while True:
                try:
                    x = int(input('Нос корабля:\nпо оси Х:  ')) - 1
                    y = int(input('по оси Y:  ')) - 1

                    if x < 0 or y < 0 or x >= field_size or y >= field_size:
                        raise ValueError
                    elif orientation == '-' and y > (field_size - ship.ship_size):
                        raise ValueError
                    elif orientation == '/' and x > (field_size - ship.ship_size):
                        raise ValueError

                    ship.x, ship.y = x, y

                    if field.check_ship_position(ship, orientation) == True:
                        count += 1
                        if orientation == '-':
                            for i in range(y, y + ship.ship_size):
                                user_field[x][i] = Cell.ship_cell
                        elif orientation == '/':
                            for j in range(x, x + ship.ship_size):
                                user_field[j][y] = Cell.ship_cell
                        else:
                            user_field[x][y] = Cell.ship_cell
                    else:
                        raise ValueError

                    field.print_field(user_field)
                    break

                except:
                    mistake += 1
                    Field.dostal(mistake)

    print('Начинаем сражение.')


'''>>>>Определим флот>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
ship1 = Ship(1, 4)  # size=1, quantity=4
ship2 = Ship(2, 3)
ship3 = Ship(3, 2)
ship4 = Ship(4, 1)
fleet = [ship4, ship3, ship2, ship1]
'''Создаем поля: игрока, АИ для показа игроку и АИ скрытое'''
field_size = battlefield_size()
field = Field(field_size)
user_field = field.get_field_type('User')
ai_field_show = field.get_field_type('AI show')
ai_field_hidden = field.get_field_type('AI hidden')

'''>>>>>>Запускаемся>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'''
set_vessels()

# field.print_field(user_field)
# user_field[0][0] = Cell.ship_cell
# user_field[1][1] = Cell.killed_cell
#
# ai_field_show[2][2] = Cell.killed_cell
# ai_field_show[3][4] = Cell.damaged_cell
#
#
# field.print_field(user_field)
# field.print_field(ai_field_show)
# field.print_field(ai_field_hidden)