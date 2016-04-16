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


class Chess():
	def __init__(self):
		"""Creates a new chess object. """
		self.cells = []
		self.playerTurn = "white"
		self.turnNumber = 1
		self.initializeChessField()
		self.freeCells = []
		self.blackCells = []
		self.whiteCells = []
		self.kingPosition = 0
		self.updateInfo()
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
		t = code % 10
		return {
			1: "pawn",
			2: "knight",
			3: "bishop",
			4: "rook",
			5: "queen",
			6: "king",
		}[t]

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
		code = self.cells[position]
		selectedColor = self.getPieceColor(code)
		selectedType = self.getPieceType(code)
		choices = []

		if selectedType == "pawn":
			if selectedColor == "black":
				if self.cells[position+8] == 0:
					choices.append(position+8)
				if position < 16 and self.cells[position+16] == 0:
					choices.append(position+16)
				if (position + 7) in self.getEnemyCells() and position % 8 > 0:
					choices.append(position+7)
				if (position + 9) in self.getEnemyCells() and position % 8 < 7:
					choices.append(position+9)
			else:
				if self.cells[position-8] == 0:
					choices.append(position-8)
				if position > 47 and self.cells[position-16] == 0:
					choices.append(position-16)
				if (position - 7) in self.getEnemyCells() and position % 8 < 7:
					choices.append(position-7)
				if (position - 9) in self.getEnemyCells() and position % 8 > 0:
					choices.append(position-9)

		elif selectedType == "knight":
			KnightMoves = [6, 10, 15, 17, -6, -10, -15, -17]
			for c in KnightMoves:
				if abs(position % 8 - (position + c) % 8) < 3:  # checks the boundaries
					choices.append(position + c)

		elif selectedType == "king":
			KingMoves = [-9, -8, -7, -1, 1, 7, 8, 9]
			for c in KingMoves:
				if abs(position % 8 - (position + c) % 8) < 3:  # checks the boundaries
					choices.append(position + c)

		elif selectedType in ["bishop", "rook", "queen"]:
			stepSizes = []
			if selectedType in ["bishop", "queen"]:
				stepSizes += [8+1, 8-1, -8+1, -8-1]
			if selectedType in ["rook", "queen"]:
				stepSizes += [8, -8, +1, -1]
			for stepSize in stepSizes:
				c = position
				for i in range(0, 7):
					if (abs(c % 8 - (c+stepSize) % 8) > 1 or
							c+stepSize not in (self.freeCells + self.getEnemyCells())):
						break
					c += stepSize
					choices.append(c)
					if c in self.getEnemyCells():
						break

		# exclude out of bounds and player cells
		choices = [cell for cell in choices
			if (cell >= 0 and cell < 64 and cell not in self.getPlayerCells())]
		return choices

	def updateInfo(self):
		self.freeCells = []
		self.blackCells = []
		self.whiteCells = []
		for i in range(0, 64):
			code = self.cells[i]
			if code == 0:
				self.freeCells.append(i)
			elif code < 10:
				self.blackCells.append(i)
			else:
				self.whiteCells.append(i)
			if self.playerTurn == "black" and code == 6:
				self.kingPosition = i
			if self.playerTurn == "white" and code == 16:
				self.kingPosition = i

		# postcondition: 
		assert len(self.cells) == 64
		assert len(self.freeCells) >= 32
		# assert len(self.getPlayerCells()) <= 32
		# assert len(self.getEnemyCells()) <= 32
		assert len(self.blackCells) <= 32
		assert len(self.whiteCells) <= 32
		assert len(self.blackCells) + len(self.whiteCells) + len(self.freeCells) == 64

	def isCheck(self):
		# TODO
		pass

	def move(self, position, moveTo):
		nextTurn = deepcopy(self)
		assert self == nextTurn  # checks all attributes

		# make the move
		nextTurn.cells[moveTo] = self.cells[position]
		nextTurn.cells[position] = 0
		if self.playerTurn == "white":
			nextTurn.playerTurn = "black"
		else:
			nextTurn.playerTurn = "white"
		nextTurn.updateInfo()

		# next turn the amount of pieces belonging to the player does not change
		len(self.getPlayerCells()) == len(nextTurn.getEnemyCells())
		# next turn the enemy will have less or equally many pieces
		assert len(self.getEnemyCells()) >= len(nextTurn.getPlayerCells())
		# next turn the enemy will have at most one piece less
		assert len(self.getEnemyCells()) <= len(nextTurn.getPlayerCells()) + 1
		# next turn there will be more or equally many free cells
		assert len(self.freeCells) <= len(nextTurn.freeCells)
		# next turn there will be at most one free cell more
		assert len(self.freeCells) >= len(nextTurn.freeCells) - 1

		return nextTurn

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
