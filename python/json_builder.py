import json
import sqlite3
import collections
from dao import DAO

class JSONBuilder:

    # Set up wrapper
    data_wrapper = collections.OrderedDict()
    db = None


    #db = DAO("sensor_data.sqlite", False)
    def __init__(self, db):
        self.db = db
        
    #def buildBaro(self):
        baro = self.db.get_baro()
        dicts = collections.OrderedDict()
        dicts['id'] = str(baro[0])
        dicts['time'] = str(baro[1])
        dicts['temp'] = str(baro[2])
        dicts['pressure'] = str(baro[3])
        data_wrapper["baro"] = dicts
    #def buildHumid(self):
    def buildIRTemp(self):
        irtemp = self.db.get_irtemp()
        dicts = collections.OrderedDict()
        dicts['id'] = str(irtemp[0][0])
        dicts['time'] = str(irtemp[0][1])
        dicts['objtemp'] = str(irtemp[0][3])
        dicts['ambtemp'] = str(irtemp[0][4])
        self.data_wrapper["irtemp"] = dicts
    #def buildOpti(self):
    def buildFile(self):
        #data_wrapper["baro"] = self.db.get_baro()
        #data_wrapper["humid"] = self.db.get_humid()

        #data_wrapper["opti"] = self.db.get_opti()
        self.buildIRTemp()
        j = json.dumps(self.data_wrapper, indent=4, separators=(',', ': '))
        data_file = '../www/html/json/current.json'
        f = open(data_file, 'w')
        f.write(j)
        print(j)

    '''
    # Get barometer data
    cur.execute("SELECT id, time, temp, pressure FROM BARO")
    for row in cur:
        dicts = collections.OrderedDict()
        dicts['id'] = str(row[0])
        dicts['time'] = str(row[1])
        dicts['temp'] = str(row[2])
        dicts['pressure'] = str(row[3])
        data_wrapper["baro"] = dicts

    # Get humidity data
    cur.execute("SELECT id, time, temp, humidity FROM HUMID")
    for row in cur:
        dicts = collections.OrderedDict()
        dicts['id'] = str(row[0])
        dicts['time'] = str(row[1])
        dicts['temp'] = str(row[2])
        dicts['humidity'] = str(row[3])
        data_wrapper["humid"] = dicts

    # Get IR temp data
    cur.execute("SELECT id, time, objTemp, ambTemp FROM IRTEMP")
    for row in cur:
        dicts = collections.OrderedDict()
        dicts['id'] = str(row[0])
        dicts['time'] = str(row[1])
        dicts['objtemp'] = str(row[2])
        dicts['ambtemp'] = str(row[3])
        data_wrapper["irtemp"] = dicts

    # Get optic data
    cur.execute("SELECT id, time, light FROM OPTI")
    for row in cur:
        dicts = collections.OrderedDict()
        dicts['id'] = str(row[0])
        dicts['time'] = str(row[1])
        dicts['light'] = str(row[2])
        data_wrapper["opti"] = dicts

    j = json.dumps(data_wrapper, indent=4, separators=(',', ': '))
    data_file = '../www/html/json/current.json'
    f = open(data_file, 'w')
    f.write(j)

    print(j)
    con.close()
'''

#for debugging
jsonB = JSONBuilder(DAO("sensor_data.sqlite",False))
jsonB.buildFile()
