'''
This code is not completely documented because it is not used in our website project.
This is an example of a class that we did not end up using in our final version.
This class was used for most game testing and was the best player for connect4 until
...the AdvisedMonteCarloPlayer was programmed.
You can try playing against a BasicMonteCarloPlayer(5, 2) and see how it works!
(Use the code provided in performance_testers to do this.)
'''

from players import Player, RandomPlayer
from monte_carlo_evaluation import monte_carlo_eval
from evaluation import WinnerRewardEvaluator

class BasicMonteCarloPlayer(Player):
    def __init__(self, simulation_amount, depth=0, rewards=(1, -1, .5)):
        self.simulation_amount = simulation_amount
        self.depth = depth
        # different rewards depending on which player number the player is in the game
        self.rewards = rewards

    def make_move(self, game):
        # Assumes it is making a move on its own turn
        poss_moves = game.get_possible_moves()
        # upgrade: use "game.get_moved_copy()"
        test_games = []
        for move in poss_moves:
            test_game = game.get_copy()
            test_game.make_move(move)
            test_games.append(test_game)

        # from https://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
        # Sort the moves based on a Monte Carlo evaluation
        scores = [monte_carlo_eval(test_game, player_number=game.active_player, evaluator=WinnerRewardEvaluator(self.rewards),
                                   move_amount=-1, simulation_amount=self.simulation_amount, depth=self.depth).value
                  for test_game in test_games]

        game.make_move(max(zip(scores, poss_moves))[1])
