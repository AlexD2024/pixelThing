//Getting info from html/python

var colorUsing = document.getElementById('colorChoice').innerHTML.trim();
var savedColors = document.getElementById('savedColors').innerHTML.trim();
var savedCoords = document.getElementById('savedCoords').innerHTML.trim();
var pos = [];
var col = [];

var canvas = document.getElementById('grid');
var context = canvas.getContext('2d');

//Functions to draw the grid.

function getSquare(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: 1 + (evt.clientX - rect.left) - (evt.clientX - rect.left)%10,
        y: 1 + (evt.clientY - rect.top) - (evt.clientY - rect.top)%10
    };
}

function drawGrid(context) {
    for (var x = 0.5; x < 2001; x += 10) {
      context.moveTo(x, 0);
      context.lineTo(x, 2000);
    }

    for (var y = 0.5; y < 2001; y += 10) {
      context.moveTo(0, y);
      context.lineTo(2000, y);
    }

    context.strokeStyle = "#ddd";
    context.stroke();
}

drawGrid(context);

//Colors a square

function fillSquare(x, y, color){
    context.fillStyle = color;
    context.fillRect(x,y,9,9);
}

//Prepares the locations and colors for usage

savedCoords = savedCoords.replace('[', '');
savedCoords = savedCoords.replace(']', '');
savedCoords = savedCoords.split(',');
savedColors = savedColors.replace('[', '');
savedColors = savedColors.replace(']', '');
savedColors = savedColors.split(',');

//Loops over the locations and colors, then calls the color function.

for (var x = 0; x < savedCoords.length; x +=1){
        var xy = savedCoords[x].split('a');
        var color = savedColors[x];
        xy[1] = xy[1].replace("'", '');
        xy[0] = xy[0].replace("'", '');
        color = color.replace("'", '');
        xy[1] = xy[1].substring(0, xy[1].length - 2);
        color = color.substring(0, color.length - 3);
        if (x == 0) {
            fillSquare(context, xy[0], xy[1], color);
        } else {
            setTimeout(fillSquare, x * 40, xy[0], xy[1], color)
        }
}

