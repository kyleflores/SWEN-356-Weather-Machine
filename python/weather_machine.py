from sensortag import SensorTag
import uuid_constants
import convert

def main():
    st = SensorTag("")
    st.write(uuid_constants.OPTI_CONF_UUID,"01")
    lux = st.read(uuid_constants.OPTI_DATA_UUID)
    lux = convert.opti(lux)
    print("lux: " + str(lux))

main()
