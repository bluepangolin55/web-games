from random import randint


def createSudoku():
	s = Sudoku()
	p = randint(0, 81)
	s.emptyCells.remove(p)
	s.insert(p, randint(1, 10))

	s.solve()
	return s


class Sudoku():
	def __init__(self):
		self.cells = []
		self.possibilites = []
		for i in range(0, 81):
			self.cells.append(0)
			self.possibilites.append(list(range(1, 10)))
		self.lines = []
		self.columns = []
		self.boxes = []
		for i in range(0, 9):
			self.lines.append(9 * [False])
			self.columns.append(9 * [False])
			self.boxes.append(9 * [False])
		self.emptyCells = list(range(0, 81))

	def printASCII(self):
		for i in range(0, 9):
			for j in range(0, 9):
				if j % 3 == 2 and j != 8:
					print(self.cells[i * 9 + j], end=' | ')
				else:
					print(self.cells[i * 9 + j], end='   ')

			print()
			if i % 3 == 2 and i != 8:
				print('_   _   _   _   _   _   _   _   _')
			else:
				print()

	def toJson(self):
		numbers = []
		for i in range(0, 9):
			for j in range(0, 9):
				numbers.append(self.getPossibleChoices(i))
		return jsonify(numbers=numbers)

	def toDict(self):
		numbers = []
		# for i in range(0, 9):
			# for j in range(0, 9):
				# numbers.append(1)
		self.printASCII();
		return {'cells': self.cells}


	def getRow(self, position):
		return position % 9

	def getColumn(self, position):
		return position // 9

	positionToBox = [
		0, 0, 0, 1, 1, 1, 2, 2, 2,
		0, 0, 0, 1, 1, 1, 2, 2, 2,
		0, 0, 0, 1, 1, 1, 2, 2, 2,
		3, 3, 3, 4, 4, 4, 5, 5, 5,
		3, 3, 3, 4, 4, 4, 5, 5, 5,
		3, 3, 3, 4, 4, 4, 5, 5, 5,
		6, 6, 6, 7, 7, 7, 8, 8, 8,
		6, 6, 6, 7, 7, 7, 8, 8, 8,
		6, 6, 6, 7, 7, 7, 8, 8, 8,
	]

	boxToPosition = [
		[0, 1, 2, 9, 10, 11, 18, 19, 20],
		[3, 4, 5, 12, 13, 14, 21, 22, 23],
		[6, 7, 8, 15, 16, 17, 24, 25, 26],
		[27, 28, 29, 36, 37, 38, 45, 46, 47],
		[30, 31, 32, 39, 40, 41, 48, 49, 50],
		[33, 34, 35, 42, 43, 44, 51, 52, 53],
		[54, 55, 56, 63, 64, 65, 72, 73, 74],
		[57, 58, 59, 66, 67, 68, 75, 76, 77],
		[60, 61, 62, 69, 70, 71, 78, 79, 80],
	]

	def getBox(self, position):
		return self.positionToBox[position]

	def insert(self, position, number):
		row = self.getRow(position)
		col = self.getColumn(position)
		box = self.boxToPosition[self.getBox(position)]
		self.cells[position] = number
		# if self.lines[0][number]:
			# self.cells[position] = number

		for i in range(0, 9):
			if (number in self.possibilites[9 * row + i]):
				self.possibilites[9 * row + i].remove(number)
			if (number in self.possibilites[9 * i + col]):
				self.possibilites[9 * i + col].remove(number)
			if (number in self.possibilites[box[i]]):
				self.possibilites[box[i]].remove(number)

	def solve(self):
		# the history stores (position, value)-tuples in the
		# order in which they were put.
		history = []
		for i in self.emptyCells:
			self.insert(i, 2)

s = createSudoku()
s.printASCII()
