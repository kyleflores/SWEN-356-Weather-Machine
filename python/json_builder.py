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
        
    def buildBaro(self, buildType):
        baro = self.db.get_recent("baro")
        dicts = collections.OrderedDict()
        dicts['id'] = str(baro[0][0])
        dicts['time'] = str(baro[0][1])
        dicts['temp'] = str(baro[0][3])
        dicts['pressure'] = str(baro[0][4])
        self.data_wrapper["baro"] = dicts

    def buildHumid(self, buildType):
        humid = self.db.get_recent("humid")
        dicts = collections.OrderedDict()
        dicts['id'] = str(humid[0][0])
        dicts['time'] = str(humid[0][1])
        dicts['temp'] = str(humid[0][3])
        dicts['humidity'] = str(humid[0][4])
        self.data_wrapper["humid"] = dicts

    def buildIRTemp(self, buildType):
        irtemp = self.db.get_recent("irtemp")
        dicts = collections.OrderedDict()
        dicts['id'] = str(irtemp[0][0])
        dicts['time'] = str(irtemp[0][1])
        dicts['objtemp'] = str(irtemp[0][3])
        dicts['ambtemp'] = str(irtemp[0][4])
        self.data_wrapper["irtemp"] = dicts

    def buildOpti(self, buildType):
        dicts = collections.OrderedDict()
        if(buildType == "current"):
            opti = self.db.get_recent("opti")
            dicts['id'] = str(opti[0][0])
            dicts['time'] = str(opti[0][1])
            dicts['light'] = str(opti[0][3])
        else:
            opti = self.db.get_hourly("opti")
            print(opti)
            for index in range(0, len(opti)):
                dicts['id'] = str(opti[index][0])
                dicts['time'] = str(opti[index][1])
                dicts['light'] = str(opti[index][3])
        self.data_wrapper["opti"] = dicts

    def buildFile(self, buildType):
        data_file = '../www/html/json/' + buildType + '.json'
        #self.buildBaro(buildType)
        #self.buildHumid(buildType)
        #self.buildIRTemp(buildType)
        self.db.open(False)
        self.buildOpti(buildType)
        j = json.dumps(self.data_wrapper, indent=4, separators=(',', ': '))
        f = open(data_file, 'w')
        f.write(j)
        print(j)
        self.db.close()
            

#for debugging
jsonB = JSONBuilder(DAO("sensor_data.sqlite"))
jsonB.buildFile("history")
