import sqlite3
import os

def main():
    #Remove old data base file
    if os.path.isfile('sensor_data.sqlite'):
        print('Deleting old data base')
        os.remove('sensor_data.sqlite')

    #Create new database and establish a connection
    new_db = sqlite3.connect('sensor_data.sqlite')
    new_db_cursor = new_db.cursor()
    
    #Add barometric pressure data table
    new_db_cursor.execute("""
        CREATE TABLE "BARO" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "time" DATETIME NOT NULL ,
"raw" TEXT NOT NULL , "temp" FLOAT NOT NULL , "barometric" FLOAT NOT NULL )
        """)

    #Add humidity sensor data table
    new_db_cursor.execute("""
        CREATE TABLE "HUMID" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "time" DATETIME NOT NULL ,
"raw" TEXT NOT NULL , "temp" FLOAT NOT NULL , "humidity" FLOAT NOT NULL )
        """)

    #Add IR Temperature sensor data table
    new_db_cursor.execute("""
        CREATE TABLE "IRTEMP" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "time" DATETIME NOT NULL ,
"raw" TEXT NOT NULL , "objTemp" FLOAT NOT NULL , "ambTemp" FLOAT NOT NULL )
        """)

    #Add light/optical sensor data table
    new_db_cursor.execute("""
        CREATE TABLE "OPTI" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "time" DATETIME NOT NULL ,
"raw" TEXT NOT NULL , "light" FLOAT NOT NULL )
        """)

    #Add movement sensors data table
    new_db_cursor.execute("""
        CREATE TABLE "MVMT" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "time" DATETIME NOT NULL ,
"raw" TEXT NOT NULL , "gyroX" FLOAT NOT NULL , "gyroY" FLOAT NOT NULL , "gyroZ" FLOAT NOT NULL , "accX" FLOAT NOT NULL ,
"accY" FLOAT NOT NULL , "accZ" FLOAT NOT NULL , "magX" FLOAT NOT NULL , "magY" FLOAT NOT NULL , "magZ" FLOAT NOT NULL )
        """)

    new_db.commit()
    new_db.close()

main()
