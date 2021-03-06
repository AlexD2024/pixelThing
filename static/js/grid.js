//Getting info from html/python

var colorUsing = document.getElementById('colorChoice').innerHTML.trim();
var savedColors = document.getElementById('savedColors').innerHTML.trim();
var savedCoords = document.getElementById('savedCoords').innerHTML.trim();
var hour = document.getElementById('hour').innerHTML.trim();
var savedTimes = document.getElementById('times').innerHTML.trim();
var pos = [];
var col = [];
var pixels = '';

var canvas = document.getElementById('grid');
var context = canvas.getContext('2d');

//Checks to make sure user has correct saved info

function checkStorage() {
    if (localStorage.getItem('count') === null) {
        localStorage.setItem('count', '0a' + hour);
        pixels = 0;
    } else if (parseInt(localStorage.getItem('count').split('a')[1]) != parseInt(hour)) {
        localStorage.setItem('count', '0a' + hour);
        pixels = 0;
    } else {
        pixels = parseInt(localStorage.getItem('count').split('a')[0]);
    }
}

checkStorage();
setInterval(checkStorage, 750);

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

function fillSquare(x, y, colorToUse){
    context.fillStyle = colorToUse;
    context.fillRect(x,y,10,10);
}


drawGrid(context);

//Prepares the locations and colors for usage
savedCoords = savedCoords.replace('[', '');
savedCoords = savedCoords.replace(']', '');
savedCoords = savedCoords.split(',');
savedColors = savedColors.replace('[', '');
savedColors = savedColors.replace(']', '');
savedColors = savedColors.split(',');
savedTimes = savedTimes.replace('[', '');
savedTimes = savedTimes.replace(']', '');
savedTimes = savedTimes.split(',');

async function delay(ms) {
    return await new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
    for (let x = 0; x < savedCoords.length; x +=1) {
        var time = parseInt(savedTimes[x]);
        let xy = savedCoords[x].split('a');
        let color = savedColors[x];
        xy[1] = xy[1].replace("'", '');
        xy[0] = xy[0].replace("'", '');
        xy[1] = xy[1].replace("'", '');
        xy[0] = xy[0].replace("'", '');
        color = color.replace("'", '');
        color = color.replace("'", '');
        if (time) {
            fillSquare(xy[0], xy[1], color);
        }
        const highestId = window.setTimeout(() => {
            for (let i = highestId; i >= 0; i--) {
            window.clearInterval(i);
            }
        }, 0);
        await delay(time/100);
    }
}
if (savedTimes[0] != 'a') {
    run();
} else {
    for (let x = 0; x < savedCoords.length; x +=1) {
        let xy = savedCoords[x].split('a');
        let color = savedColors[x];
        xy[1] = xy[1].replace("'", '');
        xy[0] = xy[0].replace("'", '');
        xy[1] = xy[1].replace("'", '');
        xy[0] = xy[0].replace("'", '');
        color = color.replace("'", '');
        color = color.replace("'", '');
        fillSquare(xy[0], xy[1], color);
    }
}

//Adds an event listener to the canvas. Only adds it if they have pixels left to use.

var acceptable = ['view', 'View', null, '']

if (acceptable.includes(colorUsing) == false) {
    if (pixels <= 4) {
        canvas.addEventListener('click', function(evt) {
            if (pixels >= 4) {
                this.removeEventListener('click', arguments.callee);
            }
            var mousePos = getSquare(canvas, evt);
            var value = mousePos.x + 'a' + mousePos.y;
            pos.push(value);
            col.push(colorUsing);
            sendPython(pos, col);
            fillSquare(mousePos.x, mousePos.y, colorUsing);
            pixels = parseInt(pixels) + 1
            localStorage.setItem('count', pixels.toString() + 'a' + hour.toString())
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
