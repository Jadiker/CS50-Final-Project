'''
By London Lowmanstone
Class for Onitama
'''
from copy import deepcopy
import random
from game import Game
from evaluation import Evaluator, Evaluation

STUDENT_STYLE = "student"
SENSEI_STYLE = "*sensei"
MIDDLE_CARD_INDEX = 2

PLAYERS = (0, 1)

ENEMY_ARCH_POSITIONS = ((3, 5), (3, 1))

class InvalidMoveError(RuntimeError):
    pass

class Card:
    def __init__(self, name, moves):
        self.name = name
        # [move, ...]
        # where a move is [direction to move pawn, ...]
        # for example, moving to the top right would be [(1, -1)] and moving right 2 spaces would be [(1, 0), (1, 0)]
        # the moves have to be done in a way that if any move in the sequence would go off the board
        # ...the final move would go off the board
        # this just means that the moves can't backtrack, since the board is rectangular
        self.moves = moves

    def __str__(self):
        def cut_edges(string):
            return string[1:-1]

        return f"<Card - {self.name}: {cut_edges(str(self.moves))}>"

    def __deepcopy__(self, memo):
        return type(self)(deepcopy(self.name, memo), deepcopy(self.moves, memo))

crab_card = Card("Crab", [(0, 1), (-2, 0), (2, 0)])
rabbit_card = Card("Rabbit", [(-1, -1), (1, 1), (2, 0)])
frog_card = Card("Frog", [(1, -1), (-1, 1), (-2, 0)])
goose_card = Card("Goose", [(-1, 0), (1, 0), (-1, 1), (1, -1)])
eel_card = Card("Eel", [(-1, 1), (-1, -1), (1, 0)])


class Pawn:
    def __init__(self, position, style, board, player, index):
        self.position = position
        self.style = style
        self.board = board
        self.player = player
        self.index = index
        self.update_board()

    def __str__(self):
        # TODO fix
        return f"<Player {self.player}'s {self.style} pawn at {self.position} (id: {id(self)})>"

    def __deepcopy__(self, memo):
        return type(self)(deepcopy(self.position, memo), deepcopy(self.style, memo),
                          deepcopy(self.board, memo), deepcopy(self.player, memo),
                          deepcopy(self.index, memo))

    def update_board(self, previous_position=None):
        if previous_position:
            assert previous_position != self.position, f"Pawn did not move from {previous_position}"
            del self.board[previous_position]
        self.board[self.position] = self

    def check_move(self, card_move):
        # new position
        if self.player == 1:
            # card moves for player 1 are flipped
            card_move = tuple(-1 * coord for coord in card_move)

        target = tuple(sum(coord) for coord in zip(self.position, card_move))
        assert target != self.position, f"Target {target} would not move {self}"
        for coord in target:
            if not (1 <= coord <= 5):
                # target position is not on the board
                raise InvalidMoveError

        captured_pawn = self.board.get(target, None)
        if captured_pawn and captured_pawn.player == self.player:
            raise InvalidMoveError

        return target, captured_pawn

    def move(self, target):
        '''Move the pawn to a position on the board'''
        print(f"PAWN with ID {id(self)} is making move in board {id(self.board)}")
        previous_position = self.position
        self.position = target
        self.update_board(previous_position)
        assert self.board[self.position] == self
        assert previous_position not in self.board

class State:
    def __init__(self, hands, board, pawns, sensei_pawns):
        self.board = board
        # player 0, player 1, middle
        self.hands = hands
        self.pawns = pawns
        self.sensei_pawns = sensei_pawns

    def __str__(self):
        ans = ""
        ans += "Board:\n"

        for position, pawn in self.board.items():
            ans += f"{position}: {str(pawn)}\n"

        ans += "\nHands:"
        for player in PLAYERS:
            hand = self.hands[player]
            ans += f"\nPlayer {player}'s hand:\n{str(hand[0])}\n{str(hand[1])}\n"

        ans += f"\nMiddle card:\n{str(self.hands[MIDDLE_CARD_INDEX])}\n"
        return ans

    def __deepcopy__(self, memo):
        return type(self)(deepcopy(self.hands, memo), deepcopy(self.board, memo),
                          deepcopy(self.pawns, memo), deepcopy(self.sensei_pawns, memo))

