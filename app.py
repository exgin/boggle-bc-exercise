from boggle import Boggle
from flask import Flask, session, render_template, request, jsonify

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "sam123"

@app.route('/')
def display_board():
    """Display a game board"""
    board = boggle_game.make_board()

    # storage our board data in session
    session['board'] = board
    
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template('base.html', board=board, highscore=highscore, nplays=nplays)

@app.route('/check-word')
def check_word():
    """Checks word is vaild in the dictionary"""
    user_guess = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board, user_guess)

    return jsonify({'result': res})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Take score, update nplays, update high score"""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)