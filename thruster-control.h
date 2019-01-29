#ifndef ROVTHRUSTER
#define ROVTHRUSTER

//// UTILITIES ////
struct __WHICHAMI__ {
    char name[25];   // Note that this is static, and will not be allocated dynamically.
    int data_source;
    int data_send;
    int fileDescriptor;
} Whichami;

//default is 0x40...
// TODO: these definitions act as names for our thrusters. What values should they hold (i2c addresses or whatev)
#define T_H_FRONTLEFT  0x40
#define T_H_FRONTRIGHT 0x40
#define T_H_BACKLEFT   0x40
#define T_H_BACKRIGHT  0x40
#define T_V_LEFT       0x40
#define T_V_RIGHT      0x40
#define T_V_FRONT      0x40
#define T_V_BACK       0x40

//need API stuff for this @Chris
// TODO: these definitions contain the port number where the respective information can be found.
#define PORT_T_H_FRONTLEFT  0
#define PORT_T_H_FRONTRIGHT 0
#define PORT_T_H_BACKLEFT   0
#define PORT_T_H_BACKRIGHT  0
#define PORT_T_V_LEFT       0
#define PORT_T_V_RIGHT      0
#define PORT_T_V_FRONT      0
#define PORT_T_V_BACK       0

//// FUNCTIONS ////
void populate_whichami(char*); 
bool do_thruster_movement(int);
static void myPwmWrite(struct wiringPiNodeStruct *node, int pin, int value);
static void myOnOffWrite(struct wiringPiNodeStruct *node, int pin, int value);
static int myOffRead(struct wiringPiNodeStruct *node, int pin);
static int myOnRead(struct wiringPiNodeStruct *node, int pin);
int baseReg(int pin);

//ifndef ROVCOMM
//#define ROVCOMM
// This should only be declared by the comm's package.
//int comms_get_int(int);
//#pragma warn The comms package have not been properly included, declaring to allow compilation
//#endif
int comms_get_int(int i) {
    return -1;
}

#endif
