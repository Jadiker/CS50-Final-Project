'''
By London Lowmanstone
Class for games
'''
import random


class Game():
    '''A class that defines two-player games
    If someone writes a class that implements the non-implemented methods below, any of the players can play that game
    That's what makes this project so cool; all of our algorithms are completely generalizable to any two-player game
    In addition, the computers learn how to play with no human heuristics - "tabula rasa"
    '''

    @classmethod
    def get_other_player(cls, player):
        '''Returns the number of the other player (either a 0 or 1)'''
        return (player + 1) % 2

    def __init__(self, state_and_player=None):
        '''Initialize the game with a state'''
        if state_and_player is None:
            self.state = self.get_initial_state()
            self.active_player = 0
        else:
            self.state, self.active_player = state_and_player

    def get_hash(self):
        '''Return a unique string for the state as if player 0 was making the next move'''
        if self.active_player == 1:
            return self.get_swapped_copy().get_state_hash()
        else:
            return self.get_state_hash()

    def get_next_level(self):
        '''Return a list of all the games that can be reached within one action from the current game'''
        ans = []
        actions = self.get_continue_moves()
        for action in actions:
            copy = self.get_copy()
            copy.make_move(action)
            ans.append(copy)
        return ans

    def get_complexity(self, depth):
        '''Determines the number of possible final states a game has with a depth search of size depth
        If you want the total complexity, use depth=-1
        upgrade: this does not work yet for games with repeated states, such as Chopsticks
        '''
        if depth == 1:
            # if you have no descendants, return 1 since you're the only final state
            return len(self.get_next_level()) or 1
        elif depth != 0:
            next_level = self.get_next_level()
            if len(next_level) == 0:
                # this is the only final state here
                return 1
            else:
                # return the number of final states of your descendants
                return sum([game.get_complexity(depth - 1) for game in next_level])
        else:
            return 0

    def get_continue_moves(self):
        '''Like get_possible_moves, except it only gets the actions if the game is not complete
        Removes the undefined behavior allowed in get_possible_moves
        '''
        if self.who_won() is None:
            return self.get_possible_moves()
        else:
            return []

    def get_swapped_copy(self):
        '''Get a copy of the game with the players swapped'''
        ans = self.get_copy()
        ans.swap_players()
        return ans

    def get_moved_copy(self, move):
        '''Get a copy of the game with the given move made'''
        ans = self.get_copy()
        ans.make_move(move)
        return ans

    def get_initial_state(self):
        '''Return the initial state of the game.
        The state can be anything (object, string, number, etc.).
        '''
        raise NotImplementedError

    def get_state_hash(self):
        '''Return a unique string for the state'''
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
        raise NotImplementedError

    def make_move(self, action):
        '''Change the state of the game and update the active player based on the action.
        Assumes the action is valid. Behavior is undefined if action is not valid.
        '''
        raise NotImplementedError

    def who_won(self):
        '''Return 0 if player 0 won, 1 if player 1 won, -1 if there was a tie, and None if the game has not finished'''
        raise NotImplementedError
