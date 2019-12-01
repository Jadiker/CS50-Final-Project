import os
import random
import time

from flask import Flask, render_template, redirect, request, jsonify
from tic_tac_toe import TicTacToe
from connect_four import ConnectFour
from advised_monte_carlo_player import AdvisedMonteCarloPlayer
from solve_player import SolvePlayer

# much of this file is modeled after CS50 psets
app = Flask(__name__)

# have the bot solve tic-tac-toe on startup
game = TicTacToe()
# create a tic-tac-toe bot that will compute and store all the best moves
tic_tac_toe_bot = SolvePlayer()
print("Solving tic-tac-toe...")
tic_tac_toe_bot.make_move(TicTacToe())

# the bot that will play against the human player
# this is set once a game is chosen
bot = None

# whether or not the server is currently working on a move
moving = False


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def homepage():
    return render_template("index.html")


@app.route("/tictactoe", methods=["GET"])
def tictactoe():
    global game, bot, moving
    # reset moving
    moving = False
    game = TicTacToe()
    # randomize the first player
    game.active_player = random.choice([0, 1])
    # use the bot that has memorized all the best moves
    bot = tic_tac_toe_bot
    return render_template("tictactoe.html", player=game.active_player)


@app.route("/connect4", methods=["GET", "POST"])
def connect4():
    global game, bot, moving
    # reset moving
    moving = False
    game = ConnectFour()
    # randomize the first player
    game.active_player = random.choice([0, 1])
    # set the bot to be the best generalizeable bot we have (with a solid speed)
    bot = AdvisedMonteCarloPlayer(7, 2, 4)
    return render_template("connect4.html", player=game.active_player)


@app.route("/human_move", methods=["POST"])
def make_human_move():
    global moving
    # bot_move is 1 if the javascript should request a bot move
    # bot_move is 0 if the javascript should not request a bot move
    bot_move = 0
    # make sure a move is not currently going on
    if not moving:
        moving = True
        move = request.form.get("move")
        # deal with race condition of a person clicking multiple times quickly
        if move:
            move = int(move)
            # make sure it really is the player's turn
            if game.active_player == 0:
                if move in game.get_continue_moves():
                    game.make_move(move)
                    if game.who_won() is None:
                        bot_move = 1
                        # It's okay if we continue to say we're "moving" when the game is done
                else:
                    # no move was actually made
                    moving = False

    # get the json dict from the game
    json_dict = game.get_json_dict()
    # tack on the bot move key/value pair
    json_dict["bot_move"] = bot_move
    return jsonify(json_dict)


@app.route("/bot_move", methods=["POST"])
def make_bot_move():
    global moving
    moving = True
    bot.make_move(game)
    time.sleep(1)
    moving = False
    return jsonify(game.get_json_dict())


@app.route("/about", methods=["GET", "POST"])
def aboutpage():
    return render_template("about.html")


@app.route("/instructions", methods=["GET", "POST"])
def instructionspage():
    return render_template("instructions.html")


if __name__ == "__main__":
    # app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))  # used to run on Cloud9
    # running on Heroku does not work yet because it looks like the global bot doesn't stay the same when hosted
    #app.run(threaded=True)  # used to run on heroku
    app.run(debug=False, port=5001) # used to run locally
