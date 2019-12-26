import RPi.GPIO as GPIO
import time

servo_pin = 20
switch_pin = 16

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.IN)

servo = GPIO.PWM(servo_pin, 50)
servo.start(0)

try:
    while True:
        swipt = GPIO.input(switch_pin)

        if swipt == False:  # 스위치 눌렀을 때
            servo.ChangeDutyCycle(12)
            time.sleep(0.1)
            servo.ChangeDutyCycle(3)
            time.sleep(0.1)
            print('i wish')
        
except KeyboardInterrupt:
    servo.stop()

GPIO.cleanup()