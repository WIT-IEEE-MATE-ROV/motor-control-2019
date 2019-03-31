import ThrusterLibrary.py
import Adafruit_PCA9685
import time

start_ALL_ESC()

duty_cycle = calc_duty_cycle(0.84)
duty_cycle = calc_off_time(0.84)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(0.36)
duty_cycle = calc_off_time(0.36)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(-0.84)
duty_cycle = calc_off_time(-0.84)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(0.36)
duty_cycle = calc_off_time(0.36)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(0.6)
duty_cycle = calc_off_time(0.6)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(0.36)
duty_cycle = calc_off_time(0.36)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(-0.6)
duty_cycle = calc_off_time(-0.6)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(0.36)
duty_cycle = calc_off_time(0.36)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(0.4)
duty_cycle = calc_off_time(0.4)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(0.6)
duty_cycle = calc_off_time(0.6)
move(11, duty_cycle, off_time)

time.sleep(5)

duty_cycle = calc_duty_cycle(0.8)
duty_cycle = calc_off_time(0.8)
move(11, duty_cycle, off_time)

time.sleep(5)