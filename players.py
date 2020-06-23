import random


class Player:
    def make_move(self, game):
        '''Make a move in the game (a Game object)'''
        raise NotImplementedError

    def __str__(self):
        return "<Player object>"


class RandomPlayer(Player):
    @classmethod
    def get_random_game(cls, game_cls):
        '''Returns a random game of the class game_cls which must be a subclass of Game'''
        game = game_cls()
        while game.who_won() is None:
            game.make_move(random.choice(game.get_possible_moves()))
        return game

    def make_move(self, game):
        '''Make a random move'''
        game.make_move(random.choice(game.get_possible_moves()))

    def __str__(self):
        '''Simple printing'''
        return "<RandomPlayer object>"


class HumanPlayer(Player):
    '''A class to allow humans to play a game in the terminal.
    Used for debugging before creating a GUI/website.

    Assumes that the game implements a __str__ method that prints out something human-understandable.
    '''
    def __init__(self, move_to_string=str):
        '''Takes a function that turns a move object into a string that the user can understand
        This function should take the parameters self.move_to_string(move, game)'''
        self.move_to_string = move_to_string

    def make_move(self, game):
        moves = game.get_possible_moves()
        print(game)
        # if all the moves are integers
        if False not in [isinstance(move, int) for move in moves]:
            while True:
                # print the human-numbered (starting at 1) version of those moves
                print("Moves:\n{}".format([move + 1 for move in moves]))
                # request a move
                try:
                    move = int(input("Type the move you'd like to do: ")) - 1
                    if move not in moves:
                        raise ValueError("Invalid user move")
                    break
                except ValueError:
                    print("Sorry, that wasn't a valid choice.")
        else:
            # print out a dictionary of indexes/keys the user can type and the corresponding move
            moves_dict = {}
            for i, move in enumerate(moves):
                try:
                    moves_dict[i] = self.move_to_string(move, game)
                except Exception:
                    raise ValueError("Converting the move to a string failed - conversion function is incorrect")
            while True:
                print("Available Moves:")
                for move_key, move_string in moves_dict.items():
                    print(f"{move_key}: {move_string}")
                print()
                # request a move
                try:
                    index = int(input("Type the index of the move you'd like to do: "))
                    move = moves[index]
                    break
                except (ValueError, IndexError):
                    print("Sorry, that wasn't a valid move choice. Please type the number of the move  you'd like to make.\n")


        # make the move
        game.make_move(move)
        print("Move made!\n")
