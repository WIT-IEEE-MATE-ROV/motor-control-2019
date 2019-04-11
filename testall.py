import ThrusterLibrary as TH
import time

TH.start_ALL_ESC()

for channel in range(0, 15):
    TH.move(channel, 0.5)
    time.sleep(.5)
    for i in (0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1):
        TH.move(channel, i)
        time.sleep(.5)
    
for channel in range(0, 15):
    TH.move(channel, .5)

