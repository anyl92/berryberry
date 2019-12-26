import RPi.GPIO as GPIO
from time import sleep
from subprocess import call
from datetime import datetime

btn_pin = 12
shutdown_sec = 2 

GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)

press_time = None

def button_state_changed(pin):
    global press_time
    if GPIO.input(pin) == 0:    # btn down
        if press_time is None:
            press_time = datetime.now()
            while True:
                print("ya")
                if GPIO.input(pin) == 1:
                    print("end")
                    break
    else:                       # btn up
        if press_time is not None:
            elapsed = (datetime.now() - press_time).total_seconds()
            press_time = None 
            if elapsed >= shutdown_sec:
                call(["shutdown", "-h", "now"], shell=False)
        
# subscribe to button presses
GPIO.add_event_detect(btn_pin, GPIO.BOTH, callback=button_state_changed)

while True:
    sleep(5)
