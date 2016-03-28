from sensortag import SensorTag
import uuid_constants
import convert
import time
from dao import DAO
from json_builder import JSONBuilder

READING_DELAY = 55

def main():
    st = SensorTag("")

    if not st.connected:
        print("Could not connect to sensortag")
        return

    #Wait for initial data gathering to be done
    time.sleep(1)
   
    db = DAO("sensor_data.sqlite")
    jb = JSONBuilder(db)
    
    data = None
    while(True):
        db.open(True)
        data = st.read(uuid_constants.IRTEMP_DATA_UUID)
        obj_temp = convert.irtemp(data[0:len(data)//2])
        amb_temp = convert.irtemp(data[len(data)//2:]) 
        db.store_irtemp(data,obj_temp,amb_temp)
        print("--------------------IR Temperature Sensor------------------")
        print("IR Object Temp = " + str(round(obj_temp,2)) + 
              " C, IR Ambient Temp = " + str(round(amb_temp,2)) + " C")

        data = st.read(uuid_constants.HUMID_DATA_UUID)
        humid_temp = convert.humid_temp(data[0:len(data)//2])
        humidity = convert.humid(data[len(data)//2:])
        db.store_humid(data, humid_temp, humidity)
        print("-----------------------Humidity Sensor---------------------")
        print("Temperature = " + str(round(humid_temp,2)) +
              " C, Humidity = " + str(round(humidity,2)) + " %RH")

        
        data = st.read(uuid_constants.BARO_DATA_UUID)
        baro_temp = convert.baro(data[0:len(data)//2])
        baro_pres = convert.baro(data[len(data)//2:])
        db.store_baro(data, baro_temp,baro_pres)
        print("--------------------------Barometer------------------------")
        print("Temperature = " + str(round(baro_temp,2)) +
              " C, Barometric Pressure = " + str(round(baro_pres,2)) + " hPa/millibars")

        data = st.read(uuid_constants.OPTI_DATA_UUID)
        lux = convert.opti(data)
        db.store_opti(data,lux)
        print("-----------------------Optical Sensor----------------------")
        print("Light = " + str(round(lux,2)) + " Lux")

        db.close()      

        #db.open(False)
        #jb.buildFile()
        #db.close()

        time.sleep(READING_DELAY)
        
    db.close()
    
main()
