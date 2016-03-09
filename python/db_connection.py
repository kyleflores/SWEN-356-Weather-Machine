import sqlite3

class db_connection:
  
  con = None
  cursor = None
  
  def __init__(self, file_name):
      pass

'''
def main():
  con = sqlite3.connect('sensor_data.sqlite')
  print("Opened database successfully")
  cur = con.cursor()
  cur.execute("SELECT time, temp, barometric  FROM BARO")
  for row in cur:
    print("time = ", row[0])
    print("temp = ", row[1])
    print("barometric = ", row[2], "\n")
  con.close()
main()
'''
