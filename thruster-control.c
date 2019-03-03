//https://github.com/Reinbert/pca9685/blob/master/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <wiringPiI2C.h>
#include "thruster-control.h"

#define PIN_BASE 300
#define MAX_PWM 4096
#define FREQ 50

/**
 * This entire program is devoted to a single thruster, as specified by the value passed to argv[argc].
 * This allows thruster control to be asynchronous and makes spawning new thruter programs pretty easy.
 */
int main(int argc, char* argv[]) {
    if(argc != 2) {
        perror("Wrong amount of arguments!\n");
        exit(1);
    }

     pca9685PWMFreq(0x40);

    populate_whichami(argv[argc]);
    if(Whichami.data_source == -1) {
        perror("Didn't recognize that thruster\n");
        exit(2);
    }

    /*initalizes the I2C system - use I2C detect to find the give device identifier
    need to upate the fd's to reflect the identifies*/
    if (wiringPiI2CSetup(fd) == -1){
        sprintf(string, "Failed to set up. (thruster %i)\n", Whichami.data_send);
        perror(string);
    }

    //send the high low signals.. didn't see those
    pca9685PWMFreq();
    while(true) {

        int thruster_goal_value = comms_get_int(Whichami.data_source);
        int error = do_thruster_movement(thruster_goal_value);

        //error is returned as 0 if there is an issue
        if(error == 0) {
            char string[75];
            sprintf(string, "Catastrophic failure of some kind, probably. (thruster %i)\n", Whichami.data_send);
            perror(string);
        }
    }
}

void pca9685PWMFreq(){
    // To set pwm frequency we have to set the prescale register. The formula is:
	// prescale = round(osc_clock / (4096 * frequency))) - 1 where osc_clock = 25 MHz
	// Further info here: http://www.nxp.com/documents/data_sheet/PCA9685.pdf Page 24
	int prescale = (int)(25000000.0f / (4096 * FREQ) - 0.5f);

	// Get settings and calc bytes for the different states.
	int settings = wiringPiI2CReadReg8(fd, PCA9685_MODE1) & 0x7F;	// Set restart bit to 0
	int sleep	= settings | 0x10;									// Set sleep bit to 1
	int wake 	= settings & 0xEF;									// Set sleep bit to 0
	int restart = wake | 0x80;										// Set restart bit to 1

	// Go to sleep, set prescale and wake up again.
	wiringPiI2CWriteReg8(I2C_ADDRESS, PCA9685_MODE1, sleep);
	wiringPiI2CWriteReg8(I2C_ADDRESS, PCA9685_PRESCALE, prescale);
	wiringPiI2CWriteReg8(I2C_ADDRESS, PCA9685_MODE1, wake);

	// Now wait a millisecond until oscillator finished stabilizing and restart PWM.
	delay(1);
	wiringPiI2CWriteReg8(I2C_ADDRESS, PCA9685_MODE1, restart);
}

/**
 * Does the thruster movement. The value provided gets sent to Whichami.data_send.
 * @param goalval The goal value.
 * @return true on success, false on fail.
 */
bool do_thruster_movement(double goalval)

    if ( -1 < goalval && goalval < 1)
        double pwm;
        if(goalval > 0){ //goes "forward"
            pwm = (goalval*4095);
            wiringPiI2CWriteReg16(I2C_ADDRESS, Whichami.pin, pwm & 0x0FFF);
            return true;
        }
        else{  //goes "backward"
            pwm = (goalval*4095*(-1));
		    //need to reverse the power/polarity
            wiringPiI2CWriteReg16(0x40, Whichami.pin, pwm & 0x0FFF);
            return false;
        }
    else{
        return false;
    }
}

/**
 * Populates the 'Whichami' struct.
 */
void populate_whichami(char* input) {
    strcpy(Whichami.name, input);

    if(!strcmp(input, "T_H_FRONTLEFT")) {
        Whichami.data_source = PORT_T_H_FRONTLEFT;
        Whichami.data_send   = T_H_FRONTLEFT;
        pin = 5; 
        return;
    }

    if(!strcmp(input, "T_H_FRONTRIGHT")) {
        Whichami.data_source = PORT_T_H_FRONTRIGHT;
        Whichami.data_send   = T_H_FRONTRIGHT;
        pin = 6; 
        return;
    }

    if(!strcmp(input, "T_H_BACKLEFT")) {
        Whichami.data_source = PORT_T_H_BACKLEFT;
        Whichami.data_send   = T_H_BACKLEFT;
        pin = 7; 
        return;
    }

    if(!strcmp(input, "T_H_BACKRIGHT")) {
        Whichami.data_source = PORT_T_H_BACKRIGHT;
        Whichami.data_send   = T_H_BACKRIGHT;
        pin = 8; 
        return;
    }

    if(!strcmp(input, "T_V_LEFT")) {
        Whichami.data_source = PORT_T_V_LEFT;
        Whichami.data_send   = T_V_LEFT;
        pin = 4; 
        return;
    }

    if(!strcmp(input, "T_V_RIGHT")) {
        Whichami.data_source = PORT_T_V_RIGHT;
        Whichami.data_send   = T_V_RIGHT;
        pin = 2; 
        return;
    }

    if(!strcmp(input, "T_V_FRONT")) {
        Whichami.data_source = PORT_T_V_FRONT;
        Whichami.data_send   = T_V_FRONT;
        pin = 1; 
        return;
    }

    if(!strcmp(input, "T_V_BACK")) {
        Whichami.data_source = PORT_T_V_BACK;
        Whichami.data_send   = T_V_BACK;
        pin = 3; 
        return;
    }

    // If we got here, there was no match... populate -1 so main can handle it.
    Whichami.data_source = -1;
    Whichami.data_send   = -1;
}
