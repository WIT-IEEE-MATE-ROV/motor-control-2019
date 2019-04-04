import time
import Adafruit_PCA9685
import math

frequency = 400                              # Hertz

pwm = Adafruit_PCA9685.PCA9685()
pwm.frequency = frequency

r_min = 0
r_max = 1
t_min = 0.6755
t_max = 0.8255

def arm_duty(val):
   duty = int(val * 4096)
   return duty

def arm_off(val):
   val = 1 - abs(val)
   off = int(val * 4096)
   return off

def calc_duty_cycle(val):
   val = ((val - r_min) / (r_max-r_min)) * (t_max - t_min) + t_min
   print("Your on time  is ", val)
   duty_cycle = int(val * 4096)
   return duty_cycle

def calc_off_time(val):
   val = ((val - r_min) / (r_max-r_min)) * (t_max - t_min) + t_min
   val = 1.2 - val
   print("Your off time is " , val)   
   off_time = int(val * 4096)
   return off_time

def start_ALL_ESC():
   arm_max = arm_duty(0.84)
   off_max = arm_off(0.84)
   arm_min = arm_duty(0.36)
   off_min = arm_off(0.36)
   arm_mid = arm_duty(0.6)
   off_mid = arm_off(0.6)
   """ 
   arm_min = calc_duty_cycle(0)
   off_min = calc_off_time(0)
   arm_mid = calc_duty_cycle(0.5)
   off_mid = calc_off_time(0.5)
   """
   for channel in range (0,15):
      pwm.set_pwm(channel, arm_max, off_max)
      time.sleep(0.1)
   for channel in range (0,15):
      pwm.set_pwm(channel, arm_min, off_min)
      time.sleep(0.1)
   for channel in range (0,15):
      pwm.set_pwm(channel, arm_mid, off_mid)
      time.sleep(0.1)

def move(channel, val):
   duty_cycle = calc_duty_cycle(val)
   off_time = calc_off_time(val)
   pwm.set_pwm(channel, off_time, duty_cycle )
