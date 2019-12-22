import smbus
import math
import time
import RPi.GPIO as GPIO
import picamera
import datetime
import RPi.GPIO as GPIO
import time
from subprocess import call
from datetime import datetime
import os
import serial
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# 우선적으로 신호가 올때 시동이 걸려야하고 시동이 걸렸을때
# 엑셀을 밟을 수 있고 동영상 녹화를 시작한다. 그러다 각도가 변하면 녹화 중지

# 우선은 함수를 먼저 선언!!

ready_to_drive = 0 # 이 값이 0이면 운전할 수 없다. 
servo_pin = 20
switch_pin = 16
btn_pin = 12
shutdown_sec = 2 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
flag = 0
older_x = 0
older_y = 0
savepath = '/home/pi/video' # 저장될 위치
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(btn_pin, GPIO.IN)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.IN)
time_limit = 0



servo = GPIO.PWM(servo_pin, 50)
servo.start(0)
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l 
    return value 
def read_word_2c(reg): 
    val = read_word(reg) 
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


press_time = None
def button_state_changed(pin):
    global press_time, flag, older_x, older_y, new_x, new_y, time_limit
    if GPIO.input(pin) == 0:    # btn down
        if press_time is None:
            press_time = datetime.now()
            ready_to_drive = 1
            print('time to drive!')
            print(ready_to_drive)
            with picamera.PiCamera() as camera:
                camera.resolution = (640,480)
                now = datetime.now() # datetime 하나만
                filename = now.strftime('%Y-%m-%d %H:%M:%S')
                camera.start_recording(output = savepath + '/' + filename+ '.h264')
                #카메라 저장 중
                try:
                    while True:
                        bus.write_byte_data(address, power_mgmt_1, 0)
                        gyroscope_xout = read_word_2c(0x43)
                        gyroscope_yout = read_word_2c(0x45)
                        gyroscope_zout = read_word_2c(0x47)
                        
                        acceleration_xout = read_word_2c(0x3b)
                        acceleration_yout = read_word_2c(0x3d)
                        acceleration_zout = read_word_2c(0x3f)
                        
                        acceleration_xout_scaled = acceleration_xout / 16384.0
                        acceleration_yout_scaled = acceleration_yout / 16384.0
                        acceleration_zout_scaled = acceleration_zout / 16384.0
                        new_x = get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
                        new_y = get_y_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
                    
                        if abs(older_x - new_x) > 40 or abs(older_y - new_y) > 40:
                            flag = 1
                        older_x = new_x
                        older_y = new_y
                        time.sleep(0.5)
                        time_limit += 1
                        swipt = GPIO.input(switch_pin)
                        
                        
                        if swipt == False:  # 스위치 눌렀을 때
                            servo.ChangeDutyCycle(12)
                            time.sleep(0.1)
                            servo.ChangeDutyCycle(3)
                            time.sleep(0.1)
                            #print('i wish')
                        if time_limit == 20:
                            break
                except KeyboardInterrupt:
                    camera.stop_recording()        
            if not flag:
                os.remove(savepath + '/' + filename+ '.h264')
                

            #버튼이 눌러졌을 때 실행된다.
    # else:                       # btn up
    #     if press_time is not None:
    #         elapsed = (datetime.now() - press_time).total_seconds()
    #         press_time = None 
    #         if elapsed >= shutdown_sec:
    #             call(["shutdown", "-h", "now"], shell=False)

# 변수들을 지정해주자


#GPIO 설정

port = '/dev/ttyACM0'
serialFromArduino = serial.Serial(port, 9600)

#GPIO.cleanup()

while True:
    #print(serialFromArduino.in_waiting)

    if (serialFromArduino.in_waiting > 0):
        input_s = serialFromArduino.readline()

        if input_s:
            print("Let's Start!")
            #GPIO.add_event_detect(btn_pin, GPIO.BOTH, callback=button_state_changed, bouncetime = 5000)
            GPIO.wait_for_edge(btn_pin, GPIO.BOTH)
            button_state_changed(btn_pin)
            
'''
new_flag = 0
while True:
    if (serialFromArduino.in_waiting >0):
        new_flag += 1
        if new_flag > 10:
            break
if new_flag > 5:
#    GPIO.wait_for_edge(btn_pin, GPIO.BOTH)
#    button_state_changed(btn_pin)
    #while True:
    GPIO.add_event_detect(btn_pin, GPIO.BOTH, callback=button_state_changed)
'''