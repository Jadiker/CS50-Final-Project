class Evaluation:
    '''A class for evaluations of different game states'''

    def __init__(self, value):
        # the value of a particular state (a number)
        self.value = value

    def __str__(self):
        return "<Evaluation object of value: {}>".format(self.value)


class Evaluator:
    def evaluate(self, game, player_number):
        '''
        Evaluates a game for a particular player. Returns an Evaluation.
        Should not modify the game itself in the evaluation.
        '''
        raise NotImplementedError


class WinnerRewardEvaluator(Evaluator):
    '''Evaluates based on the winner and the given reward list'''
    def __init__(self, rewards):
        '''Rewards are in the form (win reward, loss reward, tie reward)'''
        self.rewards = rewards

    def evaluate(self, game, player_number):
        return Evaluation(get_winner_reward(game.who_won(), player_number, self.rewards))


def get_winner_reward(winner_number, player_number, rewards):
    '''Computes the reward based on who won and who the player is'''
    if winner_number is None:
        return None
    else:
        if player_number == 0:
            player_rewards = rewards
        else:
            # flip the rewards so the index of the winning player will give the correct result
            player_rewards = (rewards[1], rewards[0], rewards[2])

        return player_rewards[winner_number]
