from players import RandomPlayer
from evaluation import Evaluation, simple_eval, winner_eval


class MonteCarloEvaluation(Evaluation):
    def __init__(self, value, simulations):
        super().__init__(value)
        self.simulations = simulations

    def __str__(self):
        return "MonteCarloEvaluation object with value: {} from {} simulations".format(self.value, self.simulations)

def monte_carlo_eval(original_game, player_number, main_player=RandomPlayer(), rewards=(1, -1, .5), simulation_amount=100, depth=0, opponent=RandomPlayer()):
    '''Returns a MonteCarloEvaluation object
    Plays random games from the given game position and averages the results

    original_game is the game to simulate from
    player_number is the number of the player whose persepective we're evaluating the game from
    main_player is a Player object that we use to simulate the moves of the player with player_number
    rewards is a tuple (or list): (points for winning, points for losing, points for tying)
    simulation_amount is how many games to simulate per possible game at the specified depth
    depth is how many layers down you want it to start simulating
    opponent is the  Player object we use to simulate the games of the player with the number that's not player_number
    '''

    if depth == 0:
        value = 0
        for _ in range(simulation_amount):
            game = original_game.get_copy()
            # set up the players
            players = [None, None]
            players[player_number] = main_player
            players[original_game.get_other_player(player_number)] = opponent

            # play out a game
            while game.who_won() is None:
                players[game.active_player].make_move(game)

            # update the value
            value += simple_eval(game, player_number, rewards).value

        # average the games' scores
        return MonteCarloEvaluation(value / simulation_amount, simulation_amount)
    else:
        winner = original_game.who_won()
        if winner is None:
            # list of MonteCarloEvaluation objects for each game
            lower_level = [monte_carlo_eval(game, player_number, main_player,
                                            rewards, simulation_amount, depth - 1, opponent)
                           for game in original_game.get_next_level()]
            # average the values across the same level
            return MonteCarloEvaluation(sum([e.value for e in lower_level]) / len(lower_level),
                                        sum([e.simulations for e in lower_level]))
        else:
            # game is finished, so use winner_eval
            return MonteCarloEvaluation(winner_eval(winner, player_number, rewards).value,
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
        print(monte_carlo_eval(g, 0, player, [1, -1, 0], 5, 3))
        print(monte_carlo_eval(g, 0, player, [0, 0, 1], 5, 3))
