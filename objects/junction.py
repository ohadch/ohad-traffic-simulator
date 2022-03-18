import random
from enum import Enum

from termcolor import colored

from objects.core import Object
from utils import Coordinates


class JunctionState(Enum):
    RED = "RED"
    GREEN = "GREEN"


class JunctionObject(Object):
    __char = "*"

    def __init__(self, position: Coordinates, initial_state: JunctionState):
        self.state: JunctionState = initial_state
        Object.__init__(self, position, self.__get_char_by_state())
        self.ticks_until_flip = 0

    def __get_char_by_state(self):
        if self.state == JunctionState.RED:
            return colored(self.__char, "red")
        else:
            return colored(self.__char, "green")

    def update(self):
        if self.ticks_until_flip > 0:
            self.ticks_until_flip -= 1
        else:
            self.state = JunctionState.RED if self.state == JunctionState.GREEN else JunctionState.GREEN
            self.ticks_until_flip = random.randint(5, 10)

        self.char = self.__get_char_by_state()
