all :
	gcc motor-master.c -o motor-master -g -Wall -Wextra -L. -I.
	make motor
	make thruster

motor :
	gcc subsystem-motor.c -o subsystem-motor -g -Wall -Wextra -L. -I.

thruster :
	gcc thruster-control.c -o thruster-control -g -Wall -Wextra -L. -I.

test : 
	gcc rovtest.c -o rovtest -g -Wall -Wextra
	./rovtest

clean :
	rm -f ./rovtest
	rm -f ./thruster-control
	rm -f ./subsystem-motor
	rm -f ./motor-master

rovmode :
	gcc include/rovcore.c include/rovonly.c rovmain.c -o rovmain_rovmode -DDEF=ROVMODE -g -Wall -Wextra -L. -march=armv6

rovmodetest: 
	gcc include/rovcore.c include/rovonly.c rovmain.c -o rovmain -g -Wall -Wextra -L. -Iinclude/ -DROVMODE

upload :
	make rovmode
	scp ./rovmain-rovmode nugget@spacenugget.local:/opt/rovmain
	ssh nugget@spacenugget.local 'systemctl restart nugget'