class Onitama(Game):
    def __str__(self):
        return f"PLayer {self.active_player}'s turn.\n{str(self.state)}\n"

    def get_initial_state(self):
        '''Return the initial state of the game.
        The state can be anything (object, string, number, etc.).
        '''
        hands = [[crab_card, rabbit_card], [goose_card, eel_card], frog_card]

        SENSEI_COLUMN = 3
        SENSEI_INDEX = 4
        STUDENT_COLUMNS = [1, 2, 4, 5]
        board = {}
        pawns = {0: [], 1: []}
        sensei_pawns = {}
        for player in PLAYERS:
            # player 0 is on row 1, the bottom row
            # player 1 is on row 5, the top row
            row = player * 4 + 1

            # place students
            for index, column in enumerate(STUDENT_COLUMNS):
                # x, y
                position = (column, row)
                pawns[player].append(Pawn(position, STUDENT_STYLE, board, player, index))

            # place sensei
            position = (SENSEI_COLUMN, row)
            sensei_pawn = Pawn(position, SENSEI_STYLE, board, player, SENSEI_INDEX)
            pawns[player].append(sensei_pawn)
            sensei_pawns[player] = sensei_pawn

        return State(hands, board, pawns, sensei_pawns)

    def get_state_hash(self):
        '''Return a unique string for the state.
        Only needed for players trying to solve the game,
        ...so I will not be implementing it (smartly) for this class.'''
        return hash(self.state)

    def get_json_dict(self):
        '''Get the json for this game in such a way that the browser can display it.
        This is only necessary for the games we are displaying on our website.
        For these games, this function should return a dictionary in the form:
        {space number: player number, ..., "active_player": active player, "winner": winner}
        To see how this is implemented in more detail, see tic_tac_toe.py.
        '''
        raise NotImplementedError

    def swap_players(self):
        '''Swap the players in a game; returns nothing
        This is never used, so I'm not implementing it.'''
        # new_hands = (self.hands[1], self.hands[0], self.hands[MIDDLE_CARD_INDEX])
        # self.state.hands = new_hands
        # new_pawns = {0: [], 1: []}
        # for pawns if self.state.pawns:
        #     for pawn in self.state.pawns:
        raise NotImplementedError

    def _assert_pawns_in_board(self):
        for pawns in self.state.pawns.values():
            for pawn in pawns:
                assert pawn.position in self.state.board, f"Pawn {pawn} disappeared from the board {board_to_string(self.state.board)}"

    def _assert_move(self, move):
        card_index, card, pawn, pawn_target, captured_pawn = move
        assert (not captured_pawn) or (self.state.board[pawn_target] == captured_pawn.position), f"The move is to {pawn_target}, but the captured pawn is at {captured_pawn.position}"
        assert (not captured_pawn) or (captured_pawn.player != pawn.player), f"Pawn {pawn} can't capture itself"
        assert pawn_target != pawn.position, f"The pawn {pawn} must actually move"

    def get_copy(self):
        '''Return a copy of the object'''
        copy = Onitama()
        copy.state = deepcopy(self.state)
        copy.active_player = self.active_player
        copy._assert_pawns_in_board()
        for pawns in self.state.pawns.values():
            for pawn in pawns:
                for copy_pawns in copy.state.pawns.values():
                    for copy_pawn in copy_pawns:
                        assert id(copy_pawn.board) == id(copy.state.board), "Pawn did not inherit correct board"
                        assert pawn != copy_pawn
                        assert pawn.board != copy_pawn.board
                        assert id(pawn) != id(copy_pawn)
                        # TODO delete
                        # print("Pair:")
                        # print(id(pawn))
                        # print(id(copy_pawn))
                        # print()
        assert id(copy.state.board) != id(self.state.board)
        print("ids")
        print(f"original: {id(self.state.board)}")
        print(f"copy:     {id(copy.state.board)}")
        return copy

    def get_possible_moves(self):
        '''Return a list of the possible moves that can be taken by the active player in the current state.
        Behavior is undefined when the game is complete.
        A single move can be anything (object, string, number, etc.).
        '''
        self._assert_pawns_in_board()
        ans = []
        hand = self.state.hands[self.active_player]
        for card_index, card in enumerate(hand):
            for card_move in card.moves:
                for pawn in self.state.pawns[self.active_player]:
                    try:
                        pawn_target, captured_pawn = pawn.check_move(card_move)
                    except InvalidMoveError:
                        continue
                    move = (card_index, card, pawn, pawn_target, captured_pawn)
                    self._assert_move(move)
                    ans.append(move)
        self._assert_pawns_in_board()
        for move in ans:
            self._assert_move(move)
        return ans

    def make_move(self, action):
        '''Change the state of the game and update the active player based on the action.
        Assumes the action is valid. Behavior is undefined if action is not valid.
        '''
        # TODO delete
        print("-------- MAKING MOVE ---------")
        print("----------BOARD----------")
        print(f"(board id is {id(self.state.board)})")
        print(board_to_string(self.state.board))
        print("-----GAME:------")
        print(self)
        print("-------MOVE-------")
        print(move_to_string(action))
        assert len(self.state.sensei_pawns) == 2, "Invalid move - game is already over"
        self._assert_pawns_in_board()
        self._assert_move(action)

        card_index, card, pawn, pawn_target, captured_pawn = action
        assert (not captured_pawn) or (self.state.board[pawn_target] == captured_pawn.position), f"The move is to {pawn_target}, but the captured pawn is at {captured_pawn.position}"
        opponent = Game.get_other_player(self.active_player)
        active_player_hand = self.state.hands[self.active_player]

        active_player_hand.append(self.state.hands[MIDDLE_CARD_INDEX])
        used_card = active_player_hand.pop(card_index)
        self.state.hands[MIDDLE_CARD_INDEX] = used_card

        pawn.move(pawn_target)
        if captured_pawn:
            assert pawn.position == captured_pawn.position, f"The pawn moved to {pawn.position}, "
            opponent_pawns = self.state.pawns[Game.get_other_player(self.active_player)]
            removed_pawn = opponent_pawns.pop(captured_pawn.index)
            assert removed_pawn == captured_pawn, f"{removed_pawn} != {captured_pawn}"
            for pawn in opponent_pawns[captured_pawn.index:]:
                # due to the pop, the indexes of all other pawns have been
                pawn.index -= 1
            if captured_pawn.style == SENSEI_STYLE:
                del self.state.sensei_pawns[opponent]
                assert self.state.sensei_pawns, "Both sensei pawns have been removed!"

        self.active_player = opponent
        self._assert_pawns_in_board()

    def who_won(self):
        '''Return 0 if player 0 won, 1 if player 1 won, -1 if there was a tie, and None if the game has not finished'''
        if len(self.state.sensei_pawns) < 2:
            # return the player who still has their sensei pawn
            # see https://stackoverflow.com/a/46042617
            return next(iter(self.state.sensei_pawns))

        for player, arch_position in enumerate(ENEMY_ARCH_POSITIONS):
            try:
                arch_pawn = self.state.board[arch_position]
                if arch_pawn.style == SENSEI_STYLE and arch_pawn.player == player:
                    return player
            except KeyError:
                # there is no pawn in the arch position
                pass

        return None


