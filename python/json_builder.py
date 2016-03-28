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
        dicts = collections.OrderedDict()

        if (buildType == "current"):
            baro = self.db.get_recent("baro")
            dicts['time'] = str(baro[0][1])
            dicts['temp'] = str(baro[0][3])
            dicts['pressure'] = str(baro[0][4])
        else:
            baro = self.db.get_hourly("baro")
            for index in range(0, len(baro)):
                currTimeDict = collections.OrderedDict()
                currTimeDict['time'] = str(baro[index][1])
                currTimeDict['temp'] = str(baro[index][3])
                currTimeDict['pressure'] = str(baro[index][4])
                dicts[index] = currTimeDict
        self.data_wrapper["baro"] = dicts

    def buildHumid(self, buildType):
        dicts = collections.OrderedDict()
        if (buildType == "current"):
            humid = self.db.get_recent("humid")
            dicts['time'] = str(humid[0][1])
            dicts['temp'] = str(humid[0][3])
            dicts['humidity'] = str(humid[0][4])
        else:
            humid = self.db.get_hourly("irtemp")
            for index in range(0, len(humid)):
                currTimeDict = collections.OrderedDict()
                currTimeDict['time'] = str(humid[index][1])
                currTimeDict['temp'] = str(humid[index][3])
                currTimeDict['humidity'] = str(humid[index][4])
                dicts[index] = currTimeDict
        self.data_wrapper["humid"] = dicts

    def buildIRTemp(self, buildType):
        dicts = collections.OrderedDict()
        if (buildType == "current"):
            irtemp = self.db.get_recent("irtemp")
            dicts['time'] = str(irtemp[0][1])
            dicts['objtemp'] = str(irtemp[0][3])
            dicts['ambtemp'] = str(irtemp[0][4])
        else:
            opti = self.db.get_hourly("irtemp")
            for index in range(0, len(opti)):
                currTimeDict = collections.OrderedDict()
                currTimeDict['time'] = str(opti[index][1])
                currTimeDict['objtemp'] = str(opti[index][3])
                currTimeDict['ambtemp'] = str(opti[index][4])
                dicts[index] = currTimeDict
        self.data_wrapper["irtemp"] = dicts

    def buildOpti(self, buildType):
        dicts = collections.OrderedDict()
        if (buildType == "current"):
            opti = self.db.get_recent("opti")
            dicts['time'] = str(opti[0][1])
            dicts['light'] = str(opti[0][3])
        else:
            opti = self.db.get_hourly("opti")
            for index in range(0, len(opti)):
                currTimeDict = collections.OrderedDict()
                currTimeDict['time'] = str(opti[index][1])
                currTimeDict['light'] = str(opti[index][3])
                dicts[index] = currTimeDict
        self.data_wrapper["opti"] = dicts

    def buildFile(self, buildType):
        data_file = '../www/html/json/' + buildType + '.json'
        self.buildBaro(buildType)
        self.buildHumid(buildType)
        self.buildIRTemp(buildType)
        self.buildOpti(buildType)
        j = json.dumps(self.data_wrapper, indent=4, separators=(',', ': '))
        f = open(data_file, 'w')
        f.write(j)
