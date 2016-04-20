var canvas = document.getElementById("a");
var context = canvas.getContext("2d");

// the cell that the player selects with a mouse
// must contain a piece of the player
var selectedCell = -1

// the cell the player wants to move to
var moveTo = -1

// this is the json object that the client receives from the server
var data

// an array holding the possible choices for the selected piece
var allPossibleChoices

// a client side representation of the field: array of 64 elements. 
// each element represents the contents of a cell
// entries are of the form: "free", "blackPawn", etc.
var cells = []

dataLoaded = false

// calculate cell size
cellSize = canvas.offsetWidth;
if(canvas.offsetHeight < cellSize){
	cellSize = canvas.offsetHeight;
}
cellSize = cellSize / 8


function getCursorPosition(canvas, event) {
	alert("hi")
	var rect = canvas.getBoundingClientRect();
	var x = event.clientX - rect.left;
	var y = event.clientY - rect.top;
	console.log("x: " + x + " y: " + y);
}

// get the most recent data from the server and
// refresh the client side representation
var getData = function(e) {
	$.getJSON(
		$SCRIPT_ROOT + '/_get_board', 
		{
			a: selectedCell,
			b: moveTo
		}, 
		function(receivedData) {
			data = receivedData
			cells = data.cells
			allPossibleChoices = data.choices
			dataLoaded = true
		}
	);
	return false;
};

// Set the global configs to synchronous 
$.ajaxSetup({
    async: false
});

// request possible choices from the server
// var getChoices = function(e) {
// 	$.getJSON(
// 		$SCRIPT_ROOT + '/_get_choices', 
// 		{
// 			a: selectedCell
// 		}, 
// 		function(data) {
// 			allPossibleChoices = data.choices
// 		}
// 	);
// 	return false;
// };

function getImage(code){
	switch(code){
		case 1: return document.getElementById("blackPawn")
		case 2: return document.getElementById("blackKnight")
		case 3: return document.getElementById("blackBishop")
		case 4: return document.getElementById("blackRook")
		case 5: return document.getElementById("blackQueen")
		case 6: return document.getElementById("blackKing")
		case 11: return document.getElementById("whitePawn")
		case 12: return document.getElementById("whiteKnight")
		case 13: return document.getElementById("whiteBishop")
		case 14: return document.getElementById("whiteRook")
		case 15: return document.getElementById("whiteQueen")
		case 16: return document.getElementById("whiteKing")
	}
}

function getPieceColor(code){
	if (code > 10){
		return "white"	
	}
	else if (code > 0){
		return "black" 
	}
	else{
		return "none"
	}
}

function getPieceType(code){
	t = code % 10
	switch(t){
		case 1: return "pawn"
		case 2: return "knight"	
		case 3: return "bishop" 
		case 4: return "rook" 
		case 5: return "queen" 
		case 6: return "king" 
		default : return "none"
	}
}


function drawField(){
	// draw the chess board
	var x = 0;
	var y = 0;
	while(y < 8){
		if((x+y) % 2 == 0){
			context.fillStyle = "#FFFFEE"
		}
		else{
			context.fillStyle = "#555555"
		}
		context.fillRect(x*cellSize, y*cellSize, cellSize, cellSize)
		x++
		if(x%8 == 0){
			x = 0
			y++
		}
	}

	// highlight the selected cell
	if(-1 < selectedCell && selectedCell < 64){
		x = selectedCell % 8
		y = Math.floor(selectedCell / 8)
		context.fillStyle = "#FFFF44"
		context.fillRect(x*cellSize, y*cellSize, cellSize, cellSize)
		// highlight the possible choices 
		context.fillStyle = "#FFAA44"
		possibleChoices = allPossibleChoices[selectedCell]
		for(var i in possibleChoices){
			x = possibleChoices[i] % 8
			y = Math.floor(possibleChoices[i] / 8)	
			context.fillRect(x*cellSize, y*cellSize, cellSize, cellSize)
		}
	}

	// draw the pieces
	for(var i in cells){
		x = i % 8
		y = Math.floor(i / 8)
		if(cells[i] != 0){
			context.drawImage(getImage(cells[i]), x*cellSize, y*cellSize, cellSize, cellSize);
		}
	}
}

canvas.addEventListener("click", mouseClicked, false)

function mouseClicked(e) {
	var x = e.pageX - $(canvas).offset().left
	var y = e.pageY - $(canvas).offset().top

	if (data == null){
		alert("data is null")
		getData()
		alert("data fetched")
		return
	}

	selection = cellFromCoordinates(x, y)
	if(getPieceColor(cells[selection]) == data.playerTurn){
		selectedCell = selection
		// getChoices()
	}
	else if(getPieceColor(cells[selectedCell]) == data.playerTurn){
		possibleChoices = allPossibleChoices[selectedCell]
		for(var i in possibleChoices){
			if(possibleChoices[i] == selection){
				// alert("move!")
				moveTo = selection
				getData()
				moveTo = -1
				selectedCell = -1
			}
		}
	}
	drawField()
}

function cellFromCoordinates(x, y){
	return Math.floor(x/cellSize) + 8*Math.floor(y/cellSize)
}

// code to be run when the website starts
getData()
drawField()



