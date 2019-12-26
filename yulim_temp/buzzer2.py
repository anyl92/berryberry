from machine import Pin
from machine import PWM
import time

p = Pin(17, Pin.OUT)

pwm = PWM(p)
pwm.duty(0)

pwm.freq(440)
pwm.duty(50)
