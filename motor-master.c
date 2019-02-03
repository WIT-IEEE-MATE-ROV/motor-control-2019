#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "../rov-core/utils.h"
#include "../comms/nugget-api.h"
#include "../rovlog/rovlog.h"

typedef char* string;

void spawnchild(string childname, string args) {
    int pid = fork();
    if(pid < 0) {
        // TODO: use roverr
        perror("Error of some kind");
        exit(pid);
    }

    if(pid == 0) {
        execl(childname, args, (char*)NULL);
        perror("child should never exit");
        exit(-1);
    }
}

int main(void) {
    rl_setfile("./rovlog.txt");
    rl_setsource("motor-master");
    rl_setlevel(INFO);

    rovlog(INFO, "Spawning children..."); // TODO: Replace with logger

    spawnchild("./thruster-control", "T_H_FRONTLEFT");
    spawnchild("./thruster-control", "T_H_FRONTRIGHT");
    spawnchild("./thruster-control", "T_H_BACKLEFT");
    spawnchild("./thruster-control", "T_H_BACKRIGHT");
    spawnchild("./thruster-control", "T_V_LEFT");
    spawnchild("./thruster-control", "T_V_RIGHT");
    spawnchild("./thruster-control", "T_V_FRONT");
    spawnchild("./thruster-control", "T_V_BACK");

    // Not yet implemented:
    //spawnchild("./subsystem-motor", "MANIPULATOR");
    rovlog(INFO, "Done spawning children");    
}
