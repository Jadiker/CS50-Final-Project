'''
This code is not completely documented because it is not used in our website project.
I have included it as an example of a player you can create with the classes that are defined in our project.
For some time, this was used as our tic-tac-toe player, but was abandoned when position evaluation was coded.
'''

from players import Player

class IndexPlayer(Player):
    '''A basic class for any player whose moves can be made out of a dictionary'''
    def __init__(self, index_func):
        # a function that returns a dict of moves to remember
        self.index_func = index_func
        # see the `memory` property of the SolvePlayer class to understand how predetermined works
        self.predetermined = {}

    def make_move(self, game):
        self.add_predetermined(self.index_func(game, player_number=game.active_player))
        game.make_move(self.predetermined[game.get_hash()][0])

    def add_predetermined(self, more):
        # a template that subclasses can override
        # completely overwrites matching values in self.predetermined with new values from more
        self.predetermined.update(more)

if __name__ == "__main__":
    '''
    This is an example of how to create and use an IndexPlayer
    '''
    from performance_testers import test_against
    from evaluation import Evaluation, simple_eval
    from connect_four import ConnectFour
    from tic_tac_toe import TicTacToe
    from minimax import complete_minimax
    from players import RandomPlayer, HumanPlayer
    from basic_monte_carlo_player import BasicMonteCarloPlayer

    def my_index(game, player_number):
        ans = complete_minimax(game, 2, my_eval)
        print([(index, ans[index][0], ans[index][1].value) for index in ans])
        return ans

    test_against((IndexPlayer(my_index), BasicMonteCarloPlayer(5, 2)), ConnectFour, comment=6)
