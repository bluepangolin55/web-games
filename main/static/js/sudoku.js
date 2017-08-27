var canvas = document.getElementById("sudoku");
var context = canvas.getContext("2d");

var color1 = "#EEEEEE"
var color2 = "#EEEEEE"

// the cell that the player selects with a mouse
var selectedCell = -1

// this is the json object that the client receives from the server
var data

var socket

// a client side representation of the field: array of 64 elements.
// each element represents the contents of a cell
// entries are of the form: "free", "blackPawn", etc.
var cells = []

// calculate cell size
cellSize = canvas.offsetWidth;
if(canvas.offsetHeight < cellSize){
	cellSize = canvas.offsetHeight;
}
cellSize = cellSize / 9


function getCursorPosition(canvas, event) {
	var rect = canvas.getBoundingClientRect();
	var x = event.clientX - rect.left;
	var y = event.clientY - rect.top;
	console.log("x: " + x + " y: " + y);
}

// Set the global configs to synchronous
$.ajaxSetup({
	async: false
});


function drawField(){
	// draw the chess board
	var x = 0;
	var y = 0;
	while(y < 9){
		if((x+y) % 2 == 0){
			context.fillStyle = color1
		}
		else{
			context.fillStyle = color2
		}
		context.fillRect(x*cellSize, y*cellSize, cellSize, cellSize)
		x++
		if(x%9 == 0){
			x = 0
			y++
		}
	}
	context.fillStyle = "#888888"
	context.fillRect(3*cellSize, 0, 2, 9*cellSize)
	context.fillRect(6*cellSize, 0, 2, 9*cellSize)
	context.fillRect(0, 3*cellSize, 9*cellSize, 2)
	context.fillRect(0, 6*cellSize, 9*cellSize, 2)
	context.font = "40px Arial";

	context.lineWidth = 4
	context.fillStyle = "#f4f4f4"
	context.strokeStyle = "#ffff22"
	context.fillRect(cellSize, 0, cellSize, cellSize);
	context.strokeRect(cellSize, 0, cellSize, cellSize);
	context.fillStyle = "#444444"


	for(var x = 0; x<9; x++){
		for(var y = 0; y<9; y++){
			value = cells[y*9 + x]
			if(value == 0){
				continue;
			}
			xMargin = 24
			yMargin = 20
			context.fillText(value, x*cellSize+xMargin, (y+1)*cellSize-yMargin)
		}
	}
}

canvas.addEventListener("click", mouseClicked, false)

function mouseClicked(e) {
	var x = e.pageX - $(canvas).offset().left
	var y = e.pageY - $(canvas).offset().top

	drawField()
}

function cellFromCoordinates(x, y){
	return Math.floor(x/cellSize) + 9*Math.floor(y/cellSize)
}


document.addEventListener("DOMContentLoaded", theDomHasLoaded, false);
window.addEventListener("load", pageFullyLoaded, false);
window.addEventListener("refresh", pageFullyLoaded, false);

function theDomHasLoaded(e) {
}

function pageFullyLoaded(e) {
}

$(document).ready(function(){
	namespace = '/test'; // change to an empty string to use the global namespace

	// the socket.io documentation recommends sending an explicit package upon connection
	// this is specially important when using the global namespace
	socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

	socket.on('turn data', function(message) {
		// alert("received something")
		data = message
		// data = []
		cells = data.cells
		// choices = data.choices
		drawField()
	});

   // event handler for new connections
	socket.on('connect', function() {
		// alert(sessionStorage.getItem("id"))
		for(let i = 0; i<81; i++){
			$("#sudoku_field").append("<input class='sudoku_cell' type='text' name='' value=''>");
			// $("#sudoku_field").append("<div class='sudoku_cell' type='text' name='' value=''>");
		}

		socket.emit('new sudoku game', {id: sessionStorage.getItem("id")});
	});


canvas.addEventListener("click", mouseClicked, false)

function mouseClicked(e) {
	// var x = e.pageX - $(canvas).offset().left
	// var y = e.pageY - $(canvas).offset().top

	// if (data == null){
		socket.emit('request data', {id: sessionStorage.getItem("id")});
		return
	// }
}

});
