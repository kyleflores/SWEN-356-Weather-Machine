import math

def humid_temp(raw):
    temp = raw[2:] + raw[0:2]
    temp = int(temp, 16)
    temp = ((float(temp) / 65536)*165.0) - 40.0
    return temp

def humid(raw):
    hum = raw[2:] + raw[0:2]
    hum = int(hum, 16)
    hum = (float(hum)/ 65536.0)*100.0
    return hum

def baro(raw):
    val = raw
    val = val[4:] + val[2:4] + val[0:2]
    val = int(val, 16)
    val = float(val) / 100.0
    return val

def opti(raw):
    val = raw
    val = val[2:] + val[0:2]
    val = int(val, 16)
    base = val & 0x0FFF
    exp = (val & 0xF000) >> 12
    val = base * (0.01 * (2.0**exp))
    return val
