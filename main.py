import random
from random import randint, shuffle


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1 for _ in range(length)]

    @property
    def tp(self):
        return self._tp

    @property
    def length(self):
        return self._length

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        if self._is_move:
            if self.tp == 1:
                self._x += go
            else:
                self._y += go

    @staticmethod
    def get_self_coord(ship):
        coord_x, coord_y = ship.get_start_coords()
        if ship.tp == 1:
            lst = [(y+coord_y, x+coord_x) for y in range(-1, 2) for x in range(-1, ship.length+1)]
        if ship.tp == 2:
            lst = [(y+coord_y, x+coord_x) for y in range(-1, ship.length+1) for x in range(-1, 2)]
        return lst

    @staticmethod
    def get_other_coord(ship):
        coord_x, coord_y = ship.get_start_coords()
        if ship.tp == 1:
            lst = [(coord_y, x+coord_x) for x in range(ship.length)]
        if ship.tp == 2:
            lst = [(y+coord_y, coord_x) for y in range(ship.length)]
        return lst

    def is_collide(self, ship):
        return any(map(lambda x: x in self.get_other_coord(ship), self.get_self_coord(self)))

    def is_out_pole(self, size):
        x, y = self.get_start_coords()
        if not (0 <= x < size) or not (0 <= y < size):
            return True
        if self.tp == 1 and x + self.length >= size:
            return True
        if self.tp == 2 and y + self.length >= size:
            return True
        return False

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = []
        self._pole = [[0 for _ in range(size)] for _ in range(size)]

    def init(self):
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(3, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2))]

        for ship in self._ships:
            if ship.tp == 1:
                lst = [(y, x) for y in range(-1, 2) for x in range(-1, ship.length+1)]

            if ship.tp == 2:
                lst = [(y, x) for y in range(-1, ship.length + 1) for x in range(-1, 2)]

            while True:
                i = randint(0, self._size - 1)
                j = randint(0, self._size - 1)
                if sum([self._pole[i+y][x+j] for y,x in lst if (i+y) < self._size and (x+j) < self._size]) == 0:
                    if ship.tp == 1:
                        if j+ship.length < self._size:
                            ship.set_start_coords(j, i)
                            self._pole[i][j:(j + ship.length)] = [1 for _ in range(ship.length)]
                            break
                    if ship.tp == 2:
                        if i+ship.length < self._size:
                            ship.set_start_coords(j, i)
                            for a in range(ship.length):
                                self._pole[i + a][j] = 1
                            break

    def get_ships(self):
        return self._ships

    def move_ships(self):
        ch = [-1, 1]
        for ship in self._ships:
            ship.move(ch[0])
            if any(map(ship.is_collide, (s for s in self._ships if s != ship))) or ship.is_out_pole(self._size):
                ship.move(ch[1])
                ship.move(ch[1])
                if any(map(ship.is_collide, (s for s in self._ships if s != ship))) or ship.is_out_pole(self._size):
                    ship.move(ch[0])
            shuffle(ch)

    def show(self):
        for cell in self.get_pole():
            print(*cell)

    def get_pole(self):
        pole = [[0 for _ in range(self._size)] for _ in range(self._size)]
        for ship in self._ships:
            x, y = ship.get_start_coords()
            if ship.tp == 1:
                pole[y][x:(x + ship.length)] = ship._cells
            if ship.tp == 2:
                for a in range(ship.length):
                    pole[y + a][x] = ship._cells[a]
        return pole


class SeaBattle:
    def __init__(self):
        self.computer_field = GamePole(SIZE_GAME_POLE)
        self.player_field = GamePole(SIZE_GAME_POLE)


SIZE_GAME_POLE = 10

pole = GamePole(SIZE_GAME_POLE)
pole.init()
pole.show()
p = pole.get_ships()
print()
pole.move_ships()
pole.show()
print()
for i in range(4):
    pole.move_ships()
    pole.show()
    print()
s = Ship(4, 1, 0, 0)
print(s.is_collide(Ship(3, 2, 0, 2)))





