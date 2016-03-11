import json
import sqlite3
import collections
from dao import DAO

class JSONBuilder:
    # Set up wrapper
    data_wrapper = collections.OrderedDict()
    db = None

    def __init__(self, db):
        self.db = db
        
    def buildBaro(self):
        baro = self.db.get_baro()
        dicts = collections.OrderedDict()
        dicts['id'] = str(baro[0][0])
        dicts['time'] = str(baro[0][1])
        dicts['temp'] = str(baro[0][3])
        dicts['pressure'] = str(baro[0][4])
        self.data_wrapper["baro"] = dicts

    def buildHumid(self):
        humid = self.db.get_humid()
        dicts = collections.OrderedDict()
        dicts['id'] = str(humid[0][0])
        dicts['time'] = str(humid[0][1])
        dicts['temp'] = str(humid[0][3])
        dicts['humidity'] = str(humid[0][4])
        self.data_wrapper["humid"] = dicts

    def buildIRTemp(self):
        irtemp = self.db.get_irtemp()
        dicts = collections.OrderedDict()
        dicts['id'] = str(irtemp[0][0])
        dicts['time'] = str(irtemp[0][1])
        dicts['objtemp'] = str(irtemp[0][3])
        dicts['ambtemp'] = str(irtemp[0][4])
        self.data_wrapper["irtemp"] = dicts

    def buildOpti(self):
        opti = self.db.get_opti()
        dicts = collections.OrderedDict()
        dicts['id'] = str(opti[0][0])
        dicts['time'] = str(opti[0][1])
        dicts['light'] = str(opti[0][3])
        self.data_wrapper["opti"] = dicts

    def buildFile(self):
        self.buildBaro()
        self.buildHumid()
        self.buildIRTemp()
        self.buildOpti()
        j = json.dumps(self.data_wrapper, indent=4, separators=(',', ': '))
        data_file = '../www/html/json/current.json'
        f = open(data_file, 'w')
        f.write(j)
        print(j)


#for debugging
jsonB = JSONBuilder(DAO("sensor_data.sqlite",False))
jsonB.buildFile()
