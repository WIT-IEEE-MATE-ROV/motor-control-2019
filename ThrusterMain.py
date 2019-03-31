from __future__ import division
import time
import Adafruit_PCA9685
import math 

# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
SLEEP              = 0x10
INVRT              = 0x10
OUTDRV             = 0x04
RESTART            = 0x80
ALLCALL            = 0x01

channel = 0                             # Channel to communicate with ESC
freq = 400                              # Hertz
wave_period = ((1/frequency) * 10^6)    # Period of one wave length in microseconds
servo_min = 0.36                        # Min duty cycle
servo_max = 0.84                        # Max duty cycle
servo_mid = 0.6                         # Middle duty cycle

pwm = Adafruit_PCA9685.PCA9685()

pwm.setPWMFreq(freq)

def PCA(channel, pulse_width):
    prescaleval = 25000000.0  # 25MHz
    prescaleval /= 4096.0  # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    prescale = int(math.floor(prescaleval + 0.5))# sets prescale value
    print(prescale)


def start_ESC(channel, servo_min, servo_mid, servo_max, wave_period):
    if pwm is not 0 :
        pwm.set_pwm(channel, servo_min, int(wave_period - servo_min))
        time.sleep(1)
        pwm.set_pwm(channel, servo_mid, int(wave_period - servo_mid))
        time.sleep(1)
        pwm.set_pwm(channel, servo_min, int(wave_period - servo_min))
        time.sleep(1)   # Guess and check amount of time needed before sending values

start_ESC(channel, servo_min, servo_mid, servo_max, wave_period)