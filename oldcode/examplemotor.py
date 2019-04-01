# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
esc_low = 900
esc_mid = 1500
esc_hi  = 2100

# Helper function to make setting a servo pulse width simpler.
def set_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

pwm.set_pwm_freq(400)


def init():
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, esc_low)
    time.sleep(1)
    pwm.set_pwm(0, 0, esc_mid)
    time.sleep(1)
    pwm.set_pwm(0, 0, esc_low)
    time.sleep(1)

def set_pwm_from_decimal(channel, perc):
    val = perc * 4096  # 4096 is the resolution, so convert to that form of units
    pwm.set_pwm()

init()
pwm.set_pwm(0, )
time.sleep(1)