import math

# Constant for Temp Sensor
SCALE_LSB = 0.03125

# Constants (acceleration range) for Movement Sensor
ACC_RANGE_2G = 0
ACC_RANGE_4G = 1
ACC_RANGE_8G = 2
ACC_RANGE_16G = 3

# PASTED FROM USER GUIDE
"""
void sensorTmp007Convert(uint16_t rawAmbTemp, uint16_t rawObjTemp, float *tAmb, float *tObj)
{
  const float SCALE_LSB = 0.03125;
  float t;
  int it;

  it = (int)((rawObjTemp) >> 2);
  t = ((float)(it)) * SCALE_LSB;
  *tObj = t;

  it = (int)((rawAmbTemp) >> 2);
  t = (float)it;
  *tTgt = t * SCALE_LSB;
}
"""
def temp(raw):
    # if obj temp
    # if amb temp
    it = int(raw >> 2)
    temp = float(it) * SCALE_LSB
    return temp

# Seems in the user guide, acc_range is defined somewhere in this file,
# not necessarily a parameter
def mvmt(raw, acc_range):
    val = None
    if acc_range == ACC_RANGE_2G:
        val = float(raw) / (32768/2)
    elif acc_range == ACC_RANGE_4G:
        val = float(raw) / (32768/4)
    elif acc_range == ACC_RANGE_8G:
        val = float(raw) / (32768/8)
    elif acc_range == ACC_RANGE_16G:
        val = float(raw) / (32768/16)
    return val

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
