import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
gpio_pin = 17
scale = [261, 294, 329, 349, 392, 440, 493, 523]
GPIO.setup(gpio_pin, GPIO.OUT)
plist = [4, 4, 5, 5, 4, 4, 2, 4, 4, 2, 2, 1]

def buzz(noteFreq, duration):
    halveWaveTime = 1 / (noteFreq * 2)
    waves = int(duration * noteFreq)
    for i in range(waves):
        GPIO.output(gpio_pin, True)
        time.sleep(halveWaveTime)
        GPIO.output(gpio_pin, False)
        time.sleep(halveWaveTime)
        
def play():
    t = 0
    notes = [261, 294, 329, 349, 392, 440, 493, 523]
    duration = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    for n in notes:
        buzz(n, duration[t])
        time.sleep(duration[t] *0.5)
        t += 1

play()

'''try:
    p = GPIO.PWM(gpio_pin, 100)
    p.start(100)
    p.ChangeDutyCycle(90)
    
    for i in plist:
        p.ChangeFrequency(scale[i])
        if i == 6:
            time.sleep(1)
        else:
            time.sleep(0.5)
    p.stop()
    
finally:
    GPIO.cleanup()
'''