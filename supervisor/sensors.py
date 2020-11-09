import sys
import datetime
fakeHardware = False

try:
    import smbus2
    import bme280
except:
    import random
    smbbus2 = None
    bme280 = None
    fakeHardware = True
    print("[Warn] unable to load hardware libraries for BME280, and starting in simulation mode", file = sys.stderr)


# samples the bme280 and returns a value (fake a value if we're not on a real pi)
def sample():
    if (fakeHardware):
        return sampleSimulate()
    else:
        return sampleSensors()

def sampleSimulate():
    global lastHumidity
    global lastTemperature
    global lastPressure
    lastHumidity += random.random() - .5
    lastTemperature += random.random() - .5
    lastPressure += random.random() - .5
    return {'temperature': lastHumidity, 
        'humidity': lastTemperature, 
        'pressure': lastPressure, 
        'id': "00000000-0000-0000-000000000000", 
        'timestamp': datetime.datetime.utcnow()}

def sampleSensors():
    return bme280.sample(bus, address, calibration_params)

def isSimulation():
    return fakeHardware

lastHumidity = 40.0
lastTemperature = 20.0
lastPressure = 980.0

if not fakeHardware:
    # BM280 init
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)
