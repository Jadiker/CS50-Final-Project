from players import RandomPlayer
from evaluation import Evaluation, get_winner_reward, WinnerRewardEvaluator


class MonteCarloEvaluation(Evaluation):
    def __init__(self, value, simulations):
        super().__init__(value)
        self.simulations = simulations

    def __str__(self):
        return "MonteCarloEvaluation object with value: {} from {} simulations".format(self.value, self.simulations)

def monte_carlo_eval(original_game, player_number, evaluator=WinnerRewardEvaluator((1, -1, .5)), simulation_amount=100,
                     initial_depth=0, play_depth=-1, main_player=RandomPlayer(), opponent=RandomPlayer()):
    '''Returns a MonteCarloEvaluation object
    Plays moves from the given game position and averages the results

    original_game is the game to simulate from
    player_number is the number of the player whose persepective we're evaluating the game from
    evaluator is the function used to evaluate a game position once the moves are complete
    main_player is a Player object that we use to simulate the moves of the player with player_number
    ...a value of -1 signifies playing until the game is over
    simulation_amount is how many games to simulate per possible game at the specified initial depth
    initial_depth is how many layers down you want it to start simulating - it will try every possible move at each layer
    play_depth is the number of moves that are played out starting from each possible game at the specified initial depth
    ...(including opponents' moves)
    opponent is the  Player object we use to simulate the games of the player with the number that's not player_number
    '''
    if initial_depth == 0:
        value = 0
        for _ in range(simulation_amount):
            game = original_game.get_copy()
            # set up the players
            players = [None, None]
            players[player_number] = main_player
            players[original_game.get_other_player(player_number)] = opponent

            # play out a game
            while game.who_won() is None:
                if play_depth > 0:
                    play_depth -= 1
                elif play_depth == 0:
                    break
                players[game.active_player].make_move(game)

            # update the value
            value += evaluator.evaluate(game, player_number).value

        # average the games' scores
        return MonteCarloEvaluation(value / simulation_amount, simulation_amount)
    else:
        winner = original_game.who_won()
        if winner is None:
            # list of MonteCarloEvaluation objects for each game
            lower_level = [monte_carlo_eval(game, player_number, evaluator, simulation_amount,
                                            initial_depth - 1, play_depth, main_player, opponent)
                           for game in original_game.get_next_level()]
            # average the values across the same level
            return MonteCarloEvaluation(sum([evaluation.value for evaluation in lower_level]) / len(lower_level),
                                        sum([evaluation.simulations for evaluation in lower_level]))
        else:
            # game is finished, so use the evaluation function at this layer since there's no more layers to explore
            return MonteCarloEvaluation(evaluator.evaluate(original_game, player_number).value,
                                        simulation_amount)


if __name__ == "__main__":
    from tic_tac_toe import TicTacToe
    from connect_four import ConnectFour
    from players import RandomPlayer
    import random

    g = TicTacToe()
    g = ConnectFour()
    player = RandomPlayer()
    for i in range(100):
        print(monte_carlo_eval(g, 0, WinnerRewardEvaluator([1, -1, 0]), 5, 3))
        print(monte_carlo_eval(g, 0, WinnerRewardEvaluator([0, 0, 1]), 5, 3))
