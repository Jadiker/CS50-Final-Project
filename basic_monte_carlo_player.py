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
# TODO delete
from onitama import board_to_string

class BasicMonteCarloPlayer(Player):
    def __init__(self, simulation_amount=4, initial_depth=0, play_depth=-1, evaluator=WinnerRewardEvaluator((1, -1, .5))):
        self.simulation_amount = simulation_amount
        self.initial_depth = initial_depth
        self.play_depth = play_depth
        self.evaluator = evaluator

    def make_move(self, game):
        assert game.who_won() is None, "Can't make a move in a game that is already over"
        # Assumes it is making a move on its own turn
        poss_moves = game.get_possible_moves()
        for move in poss_moves:
            game._assert_move(move)
        # upgrade: use "game.get_moved_copy()"
        test_games = []
        # TODO delete
        # print("---------REAL BOARD BEFORE----------")
        # print(board_to_string(game.state.board))
        # print("-----REAL GAME BEFORE-----")
        # print(game)
        game_string = str(game)
        for move in poss_moves:
            # TODO delete
            game._assert_move(move)
            test_game = game.get_copy()
            # TODO delete
            test_game._assert_move(move)
            # TODO delete
            # print("---------TEST BOARD BEFORE----------")
            # print(board_to_string(test_game.state.board))
            # print("-----TEST GAME BEFORE-----")
            # print(test_game)
            # print("-------TEST MOVE BEFORE-------")
            # print(move)
            new_game_string = str(game)
            assert game_string == new_game_string, f"The game changed (without any moves being made)\n*FROM*:\n{game_string}\n\n*TO*:\n{new_game_string}"
            # TODO delete assertions and prints around here
            # print(f"The ID of the board I expect the move to be made in is:\n{id(test_game.state.board)}\n^^^that")
            test_game.make_move(move)
            new_game_string = str(game)
            assert game_string == new_game_string, f"The game changed (without any moves being made)\n*FROM*:\n{game_string}\n\n*TO*:\n{new_game_string}"
            # TODO delete
            # print("------DEBUGGING AFTER--------")
            # print("---------TEST BOARD AFTER----------")
            # print(board_to_string(test_game.state.board))
            # print("-----TEST GAME AFTER-----")
            # print(test_game)
            # print("-------TEST MOVE AFTER-------")
            # print(move)
            # TODO delete
            # print("---------REAL BOARD AFTER----------")
            # print(board_to_string(game.state.board))
            # print("-----REAL GAME AFTER-----")
            # print(game)
            test_games.append(test_game)

        # TODO delete
        # print("poss moves:")
        # print(poss_moves)

        # from https://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
        # Sort the moves based on a Monte Carlo evaluation
        scores = [monte_carlo_eval(test_game, player_number=game.active_player, evaluator=self.evaluator,
                                   simulation_amount=self.simulation_amount, initial_depth=self.initial_depth,
                                   play_depth=self.play_depth).value
                  for test_game in test_games]

        # TODO delete
        # print("zipped")
        # print(list(zip(scores, poss_moves)))
        best_score, best_move = max(zip(scores, poss_moves), key=lambda score_move_tuple: score_move_tuple[0])
        print("best move")
        print(best_move)
        print(f"with score of: {best_score}")
        assert game.who_won() is None, "Game finished without any moves being made"
        game.make_move(best_move)
