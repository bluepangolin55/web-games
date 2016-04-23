from main import app, socketio
from flask import jsonify, render_template, request
from flask.ext.socketio import SocketIO, emit
import json
from threading import Thread, Event
import time
from .chess import Chess, Move
from .AI import AI


# --- global variables ---

chess = None
ai = AI()

def calculateEnemyMove():
	global chess
	global ai
	move = ai.nextMove(chess)
	chess.applyMove(move)
	socketio.emit('turn data', chess.toDict(), json=True, namespace='/test')
	print("sent ai move")

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

@socketio.on('new chess game', namespace='/test')
def newGame(message):
	global chess
	chess = Chess()
	socketio.emit('turn data', chess.toDict(), json=True, namespace='/test')

@socketio.on('request data', namespace='/test')
def newGame(message):
	global chess
	print("requesting turn data")
	socketio.emit('turn data', chess.toDict(), json=True, namespace='/test')

@socketio.on('submit move', namespace='/test')
def nextMove(message):
	global chess
	print("move submitted")
	selection = message['from']
	moveTo = message['to']

	move = Move(selection, moveTo, chess)
	chess.applyMove(move)
	socketio.emit('turn data', chess.toDict(), json=True, namespace='/test')
	thread = Thread(target=calculateEnemyMove)
	thread.daemon = True
	thread.start()
	socketio.emit('turn data', chess.toDict(), json=True, namespace='/test')

