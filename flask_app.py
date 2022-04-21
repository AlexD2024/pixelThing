import mysql.connector
from flask import Flask, render_template, request, url_for, jsonify
from datetime import datetime as dt

#Sets the current year when the program in ran

currentYear = dt.now().year

#Creates the flask app

app = Flask(__name__)

#Connects to MYSQL

db = mysql.connector.connect(
  host="HOST",
  user="USER",
  password="PASSWORD",
  database='DB'
)

cursor = db.cursor()
insert = "INSERT INTO pixels (location, color) VALUES (%s, %s)"
getColors = "SELECT color FROM pixels"
getLocations = 'SELECT location FROM pixels'
getTables = 'SHOW TABLES'

# Shows grid/ asks for color

@app.route('/')
def index():
    return render_template('colorselect.html')

@app.route('/', methods=['POST'])
def colorSelected():
    db.reconnect()

    colors = []
    coords = []

    if 'color' in request.form:
        color = request.form['color']

    cursor.execute(getColors)
    allColors = cursor.fetchall()
    cursor.execute(getLocations)
    allCoords = cursor.fetchall()
    for items in allColors:
        for item in items:
            colors.append(item)
    for items in allCoords:
        for item in items:
            coords.append(item)
    return render_template('index.html', savedCol=colors, savedCoo=coords, hour=dt.now().hour, color=color)

# View current page

@app.route('/view')
def viewPage():
    db.reconnect()

    colors = []
    coords = []

    cursor.execute(getColors)
    allColors = cursor.fetchall()
    cursor.execute(getLocations)
    allCoords = cursor.fetchall()
    for items in allColors:
        for item in items:
            colors.append(item)
    for items in allCoords:
        for item in items:
            coords.append(item)
    return render_template('index.html', savedCol=colors, savedCoo=coords)

# View previous pages

@app.route('/previous')
def viewPrev():
    db.reconnect()

    cursor.execute('SELECT YEAR(date) FROM pixels')
    date = cursor.fetchone()
    if currentYear not in date:
        cursor.execute(f"CREATE TABLE `{currentYear}` AS SELECT * FROM pixels")
        cursor.execute('TRUNCATE TABLE pixels')
        cursor.execute("INSERT INTO pixels (location, color) VALUES ('601a131', '#ffffff')")
        db.commit()
    return render_template('yearSelector.html')

@app.route('/previous', methods=['POST'])
def viewPrevious():
    db.reconnect()

    colors = []
    coords = []

    if 'year' in request.form:
        year = request.form['year']

    cursor.execute(getTables)
    data = cursor.fetchall()
    print(data)
    for item in data:
        print(item[0])
        if str(year) == str(item[0]):
            cursor.execute(f'SELECT color FROM `{year}`')
            allColors = cursor.fetchall()
            cursor.execute(f'SELECT location FROM `{year}`')
            allCoords = cursor.fetchall()
            for items in allColors:
                for item in items:
                    colors.append(item)
            for items in allCoords:
                for item in items:
                    coords.append(item)
            return render_template('index.html', savedCol=colors, savedCoo=coords)
        else:
            return render_template('yearSelector.html', error='No page on file for that year.')

# For getting pixel location and color from js

@app.route('/getData/', methods=['POST'])
def get_post_json():
    db.reconnect()

    data = request.get_json()
    location = data['loc']
    color = data['color']

    values = (location[len(location)-1], color[len(color)-1])

    cursor.execute(insert, values)
    db.commit()

    return jsonify('success')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8085, debug=True)
