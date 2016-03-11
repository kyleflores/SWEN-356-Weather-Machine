import json
import sqlite3
import collections

def main():
    con = sqlite3.connect('sensor_data.sqlite')
    cur = con.cursor()
    cur.execute("SELECT id, time, temp, barometric  FROM BARO")
    data_array = []
    for row in cur:
        dicts = collections.OrderedDict()
        print(str(row[0]))
        print(str(row[1]))
        print(str(row[2]))
        dicts['id'] = str(row[0])
        dicts['time'] = str(row[1])
        dicts['temp'] = str(row[2])
        dicts['barometric'] = str(row[3])
        data_array.append(dicts)
    con.close()
    j = json.dumps(data_array)
    data_file = '../www/html/json/current.json'
    f = open(data_file, 'w')
    print(f)
    print(j)
    
main()
