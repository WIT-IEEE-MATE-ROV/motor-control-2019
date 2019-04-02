import time
import Adafruit_PCA9685
import math

#frequency = 400                              # Hertz

pwm = Adafruit_PCA9685.PCA9685()
#pwm.setPWMFreq(frequency)

r_min = 0
r_max = 1
t_min = 0.36
t_max = 0.84

def calc_duty_cycle(val):
   val = ((val - r_min) / (r_max-r_min)) * (t_max - t_min) + t_min
   duty_cycle = int(val * 4096)
   return duty_cycle

def calc_off_time(val):
   val = 1 - val
   val = ((val - r_min) / (r_max-r_min)) * (t_max - t_min) + t_min
   off_time = int(val * 4096)
   return off_time

def start_ALL_ESC():
   if pwm is not 0:
      arm_min = calc_duty_cycle(0)
      off_min = calc_off_time(0)
      arm_mid = calc_duty_cycle(0.5)
      off_mid = calc_off_time(0.5)

      for channel in range (0,15):
         pwm.set_pwm(channel, arm_min, off_min)
         time.sleep(0.1)
      for channel in range (0,15):
         pwm.set_pwm(channel, arm_mid, off_mid)
         time.sleep(0.1)
      for channel in range (0,15):
         pwm.set_pwm(channel, arm_min, off_min)
         time.sleep(0.1)

def move(channel, val):
   duty_cycle = calc_duty_cycle(val)
   off_time = calc_off_time(val)
   pwm.set_pwm(channel, duty_cycle, off_time)