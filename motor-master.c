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
    rovlog(INFO, "Done spawning children, starting sensor listeners to do PID stuff");

    LISTENER accel_x = get_listener("sensor/accelerometer/x", _double);
    LISTENER accel_y = get_listener("sensor/accelerometer/y", _double);
    LISTENER accel_z = get_listener("sensor/accelerometer/z", _double);

    LISTENER gyro_r = get_listener("sensor/gyroscope/roll", _double);
    LISTENER gyro_p = get_listener("sensor/gyroscope/pitch", _double);
    LISTENER gyro_y = get_listener("sensor/gyroscope/yaw", _double);

    LISTENER goal_x = get_listener("goals/x", _double);
    LISTENER goal_y = get_listener("goals/y", _double);
    LISTENER goal_z = get_listener("goals/z", _double);

    LISTENER goal_roll = get_listener("goals/roll", _double);
    LISTENER goal_pitch = get_listener("goals/pitch", _double);
    LISTENER goal_yaw = get_listener("goals/yaw", _double);

    while(1) {
        double sensor_state[] =  {
            get_double(accel_x),
            get_double(accel_y),
            get_double(accel_z),

            get_double(gyro_r),
            get_double(gyro_p),
            get_double(gyro_y)
        };
        
        double goal_state[] = {
            get_double(goal_x),
            get_double(goal_y),
            get_double(goal_z),

            get_double(goal_roll),
            get_double(goal_pitch),
            get_double(goal_yaw)
        };
    }
}
