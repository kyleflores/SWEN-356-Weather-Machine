import sqlite3
from datetime import datetime, timedelta

TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
DB_NAME = '/home/pi/SWEN-356-Weather-Machine/python/sensor_data.sqlite'

class DAO:

    connection = None
    cursor = None
    saving = False
    file_name = ""

    def __init__(self, file_name):
        self.file_name = file_name

    def save(self):
        if self.saving:
            self.connection.commit()

    def open(self, saving):
        if not saving:
            self.connection = sqlite3.connect("file:" + self.file_name + "?mode=ro",uri=True)
        else:
            self.connection = sqlite3.connect(self.file_name)
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

    def get_recent(self,table_name, entries=1):
        data = self.cursor.execute("SELECT * FROM " + table_name.upper() + " AS t WHERE t.time > ? ORDER BY t.time DESC LIMIT ?",
                                   (datetime.today().replace(hour=0,minute=0,second=0,microsecond=0) - timedelta(days=1),
                                    str(entries))).fetchall()
        data.reverse()
        return data

    def get_hourly(self, table_name):
        last_day = datetime.today().replace(minute=0,second=0,microsecond=0) - timedelta(days=1)
        data = self.cursor.execute("SELECT * FROM " + table_name.upper() + " AS t WHERE t.time > ? ORDER BY t.time ASC",
                                   (last_day,)).fetchall()

        hourly_data = []
        i = 0

        for hour in range(0,24):
            while(i < len(data)):
                data_el = datetime.strptime(data[i][1],TIME_FORMAT)
                data_hour = (data_el.hour - last_day.hour + (0 if data_el.day == last_day.day else 24)) % 24
                if data_hour == hour:#((hour + last_day.hour) % 24):
                    hourly_data.append(data[i])
                    i += 1
                    break
                elif data_hour > hour:#((hour + last_day.hour) % 24):
                    break
                i += 1

        return hourly_data

    def get_daily(self, table_name):
        old_day = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
        date = []

        daily_data = []
        i = -1

        for day in range(0,7):
            data = self.cursor.execute("SELECT * FROM " + table_name.upper() + " AS t WHERE t.time > ?  AND t.time < ?ORDER BY t.time ASC",
                                   (old_day ,old_day + timedelta(hours=(5 if i == 0 else 24)))).fetchall()
            if len(data) > 0:
                daily_data.append(data[i])

            i=0
            old_day = datetime.today().replace(hour=11,minute=0,second=0,microsecond=0) - timedelta(days=day + 1)

        daily_data.reverse()
        return daily_data
