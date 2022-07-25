from flask import Flask
from flask import request
import sys
import csv
import sqlite3

# create sqlite3 database
db = sqlite3.connect('./sensorRead.db')

# create table with columns for distance and time and Date
db.execute('''CREATE TABLE IF NOT EXISTS SensorData
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            distance INTEGER,
            gripperAngle INTEGER,
            time TEXT)''')


# create flask app
app=Flask(__name__)
#create get end point
@app.route('/update_distance')
def update_distance():
    #get ultrasonic distance argument 
    ultrasonicDistance=request.args.get('ultrasonicDistance')
    gripperAngle=request.args.get('gripperAngle')
    
    dataBase = sqlite3.connect('./sensorRead.db')
    #write to db
    dataBase.execute('INSERT INTO SensorData (distance, gripperAngle, time) VALUES (?, ?, datetime("now"))', (ultrasonicDistance, gripperAngle))
    dataBase.commit()
    dataBase.close()
   
    return "200"
        
if __name__ == '__main__':
   
   app.run(host='0.0.0.0', debug = True, port=1880)
    