import mysql.connector
import sys

#Connects to MYSQL

db = mysql.connector.connect(
  host="HOST",
  user="USER",
  password="PASSWORD",
  database='DB'
)

cursor = db.cursor()

def restorePrevious(length):
    cursor.execute(f'DELETE FROM pixels WHERE date > DATE(NOW() - INTERVAL {length} DAY)')
    db.commit()
    print('deleted!')

if __name__ == '__main__':
    restorePrevious(sys.argv[1])
