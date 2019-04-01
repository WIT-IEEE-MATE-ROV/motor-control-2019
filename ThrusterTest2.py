import ThrusterLibrary as TH
import time

TH.start_ALL_ESC()

for i in [.6, .7, .84, .7, .6, .5, .4, .36, .6]:
	TH.move(11, i)
	time.sleep(1)