import sqlite3
import sys
from dao import DAO, DB_NAME
from datetime import datetime, timedelta

LOW = 0
MED = 1
HIGH = 2 
EMERGENCY = 3

NOTIFICATIONS_DATABASE = "notifications.sqlite"

'''NOTIFICATION_FUNCTIONS = {
    LOW: low_notifications,
    MED: med_notifications,
    HIGH: high_notifications,
    EMERGENCY: emergency_notifications}'''

def generate_notification(threshold):
    notifications_db = sqlite3.connect(NOTIFICATIONS_DATABASE)
    notifications_db_cur = notifications_db.cursor()

    sensor_data_db = DAO(DB_NAME)
    
    notifications = []
    
    for i in range(threshold,HIGH + 1): 
        for notification in NOTIFCATION_FUNCTIONS[i](sensor_data_db):
            notifications_db_cur.execute(
                "INSERT INTO NOTIFICATIONS (time,importance,message,viewed) VALUES (?,?,?,?)",
                datetime.now(),i,notification,False)

    notifications_db.commit()
    notifcations_db.close()

'''
These fucntions generate notifcations of their respective importance

@param db DAO object with a connection to the sensor data database

@return Array or messages
'''
def low_notifications(db):
    notifications = []
    db.open(False)
    
    reading = db.get_recent("baro")
    notifications.append("The current temperature is " + str(reading[0][3]) + "°C")
    
    db.close()
    return notifications

def med_notifications(db):
    notifications = []
    db.open(False)

    readings = db.get_recent("baro") + db.get_recent("humid")
    notifications.append("The current temperature is " + 
                        str(readings[0][3]) + 
                        "°C with a relative humidty of " +
                        str(readings[1][4]) + "%")

    db.close()
    return notifications

def high_notifications(db):
    notifications = []
    db.open(False)

    readings = []
    for s in ["baro","humid","irtemp","opti"]:
        readings += db.get_recent(s)
    notifications.append("Current weather:\nTemperature: " +
                        str(readings[0][3]) + "°C\nHumidity: " +
                        str(readings[1][4]) + "%\nBarometric Pressure: " +
                        str(readings[0][4]) + "hBa\nLuminosity: " +
                        str(readings[3][3]) + "Lux")

    db.close()
    return notifications

def emergency_notifications(db):
    return []

NOTIFICATION_FUNCTIONS = {
    LOW: low_notifications,
    MED: med_notifications,
    HIGH: high_notifications,
    EMERGENCY: emergency_notifications}

def main():
    if not len(sys.argv) == 2:
        print("Incorrect number of arguments")

    theshold = int(sys.argv[1])

    generate_notification(threshold)

main()
