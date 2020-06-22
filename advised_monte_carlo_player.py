from position_eval import position_eval
from monte_carlo_evaluation import monte_carlo_eval
from players import Player, RandomPlayer


class AdvisedMonteCarloPlayer(Player):
    '''
    A basic monte carlo player that takes certain wins and ties and avoids certain
    '''

    def __init__(self, mc_simulation_amount, mc_depth, pe_depth, mc_rewards=(1, -1, .5), pe_rewards=(2, -2, .9, 0, 0), main_player=RandomPlayer(), opponent=RandomPlayer()):
        '''
        mc is short for "MonteCarlo"
        mc_simulation_amount: how many times the monte carlo evaluator should simulate each end position
        mc_depth: how many moves the MonteCarlo simulation should look ahead (should be at least 1)
        pe_depth: how many moves the position evaluator should look ahead (should be at least 1)
        mc_rewards: the monte carlo evaluation rewards for (win, loss, tie)
        pe_rewards: the position evaluator rewards for (win, loss, tie, undetermined)
        main_player: the player who is making the moves in the AdvisedMonteCarloPlayer's position when simulating games
        opponent: the player who is playing against the main_player when simulating games
        '''
        self.mc_simulation_amount = mc_simulation_amount
        self.mc_depth = mc_depth
        self.mc_rewards = mc_rewards
        self.pe_depth = pe_depth
        self.pe_rewards = pe_rewards
        self.sim_main_player = main_player
        self.sim_opponent = opponent

        # the position evaluation function
        self.pe_func = lambda game, player_number: position_eval(game, player_number,
                                                                 self.pe_depth - 1, self.pe_rewards)

        # the monte carlo evaluation function
        self.mc_func = lambda game, player_number: monte_carlo_eval(game, player_number, rewards=self.mc_rewards,
                                                                    simulation_amount=self.mc_simulation_amount, depth=self.mc_depth,
                                                                    main_player=self.sim_main_player, opponent=self.sim_opponent)

    def make_move(self, game):
        main_player = game.active_player
        # Assumes it is making a move on its own turn
        moves = game.get_possible_moves()
        # get a list of all the possible games for the next move
        test_games = [game.get_moved_copy(move) for move in moves]
        # score those games based on the position evaluation
        pe_scores = [self.pe_func(test_game, main_player).value for test_game in test_games]
        # upgrade: could check if there are certain win or loss moves and then skip monte carlo if that's the case
        # score those games based on monte carlo simulations
        mc_scores = [self.mc_func(test_game, main_player).value for test_game in test_games]
        # from https://stackoverflow.com/questions/4233476/sort-a-list-by-multiple-attributes
        # make the best move first based on position evaluation score and then based on  monte carlo score
        game.make_move(max([(moves[i], (pe_scores[i], mc_scores[i]))
                            for i in range(len(moves))], key=lambda x: x[1])[0])


if __name__ == "__main__":
    from performance_testers import test_against
    from connect_four import ConnectFour
    from tic_tac_toe import TicTacToe
    from players import RandomPlayer, HumanPlayer
    from basic_monte_carlo_player import BasicMonteCarloPlayer

    test_against((AdvisedMonteCarloPlayer(6, 2, 6),
                  AdvisedMonteCarloPlayer(5, 2, 4)), ConnectFour, comment=6)
