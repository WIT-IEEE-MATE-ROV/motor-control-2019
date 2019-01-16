# motor-control
For controlling the motors on the ROV.

Motor:
https://www.adafruit.com/product/815

https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/overview

c has a servo.h library

How servos work:
http://www.basicx.com/Products/robotbook/servo%20intro.pdf (supper good if you want to understand whats going on)
also has programing tips at the end 

send pulses to the servo's control board
Servos interpret pulse width as positions
each position along the arc traced out by the rotating shaft has a corresponding pulse width
send a pulse to the servo, the control board calculates which way the shaft should rotate to get to corresponding position
2 ways to wire: position increasing clockwise(BlueBird) or increasing counterclockwise based on pulse widths received
bigger the pulse width bigger the movement in that direction
all have a center position/ neutral position

need to know if servo is modified or unmodified (differs in programing)!!

modified servo full rotation in either direction 
pulses are sent at the desired pulse width of the location it wants it to be at until it has reached the desiered spped
could take a couple pulses (works with a longer or shorter pulse width)

So this has some code at the bottom(in Malay - so ugh thx google translate)- but simple c code
http://thouth.net/rweasy/-1ODVY/4116/pic-lesson-servo-motor?rndad=1160462865-1547608432
