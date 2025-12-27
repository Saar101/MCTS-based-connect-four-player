import random
from MCTSNode import MCTSNode


class MCTSPlayer:
    """
    Implements MCTS to choose a move in ConnectFour.

    - Uses make/unmake (single shared game state).
    - Nodes store only stats and the move from parent (no cloned states).
    - Result convention:
        +1 = RED wins
        -1 = YELLOW wins
         0 = draw
      (Matches ConnectFour.status in the provided implementation.)
    """

    def __init__(self, exploration_c=1.41421356237, use_win_heuristic=True):
        self.c = exploration_c
        self.use_win_heuristic = use_win_heuristic

    def choose_move(self, game, iterations):
        legal = game.legal_moves()
        if game.status != game.ONGOING or not legal:
            return None

        # ---- Immediate win heuristic (safe with make/unmake) ----
        if self.use_win_heuristic:
            for mv in legal:
                if self._is_immediate_win(game, mv):
                    return mv
        # --------------------------------------------------------

        root = MCTSNode(parent=None, move=None, untried_moves=legal)

        for _ in range(iterations):
            node = root
            path_moves = []   # moves made during selection/expansion (to undo later)

            # 1) Selection
            while game.status == game.ONGOING and node.is_fully_expanded() and node.children:
                node = node.best_child_uct(self.c)
                game.make(node.move)
                path_moves.append(node.move)

            # Terminal during selection -> backprop only
            if game.status != game.ONGOING:
                self._backpropagate(node, game.status)
                for mv in reversed(path_moves):
                    game.unmake(mv)
                continue

            # 2) Expansion
            if node.untried_moves:
                mv = random.choice(node.untried_moves)
                node.untried_moves.remove(mv)

                game.make(mv)
                path_moves.append(mv)

                node = node.add_child(mv, game.legal_moves())

            # 3) Simulation (rollout)
            rollout_moves = []
            while game.status == game.ONGOING:
                mv = self._rollout_policy(game)
                game.make(mv)
                rollout_moves.append(mv)

            result = game.status  # +1 / -1 / 0

            # 4) Backpropagation
            self._backpropagate(node, result)

            # Undo rollout, then undo selection/expansion path
            for mv in reversed(rollout_moves):
                game.unmake(mv)
            for mv in reversed(path_moves):
                game.unmake(mv)

        # Choose final move: highest visit count
        if not root.children:
            return random.choice(legal)

        return max(root.children.items(), key=lambda item: item[1].visits)[0]

    def _backpropagate(self, node, result):
        cur = node
        while cur is not None:
            cur.update(result)
            cur = cur.parent

    def _rollout_policy(self, game):
        legal = game.legal_moves()

        # Optional heuristic in rollout: immediate win
        if self.use_win_heuristic:
            for mv in legal:
                if self._is_immediate_win(game, mv):
                    return mv

        return random.choice(legal)

    def _is_immediate_win(self, game, mv):
        """
        Safely checks if playing mv wins immediately for the current player,
        without corrupting game state due to ConnectFour's terminal-move behavior.

        Returns True/False and restores game state exactly.
        """
        current_player = game.player

        game.make(mv)
        won_now = (game.status == current_player)

        # If game became terminal (win/draw), ConnectFour.make() does NOT switch player.
        # But ConnectFour.unmake() ALWAYS switches player.
        # So we "align" player before unmake so that unmake restores correctly.
        if game.status != game.ONGOING and game.player == current_player:
            game.player = game.other(game.player)

        game.unmake(mv)
        return won_now
