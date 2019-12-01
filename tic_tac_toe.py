'''
By London Lowmanstone
Class for the game Tic-tac-toe
'''

from game import Game


class TicTacToe(Game):
    '''Class that implements the game tic-tac-toe.

    See the Game class documentation for explanations of each method.
    '''

    def get_initial_state(self):
        '''The state of the game is a list of nine numbers.

        Each number represents which player has moved in a particular slot.
        X is 1, O is 0, and -1 represents an empty slot.

        The slots are labeled as follows:
        0 1 2
        3 4 5
        6 7 8

        For example, if the game looks like:
        X - O
        X O -
        - X O

        then the state of the game will be
        [1, -1, 0, 1, 0, -1, -1, 1, 0]
        '''
        # return an empty board
        return [-1] * 9

    def get_state_hash(self):
        '''Return a human-readable hash.

        This hash is also used by the __str__ method below, so edit with caution.
        '''
        # technically, this doesn't have to be human-readable, but it was useful for debugging
        string_list = ["O", "X", " "]
        ans = ""
        for val in self.state:
            ans += string_list[val]
        return ans

    def get_json_dict(self):
        # the dictionary we will return
        ans = {}
        # iterate through each slot on the board
        for i, val in enumerate(self.state):
            # the key is the number of the slot
            # the value is the player who moved in that slot
            ans[str(i)] = val
        # add the active player key and value
        ans["active_player"] = self.active_player
        # add the winner key and value
        winner = self.who_won()
        if winner is None:
            ans["winner"] = -2
        else:
            ans["winner"] = winner

        # return the result
        return ans

    def swap_players(self):
        self.state = [Game.get_other_player(val) if val >= 0 else -1 for val in self.state]

    def get_copy(self):
        return TicTacToe((self.state[:], self.active_player))

    def get_possible_moves(self):
        return [i for i in range(len(self.state)) if self.state[i] == -1]

    def make_move(self, action):
        self.state[action] = self.active_player
        self.active_player = Game.get_other_player(self.active_player)

    def who_won(self):
        if -1 in self.state:
            # game is not done, default to unfinished
            ans = None
        else:
            # game is done, default to tie
            ans = -1

        # the current player number we're checking to see if they won
        player = None
        '''
        When checking is 0 we check rows
        When checking is 1 we check columns
        When checking is 2 we check top left diagonal
        When checking is 3 we check top right diagonal
        '''
        # upgrade: less duplicate code
        for checking in range(4):
            # the number of the symbol in the series we're looking for
            for i in range(3):
                if checking < 2:
                    # checking rows and columns
                    for j in range(3):
                        if checking == 0:
                            # checking rows
                            # iterate through the row
                            val = self.state[i * 3 + j]
                        else:
                            # checking == 1
                            # checking columns
                            # iterate through the column
                            val = self.state[i + j * 3]

                        if val == -1:
                            # person doesn't have the entire row or column
                            break
                        else:
                            # if it just started checking this line
                            if j == 0:
                                # whoever has the first space must have the other two to win
                                player = val
                            # if the player doesn't have a win
                            elif not val == player:
                                break
                            # if the player does have a win
                            elif j == 2:
                                return player
                else:
                    # checking diagonals
                    if checking == 2:
                        # want it to check slots 0, 4, 8
                        val = self.state[i * 4]
                    else:
                        # checking == 3
                        # want it to check slots 2, 4, 6
                        val = self.state[(i + 1) * 2]

                    if val == -1:
                        # person doesn't have the row or column
                        break
                    else:
                        # if we just started checking this diagonal
                        if i == 0:
                            # whoever has the first space must have the other two to win
                            player = val
                        elif not val == player:
                            # if the player doesn't have a win
                            break
                        elif i == 2:
                            # if the player does have a win
                            return player
        return ans

    def __str__(self):
        if self.active_player == 0:
            this = self
        else:
            this = self.get_swapped_copy()

        # replace the spaces in the hash with dashes to make it move human-readable
        ans = this.get_hash().replace(" ", "-")
        # format in the rows
        return "{}'s turn:\n{}\n{}\n{}".format(["O", "X"][self.active_player], ans[0:3], ans[3:6], ans[6:9])
