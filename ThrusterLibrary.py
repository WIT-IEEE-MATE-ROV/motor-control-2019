import time
import Adafruit_PCA9685
import math

# Max Forwards = 1
# Stop = 0.5
# Max Backwards = 0

frequency = 400                              # Hertz

pwm = Adafruit_PCA9685.PCA9685()
pwm.setPWMFreq(frequency)

def calc_duty_cycle(val):                    # Input decimal percentage of duty cycle
   duty_cycle = int(val * .48)
   duty_cycle = int(.36 + duty_cycle)
   duty_cycle = int(duty_cycle * 4096)
   return duty_cycle


def calc_off_time(val):
   off_time = int(val * .48)
   off_time = int(.36 + off_time)
   off_time = int((1 - abs(off_time)) * 4096)
   return off_time


def start_ALL_ESC():
   if pwm is not 0:
       servo_min = calc_duty_cycle(0.36)
       off_min = calc_off_time(0.36)
       servo_mid = calc_duty_cycle(0.6)
       off_mid = calc_off_time(0.6)
       pwm.set_all_pwm(servo_min, off_min)
       time.sleep(1)
       pwm.set_all_pwm(servo_mid, off_mid)
       time.sleep(1)
       pwm.set_all_pwm(servo_min, off_min)
       time.sleep(1)


def move(channel, val):
   duty_cycle = calc_duty_cycle(val)
   off_time = calc_off_time(val)
   pwm.set_pwm(channel, duty_cycle, off_time)