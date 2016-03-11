import json
import sqlite3
import collections

def main():
    con = sqlite3.connect('sensor_data.sqlite')
    cur = con.cursor()
    cur.execute("SELECT id, time, temp, pressure FROM BARO")

    data_array = []
    for row in cur:
        dicts = collections.OrderedDict()
        dicts['id'] = str(row[0])
        dicts['time'] = str(row[1])
        dicts['temp'] = str(row[2])
        dicts['pressure'] = str(row[3])
        data_array.append(dicts)
    con.close()
    j = json.dumps(data_array, indent=4, separators=(',', ': '))
    data_file = '../www/html/json/current.json'
    f = open(data_file, 'w')
    f.write(j)

    # print(f)
    print(j)
    
main()
