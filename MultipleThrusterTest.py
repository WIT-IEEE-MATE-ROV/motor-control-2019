import ThrusterLibrary as TH
import time

TH.start_ALL_ESC()

TH.move(5, 0.8)
time.sleep(0.1)
TH.move(6, 0.8)
time.sleep(0.1)
TH.move(7, 0.8)
time.sleep(0.1)
TH.move(9, 0.8)
time.sleep(0.1)

time.sleep(3)

TH.move(5, 0.5)
TH.move(6, 0.5)
TH.move(7, 0.5)
TH.move(9, 0.5)
