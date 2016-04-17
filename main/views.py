from main import app
from flask import jsonify, render_template, request
import json
import threading
import time
from .chess import Chess, Move
from .AI import AI

chess = None
ai = AI()
player = "white"


@app.route('/')
@app.route('/index')
def index():
	global chess
	chess = Chess()
	return render_template('index.html',
						   title='Home')
@app.route('/about')
def about():
	return render_template('about.html',
						   title='About')

@app.route('/_add_numbers')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	return jsonify(result=a + b)

@app.route('/_get_board')
def get_board():
	selection = request.args.get('a', 0, type=int)
	moveTo = request.args.get('b', 0, type=int)

	global chess
	global player
	global ai

	if(moveTo != -1):
		if player == chess.playerTurn:
			print("------> player")
			# chess = chess.move(selection, moveTo)
			move = Move(selection, moveTo, chess)
			chess.applyMove(move)
			print("------> ai")
			move = ai.nextMove(chess)
			chess.applyMove(move)

	return chess.toJson()


# receives the selected piece of the player
# returns a json file containing an array of all possible choices
@app.route('/_get_choices')
def get_choices(): 
	selection = request.args.get('a', 0, type=int)
	return jsonify(choices = chess.getPossibleChoices(selection))
	# return jsonify(choices=chess.coveredByWhite)


with app.test_request_context('/hello', method='POST'):
	# now you can do something with the request until the
	# end of the with block, such as basic assertions:
	print("hi")
