import datetime
import os
import time


class Game:

    def __init__(self):
        self.frame_rate_sec = 1

    def render(self):
        print(datetime.datetime.now())

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        while True:
            self.clear_screen()
            self.render()
            time.sleep(self.frame_rate_sec)
