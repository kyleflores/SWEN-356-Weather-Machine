'''
    file: convert.py

    authors: Maxwell Hadley
             Thong Nguyen
             Matthew Waite
             Brian Nugent
             Kyle Flores
    
    This file contains all the functions necessary for converting
    from hex strings read from a TI SensorTag cc2650 to float values
'''

'''
    Converts from hex string to float for both object and
    ambient temperature data from the TMP007 sensor
'''
def irtemp(raw):
    val = reverse_bytes(raw)
    val = int(val, 16) >> 2
    val = float(val) * 0.03125
    return val

'''
    Converts from hex string to float for temperature data
    from the HDC1000 sensor
'''
def humid_temp(raw):
    temp = reverse_bytes(raw)
    temp = int(temp, 16)
    temp = ((float(temp) / 65536)*165.0) - 40.0
    return temp

'''
    Converts from hex string to float for humidity data
    from the HDC1000 sensor
'''
def humid(raw):
    hum = reverse_bytes(raw)
    hum = int(hum, 16)
    hum = (float(hum)/ 65536.0)*100.0
    return hum

'''
    Converts from hex string to float for both temperature and
    barometric pressure data from the BMP280 sensor
'''
def baro(raw):
    val = reverse_bytes(raw)
    val = int(val, 16)
    val = float(val) / 100.0
    return val

'''
    Converts from hex string to float for light data
    from the OPT3001 sensor
'''
def opti(raw):
    lux = reverse_bytes(raw)
    lux = int(lux, 16)
    base = lux & 0x0FFF
    exp = (lux & 0xF000) >> 12
    lux = base * (0.01 * (2.0**exp))
    return lux

'''
    Converts from hex string to float for any gyroscopic data
    from the MPU9250 sensor
'''
def mvmt_gyro(raw):
    gyro = reverse_bytes(raw)
    gyro = get_signed(int(gyro, 16))
    gyro = float(gyro) / (65536.0 / 500.0)
    return gyro

'''
    Converts from hex string to float for any accelerometer data
    from the MPU9250 sensor
'''
def mvmt_acc(raw, g_range):
    acc = reverse_bytes(raw)
    acc = get_signed(int(acc, 16))
    acc = float(acc) / (32768 / 2**g_range)
    return acc

'''
    Converts from hex string to float for any magnetometer data
    from the MPU9250 sensor
'''
def mvmt_mag(raw):
    mag = reverse_bytes(raw)
    mag = get_signed(int(mag, 16))
    mag = float(mag)
    return mag

'''
    Reverses a hex string by each byte which is 2 characters
'''
def reverse_bytes(byte_string):
    count = len(byte_string)
    new_byte_string = ""
    for i in range(0,count//2):
        new_byte_string += byte_string[count - (2*i) - 2:count - (2*i)]
    return new_byte_string

'''
    Converts a 16 bit signed integer to a 32 bit signed integer
'''
def get_signed(val):
    if (val & 0x8000) > 0:
        val = -(((~val) & 0x0000FFFF) + 1)
    return val
