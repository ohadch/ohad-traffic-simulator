import os
import time
from typing import List, Any


class Object:

    def __init__(self):
        pass

    def __str__(self):
        raise NotImplementedError


class BorderObject(Object):
    def __init__(self):
        Object.__init__(self)

    def __str__(self):
        return '+'


class BoardPoint:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.object: [Object, None] = None

    def __str__(self):
        return str(self.object) if self.object else ' '


class Board:

    def __init__(self, num_rows: int, num_cols: int):
        self.matrix: List[List[BoardPoint]] = [
            [BoardPoint(col, row) for col in range(num_cols)]
            for row in range(num_rows)
        ]

    def draw(self) -> None:
        """
        Draws the board.
        """
        border_str = BorderObject().__str__()

        print(border_str * (len(self.matrix[0]) + 2))

        for row in self.matrix:
            row_strs_list = [point.__str__() for point in row]
            print("".join([border_str, *row_strs_list, border_str]))

        print(border_str * (len(self.matrix[0]) + 2))

class Game:

    def __init__(self):
        self.frame_rate_sec = 1
        self.board = Board(10, 10)

    def draw(self):
        self.board.draw()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        while True:
            self.clear_screen()
            self.draw()
            time.sleep(self.frame_rate_sec)
