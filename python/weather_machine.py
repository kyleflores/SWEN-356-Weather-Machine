from sensortag import SensorTag
import uuid_constants
import convert
import time

READING_DELAY = 90

def main():
    st = SensorTag("")

    if not st.connected:
        print("Could not connect to sensortag")
        return

    #Wait for initial data gathering to be done
    time.sleep(1)
    
    data = None
    while(True):
        data = st.read(uuid_constants.IRTEMP_DATA_UUID)
        obj_temp = convert.irtemp(data[0:len(data)//2])
        amb_temp = convert.irtemp(data[len(data)//2:]) 
        print("IR Obj Temp = " + str(obj_temp) + 
              "C, IR Amb Temp = " + str(amb_temp) + "C")

        data = st.read(uuid_constants.HUMID_DATA_UUID)
        humid_temp = convert.humid_temp(data[0:len(data)//2])
        humidity = convert.humid(data[len(data)//2:])
        print("Humid Temp = " + str(humid_temp) +
              "C, Humidity = " + str(humidity) + "%RH")

        
        data = st.read(uuid_constants.BARO_DATA_UUID)
        baro_temp = convert.baro(data[0:len(data)//2])
        baro_pres = convert.baro(data[len(data)//2:])
        print("Baro Temp = " + str(baro_temp) +
              "C, Barometric Pressure = " + str(baro_pres) + "hPa")

        data = st.read(uuid_constants.OPTI_DATA_UUID)
        lux = convert.opti(data)
        print("Lux = " + str(lux) + "lux")

        #data = st.read(uuid_constants.MVMT_DATA_UUID)
        #process movement data        

        #time.sleep(READING_DELAY)
        time.sleep(3)

main()
