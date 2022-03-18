from objects.core import Object

from utils import Coordinates


class WallObject(Object):

    def __init__(self, center: Coordinates):
        super().__init__(center, "#")

    def update(self):
        pass
