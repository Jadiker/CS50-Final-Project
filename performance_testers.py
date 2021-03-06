'''
Written by London Lowmanstone
Based on code I wrote in high school.
'''
import random
import useful_functions as useful


def test_against(players, start_game, game_parameters=None, rounds=50, games_per_round=1000,
                 randomize_first_player=True, is_initial_state=True, comment=2, pct_increment=2):
    '''Returns a tuple of lists in the form (highs, lows, ranges, averages) with stats for player 0's performance against player 1
    Each list is in the form [wins, losses, ties], and the names are pretty self-explanatory.
    For example, highs is a list of the most amount of wins, losses, and ties it achieved across any round.

    players: a tuple in the form (player 0, player 1) where both are Player objects
    start_game: an instance of a Game (or Game subclass) that the players should start at for each game they play
    rounds: the number of rounds the players will play against each other
    games_per_round: how many games are played per round
    randomize_first_player: whether or not to randomize who goes first; if False, uses the active player in the start game
    is_initial_state: whether or not the start_game is in its initial state (if False, randomizing the first player may take longer)
    comment: how verbose the print statements are; higher integers give more print statements
    pct_increment: how much the percentage should increase by when it prints out
    '''


    # default to values for each list that will be overridden
    lows = [games_per_round + 1] * 3
    highs = [-1] * 3
    overall = [0] * 3
    for i in range(rounds):
        results = [0] * 3  # [wins, losses, ties] for the player
        for game_num in range(games_per_round):
            if comment > 3:
                print("Testing game {}/{}".format((game_num + 1), games_per_round))

            # set up the game from the start_game
            if randomize_first_player:
                # randomize who goes first
                if is_initial_state:
                    # no need to swap the players; no one has moved yet
                    game = start_game.get_copy()
                    if random.choice([True, False]):
                        game.active_player = 0
                    else:
                        game.active_player = 1
                else:
                    # we need to swap the players if a different one is going to go first
                    if random.choice([True, False]):
                        game = start_game.get_copy()
                    else:
                        game = start_game.get_swapped_copy()
            else:
                # not randomizing the first player, so we can just copy the starting game
                game = start_game.get_copy()

            while game.who_won() is None:
                players[game.active_player].make_move(game)
                if comment > 5:
                    print(game)

            # update the results; this works because player 0 is always the player we care about
            results[game.who_won()] += 1
            if comment > 3:
                if comment > 4:
                    print(game)
                print("Results so far in round:\n{}".format(results))

        if comment > 2:
            print("Results of one round:\n{}".format(results))

        if pct_increment > 0 and comment > 1:
            useful.print_percent(i, rounds, increment_amt=pct_increment, round_amt=i)

        # update the lists
        for j, testVal in enumerate(results):
            lows[j] = min(lows[j], testVal)
            highs[j] = max(highs[j], testVal)
            overall[j] += testVal

    # compute the other stats lists
    ranges = [highs[i] - lows[i] for i in range(3)]
    avgs = [overall[i] / rounds for i in range(3)]

    if comment > 0:
        print("Highs: {}".format(highs))
        print("Lows: {}".format(lows))
        print("Ranges: {}".format(ranges))
        print("Averages: {}".format(avgs))
    return (highs, lows, ranges, avgs)


if __name__ == "__main__":
    '''Play and test different players.
    Currently this is set up for you to play against the perfect tic-tac-toe player
    '''
    '''
    These are some notes about how good different players were against each other:

    # significant difference: 74 - 15, no ties.
    # test_against((BasicMonteCarloPlayer(30, 1), BasicMonteCarloPlayer(30)), ConnectFour, 100, 100, comment=4)

    # no significant difference: 29 - 28 - 2
    # test_against((BasicMonteCarloPlayer(40, 1), BasicMonteCarloPlayer(30, 1)), ConnectFour, 1, 100, comment=4)

    # significant: 71 - 6 - 2 (Mainly lost when it had a perfect trap set up that was blocked by an opponent, then it gave up easy wins; should be fixed with minimax)
    # test_against((BasicMonteCarloPlayer(5, 3), BasicMonteCarloPlayer(30)), ConnectFour, 1, 100, comment=6)
    '''
    from tic_tac_toe import TicTacToe
    from connect_four import ConnectFour
    from otrio import Otrio
    from players import RandomPlayer, HumanPlayer
    from advised_monte_carlo_player import AdvisedMonteCarloPlayer
    from basic_monte_carlo_player import BasicMonteCarloPlayer
    from solve_player import SolvePlayer
    from sizeable_connect_x import SizeableConnectX
    from onitama import Onitama, PawnCountingEvaluator
    from onitama import move_to_string as onitama_move_to_string
    start_game = SizeableConnectX(4, 4, 4)
    # game
    # start_game = Otrio()
    start_game = Onitama()

    # player 1
    # p1 = HumanPlayer(onitama_move_to_string)
    # p1 = HumanPlayer()
    # p1 = AdvisedMonteCarloPlayer(2, 2, 2)
    # p1 = BasicMonteCarloPlayer()
    # p1 = RandomPlayer()
    # this one is a litte too aggressive to its own detriment
    # p1 = BasicMonteCarloPlayer(5, 2, 4, PawnCountingEvaluator())
    # too slow lol didn't realize what parameters I was putting into the BasicMonteCarloPlayer, the fact that it made any moves is amazing
    # p1 = AdvisedMonteCarloPlayer(pe_depth=1, mc_simulation_amount=5, mc_initial_depth=2, mc_play_depth=4, mc_evaluator=PawnCountingEvaluator(), pe_rewards=(2, -2, .9, 0, 0), main_player=RandomPlayer(), opponent=BasicMonteCarloPlayer(3, 2))
    p1 = AdvisedMonteCarloPlayer(pe_depth=1, mc_simulation_amount=5, mc_initial_depth=2, mc_play_depth=4,
                                 mc_evaluator=PawnCountingEvaluator(),
                                 pe_rewards=(2, -2, .9, 0, 0),
                                 main_player=RandomPlayer(),
                                 opponent=BasicMonteCarloPlayer(simulation_amount=3,
                                                                initial_depth=0,
                                                                play_depth=2,
                                                                evaluator=PawnCountingEvaluator()))

    # player 2
    # p2 = BasicMonteCarloPlayer(5, 2)
    p2 = RandomPlayer()

    '''
    # Create a player that solves the game
    s = SolvePlayer()
    print("Solving...")
    s.make_move(start_game.get_copy())
    print("Solved!")
    p2 = s
    '''

    # Test how good player 1 is against player 2
    test_against((p1, p2), start_game, rounds=10, games_per_round=100, comment=6, randomize_first_player=False)
