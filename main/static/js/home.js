var canvas = document.getElementById("chess");
var context = canvas.getContext("2d");

// this is the json object that the client receives from the server
var data

// this is the users ID that is established when he enters the website.
var id

var socket


// calculate cell size
cellSize = canvas.offsetWidth;
if(canvas.offsetHeight < cellSize){
	cellSize = canvas.offsetHeight;
}
cellSize = cellSize / 8


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
}

canvas.addEventListener("click", mouseClicked, false)

function mouseClicked(e) {
	var x = e.pageX - $(canvas).offset().left
	var y = e.pageY - $(canvas).offset().top

	if (data == null){
		socket.emit('request data', {data: 'Hi there!!'});
		return
	}
	drawField()
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

	socket.on('new ID', function(message) {
		// alert("received something")
		id = message.id
		sessionStorage.setItem("id", id)
		// alert(sessionStorage.getItem("id"))

		drawField()
	});

   // event handler for new connections
	socket.on('connect', function() {
		socket.emit('request ID', {data: 'Hi there!!'});
	});

});
