#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "./WiringPi/wiringPi/wiringPi.h"
#include "./WiringPi/wiringPi/wiringPiI2C.h"
#include "./pca9685.c"
#include "thruster-control.h"

#include "rov-standard-utils.h"
#include "pca9685.h"

//Setup Registers
#define PCA9685_MODE1 0x0
#define PCA9685_PRESCALE 0xFE

/**
 * This entire program is devoted to a single thruster, as specified by the value passed to argv[argc].
 * This allows thruster control to be asynchronous and makes spawning new thruter programs pretty easy.
 */
int main(int argc, char* argv[]) {
    rl_setfile("./rovlog.txt");
    rl_setlevel(INFO);
    rl_setsource("Unspecified thruster-control");

    if(argc != 2) {
        rovlog(FATAL, "Wrong amount of arguments!");
        exit(1);
    }

    populate_whichami(argv[argc]);
    if(Whichami.data_source[0] == '\0') {
        rovlog(FATAL, "Didn't recognize that thruster");
        exit(2);
    }

    rl_setsource(Whichami.name);
    LISTENER thruster_listener = get_listener(Whichami.data_source, _double);

    while(true) {
        double thruster_goal_value = get_double(thruster_listener);
        bool error = false;
        error = do_thruster_movement(thruster_goal_value);
        
        if(error) {
            char string[75];
            sprintf(string, "Catastrophic failure of some kind, probably. (thruster %i)", Whichami.data_send);
            rovlog(FATAL, string);
        }
    }
}

/**
 * Does the thruster movement. The value provided gets sent to Whichami.data_send.
 * @param goalval The goal value.
 * @return true on success, false on fail.
 */
//PWM max = 4095
bool do_thruster_movement(double goalval) {
    // goal value= percent pressed forward on joystick... speed
    //.h file that takes the goalval and translates into a pwm for speed
    if ( -1 < goalval && goalval < 1) {
        double pwm;
        if(goalval > 0){ //goes "forward"
            pwm = (goalval*4095);
            /*****************************
             * Commented out to allow compiling. @Julie-- this is expected a node struct, but you're 
             * handing it an int file descritor.
             */
            //myPwmWrite(Whichami.fd, pwm);
            //may need to check that it actually wrote the corect valur for troubleshooting
            return true;
        }
        else{  //goes "backward"
            pwm = (goalval*4095*(-1));
            //myPwmWrite(Whichami.fd, pwm);
            //msy need to add in reading
            return true;
        }
    } else
        return false;
}

/**
 * Populates the 'Whichami' struct.
 */
void populate_whichami(char* input) {
    strcpy(Whichami.name, input);

    if(!strcmp(input, "T_H_FRONTLEFT")) {
        strcpy(Whichami.data_source, API_T_H_FRONTLEFT);
        Whichami.data_send   = T_H_FRONTLEFT;
        return;
    }

    if(!strcmp(input, "T_H_FRONTRIGHT")) {
        strcpy(Whichami.data_source, API_T_H_FRONTRIGHT);
        Whichami.data_send   = T_H_FRONTRIGHT;
        return;
    }
   
    if(!strcmp(input, "T_H_BACKLEFT")) {
        strcpy(Whichami.data_source, API_T_H_BACKLEFT);
        Whichami.data_send   = T_H_BACKLEFT;
        return;
    }
   
    if(!strcmp(input, "T_H_BACKRIGHT")) {
        strcpy(Whichami.data_source, API_T_H_BACKRIGHT);
        Whichami.data_send   = T_H_BACKRIGHT;
        return;
    }
   
    if(!strcmp(input, "T_V_LEFT")) {
        strcpy(Whichami.data_source, API_T_V_LEFT);
        Whichami.data_send   = T_V_LEFT;
        return;
    }
   
    if(!strcmp(input, "T_V_RIGHT")) {
        strcpy(Whichami.data_source, API_T_V_RIGHT);
        Whichami.data_send   = T_V_RIGHT;
        return;
    }
   
    if(!strcmp(input, "T_V_FRONT")) {
        strcpy(Whichami.data_source, API_T_V_FRONT);
        Whichami.data_send   = T_V_FRONT;
        return;
    }
   
    if(!strcmp(input, "T_V_BACK")) {
        strcpy(Whichami.data_source, API_T_V_BACK);
        Whichami.data_send   = T_V_BACK;
        return;
    }

    // If we got here, there was no match... populate -1 so main can handle it.
    Whichami.data_source[0] = '\0';
    Whichami.data_send      = -1;
}
