from game import Game, Board


def main():
    frame_rate_sec = 0.027

    board = Board(
        map_size_x=11,
        map_size_y=11,
    )

    Game(
        board=board,
        frame_rate_sec=frame_rate_sec
    ).run()


if __name__ == '__main__':
    main()