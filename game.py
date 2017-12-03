'''
By London Lowmanstone
Class for games
'''
import random

class Game():
    @classmethod
    def get_other_player(cls, player):
        '''Returns the number of the other player (either a 0 or 1)'''
        return (player + 1) % 2
    
    '''
    TODO documentation
    '''
    def __init__(self, state_and_player=None):
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
        '''Return a list of all the games that can be reached with one action from the current game'''
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
        TODO this does not work yet for games with repeated states, such as Chopsticks
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
                return sum([game.get_complexity(depth-1) for game in next_level])
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
        ans = self.get_copy()
        ans.swap_players()
        return ans
        
    def get_moved_copy(self, move):
        ans = self.get_copy()
        ans.make_move(move)
        return ans
        
    def get_active_zero_copy(self):
        if self.active_player == 0:
            return self.get_copy()
        else:
            return self.get_swapped_copy()
    
    def get_initial_state(self):
        raise NotImplementedError
    
    def get_state_hash(self):
        '''Return a unique string for the state'''
        raise NotImplementedError
    
    def get_properties(self):
        '''This returns a mutable list of numbers of constant length describing the state, or None
        This is what we'd feed into a neural net to learn about the game
        
        For example, if the game really was player 1's turn to move, it would swap all the pieces and then return the same values
        ...as if player 0 had made all the moves that player 1 did and vice versa
        
        TODO this will need to be defined better if/when we actually start using neural networks
        TODO determine if this can be mutable
        '''
        raise NotImplementedError
        
    def swap_players(self):
        '''Swap the players in a game. Returns nothing.'''
        raise NotImplementedError
        
    def get_copy(self):
        '''Return a copy of the object'''
        raise NotImplementedError
    
    def get_possible_moves(self):
        '''Return a list of the possible actions that can be taken by self.active_player in the self.state state
        Behavior is undefined when the game is complete
        '''
        raise NotImplementedError
        
    def make_move(self, action):
        '''Change the state of the game and update the active player based on the action
        Assumes the action is valid. Behavior is undefined if action is not valid.
        '''
        raise NotImplementedError
        
    def who_won(self):
        '''Return 0 if player 0 won, 1 if player 1 won, -1 if there was a tie, and None if the game has not finished'''
        raise NotImplementedError
        

if __name__ == "__main__":
    from tic_tac_toe import TicTacToe
    print("Working...")
    #print("Number of end states in TicTacToe: {}".format(TicTacToe().get_complexity(-1)))
    from connect_four import ConnectFour
    print(ConnectFour.get_random_game())