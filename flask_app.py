import os
from flask import Flask, render_template, request, url_for, jsonify, session
from datetime import datetime as dt

app = Flask(__name__)
app.secret_key = 'HUHtgTYFGT7HUgYfYUU'

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

    userIP = request.headers['X-Real-Ip']
    with open('/home/CashDot/Pixel Site/saves/pixelUsage/pixelUsage.txt', 'r+') as file:
        allIP = file.read()
        toWrite = []
        allIP = allIP.split('-')
        allIP.remove('')

        with open(f"/home/CashDot/Pixel Site/saves/pixelUsage/{userIP}.txt", 'a+') as f:
                nextTicker = f.readline(0)
        if 'ticker' in session:
            currentTick = session['ticker']
        else:
            with open(f"/home/CashDot/Pixel Site/saves/pixelUsage/{userIP}.txt", 'w') as f:
                session['ticker'] = int(nextTicker)
                f.write(str(int(nextTicker)+1))

        for IP in allIP:
            IP = IP.split('l')

            if str(userIP) == IP[0] and str(IP[1].split('a')[1]) == str(currentTick):
                pixels = IP[1]
                userIP = IP[0]
                break
            else:
                pixels = '0a' + str(nextTicker)
                toWrite.append(userIP + 'l' + '0a' + str(nextTicker) + '-')
                for item in toWrite:
                    file.write(item)
                break

        return render_template('index.html', color=color, savedCol=colors, savedCoo=coords, pixels=pixels)

    return render_template('index.html', savedCol=colors, savedCoo=coords)

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
    saved = f.read()
    saved2 = file.read()
    f.write(color[len(color)-1] + '\n')
    file.write(location[len(location)-1] + '\n')
    f.close()
    file.close()

    with open('/home/CashDot/Pixel Site/saves/pixelUsage/pixelUsage.txt', 'r+') as file:
        userIP = request.headers['X-Real-Ip']
        allIP = file.read()
        allIP = allIP.split('-')
        allIP.remove('')
        file.seek(0)
        file.truncate()
        toWrite = []
        currentTick = session['ticker']
        for IP in allIP:
            IP = IP.split('l')

            with open(f"/home/CashDot/Pixel Site/saves/pixelUsage/{IP[0]}.txt", 'a+') as f:
                nextTicker = f.read()
            with open(f"/home/CashDot/Pixel Site/saves/pixelUsage/{IP[0]}.txt", 'w') as f:
                if nextTicker == '':
                    nextTicker = 7
                    f.write(str(nextTicker))


                if str(userIP) == IP[0] and int(currentTick) == int(IP[1].split('a')[1]):
                    pixels = int(IP[1].split('a')[0])
                    pixels += 1
                    userIP = IP[0]
                    toWrite.append(userIP + 'l' + str(pixels) + 'a' + IP[1].split('a')[1] + '-')
                    break
        for item in toWrite:
            file.write(item)

    return jsonify('success')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8085, debug=True)