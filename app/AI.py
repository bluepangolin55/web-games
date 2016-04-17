from .chess import Chess, Move
from random import random

# a map of how valuable a position is
cellValues = [
			0, 0, 0, 0, 0, 0, 0, 0,
			0, 1, 1, 1, 1, 1, 1, 0,
			0, 1, 2, 2, 2, 2, 1, 0,
			0, 1, 2, 4, 4, 2, 1, 0,
			0, 1, 2, 4, 4, 2, 1, 0,
			0, 1, 2, 2, 2, 2, 1, 0,
			0, 1, 1, 1, 1, 1, 1, 0,
			0, 0, 0, 0, 0, 0, 0, 0]

pieceValues = {
	0: 0,
	1: 1, 11: 1,
	2: 3, 12: 3,
	3: 3, 13: 3,
	4: 5, 14: 5,
	5: 9, 15: 9,
	6: 0, 16: 0
}


class AI():
	def __init__(self):
		pass

	def nextMove(self, state):
		"""pre: isinstance(state, Chess) """
		assert(isinstance(state, Chess))

		player = state.playerTurn

		bestMove = None
		bestGrade = - 999
		for cell in state.getPlayerCells():
			for choice in state.getPossibleChoices(cell):
				# nextTurn = state.move(cell, choice)
				move = Move(cell, choice, state)
				print(player)
				print("from: " + str(move.moveFrom))
				print("to: " + str(move.moveTo))
				state.applyMove(move)
				grade = self.gradeTurn(state, player) + random()
				state.revertMove(move)
				print("grade " + str(grade))
				if(grade > bestGrade):
					bestMove = move
					bestGrade = grade

		return bestMove

	def gradeTurn(self, turn, player=None):
		assert(isinstance(turn, Chess))
		if player is None:
			player = turn.playerTurn
		assert(type(player) is str)
		opponent = {"white": "black", "black": "white"}[player]
		scores = []
		weights = [10, 1]

		relPieceValues = self.totalPieceValues(turn)
		scores.append(relPieceValues[player] - relPieceValues[opponent])

		choices = self.gradedNumberOfChoices(turn)
		scores.append(choices[player] - 10*choices[opponent])

		return sum([a*b for a, b in zip(scores, weights)])

	def totalPieceValues(self, state):
		black = 0
		white = 0
		for cell in state.blackCells:
			black += pieceValues[state.cells[cell]]
		for cell in state.whiteCells:
			white += pieceValues[state.cells[cell]]
		return {'white': white, 'black': black}

	#  gives a grade for well positioned units
	def advancementGrade(self, state):
		white = 0
		black = 0
		for cell in state.blackCells:
			black += pieceValues[state.cells[cell]]
		for cell in state.whiteCells:
			white += pieceValues[state.cells[cell]]
		return {'white': white, 'black': black}

	def numberOfChoices(self, state):
		"""Returns the number of choices for both players in the current turn."""
		black = 0
		white = 0
		for cell in state.blackCells:
			black = len(state.getPossibleChoices(cell))
		for cell in state.whiteCells:
			white = len(state.getPossibleChoices(cell))
		return {"black": black, "white": white}

	def gradedNumberOfChoices(self, state):
		"""Returns the weighted number of choices
			for both players in the current turn.
			Implements all other tactics"""
		print("grading number of choices")
		print("player is: " + state.playerTurn)
		black = 0
		white = 0
		for cell in state.blackCells:
			for target in state.getPossibleChoices(cell):
				if target in state.whiteCells:
					black += pieceValues[state.cells[target]]
				# if target > 31:
					# black += 1
				# black += cellValues[target]
		for cell in state.whiteCells:
			for target in state.getPossibleChoices(cell):
				if target in state.blackCells:
					white += pieceValues[state.cells[target]]
				# if target < 32:
					# white += 1
				# white += cellValues[target]
		return {"black": black, "white": white}

	def spaceGradeLarryEvans(self, state):
		"""Returns the number of choices that move a piece to the opponents territory
			for both players in the current turn. Defined by Larry Evans."""
		black = 0
		white = 0
		for cell in state.blackCells:
			for c in state.getPossibleChoices(cell):
				if c > 31:
					black += 1
		for cell in state.whiteCells:
			for c in state.getPossibleChoices(cell):
				if c < 32:
					white += 1
		return {"black": black, "white": white}

	def defense(self, state):
		black = 0
		white = 0
		for cell in state.whiteCells:
			for c in state.getPossibleChoices(cell):
				if cell in state.blackCells:
					black -= pieceValues[state.cells[cell]]

		for cell in state.blackCells:
			for c in state.getPossibleChoices(cell):
				if cell in state.whiteCells:
					white -= pieceValues[state.cells[cell]]
		return {"black": black, "white": white}

	def controlOfCenter(self, state):
		"""Returns the number of choices weighted by a space map.
			Controlling the center is important. """
		black = 0
		white = 0
		for cell in state.blackCells:
			for target in state.getPossibleChoices(cell):
				black += cellValues[target]
		for cell in state.whiteCells:
			for target in state.getPossibleChoices(cell):
				white += cellValues[target]
		return {"black": black, "white": white}
