from flask import jsonify
from copy import deepcopy


""" A Chess object represents a turn in a chess game.
	The class also provides methods to get information about the chess object
	as well as a method that calculates the next turn based on a move.
	Moves are represented as pairs of chess coordinates, {a7, d2} for example.

	The chess turn is represented the following way:
	- An array of 64 elements, representing the contents of each field where:
		0: free cell
		1: black pawn    11: white pawn
		2: black knight  12: white knight
		3: black bishop  13: white bishop
		4: black rook    14: white rook
		5: black queen   15: white queen
		6: black king    16: white king
	- A string indicating who'se turn it is.
	- The number of the current turn.
	- A list of free cells.
	- A list of cells with white pieces.
	- A list of cells with white pieces.
	- The position of the white king.
	- The position of the black king.
"""

opponent = {
	"white": "black",
	"black": "white"
}

pieceType = {
		1: "pawn", 11: "pawn",
		2: "knight", 12: "knight",
		3: "bishop", 13: "bishop",
		4: "rook", 14: "rook",
		5: "queen", 15: "queen",
		6: "king", 16: "king",
		0: "none"
}


PAWN_ATTACK_MOVES = {"black": [7, 9], "white": [-7, -9]}
KNIGHT_MOVES = [6, 10, 15, 17, -6, -10, -15, -17]
KING_MOVES = [-9, -8, -7, -1, 1, 7, 8, 9]

BISHOP_STEPS = [-9, -7, 7, 9]
ROOK_STEPS = [-8, -1, 1, 8]
QUEEN_STEPS = BISHOP_STEPS + ROOK_STEPS


class Move():
	def __init__(self, moveFrom, moveTo, chess):
		self.moveFrom = moveFrom
		self.moveTo = moveTo
		self.previousValue = chess.cells[moveTo]


def moveInBoundries(pos, target):
	"""Guarantees that the move from 'pos' to 'target' lies in the boundries."""
	return abs(pos % 8 - target % 8) < 4 and target >= 0 and target < 63

