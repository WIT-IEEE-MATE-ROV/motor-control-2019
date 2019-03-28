# to do list
# Establish ESC communitcation
# Get PCA values
#
#
from __future__ import division
import time
import Adafruit_PCA9685
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
# other shit
freq_hz = 50
goalval = 1
channel = 4
servo_max = 150
servo_min = 600

pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)


def PCA(goalval,channel):
    prescaleval = 25000000.0  # 25MHz
    prescaleval /= 4096.0  # 12-bit
    prescaleval /= float(freq_hz)
    prescaleval -= 1.0
    prescale = int(math.floor(prescaleval + 0.5))# sets prescale value
    print(prescale)
    if (goalval > 0) : # goes "forward"
        pulse = (goalval * prescale )
        pwm.set_pwm(0, 0, servo_min)
        time.sleep(1)
        pwm.set_pwm(0, 0, servo_max)
        time.sleep(1)
        pwm.set_pwm(channel, 0, pulse)
    else:  # goes "backward"
        pulse = (goalval * prescale)
        pwm.set_pwm(0, 0, servo_min)
        time.sleep(1)
        pwm.set_pwm(0, 0, servo_max)
        time.sleep(1)
        pwm.set_pwm(channel, 0, pulse)



#def ESC(pwm):
 #   while (pwm != 0) :# place holder
  #      pwm.set_pwm(0, 0, servo_min)
   #     time.sleep(1)
    #    pwm.set_pwm(0, 0, servo_max)
     #   time.sleep(1)
      #  pwm.set_pwm(channel, 0, pwm)