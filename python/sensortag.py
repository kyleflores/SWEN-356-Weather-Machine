import pexpect
import time

class SensorTag:

    def __init__(self, mac_address):
        self.gatt_term = pexpect.spawn("sh run_gatt.sh " + mac_address)
        self.gatt_term.expect("\[*\]\[LE\]> ")
        connection_attempts = 0
        while connection_attempts < 12:
            print("Attempting Sensor Tag connection #" + str(connection_attempts + 1))
            self.gatt_term.sendline("connect")
            response = self.gatt_term.expect( \
            ["Error: connect error: Transport endpoint is not connected*","Connection Successful","*Error*"])
            if response == 1:
                print("Could not connect to device at Sensor Tag at mac address: " + mac_address + "; make sure the device is on.")
                print("Trying to connect again in 5 seconds.")
                time.sleep(5)
            elif response == 2:
                print("Sucessfully connected to sensor tag at mac address: " + mac_address)
                #self.gatt_term.expect("\[*\]\[LE\]> ")
                break
            elif response == 3:
                pass
            connection_attempts += 1
        return response - 2
            
