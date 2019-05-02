import time
import Adafruit_PCA9685 as Ada
import math

frequency = 400                              # Hertz

pwm = Ada.PCA9685()
pwm.frequency = frequency

r_min = 0
r_max = 1
t_min = 0.69
t_max = 0.83
t_mid = (t_max + t_min)/2


def calc_duty_cycle_noscale(val): #FIX
#   print("On time  is ", val)
   duty_cycle = int(val * 4096)
   return duty_cycle


def calc_off_time_noscale(val): #FIX
   val = 1 - val
#   print("Off time is " , val)   
   off_time = int(val * 4096)
   return off_time


def calc_duty_cycle(val): #FIX
   val = ((val - r_min) / (r_max-r_min)) * (t_max - t_min) + t_min
#   print("On time  is ", val)
   duty_cycle = int(val * 4096)
   return duty_cycle


def calc_off_time(val): #FIX
   val = ((val - r_min) / (r_max-r_min)) * (t_max - t_min) + t_min
   val = 1.2 - val
#   print("Off time is " , val)   
   off_time = int(val * 4096)
   return off_time


def start_ALL_ESC():
#   print t_mid
   move(0, .85) # The dumper is on channel 0, so we don't want to initialize this
   for channel in range (1,14):
      move(channel,1)
      time.sleep(.1)
   for channel in range (1,14):
      move(channel,0)
      time.sleep(.1)
   for channel in range (1,14):
      move(channel,.5)
      time.sleep(.1)

def start_ALL_TEST():
   for channel in range (0,15):
      move(channel,1)
      time.sleep(.1)
      move(channel,0)
      time.sleep(.1)
      move(channel, .5)
      time.sleep(1)

def move(channel, val):
   duty_cycle = calc_duty_cycle(val)
   off_time = calc_off_time(val)
   pwm.set_pwm(channel, off_time, duty_cycle )

def send(channel, val):
    pwm.set_pwm(channel, 0, int(val*4096))

def Stop_All():
   for channel in range (0,15):
      move(channel, .5)
      time.sleep(.1)
