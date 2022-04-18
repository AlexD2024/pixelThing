import os
from flask import Flask, render_template, request, url_for, jsonify, session
from flask_session import Session
from datetime import datetime as dt

#Configuring the flask app

app = Flask(__name__)

# Shows grid/ asks for color

@app.route('/')
def index():
    return render_template('colorselect.html')

@app.route('/', methods=['POST'])
def colorSelected():
    if 'color' in request.form:
        color = request.form['color']

    with open('/home/CashDot/Pixel Site/saves/colors.txt', 'r') as f:
        with open('/home/CashDot/Pixel Site/saves/location.txt', 'r') as file:
            colors = f.readlines()
            coords = file.readlines()

    return render_template('index.html', savedCol=colors, savedCoo=coords, hour=dt.now().hour, color=color)

# View current page

@app.route('/view')
def viewPage():
    with open('/home/CashDot/Pixel Site/saves/colors.txt', 'r') as f:
        with open('/home/CashDot/Pixel Site/saves/location.txt', 'r') as file:
            colors = f.readlines()
            coords = file.readlines()

    return render_template('index.html', savedCol=colors, savedCoo=coords)

# View previous pages

@app.route('/previous')
def viewPrev():
    return render_template('yearSelector.html')

@app.route('/previous', methods=['POST'])
def viewPrevious():
    prevPath = '/home/CashDot/Pixel Site/saves/previous/'
    if 'year' in request.form:
        year = request.form['year']

    if os.path.isdir(prevPath + year):
        if os.path.isdir(prevPath + year):
            with open(prevPath + year + '/colors.txt', 'r') as f:
                with open(prevPath + year + '/location.txt', 'r') as file:
                    colors = f.readlines()
                    coords = file.readlines()
                    return render_template('previous.html', savedCol=colors, savedCoo=coords, hour=dt.now().hour)
    else:
        return render_template('yearSelector.html', error='No page on file for that year.')

# For getting pixel location and color from js

@app.route('/getData/', methods=['POST'])
def get_post_json():
    data = request.get_json()
    location = data['loc']
    color = data['color']

    f = open('/home/CashDot/Pixel Site/saves/colors.txt', 'r+')
    file = open('/home/CashDot/Pixel Site/saves/location.txt', 'r+')
    f.read()
    file.read()
    f.write(color[len(color)-1] + '\n')
    file.write(location[len(location)-1] + '\n')
    f.close()
    file.close()

    return jsonify('success')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8085, debug=True)