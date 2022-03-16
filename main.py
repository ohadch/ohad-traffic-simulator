from game import Game, Board


def main():
    frame_rate_sec = 1
    board = Board(
        num_rows=30,
        num_cols=30
    )

    Game(
        board=board,
        frame_rate_sec=frame_rate_sec
    ).run()


if __name__ == '__main__':
    main()