#Runs once a day, every day

from datetime import date as d

with open('/home/AlexDooley/Pixel Site test/saves/colors.txt', 'r+') as file:
    with open('/home/AlexDooley/Pixel Site test/saves/location.txt', 'r+') as f:
        with open(f'/home/AlexDooley/Pixel Site test/backups/{d.today()}-loc.txt', 'w') as locSave:
            with open(f'/home/AlexDooley/Pixel Site test/backups/{d.today()}-col.txt', 'w') as colSave:
                for item in file.readlines():
                    colSave.write(item)
                for item in f.readlines():
                    locSave.write(item)
