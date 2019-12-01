from players import Player
from minimax import complete_minimax
from evaluation import simple_eval


class SolvePlayer(Player):
    def __init__(self):
        '''Initialize a SolvePlayer

        self.memory is a dictionary in the form {game hash: (best move, expected value), ...}
        The player will use self.memory to look up the best moves to make.
        self.my_eval is a customized simple evaluation function to tell if a game is a win, loss, or tie
        '''
        self.memory = {}
        self.my_eval = lambda game, player_number: simple_eval(game, player_number, [1, -1, 0])

    def make_move(self, game):
        '''Makes a logically best move possible in a game.

        Solves unseen positions and then looks up solutions from its memory.
        '''
        try:
            # check to see if we've already solved this position
            game.make_move(self.memory[game.get_hash()][0])
        except KeyError:
            # we hadn't already solved it
            # solve it and remember the solution in memory
            self.memory.update(complete_minimax(game, -1, self.my_eval))
            # try again
            self.make_move(game)

    def __str__(self):
        return "<SolvePlayer object>"
