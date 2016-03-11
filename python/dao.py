import sqlite3
from datetime import datetime, date

DB_NAME = 'sensor_data.sqlite'

class DAO:
  
    connection = None
    cursor = None
    saving = False
  
    def __init__(self, file_name, saving):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()
        self.saving = saving

    def save(self):
        if self.saving:
            self.connection.commit()

    def close(self):
        self.save()
        self.connection.close()
        self.cursor = None
        self.connection = None

    def store_irtemp(self, raw, obj_temp, amb_temp):
        self.cursor.execute("INSERT INTO IRTEMP (time,raw,objTemp,ambTemp) VALUES (?,?,?,?)",
                            (datetime.now(),raw,round(obj_temp,2),round(amb_temp,2)))
        self.save()

    def store_humid(self, raw, temp, humidity):
        self.cursor.execute("INSERT INTO HUMID (time,raw,temp,humidity) VALUES (?,?,?,?)",
                            (datetime.now(),raw,round(temp,2),round(humidity,2)))
        self.save()

    def store_baro(self, raw, temp, pressure):
        self.cursor.execute("INSERT INTO BARO (time,raw,temp,pressure) VALUES (?,?,?,?)",
                            (datetime.now(),raw,round(temp,2),round(pressure,2)))
        self.save()

    def store_opti(self,raw,light):
        self.cursor.execute("INSERT INTO OPTI (time,raw,light) VALUES (?,?,?)",
                            (datetime.now(),raw,round(light,2)))
        self.save()

    def get_irtemp(self,entries=1):
        data = self.cursor.execute("SELECT * FROM IRTEMP AS ir WHERE ir.time > ? ORDER BY ir.id DESC LIMIT ?",
                                   (datetime.today().replace(hour=0,minute=0,second=0,microsecond=0),str(entries))).fetchall()
        return data
    def get_hourly_irtemp(self):
        pass

    def get_daily_irtemp(self):
        pass
