import sqlite3
from datetime import datetime, date, timedelta

TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
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
        data = self.cursor.execute("SELECT * FROM IRTEMP AS ir WHERE ir.time > ? ORDER BY ir.time DESC LIMIT ?",
                                   (datetime.today().replace(hour=0,minute=0,second=0,microsecond=0),str(entries))).fetchall()
        return data

    def get_hourly_irtemp(self):
        last_day = datetime.today().replace(minute=0,second=0,microsecond=0) - timedelta(days=1)
        data = self.cursor.execute("SELECT * FROM IRTEMP AS ir WHERE ir.time > ? ORDER BY ir.time ASC",
                                   (last_day,)).fetchall()

        hourly_data = []
        i = 0

        for hour in range(0,24):
            while(i < len(data)):
                data_el = datetime.strptime(data[i][1],TIME_FORMAT)
                if data_el.hour == ((hour + last_day.hour) % 24):
                    hourly_data.append(data[i])
                    i += 1
                    break
                elif data_el.hour > ((hour + last_day.hour) % 24):
                    break
                i += 1

        return hourly_data

    def get_daily_irtemp(self):
        pass

    def get_humid(self,entries=1):
        data = self.cursor.execute("SELECT * FROM HUMID AS h WHERE h.time > ? ORDER BY h.id DESC LIMIT ?",
                                   (datetime.today().replace(hour=0,minute=0,second=0,microsecond=0),str(entries))).fetchall()
        return data

    def get_baro(self,entries=1):
        data = self.cursor.execute("SELECT * FROM BARO AS b WHERE b.time > ? ORDER BY b.id DESC LIMIT ?",
                                   (datetime.today().replace(hour=0,minute=0,second=0,microsecond=0),str(entries))).fetchall()
        return data

    def get_opti(self,entries=1):
        data = self.cursor.execute("SELECT * FROM OPTI AS o WHERE o.time > ? ORDER BY o.id DESC LIMIT ?",
                                   (datetime.today().replace(hour=0,minute=0,second=0,microsecond=0),str(entries))).fetchall()
        return data