class PawnCountingEvaluator(Evaluator):
    '''Evaluator that counts how many pawns you have left'''
    def __init__(self, win_loss_rewards=[100, -100]):
        self.win_loss_rewards = win_loss_rewards

    def evaluate(self, game, player_number):
        winner = game.who_won()
        if winner is None:
            # return the number of pawns that player has
            return Evaluation(len(game.state.pawns[player_number]))
        else:
            if winner == player_number:
                return Evaluation(self.win_loss_rewards[0])
            else:
                return Evaluation(self.win_loss_rewards[1])


def move_to_string(move):
    card_index, card, pawn, pawn_target, captured_pawn = move
    if pawn_target in ENEMY_ARCH_POSITIONS:
        arch_owner = Game.get_other_player(ENEMY_ARCH_POSITIONS.index(pawn_target))
        pawn_target = f"Player {arch_owner}'s *arch at {pawn_target}"
    ans = f"{card.name} - moving {pawn.style} pawn at {pawn.position} to {pawn_target}"
    if captured_pawn:
        ans += f" capturing {str(captured_pawn)[1:-1]}"
    return ans

def board_to_string(board):
    ans = "\n<Board:\n"
    for pawn, position in board.items():
        ans += f"{position}: {pawn}\n"
    ans += ">"
    return ans


if __name__ == "__main__":
    game = Onitama()
    # print(game)
    # for move in game.get_possible_moves():
    #     print(move_to_string(move))
        # card_index, pawn, pawn_target, captured_pawn = move
        # print(f"<Using {game.state.hands[game.active_player][card_index]} move {pawn} to {pawn_target} capturing {captured_pawn}>")
        # # print(card_index, pawn, pawn_target, captured_pawn)

    copy = game.get_copy()
    for copy_pawns in copy.state.pawns.values():
        for copy_pawn in copy_pawns:
            print(copy_pawn)
            assert copy_pawn not in game.state.pawns[0]
            assert copy_pawn not in game.state.pawns[1]
