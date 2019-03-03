#ifndef ROVTHRUSTER
#define ROVTHRUSTER

//// UTILITIES ////
struct __WHICHAMI__ {
    char name[25];   // Note that this is static, and will not be allocated dynamically.
    char data_source[64];
    int data_send;
    int fd; //register on pca(0-16)
} Whichami;

//default is 0x40...
#define I2C_ADDRESS 0x40

#define T_H_FRONTLEFT  5
#define T_H_FRONTRIGHT 6
#define T_H_BACKLEFT   7
#define T_H_BACKRIGHT  8
#define T_V_LEFT       4
#define T_V_RIGHT      2
#define T_V_FRONT      1
#define T_V_BACK       3

//need API stuff 
// TODO: these definitions contain the port number where the respective information can be found.
#define API_T_H_FRONTLEFT  "motor/thruster/fl/goal\0"
#define API_T_H_FRONTRIGHT "motor/thruster/fr/goal\0"
#define API_T_H_BACKLEFT   "motor/thruster/bl/goal\0"
#define API_T_H_BACKRIGHT  "motor/thruster/br/goal\0"
#define API_T_V_LEFT       "motor/thruster/l/goal\0"
#define API_T_V_RIGHT      "motor/thruster/r/goal\0"
#define API_T_V_FRONT      "motor/thruster/f/goal\0"
#define API_T_V_BACK       "motor/thruster/b/goal\0"

//// FUNCTIONS ////
void populate_whichami(char*); 
bool do_thruster_movement(double);


#endif
