from game import Game

SKIP_MOVE = [-1, -1]
SKIP_MOVES = [SKIP_MOVE]

class Slot:
    def __init__(self, slots=None):
        if slots is None:
            slots = [None, None, None]
        # small, medium, big
        self.slots = slots

    def swap_players(self):
        for slot_index, slot in enumerate(self.slots):
            if slot is not None:
                self.slots[slot_index] = Game.get_other_player(slot)

    def get_copy(self):
        return Slot(self.slots[:])

    def get_possible_moves(self):
        ans = []
        for slot_index, slot in enumerate(self.slots):
            if slot is None:
                ans.append(slot_index)
        return ans

    def make_move(self, move, player):
        self.slots[move] = player

    def check_slot(self, number):
        return self.slots[number]

    def __str__(self):
        return str(self.slots)

class Otrio(Game):
    def __str__(self):
        def slot_str(slot):
            '''Returns a string that is three digits. Relies on the fact that players are numbers.
            0 is empty, 1 is player 0, and 2 is player 1'''
            ans = ""
            for slot_index in [0, 1, 2]:
                slot_value = slot.check_slot(slot_index)
                if slot_value is None:
                    ans += "0"
                else:
                    ans += str(int(slot_value) + 1)
            return ans

        ans = ""
        ans += f"Pieces left:{self.state[0]}\n"
        line = "-" * 11  + "\n"
        ans += line
        for slot_index, slot in enumerate(self.state[1]):
            ans += slot_str(slot) + " "
            if slot_index % 3 == 2:
                ans += "\n"
        ans += line
        return ans[:-1] # cutoff the last newline

    def get_initial_state(self):
        '''Return the initial state of the game.
        The state can be anything (object, string, number, etc.).
        '''
        # how many pieces left of each size for each player
        pieces = [[3, 3, 3], [3, 3, 3]]
        board = []
        for slot_index in range(9):
            board.append(Slot())
        board[4].make_move(1, 2) # put the blocker in the middle
        return (pieces, board)

    def get_state_hash(self):
        '''Return a unique string for the state'''
        return str([str(slot) for slot in self.state[1]])

    def swap_players(self):
        '''Swap the players in a game; returns nothing'''
        for slot in self.state[1]:
            slot.swap_players()
        self.state[0][0], self.state[0][1] = self.state[0][1], self.state[0][0]

    def get_copy(self):
        '''Return a copy of the object'''
        return Otrio((([pieces[:] for pieces in self.state[0]], [slot.get_copy() for slot in self.state[1]]), self.active_player))

    def get_possible_moves(self):
        '''Return a list of the possible moves that can be taken by the active player in the current state.
        Behavior is undefined when the game is complete.
        A single move can be anything (object, string, number, etc.).
        '''
        ans = []
        for slot_index, slot in enumerate(self.state[1]):
            for open_slot in slot.get_possible_moves():
                if self.state[0][self.active_player][open_slot] > 0:
                    ans.append([slot_index, open_slot])
        if not ans:
            # there are no moves available, so you can skip your turn
            ans = SKIP_MOVES
        return ans

    def make_move(self, action):
        '''Change the state of the game and update the active player based on the action.
        Assumes the action is valid. Behavior is undefined if action is not valid.
        '''
        slot_index, slot_move = action
        # if it's not a skip move
        if action != SKIP_MOVE:
            self.state[1][slot_index].make_move(slot_move, self.active_player)
            self.state[0][self.active_player][slot_move] -= 1
        self.active_player = Game.get_other_player(self.active_player)

    def who_won(self):
        '''Return 0 if player 0 won, 1 if player 1 won, -1 if there was a tie, and None if the game has not finished'''
        pieces, board = self.state
        # Detect single-slot wins
        for slot in board:
            inner_slot0 = slot.check_slot(0)
            inner_slot1 = slot.check_slot(1)
            inner_slot2 = slot.check_slot(2)

            if inner_slot0 is not None and inner_slot0 == inner_slot1 and inner_slot1 == inner_slot2:
                return inner_slot0

        def get_next_right(num):
            return num + 1

        def get_next_left(num):
            return num - 1

        def get_next_down(num):
            return num + 3

        def get_next_down_left(num):
            return get_next_left(get_next_down(num))

        def get_next_down_right(num):
            return get_next_right(get_next_down(num))

        for starting_pieces, get_next in [([0, 1, 2], get_next_down), ([0, 3, 6], get_next_right), ([0], get_next_down_right), ([2], get_next_down_left)]:
            # check for non-single-slot wins
            for slot_index in starting_pieces:
                first_slot_index = slot_index
                middle_slot_index = get_next(slot_index)
                last_slot_index = get_next(middle_slot_index)

                # check for ascending and descending wins
                # see if middle is taken - you can't have an ascending or descending win unless you have the middle of the middle
                possible_winner = board[middle_slot_index].check_slot(1)
                if possible_winner is not None:
                    # check for ascending and descending wins
                    for index1, index2 in [[0, 2], [2, 0]]:
                        if board[first_slot_index].check_slot(index1) == possible_winner and board[last_slot_index].check_slot(index2) == possible_winner:
                            return possible_winner

                # check for same-piece wins
                for piece_size in [0, 1, 2]:
                    possible_winner = board[first_slot_index].check_slot(piece_size)
                    if possible_winner is not None and board[middle_slot_index].check_slot(piece_size) == possible_winner and board[last_slot_index].check_slot(piece_size) == possible_winner:
                        return possible_winner

        # check for a tie
        possible_moves = self.get_possible_moves()
        if possible_moves == SKIP_MOVES:
            self.active_player = Game.get_other_player(self.active_player)
            # see if the other player has any moves they can make
            possible_moves = self.get_possible_moves()
            # switch the player back to normal
            self.active_player = Game.get_other_player(self.active_player)
            if possible_moves == SKIP_MOVES:
                # Nobody can move - it's a tie
                return -1

        return None

if __name__ == "__main__":
    minigame = Otrio()
    print(minigame.get_possible_moves()[:10])
    print(minigame)
    minigame.make_move([0, 0])
    minigame.make_move([1, 0])
    minigame.make_move([3, 0])
    minigame.make_move([1, 1])
    minigame.make_move([6, 0])
    minigame.make_move([1, 2])
    print(minigame)
    print(minigame.get_possible_moves())
    print(minigame.who_won())
