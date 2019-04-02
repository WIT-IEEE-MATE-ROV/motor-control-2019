import time
import Adafruit_PCA9685

# Max Forwards = 1
# Stop = 0.5
# Max Backwards = 0

frequency = 400                              # Hertz

pwm = Adafruit_PCA9685.PCA9685()
#pwm.setPWMFreq(frequency)


def calc_duty_cycle(val):                    # Input decimal percentage of duty cycle
    duty_cycle = float(val * .48)
    duty_cycle = float(.36 + duty_cycle)
    duty_cycle = float(duty_cycle * 4096)
    return duty_cycle


def arm_duty(val):
    arm_duty_cycle = int(val * 4096)
    return arm_duty_cycle


def arm_off(val):
    arm_off_time = int((1-abs(val))*4096)
    return arm_off_time


def calc_off_time(val):
    off_time = float(val * .48)
    off_time = float(.36 + off_time)
    off_time = float((1 - abs(off_time)) * 4096)
    return off_time


def start_ALL_ESC():
    if pwm is not 0:
        servo_min = arm_duty(.36)
        off_min = arm_off(.36)
        servo_mid = arm_duty(0.6)
        off_mid = arm_off(0.6)

        for channel in range (0,15):
            pwm.set_pwm(channel, servo_min, off_min)
            time.sleep(1)

            pwm.set_pwm(channel, servo_mid, off_mid)
            time.sleep(1)

            pwm.set_pwm(channel, servo_min, off_min)
            time.sleep(1)

            pwm.set_pwm(channel, servo_mid, off_mid)

                

def move(channel, val):
    duty_cycle = int(calc_duty_cycle(val))
    off_time = int(calc_off_time(val))
    pwm.set_pwm(channel, duty_cycle, off_time)


