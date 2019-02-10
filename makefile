objects = ../comms/nugget-api.o ../rov-core/rov-util.o ../rovlog/rovlog.o 
stdflag = -g -Wall -Wextra -L. -I. -lm -Wl,-unresolved-symbols=ignore-in-shared-libs

all :
	make master
	make motor
	make thruster

master :
	gcc motor-master.c -o motor-master $(stdflag) $(objects)

motor :
	gcc subsystem-motor.c -o subsystem-motor $(stdflag) $(objects)

thruster :
	gcc thruster-control.c -o thruster-control $(stdflag) $(objects)

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


