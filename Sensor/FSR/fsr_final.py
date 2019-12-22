import spidev
import time
import RPi.GPIO as GPIO

LedPin = 12
Led_status = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(LedPin, GPIO.OUT)
GPIO.output(12, GPIO.LOW)

#Define Variables
delay = 0.5
pad_channel = 0

#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1000000

def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

try:
    while True:
        pad_value = readadc(pad_channel)
        voltage = pad_value * 3.3 / 1024
        if pad_value >= 200:
            GPIO.output(LedPin, Led_status)
        else:
            GPIO.output(LedPin, False)
        print("---------------------------------------")
        print("Pressure Pad Value: %d" % pad_value)
        print("Voltage: %d" % voltage)
        time.sleep(delay)

except KeyboardInterrupt:
    pass
