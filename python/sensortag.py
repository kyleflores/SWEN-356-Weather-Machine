import pexpect
import time

class SensorTag:

    connected = False
    gatt_term = None
    handles = {}

    def __init__(self, mac_address):
        self.gatt_term = pexpect.spawn("sh run_gatt.sh " + mac_address)
        self.gatt_term.expect("\[[^\]]*\]\[LE\]> ")
        connection_attempts = 0
        while connection_attempts < 5:
            print("Attempting Sensor Tag connection #" + str(connection_attempts + 1))
            self.gatt_term.sendline("connect")
            response = self.gatt_term.expect(["Error[.]*", "Connection Successful[.]*"])
            if response == 0:
                print("Could not connect to device at Sensor Tag at mac address: " + mac_address + "; make sure the device is on.")
                print("Trying to connect again in 5 seconds.")
                time.sleep(5)
            elif response == 1:
                print("Sucessfully connected to sensor tag at mac address: " + mac_address)
                connected = True
                #self.gatt_term.expect("\[*\]\[LE\]> ")
                break
            connection_attempts += 1
        for uuid in [IRTEMP_CONF_UUID, MVMT_CONF_UUID, HUMID_CONF_UUID, BARO_CONF_UUID, OPTI_CONF_UUID]:
            self.gatt_term.sendline("char-read-uuid" + uuid)
            self.gatt_term.expect("\[[^\]]*\]\[LE\]> ")
            self.gatt_term.before
            #configureing handles

    def read(self, uuid)
    
    def write(self, uuid)
