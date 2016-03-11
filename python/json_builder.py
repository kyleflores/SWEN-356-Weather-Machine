import json
import sqlite3
import collections

def main():
    con = sqlite3.connect('sensor_data.sqlite')
    cur = con.cursor()

    # Set up wrapper
    data_wrapper = collections.OrderedDict()

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

    j = json.dumps(data_wrapper, indent=2, separators=(',', ': '))
    data_file = '../www/html/json/current.json'
    f = open(data_file, 'w')
    f.write(j)

    print(j)
    con.close()
    
main()
