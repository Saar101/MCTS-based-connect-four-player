import random
from MCTSNode import MCTSNode


class MCTSPlayer:
    """
    Implements MCTS to choose a move in ConnectFour.

    Add-on (as requested):
    If the AI is the first player (RED) and the board is empty,
    the first move is always column 3 (the strongest opening move).
    """

    def __init__(self, exploration_c=1.41421356237, use_win_heuristic=True):
        self.c = exploration_c
        self.use_win_heuristic = use_win_heuristic

    def choose_move(self, game, iterations):
        legal = game.legal_moves()

        # Terminal or no legal moves
        if game.status != game.ONGOING or not legal:
            return None

        # --------------------------------------------------
        # FIXED OPENING: AI starts as RED -> always play center
        # --------------------------------------------------
        if game.player == game.RED and sum(game.heights) == 0:
            return 3
        # --------------------------------------------------

        # Root player = who the AI is in THIS call
        root_player = game.player
        flip_for_root = (root_player == game.YELLOW)

        # Heuristics: immediate win / immediate block
        if self.use_win_heuristic:
            for mv in legal:
                if self._is_immediate_win(game, mv):
                    return mv

            blocking_move = self._find_blocking_move(game, legal)
            if blocking_move is not None:
                return blocking_move

        root = MCTSNode(parent=None, move=None, untried_moves=legal)

        for _ in range(iterations):
            node = root
            path_moves = []

            # 1) Selection
            while game.status == game.ONGOING and node.is_fully_expanded() and node.children:
                node = node.best_child_uct(self.c)
                game.make(node.move)
                path_moves.append(node.move)

            # Terminal during selection
            if game.status != game.ONGOING:
                result = game.status
                if flip_for_root:
                    result = -result
                self._backpropagate(node, result)
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

            # 3) Simulation
            rollout_moves = []
            while game.status == game.ONGOING:
                mv = self._rollout_policy(game)
                game.make(mv)
                rollout_moves.append(mv)

            result = game.status
            if flip_for_root:
                result = -result

            # 4) Backpropagation
            self._backpropagate(node, result)

            # Undo
            for mv in reversed(rollout_moves):
                game.unmake(mv)
            for mv in reversed(path_moves):
                game.unmake(mv)

        # Final choice: highest visit count
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

        if self.use_win_heuristic:
            for mv in legal:
                if self._is_immediate_win(game, mv):
                    return mv

            block = self._find_blocking_move(game, legal)
            if block is not None:
                return block

        return random.choice(legal)

    def _find_blocking_move(self, game, legal_moves):
        safe_moves = []
        bad_moves_exist = False

        for mv in legal_moves:
            game.make(mv)

            if game.status != game.ONGOING:
                game.player = game.other(game.player)
                game.unmake(mv)
                continue

            opponent_has_win = False
            for opp_mv in game.legal_moves():
                if self._is_immediate_win(game, opp_mv):
                    opponent_has_win = True
                    break

            game.unmake(mv)

            if opponent_has_win:
                bad_moves_exist = True
            else:
                safe_moves.append(mv)

        if bad_moves_exist and safe_moves:
            return random.choice(safe_moves)

        return None

    def _is_immediate_win(self, game, mv):
        current_player = game.player

        game.make(mv)
        won_now = (game.status == current_player)

        if game.status != game.ONGOING and game.player == current_player:
            game.player = game.other(game.player)

        game.unmake(mv)
        return won_now
