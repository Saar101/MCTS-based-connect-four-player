from connect_four_class import ConnectFour
from MCTSPlayer import MCTSPlayer


def ask_human_move(game: ConnectFour) -> int:
    while True:
        try:
            mv = int(input("Choose a column (0-6): ").strip())
            if mv in game.legal_moves():
                return mv
            print("Illegal move. Legal moves are:", game.legal_moves())
        except ValueError:
            print("Please enter a number 0-6.")


def main():
    game = ConnectFour()

    # Configure AI strength/speed here:
    iterations = 800
    ai = MCTSPlayer(exploration_c=1.4, use_win_heuristic=True)

    print("=== Connect Four: You vs MCTS ===")
    print("Board shows: R = RED, Y = YELLOW, . = empty")
    print("Columns are 0..6\n")

    # Choose side
    side = input("Do you want to play as RED (first)? [y/n]: ").strip().lower()
    human_is_red = (side == "y" or side == "yes")

    print("\nGame start!\n")

    while game.status == game.ONGOING:
        print(game)
        print("\nLegal moves:", game.legal_moves())
        print("Turn:", "RED" if game.player == game.RED else "YELLOW")

        human_turn = (game.player == game.RED and human_is_red) or (game.player == game.YELLOW and not human_is_red)

        if human_turn:
            mv = ask_human_move(game)
            game.make(mv)
        else:
            mv = ai.choose_move(game, iterations=iterations)
            print(f"AI chooses: {mv}  (iterations={iterations})")
            game.make(mv)

        print("\n" + "-" * 40 + "\n")

    # Game over
    print(game)
    if game.status == game.RED:
        print("\nResult: RED wins!")
    elif game.status == game.YELLOW:
        print("\nResult: YELLOW wins!")
    else:
        print("\nResult: Draw!")


if __name__ == "__main__":
    main()