class Chess():
	def __init__(self):
		"""Creates a new chess object. """
		self.cells = []
		self.playerTurn = "white"
		self.turnNumber = 1
		self.initializeChessField()
		self.freeCells = set(range(16, 48))
		self.blackCells = set(range(0, 16))
		self.whiteCells = set(range(48, 64))
		self.whiteKing = 60
		self.blackKing = 4
		assert len(self.cells) == 64
		assert len(self.freeCells) == 32
		assert len(self.blackCells) == 16
		assert len(self.whiteCells) == 16
		assert self.turnNumber == 1
		assert self.playerTurn == "white"

	# initializes the chess field
	def initializeChessField(self):
		"""initializes the chess field"""
		self.cells = [4, 2, 3, 5, 6, 3, 2, 4]
		self.cells += 8*[1]
		self.cells += 32*[0]
		self.cells += 8*[11]
		self.cells += [14, 12, 13, 15, 16, 13, 12, 14]
		assert len(self.cells) == 64

	def getPieceColor(self, code):
		if(code > 10):
			return "white"
		elif(code > 0):
			return "black"
		else:
			return "none"

	def getPieceType(self, code):
		return pieceType[code]

	def getPlayerCells(self):
		return {
				True: self.whiteCells,
				False: self.blackCells
		}[self.playerTurn == "white"]

	def getEnemyCells(self):
		return {
				True: self.blackCells,
				False: self.whiteCells
		}[self.playerTurn == "white"]

	def getPossibleChoices(self, position):
		assert position >= 0 and position <= 63
		# print("getting possible choices ")
		code = self.cells[position]
		player = self.getPieceColor(code)
		selectedType = pieceType[code]
		if player == "black":
			enemyCells = self.whiteCells
		else:
			enemyCells = self.blackCells
		choices = set()

		if selectedType == "pawn":
			if player == "black":
				if self.cells[position+8] == 0:
					choices.add(position+8)
				if (position < 16 and
					self.cells[position+8] == self.cells[position+16] == 0):
					choices.add(position+16)
			else:
				if self.cells[position-8] == 0:
					choices.add(position-8)
				if (position > 47 and
					self.cells[position-8] == self.cells[position-16] == 0):
					choices.add(position-16)
			for c in PAWN_ATTACK_MOVES[player]:
				target = position + c
				if (target in enemyCells and
					abs(position % 8 - (target) % 8) < 3):  # checks the boundaries
						choices.add(target)
		else:
			self.getCellsTargetedBy(position, choices)

		validChoices = self.freeCells | enemyCells
		choices = choices & validChoices

		toExclude = set()
		for choice in choices:
			move = Move(position, choice, self)
			self.applyMove(move)
			if self.isCheck(player):
				toExclude.add(choice)
			self.revertMove(move)
		return list(choices-toExclude)

	def isCheck(self, player):
		covered = self.getCoveredCells(opponent[player])
		if player == "white":
			return self.whiteKing in covered
		else:
			return self.blackKing in covered

	def isCheckMate(self):
		return len(self.getPossibleChoices()) == 0

	def getCoveredCells(self, player):
		"""Returns all cells that are coverd by this player.
			This ignores the possiblity that a turn might not be possibile
			because of check. """
		covered = set()
		if player == "black":
			playerCells = self.blackCells
			enemyCells = self.whiteCells
		else:
			playerCells = self.whiteCells
			enemyCells = self.blackCells

		for position in playerCells:
			self.getCellsTargetedBy(position, covered)

		validChoices = self.freeCells | enemyCells
		return covered & validChoices

	def getCellsTargetedBy(self, position, returnSet):
		""" Puts all cells that are attacked from this position
			into the specified return set.
			For performance reasons this doesn't guarantee that the
			cells are in bounds!"""
		code = self.cells[position]
		player = self.getPieceColor(code)
		selectedType = pieceType[code]
		if player == "black":
			playerCells = self.blackCells
			enemyCells = self.whiteCells
		else:
			playerCells = self.whiteCells
			enemyCells = self.blackCells

		if selectedType in ["pawn", "knight", "king"]:
			targets = {"pawn": PAWN_ATTACK_MOVES[player],
						"knight": KNIGHT_MOVES,
						"king": KING_MOVES}[selectedType]
			for c in targets:
				target = position + c
				if abs(position % 8 - (target) % 8) < 3:  # checks the boundaries
						returnSet.add(target)

		elif selectedType in ["bishop", "rook", "queen"]:
			stepSizes = {"bishop": BISHOP_STEPS,
						"rook": ROOK_STEPS,
						"queen": QUEEN_STEPS}[selectedType]
			for stepSize in stepSizes:
				c = position
				for i in range(0, 7):
					if (abs(c % 8 - (c+stepSize) % 8) > 1 or
							c+stepSize in playerCells):
						break
					c += stepSize
					returnSet.add(c)
					if c in enemyCells:
						break

	def applyMove(self, move):
		piece = self.cells[move.moveFrom]
		player = self.getPieceColor(piece)
		target = self.getPieceColor(move.previousValue)
		assert player != target

		self.cells[move.moveTo] = self.cells[move.moveFrom]
		self.cells[move.moveFrom] = 0

		# from cell
		self.freeCells.add(move.moveFrom)
		# if self.playerTurn == "black":
		if player == "black":
			self.blackCells.remove(move.moveFrom)
			self.blackCells.add(move.moveTo)
		else:
			self.whiteCells.remove(move.moveFrom)
			self.whiteCells.add(move.moveTo)

		# to cell
		if move.previousValue == 0:
			self.freeCells.remove(move.moveTo)
		elif move.previousValue < 10:
			self.blackCells.remove(move.moveTo)
		else:
			self.whiteCells.remove(move.moveTo)

		if piece == 6:
			self.blackKing = move.moveTo
		if piece == 16:
			self.whiteKing = move.moveTo

		self.turnNumber += 1
		self.playerTurn = opponent[self.playerTurn]
		assert len(self.cells) == 64
		assert len(self.freeCells) >= 32
		assert len(self.blackCells) <= 32
		assert len(self.whiteCells) <= 32
		assert len(self.blackCells) + len(self.whiteCells) + len(self.freeCells) == 64

	def revertMove(self, move):
		assert isinstance(move, Move)
		player = self.getPieceColor(self.cells[move.moveTo])
		self.cells[move.moveFrom] = self.cells[move.moveTo]
		self.cells[move.moveTo] = move.previousValue
		piece = self.cells[move.moveFrom]

		self.turnNumber -= 1
		self.playerTurn = opponent[self.playerTurn]

		# from cell
		self.freeCells.remove(move.moveFrom)
		# if self.playerTurn == "black":
		if player == "black":
			self.blackCells.add(move.moveFrom)
			self.blackCells.remove(move.moveTo)
		else:
			self.whiteCells.add(move.moveFrom)
			self.whiteCells.remove(move.moveTo)

		# to cell
		if move.previousValue == 0:
			self.freeCells.add(move.moveTo)
		elif move.previousValue < 10:
			self.blackCells.add(move.moveTo)
		else:
			self.whiteCells.add(move.moveTo)

		if piece == 6:
			self.blackKing = move.moveFrom
		if piece == 16:
			self.whiteKing = move.moveFrom

		assert len(self.cells) == 64
		assert len(self.freeCells) >= 32
		assert len(self.blackCells) <= 32
		assert len(self.whiteCells) <= 32
		assert len(self.blackCells)+len(self.whiteCells)+len(self.freeCells) == 64

	def toJson(self):
		return jsonify(playerTurn=self.playerTurn, cells=self.cells)

	def printASCII(self):
		for i in range(0, 8):
			for j in range(0, 8):
				print(self.cells[i*8+j], end='\t')
			print()
			print()
			print()
			print()

	def __eq__(self, other):
		return self.__dict__ == other.__dict__
