import RPi.GPIO as GPIO      # gpio 라이브러리
from time import sleep       # sleep 라이브러리

LED = 23
Button = 18

GPIO.setmode(GPIO.BCM)      # GPIO 모드 셋팅

GPIO.setup(LED, GPIO.OUT)   # LED 출력으로 설정
GPIO.setup(Button, GPIO.IN) # 버튼 입력으로 설정

print('Start the GPIO App')  # 시작을 알리자!
print("Press the button (CTRL-C to exit)")
try:
        while True:
                if GPIO.input(Button)==0:
                        GPIO.output(LED, True)
                        print("Button was Pressed!")
                else:
			GPIO.output(LED, False)
                        print("Button was Not Pressed!")
                sleep(1)
except KeyboardInterrupt:      # CTRL-C를 누르면 발생
        GPIO.cleanup()
