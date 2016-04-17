var canvas = document.getElementById("a");
var context = canvas.getContext("2d");

// the cell that the player selects with a mouse
// must contain a piece of the player
var selectedCell = -1

// this is the json object that the client receives from the server
var turnData

// an array holding the possible choices for the selected piece
var possibleChoices

// a client side representation of the field: array of 64 elements. 
// each element represents the contents of a cell
// entries are of the form: "free", "blackPawn", etc.
var cells = []

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
		}, 
		function(data) {
			turnData = data
			cells = data.cells
			// for(var i = 0; i<63; i++){
			// 	cells[i] = "free"
			// }
			// function f1(positions, name){
			// 	for(i in positions){
			// 		cells[positions[i]] = name
			// 	}
			// }
			// f1(turnData.black.pawns, "blackPawn")
			// f1(turnData.black.knights, "blackKnight")
			// f1(turnData.black.bishops, "blackBishop")
			// f1(turnData.black.rooks, "blackRook")
			// f1(turnData.black.queens, "blackQueen")
			// f1(turnData.black.kings, "blackKing")
			// f1(turnData.white.pawns, "whitePawn")
			// f1(turnData.white.knights, "whiteKnight")
			// f1(turnData.white.bishops, "whiteBishop")
			// f1(turnData.white.rooks, "whiteRook")
			// f1(turnData.white.queens, "whiteQueen")
			// f1(turnData.white.kings, "whiteKing")

		}
	);
	return false;
};

// request possible choices from the server
var getChoices = function(e) {
	$.getJSON(
		$SCRIPT_ROOT + '/_get_choices', 
		{
			// a: selectedCell;
		}, 
		function(data) {
			possibleChoices = data.choices
		}
	);
	return false;
};

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
		for(var i in possibleChoices){
			x = possibleChoices[i] % 8
			y = Math.floor(possibleChoices[i] / 8)	
			context.fillRect(x*cellSize, y*cellSize, cellSize, cellSize)
		}
	}

	// draw the pieces
	context.fillStyle = "#000000"
	drawPieces(turnData.black.pawns, document.getElementById("blackPawn"))
	drawPieces(turnData.black.knights, document.getElementById("blackKnight"))
	drawPieces(turnData.black.bishops, document.getElementById("blackBishop"))
	drawPieces(turnData.black.rooks, document.getElementById("blackRook"))
	drawPieces(turnData.black.queens, document.getElementById("blackQueen"))
	drawPieces(turnData.black.kings, document.getElementById("blackKing"))

	context.fillStyle = "#FFFFFF"
	drawPieces(turnData.white.pawns, document.getElementById("whitePawn"))
	drawPieces(turnData.white.knights, document.getElementById("whiteKnight"))
	drawPieces(turnData.white.bishops, document.getElementById("whiteBishop"))
	drawPieces(turnData.white.rooks, document.getElementById("whiteRook"))
	drawPieces(turnData.white.queens, document.getElementById("whiteQueen"))
	drawPieces(turnData.white.kings, document.getElementById("whiteKing"))
}

// draw chess pieces at the given positions
function drawPieces(positions, image) {
	for(i in positions){
		x = positions[i] % 8
		y = Math.floor(positions[i] / 8)
		context.drawImage(image, x*cellSize, y*cellSize, cellSize, cellSize);
	}
}

function fillCircle(context, x, y, radius){
	context.beginPath();
	context.arc(x + radius, y + radius, radius, 0, 2*Math.PI)
	context.closePath();
	context.stroke();
	context.fill()
}

canvas.addEventListener("click", mouseClicked, false)

function mouseClicked(e) {
	getData()
	var x = e.pageX - $(canvas).offset().left
	var y = e.pageY - $(canvas).offset().top

	selection = cellFromCoordinates(x, y)
	if(cells[selection].charAt(0) == turnData.playerTurn.charAt(0)){
		selectedCell = selection
		getChoices()
	}
	else if(cells[selectedCell].charAt(0) == turnData.playerTurn.charAt(0)){
		for(var i in possibleChoices){
			if(possibleChoices[i] == selection){
				alert("move!")
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
