import ThrusterLibrary as TH
import time

TH.start_ALL_ESC()
 
channel = 8

TH.move(channel, 0.1)
time.sleep(10)
TH.move(channel, 0.5)

""" 
for channel in (4, 11)
     TH.move(channe, .9)
     Time.sleep

#go forward
TH.move(5, 0.1)
time.sleep(0.1)
TH.move(6, 0.9)
time.sleep(0.1)
TH.move(7, 0.1)
time.sleep(0.1)
TH.move(9, 0.9)
time.sleep(0.1)

time.sleep(5)

TH.move(5, 0.5)
time.sleep(0.1)
TH.move(6, 0.5)
time.sleep(0.1)
TH.move(7, 0.5)
time.sleep(0.1)
TH.move(9, 0.5)
time.sleep(0.1)

time.sleep(3)


# go down
TH.move(4, 0.1)
time.sleep(0.1)
TH.move(11, 0.1)
time.sleep(0.1)

time.sleep(8)

TH.move(4, 0.5)
time.sleep(0.1)
TH.move(11, 0.5)
time.sleep(0.1)

time.sleep(1)

#go up
TH.move(4, 0.9)
time.sleep(0.1)
TH.move(11, 0.9)
time.sleep(0.1)

time.sleep(8)

TH.move(4, 0.5)
time.sleep(0.1)
TH.move(11, 0.5)
time.sleep(0.1)

time.sleep(3)

#go back
TH.move(5, 0.9)
time.sleep(0.1)
TH.move(6, 0.1)
time.sleep(0.1)
TH.move(7, 0.9)
time.sleep(0.1)
TH.move(9, 0.1)
time.sleep(0.1)

time.sleep(5)

TH.move(5, 0.5)
time.sleep(0.1)
TH.move(6, 0.5)
time.sleep(0.1)
TH.move(7, 0.5)
time.sleep(0.1)
TH.move(9, 0.5)
"""
