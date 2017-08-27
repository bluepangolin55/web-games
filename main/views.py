from main import app, socketio
from flask import render_template
import sys
from threading import Thread
from .chess import Chess, Move
from .sudoku import Sudoku
from .AI import AI
from random import randint


# --- global variables ---

games = dict()
ai = AI()

def calculateEnemyMove(chess):
	global ai
	move = ai.nextMove(chess)
	chess.applyMove(move)
	socketio.emit('turn data', chess.toDict(), json=True, namespace='/test')
	print("sent ai move")
	sys.stdout.flush()

@app.route('/')
@app.route('/index')
def index():
	global chess
	chess = Chess()
	return render_template('index.html', title='Home')

@app.route('/about')
def about():
	return render_template('about.html',
						   title='About')

@app.route('/chess')
def chess():
	global chess
	chess = Chess()
	return render_template('chess.html', title='Chess')

@app.route('/sudoku')
def sudoku():
	return render_template('sudoku.html', title='Sudoku')

@socketio.on('request ID', namespace='/test')
def newID(message):
	id = randint(0,100)
	print(id)
	sys.stdout.flush()
	socketio.emit('new ID', {'id': id}, json=True, namespace='/test')

@socketio.on('new chess game', namespace='/test')
def newGame(message):
	id = message['id']
	games[id] = Chess()
	# chess = Chess()
	print("starting new chess game")
	print(message['id'])
	sys.stdout.flush()
	socketio.emit('turn data', games[id].toDict(), json=True, namespace='/test')

@socketio.on('new sudoku game', namespace='/test')
def newGame(message):
	id = message['id']
	games[id] = Sudoku()
	# chess = Chess()
	print("starting new sudoku game")
	print(message['id'])
	sys.stdout.flush()
	# socketio.emit('turn data', games[id].toDict(), json=True, namespace='/test')

@socketio.on('request data', namespace='/test')
def newGame(message):
	print("requesting turn data")
	sys.stdout.flush()
	id = message['id']
	socketio.emit('turn data', games[id].toDict(), json=True, namespace='/test')

@socketio.on('submit move', namespace='/test')
def nextMove(message):
	print("move submitted")
	sys.stdout.flush()
	id = message['id']
	chess = games[id]
	selection = message['from']
	moveTo = message['to']

	move = Move(selection, moveTo, chess)
	chess.applyMove(move)
	socketio.emit('turn data', chess.toDict(), json=True, namespace='/test')
	thread = Thread(target=calculateEnemyMove(chess))
	thread.daemon = True
	thread.start()
	socketio.emit('turn data', chess.toDict(), json=True, namespace='/test')
