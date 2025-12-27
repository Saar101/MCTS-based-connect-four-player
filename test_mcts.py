from connect_four_class import ConnectFour
from MCTSPlayer import MCTSPlayer


def snapshot_game(g: ConnectFour):
    """Take a deep-ish snapshot of the game state for equality checks."""
    board_copy = [col[:] for col in g.board]
    heights_copy = g.heights[:]
    return (board_copy, heights_copy, g.player, g.status)


def assert_game_restored_after_choose_move(iterations=200):
    g = ConnectFour()
    ai = MCTSPlayer()

    # Make a few moves so we test from a non-initial position
    g.make(3)
    g.make(3)
    g.make(2)

    before = snapshot_game(g)

    mv = ai.choose_move(g, iterations=iterations)
    assert mv in g.legal_moves(), f"choose_move returned illegal move: {mv}"

    after = snapshot_game(g)

    assert after[0] == before[0], "Board changed after choose_move (make/unmake bug)"
    assert after[1] == before[1], "Heights changed after choose_move (make/unmake bug)"
    assert after[2] == before[2], "Player changed after choose_move"
    assert after[3] == before[3], "Status changed after choose_move"

    print("OK: game restored after choose_move()")


def assert_terminal_state_handled():
    g = ConnectFour()
    ai = MCTSPlayer()

    # Create a terminal state by playing legal random moves
    import random
    while g.status == g.ONGOING:
        g.make(random.choice(g.legal_moves()))

    # In a terminal state, there are no legal moves; choose_move should return None
    mv = ai.choose_move(g, iterations=50)
    assert mv is None, f"Expected None on terminal state, got {mv}"

    print("OK: terminal state handled (choose_move returns None)")


def assert_ai_picks_immediate_win():
    g = ConnectFour()
    ai = MCTSPlayer(use_win_heuristic=True)

    # Build a position where RED has an immediate winning move in column 0 (vertical 4)
    # Sequence:
    # R:0, Y:1, R:0, Y:1, R:0, Y:2  -> now R can play 0 and win.
    g.make(0)  # R
    g.make(1)  # Y
    g.make(0)  # R
    g.make(1)  # Y
    g.make(0)  # R
    g.make(2)  # Y

    mv = ai.choose_move(g, iterations=50)
    assert mv == 0, f"Expected immediate winning move 0, got {mv}"

    # Also make sure game state did not change
    # (choose_move must restore state)
    assert g.status == g.ONGOING, "Game status changed after choose_move in immediate-win test"

    print("OK: immediate win heuristic works")


if __name__ == "__main__":
    print("Running MCTS tests...\n")
    assert_game_restored_after_choose_move(iterations=200)
    assert_terminal_state_handled()
    assert_ai_picks_immediate_win()
    print("\nAll tests passed ✅")
