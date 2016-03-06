import pexpect
import time
import re
import uuid_constants

class SensorTag:

    connected = False
    gatt_term = None
    handles = {}

    def __init__(self, mac_address):
        self.gatt_term = pexpect.spawn("sh run_gatt.sh " + mac_address)
        self.gatt_term.expect('\[[:0-9a-fA-F]*\]\[LE\]>', timeout=10)
        self.gatt_term.sendline('connect')
        try:
            self.gatt_term.expect('Connection successful.*\[LE\]>',timeout=30)
        except pexpect.exceptions.TIMEOUT:
            print("Couldn't connect to SensorTag: Make sure the mac address is correct and the Sensortag is searching")
            return
        connected = True
        for uuid in [uuid_constants.IRTEMP_CONF_UUID, uuid_constants.MVMT_CONF_UUID, uuid_constants.HUMID_CONF_UUID,
uuid_constants.BARO_CONF_UUID, uuid_constants.OPTI_CONF_UUID]:
            time.sleep(1)
            self.gatt_term.sendline("char-read-uuid " + uuid)
            time.sleep(1)
            self.gatt_term.expect('\r\n.*\[LE\]>')
            #print(re.findall("0x[0-9a-fA-F]*",self.gatt_term.after.decode("utf-8"))[0])
            self.handles[uuid] = re.findall("0x[0-9a-fA-F]*",self.gatt_term.after.decode("utf-8"))[0]
        #print("Handles found:\n" + str(self.handles))

    def read(self, uuid):
        pass
    
    def write(self, uuid):
        pass
