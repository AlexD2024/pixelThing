import mysql.connector
from flask import Flask, render_template, request, url_for, jsonify, redirect, make_response
from datetime import datetime as dt
from argon2 import PasswordHasher
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

ph = PasswordHasher()

#Sets the current year when the program in ran

currentYear = dt.now().year

#Creates the flask app

app = Flask(__name__)
app.config.from_pyfile('config.py')
mail = Mail(app)

#Email token generator
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

#Connects to MYSQL

db = mysql.connector.connect(
    host="HOST",
    user="USER",
    password="PASSWORD",
    database='DB'
)

#Defines MySQL commands

cursor = db.cursor()
insert = "INSERT INTO pixels (location, color) VALUES (%s, %s)"
getColors = "SELECT color FROM pixels"
getLocations = 'SELECT location FROM pixels'
getTables = 'SHOW TABLES'
getEmail = 'SELECT email FROM users'

#Logout page

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('user')
    return resp

@app.route('/confirm/<token>')
def confirm(token):
    email = serializer.loads(
            token,
            salt=app.config['EMAIL_SALT'],
            max_age=3600
        )
    cursor.execute(f"UPDATE users SET verified=True WHERE email='{email}'")
    db.commit()
    return redirect(url_for('login'))

#Login pages

@app.route('/login')
def login():
    if request.cookies.get('user'):
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def logged():
    db.reconnect()
    user = request.form['username']
    password = request.form['pass']

    if request.cookies.get('user'):
        return redirect(url_for('index'))

    try:
        cursor.execute(f"SELECT password FROM users WHERE username='{user}'")
        passwordStored = cursor.fetchone()
        try:
            if ph.verify(passwordStored[0], password):
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('user', user)
                return resp
        except Exception:
            return(render_template('login.html', error='Incorrect password! Please try again.'))
    except Exception:
        return(render_template('login.html', error='No user found! Please try again.'))

#Signup pages

@app.route('/signup')
def signup():
    if request.cookies.get('user'):
        return redirect(url_for('index'))
    else:
        return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signingUp():
    db.reconnect()
    email = request.form['email']
    user = request.form['username']
    password = request.form['pass']
    password = ph.hash(password)

    cursor.execute('SELECT username FROM users')
    users = cursor.fetchall()
    cursor.execute(getEmail)
    emails = cursor.fetchall()

    for email1 in emails:
        for user1 in users:
            if user in user1:
                return render_template('signup.html', error='Username in use, please pick a different name.')
            elif email in email1:
                return render_template('signup.html', error='Email in use, please use a different email.')

    cursor.execute(f"INSERT INTO users (username, password, email) VALUES ('{user}', '{password}', '{email}')")
    db.commit()
    token = serializer.dumps(email, salt=app.config['EMAIL_SALT'])
    msg = Message(
        'Confirmation Email -- Pixel Coloring',
        recipients=[email],
        html=render_template('confimed.html', confirm_url=url_for('confirm', token=token)),
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
    return redirect(url_for('index'))

# Shows grid/ asks for color

@app.route('/')
def index():
    if request.cookies.get('user'):
        return render_template('colorselect.html')
    else:
        return redirect('/login')

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
    return render_template('index.html', savedCol=colors, savedCoo=coords, hour=dt.now().hour, color=color, savedTimes='[a,a]')

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

    return render_template('index.html', savedCol=colors, savedCoo=coords, savedTimes='[a,a]')

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
    times = []

    if 'year' in request.form:
        year = request.form['year']

    cursor.execute(getTables)
    data = cursor.fetchall()
    for item in data:
        if str(year) == str(item[0]):
            cursor.execute(f'SELECT color FROM `{year}`')
            allColors = cursor.fetchall()
            cursor.execute(f'SELECT location FROM `{year}`')
            allCoords = cursor.fetchall()
            cursor.execute(f"SELECT time FROM `{year}`")
            allTimes = cursor.fetchall()

            for items in allColors:
                for item in items:
                    colors.append(item)
            for items in allCoords:
                for item in items:
                    coords.append(item)
            x = 1
            while x < len(allTimes):
                total = 0
                item = allTimes[x][0]
                try:
                    item = item - allTimes[x-1][0]
                    total += item.total_seconds()
                except IndexError:
                    print('error')

                if total <= 0:
                    total = 1.0

                times.append(total)
                x += 1

            return render_template('index.html', savedCol=colors, savedCoo=coords, savedTimes=times)
        else:
            return render_template('yearSelector.html', error='No page on file for that year.')

# For getting pixel location and color from js

@app.route('/getData/', methods=['POST'])
def get_post_json():
    db.reconnect()

    data = request.get_json()
    location = data['loc']
    color = data['color']
    cursor.execute(f"SELECT placed FROM users WHERE username='{request.cookies.get('user')}'")
    pixels = cursor.fetchone()
    cursor.execute(f"SELECT hour FROM users WHERE username='{request.cookies.get('user')}'")
    hour = cursor.fetchone()
    cursor.execute(f"SELECT verified FROM users WHERE username='{request.cookies.get('user')}'")
    verified = cursor.fetchone()
    if verified[0]:
        if hour[0] != dt.now().hour:
            cursor.execute(f"UPDATE users SET hour='{dt.now().hour}', placed='0' WHERE username='{request.cookies.get('user')}'")
            db.commit()
        if pixels[0] != 5:
            pixels = pixels[0] + 1
            values = (location[len(location)-1], color[len(color)-1])
            cursor.execute(f"UPDATE users SET placed='{pixels}' WHERE username='{request.cookies.get('user')}' ")
            cursor.execute(insert, values)
            db.commit()
            return jsonify('Saved!')
        else:
            return jsonify('Too many pixels placed!')
    return jsonify('Not verified!')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8085, debug=True)
