import smbus
import math
import time
import RPi.GPIO as GPIO
import picamera
import datetime
import os
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
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
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
flag = 0
older_x = 0
older_y = 0
stop_sign = 0
savepath = '/home/pi/video'

with picamera.PiCamera() as camera:
    camera.resolution = (640,480)
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d %H:%M:%S')
    camera.start_recording(output = savepath + '/' + filename+ '.h264')
    while True:
        print(1)
        # Aktivieren, um das Modul ansprechen zu koennen
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
        print("X Rotation: " , get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled))
        print("Y Rotation: " , get_y_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled))
        if abs(older_x - new_x) > 60 or abs(older_y - new_y) > 60:
            flag = 1
        older_x = new_x
        older_y = new_y
        print(flag)
        time.sleep(1)
        stop_sign += 1
        if stop_sign == 15:
            break
        
        
    camera.stop_recording()
if not flag:
    os.remove(savepath + '/' + filename+ '.h264')
