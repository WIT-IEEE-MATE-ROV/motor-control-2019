#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

typedef char* string;

int spawnchild(string childname, string args) {
    int pid = fork();
    if(pid < 0) {
        // TODO: use roverr
        perror("Error of some kind");
        exit(pid);
    }

    if(pid == 0) {
        execl(childname, args);
        perror("child should never exit");
        exit(-1);
    }

    return pid;
}

int main(void) {
    printf("Spawning children...\n"); // TODO: Replace with logger

    int pid1 = spawnchild("./thruster-control", "T_H_FRONTLEFT");
    int pid2 = spawnchild("./thruster-control", "T_H_FRONTRIGHT");
    int pid3 = spawnchild("./thruster-control", "T_H_BACKLEFT");
    int pid4 = spawnchild("./thruster-control", "T_H_BACKRIGHT");
    int pid5 = spawnchild("./thruster-control", "T_V_LEFT");
    int pid6 = spawnchild("./thruster-control", "T_V_RIGHT");
    int pid7 = spawnchild("./thruster-control", "T_V_FRONT");
    int pid8 = spawnchild("./thruster-control", "T_V_BACK");

    // Not yet implemented:
    //int pid9 = spawnchild("./subsystem-motor", "MANIPULATOR");
    
    printf("All done!\n");
}
