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

    def save(self):
        if self.saving:
            self.connection.commit()

'''
def main():
  con = sqlite3.connect('sensor_data.sqlite')
  print("Opened database successfully")
  cur = con.cursor()
  cur.execute("SELECT time, temp, barometric  FROM BARO")
  for row in cur:
    print("time = ", row[0])
    print("temp = ", row[1])
    print("barometric = ", row[2], "\n")
  con.close()
main()
'''
