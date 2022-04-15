//Getting info from html/python

var colorUsing = document.getElementById('colorChoice').innerHTML.trim();
var savedColors = document.getElementById('savedColors').innerHTML.trim();
var savedCoords = document.getElementById('savedCoords').innerHTML.trim();
var pixels = document.getElementById('pixels').innerHTML.trim().split('a')[0];
var pos = [];
var col = [];

var canvas = document.getElementById('grid');
var context = canvas.getContext('2d');

//Functions to draw grid

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

function fillSquare(context, x, y, colorToUse){
    context.fillStyle = colorToUse;
    context.fillRect(x,y,9,9);
}


drawGrid(context);

//Prepares the locations and colors for usage

savedCoords = savedCoords.replace('[', '');
savedCoords = savedCoords.replace(']', '');
savedCoords = savedCoords.split(',');
savedColors = savedColors.replace('[', '');
savedColors = savedColors.replace(']', '');
savedColors = savedColors.split(',');

for (var x = 0; x < savedCoords.length; x +=1){
    var xy = savedCoords[x].split('a');
    var color = savedColors[x];
    xy[1] = xy[1].replace("'", '');
    xy[0] = xy[0].replace("'", '');
    color = color.replace("'", '');
    xy[1] = xy[1].substring(0, xy[1].length - 2);
    color = color.substring(0, color.length - 3);
    fillSquare(context, xy[0], xy[1], color);
}

//Adds an event listener to the canvas. Only adds it if they have pixels left to use.

var acceptable = ['view', 'View', null, '']

if (acceptable.includes(colorUsing) == false) {
    if (parseInt(pixels) <= 4) {
        canvas.addEventListener('click', function(evt) {
            if (parseInt(pixels) >= 4) {
                this.removeEventListener('click', arguments.callee);
            }
            var mousePos = getSquare(canvas, evt);
            var value = mousePos.x + 'a' + mousePos.y;
            pos.push(value);
            col.push(colorUsing);
            sendPython(pos, col);
            fillSquare(context, mousePos.x, mousePos.y, colorUsing);
            pixels += 1;
        }, false);
    }
}

//Sends data to python

function sendPython(pos, col) {
    $.ajax({
        type: "POST",
        url: "/getData/",
        contentType: "application/json",
        data: JSON.stringify({'loc':pos, 'color':col}),
        dataType: "json",
        success: function(response) {
            console.log(response);
        },
        error: function(err) {
            console.log(err);
        }
    });
}