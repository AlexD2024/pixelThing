#Runs once a day, every day
import os
from datetime import date as d

colorPathBack = f'/home/CashDot/Pixel Site/backups/{d.today().year}/{d.today()}-col.txt'
locPathBack = f'/home/CashDot/Pixel Site/backups/{d.today().year}/{d.today()}-loc.txt'
colPath = '/home/CashDot/Pixel Site/saves/colors.txt'
locPath = '/home/CashDot/Pixel Site/saves/location.txt'

if not os.path.isdir(f'/home/CashDot/Pixel Site/backups/{d.today().year}'):
    os.mkdir(f'/home/CashDot/Pixel Site/backups/{d.today().year}')

with open(colPath, 'r+') as file:
    with open(locPath, 'r+') as f:
        with open(locPathBack, 'w') as locSave:
            with open(colorPathBack, 'w') as colSave:
                for item in file.readlines():
                    colSave.write(item)
                for item in f.readlines():
                    locSave.write(item)

#Checks if a new year ticked over.
if not os.path.isdir(f'/home/CashDot/Pixel Site/saves/previous/{d.today().year - 1}'):
    os.mkdir(f'/home/CashDot/Pixel Site/saves/previous/{d.today().year - 1}')
    with open(colPath, 'r+') as file:
        with open(locPath, 'r+') as f:
            locations = f.readlines()
            colors = file.readlines()
            f.seek(0)
            file.seek(0)
            f.truncate(0)
            file.truncate(0)
            with open(f'/home/CashDot/Pixel Site/saves/previous/{d.today().year - 1}/colors.txt', 'w') as colSaving:
                for item in colors:
                    colSaving.write(item)
            with open(f'/home/CashDot/Pixel Site/saves/previous/{d.today().year - 1}/location.txt', 'w') as locSaving:
                for item in locations:
                    locSaving.write(item)
