import sqlite3
import sys
from dao import DAO, DB_NAME
from datetime import datetime, timedelta
import json

LOW = 0
MED = 1
HIGH = 2 
EMERGENCY = 3

NOTIFICATIONS_DATABASE = "/home/pi/SWEN-356-Weather-Machine/python/notifications.sqlite"
NOTIFICATIONS_JSON = "/home/pi/SWEN-356-Weather-Machine/www/html/json/notifications.json"

def generate_notification(threshold):
    notifications_db = sqlite3.connect(NOTIFICATIONS_DATABASE)
    notifications_db_cur = notifications_db.cursor()

    sensor_data_db = DAO(DB_NAME)
    
    notifications = []
    
    for notification in NOTIFICATION_FUNCTIONS[threshold](sensor_data_db):
        print("Added notification:\nTime: " + str(datetime.now()) + 
                "\nImportance: " + str(threshold) + 
                "\nMessage: " + notification)
        notifications_db_cur.execute(
            "INSERT INTO NOTIFICATIONS (time,importance,message,viewed) VALUES (?,?,?,?)",
            (datetime.now(),threshold,notification,False))

    push_notifications(notifcations_db)

    notifications_db.commit()
    notifications_db.close()

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

def push_notifications(db):
    db_cur = db.cursor()
    old_notifications = json.loads(open(NOTIFICATIONS_JSON,"r").read())
    new_notifications = {}
    for key, value in old_notifications.items():
        if value['viewed'] == 1:
            db_cur.execute("UPDATE notifications SET viewed = 1 WHERE id = ?", (value['id'],))
    db.commit()
    unviewed_notifications = db_cur.execute("SELECT * FROM notifications AS n WHERE n.viewed = 0").fetchall()
    for i in range(len(unviewed_notifications)):
        new_notifications[i] = {}
        new_notifications[i]["id"] = unviewed_notifications[i][0]
        new_notifications[i]["time"] = unviewed_notifications[i][1]
        new_notifications[i]["viewed"] = 0
        new_notifications[i]["priority"] = unviewed_notifications[i][2]
        new_notifications[i]["message"] = unviewed_notifications[i][3]
    json_file = open(NOTIFICATIONS_JSON,"w")
    json_file.write(json.dumps(new_notifications,indent=4))
    json_file.close()

NOTIFICATION_FUNCTIONS = {
    LOW: low_notifications,
    MED: med_notifications,
    HIGH: high_notifications,
    EMERGENCY: emergency_notifications}

def main():
    if not len(sys.argv) == 2:
        print("Incorrect number of arguments")

    threshold = int(sys.argv[1])

    generate_notification(threshold)

main()
