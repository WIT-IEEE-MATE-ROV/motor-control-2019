import ThrusterLibrary as TH
import time

channel = 10

TH.move(channel, 1)
time.sleep(0.5)
TH.move(channel, 0)
time.sleep(0.5)
TH.move(channel, 0.5)
time.sleep(0.5)

for i in [0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.5]:
   TH.move(channel, i)
   time.sleep(1)

""" 
for i in [0.6, 0.7, 0.8, 0.9, 0.8, 0.7, 0.6, 0.5]:
   TH.move(channel, i)
   time.sleep(1)
"""
