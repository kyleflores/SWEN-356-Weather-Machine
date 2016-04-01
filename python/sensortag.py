import pexpect
import time
import re
import uuid_constants

class SensorTag:

    connected = False
    gatt_term = None
    mac_address = ""
    handles = {}

    def __init__(self, mac_address):
        self.mac_address = mac_address.upper()
        self.gatt_term = pexpect.spawn("sh run_gatt.sh " + self.mac_address)
        self.gatt_term.expect('\[' + self.mac_address + '\]\[LE\]>', timeout=10)
        self.gatt_term.sendline('connect')
        try:
            self.gatt_term.expect('Connection successful.*\[LE\]>',timeout=30)
        except pexpect.exceptions.TIMEOUT:
            print("Couldn't connect to SensorTag: Make sure the mac address is correct and the Sensortag is searching")
            return
        self.connected = True
        for k,v in uuid_constants.SENSOR_ON.items():
            if not self.write(k,v):
                print("Failed to turn on device with uuid = " + str(k))
            else:
                print("Successfully turned on device with uuid = " + str(k))

    def read(self, read_from):
        self.gatt_term.sendline("char-read-uuid " + read_from)
        self.gatt_term.expect("value: [0-9a-fA-F ]*")
        value = re.findall("value:([0-9a-fA-F ]*)",self.gatt_term.after.decode("utf-8"))[0]
        value = value.replace(' ', '')        
        return value
    
    def write(self, write_to, to_write):
        if not (write_to in self.handles):
            self.get_handle(write_to)
        self.gatt_term.sendline("char-write-cmd " + self.handles[write_to] + " " + to_write)
        time.sleep(.1)
        written = self.read(write_to)
        return (written == to_write)

    def get_handle(self, uuid):
        self.gatt_term.sendline("char-read-uuid " + uuid)
        self.gatt_term.expect("handle: .* ")
        self.handles[uuid] = re.findall("0x[0-9a-fA-F]*",self.gatt_term.after.decode("utf-8"))[0]
