'''
By London Lowmanstone
Class for Onitama
'''
import random
from game import Game

STUDENT_STYLE = "student"
MASTER_STYLE = "master"
MIDDLE_CARD_INDEX = 2

PLAYERS = (0, 1)

ENEMY_ARCH_POSITIONS = ((5, 3), (1, 3))

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

crab_card = Card("Crab", [(0, 1), (-2, 0), (2, 0)])
rabbit_card = Card("Rabbit", [(-1, -1), (1, 1), (2, 0)])
frog_card = Card("Frog", [(1, -1), (-1, 1), (-2, 0)])
goose_card = Card("Goose", [(-1, 0), (1, 0), (-1, 1), (1, -1)])
eel_card = Card("Eel", [(-1, 1), (-1, -1), (1, 0)])

class State:
    def __init__(self, hands, board, pawns, master_pawns):
        self.board = board
        # player 0, player 1, middle
        self.hands = hands
        self.pawns = pawns
        self.master_pawns = master_pawns

    def __str__(self):
        ans = ""
        ans += "Board:\n"

        for position, pawn in self.board.items():
            ans += f"{position}: {str(pawn)}\n"

        ans += "\nHands:\n"
        for player in PLAYERS:
            hand = self.hands[player]
            ans += f"Player {player}'s hand:\n{str(hand[0])}\n{str(hand[1])}\n"

        ans += f"\nMiddle card:\n{str(self.hands[MIDDLE_CARD_INDEX])}\n"
        return ans

class Pawn:
    def __init__(self, position, style, board, player, index):
        self.style = style
        self.position = position
        self.board = board
        self.player = player
        self.index = index
        self.update_board()

    def __str__(self):
        return f"<Player {self.player}'s {self.style} pawn at {self.position} (index {self.index})>"

    def update_board(self):
        self.board[self.position] = self

    def check_move(self, move):
        # new position
        if self.player == 1:
            # moves for player 1 are flipped
            move = tuple(-1 * coord for coord in move)

        target = tuple(sum(coord) for coord in zip(self.position, move))
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
        self.position = target
        self.update_board()


class Onitama(Game):
    def __str__(self):
        return f"PLayer {self.active_player}'s turn.\n{str(self.state)}\n"

    def get_initial_state(self):
        '''Return the initial state of the game.
        The state can be anything (object, string, number, etc.).
        '''
        hands = [[crab_card, rabbit_card], [goose_card, eel_card], frog_card]

        MASTER_COLUMN = 3
        MASTER_INDEX = 4
        STUDENT_COLUMNS = [1, 2, 4, 5]
        board = {}
        pawns = {0: [], 1: []}
        master_pawns = {}
        for player in PLAYERS:
            # player 0 is on row 1, the bottom row
            # player 1 is on row 5, the top row
            row = player * 4 + 1

            # place students
            for index, column in enumerate(STUDENT_COLUMNS):
                # x, y
                position = (column, row)
                pawns[player].append(Pawn(position, STUDENT_STYLE, board, player, index))

            # place master
            position = (MASTER_COLUMN, row)
            master_pawn = Pawn(position, MASTER_STYLE, board, player, MASTER_INDEX)
            pawns[player].append(master_pawn)
            master_pawns[player] = master_pawn

        return State(hands, board, pawns, master_pawns)


    def get_state_hash(self):
        '''Return a unique string for the state.
        Only needed for players trying to solve the game,
        ...so I will not be implementing it for this class.'''
        raise NotImplementedError

    def get_json_dict(self):
        '''Get the json for this game in such a way that the browser can display it.
        This is only necessary for the games we are displaying on our website.
        For these games, this function should return a dictionary in the form:
        {space number: player number, ..., "active_player": active player, "winner": winner}
        To see how this is implemented in more detail, see tic_tac_toe.py.
        '''
        raise NotImplementedError

    def swap_players(self):
        '''Swap the players in a game; returns nothing'''
        raise NotImplementedError

    def get_copy(self):
        '''Return a copy of the object'''
        raise NotImplementedError

    def get_possible_moves(self):
        '''Return a list of the possible moves that can be taken by the active player in the current state.
        Behavior is undefined when the game is complete.
        A single move can be anything (object, string, number, etc.).
        '''
        ans = []
        hand = self.state.hands[self.active_player]
        for card_index, card in enumerate(hand):
            for move in card.moves:
                for pawn in self.state.pawns[self.active_player]:
                    try:
                        pawn_target, captured_pawn = pawn.check_move(move)
                    except InvalidMoveError:
                        continue
                    ans.append((card_index, pawn, pawn_target, captured_pawn))
        return ans

    def make_move(self, action):
        '''Change the state of the game and update the active player based on the action.
        Assumes the action is valid. Behavior is undefined if action is not valid.
        '''
        card_index, pawn, pawn_target, captured_pawn = action
        opponent = Game.get_other_player(self.active_player)
        active_player_hand = self.state.hands[self.active_player]

        active_player_hand.append(self.state.hands[MIDDLE_CARD_INDEX])
        used_card = active_player_hand.pop(card_index)
        self.state.hands[MIDDLE_CARD_INDEX] = used_card

        pawn.move(pawn_target)
        if captured_pawn:
            opponent_pawns = self.state.pawns[Game.get_other_player(self.active_player)]
            removed_pawn = opponent_pawns.pop(captured_pawn.index)
            assert removed_pawn == captured_pawn
            for pawn in opponent_pawns[captured_pawn.index:]:
                # due to the pop, the indexes of all other pawns have been
                pawn.index -= 1
            if captured_pawn.style == MASTER_STYLE:
                del self.state.master_pawns[opponent]

        self.active_player = opponent

    def who_won(self):
        '''Return 0 if player 0 won, 1 if player 1 won, -1 if there was a tie, and None if the game has not finished'''
        if len(self.state.master_pawns) < 2:
            # return the player who still has their master pawn
            # see https://stackoverflow.com/a/46042617
            return next(iter(self.state.master_pawns))

        for player, arch_position in enumerate(ENEMY_ARCH_POSITIONS):
            try:
                arch_pawn = self.state.board[arch_position]
                if arch_pawn.style == MASTER_STYLE and arch_pawn.player == player:
                    return player
            except KeyError:
                # there is no pawn in the arch position
                pass

        return None


if __name__ == "__main__":
    game = Onitama()
    print(game)
    print(game.get_possible_moves())
    print()
    for move in game.get_possible_moves():
        card_index, pawn, pawn_target, captured_pawn = move
        print(f"<Using {game.state.hands[game.active_player][card_index]} move {pawn} to {pawn_target} capturing {captured_pawn}>")
        # print(card_index, pawn, pawn_target, captured_pawn)
