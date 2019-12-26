import RPi.GPIO as GPIO
import time

LED = 23
Button = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(Button, GPIO.IN)

print('start')
try:
	while True:
		if GPIO.input(Button) == 0:
			GPIO.output(LED, True)
			print('press ')
		else:
			GPIO.output(LED,False)
			print('not press')

		time.sleep(2)
except KeyboardInterrupt:
	GPIO.cleanup()
