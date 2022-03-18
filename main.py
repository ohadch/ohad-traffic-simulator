import game_globals

from game import Game, Board


def main():
    frame_rate_sec = 0.3

    game_globals.BOARD = Board(
        map_size_x=21,
        map_size_y=21,
    )

    game_globals.GAME = Game(
        board=game_globals.BOARD,
        frame_rate_sec=frame_rate_sec
    )

    game_globals.GAME.run()


if __name__ == '__main__':
    main()
