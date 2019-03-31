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

channel = 11                            # Channel to communicate with ESC
#freq = 400                              # Hertz
servo_min = int(0.36 * 4096)            # Min duty cycle
off_min = int((1-servo_min) * 4096)     # Min off time
servo_max = int(0.84 * 4096)            # Max duty cycle
off_max = int((1-servo_max) * 4096)     # Max off time
servo_mid = int(0.6 * 4096)             # Middle duty cycle
off_mid = int((1-servo_mid) * 4096)     # Middle off time

pwm = Adafruit_PCA9685.PCA9685()

#pwm.setPWMFreq(freq)

def PCA(channel, pulse_width):
    prescaleval = 25000000.0  # 25MHz
    prescaleval /= 4096.0  # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    prescale = int(math.floor(prescaleval + 0.5))# sets prescale value
    print(prescale)


def start_ESC(channel, servo_min, servo_mid, servo_max):
    if pwm is not 0 :
        pwm.set_pwm(channel, servo_min, off_min)
        time.sleep(1)
        pwm.set_pwm(channel, servo_mid, off_mid)
        time.sleep(1)
        pwm.set_pwm(channel, servo_min, off_min)
        time.sleep(1)

start_ESC(channel, servo_min, servo_mid, servo_max)