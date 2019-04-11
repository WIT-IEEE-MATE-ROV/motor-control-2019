import ThrusterLibrary as TH
import time

# Lateral: 5, 6, 7, 9 (temporary)
# Vertical: 4, 11

channel = 11

#TH.start_ALL_ESC()
#TH.start_ALL_TEST()

""" 
TH.move(channel, .9)
time.sleep(0.1)
TH.move(channel, 0)
time.sleep(0.1)
TH.move(channel, 0.5)
time.sleep(0.1)
"""
try:
#    TH.move(channel, 0.7)
#    TH.move(11, 0.7)
#    #TH.move(4 ,0.7)
#    time.sleep(5)
#    TH.move(channel, 0.5)
#    TH.move(11, .5)
#    #TH.move(4, .5)
#    time.sleep(1)
    TH.move(channel, .95)
    time.sleep(1)
    TH.move(channel, .05)
    time.sleep(1)
    TH.move(channel, .5)
    time.sleep(1)
    TH.move(channel, .95)
    time.sleep(1)
    TH.move(channel, .05)
    time.sleep(1)
    TH.move(channel, .5)
    time.sleep(1)
except:
    TH.move(channel, 0.5)

