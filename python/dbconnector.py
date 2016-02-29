import sqlite3
import jinja2
from jinja2 import Template

def main():
  con = sqlite3.connect('sensor_data.sqlite')
  print("Opened database successfully")
  cur = con.cursor()
  cur.execute("SELECT time, temp, barometric  FROM BARO")
  #ti = Template("{{ time }}")
  #tmp = Template("{{ temp }}")
  #pr = Template("{{ pressure }}")
  

  for row in cur:
    print("time = ", row[0])
    #ti.render(row[0])
    time = row[0]
    print("temp = ", row[1])
    #tmp.render(row[1])
    temp = row[1]
    print("barometric = ", row[2], "\n")
    #pr.render(row[2])
    pressure = row[2]
  con.close()

  return render_template('../www/html/status.html', time, temp, pressure)
main()
