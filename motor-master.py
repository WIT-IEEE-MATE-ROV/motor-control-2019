# motor-master
# @cst <chris thierauf chris@cthierauf.com>
import socket, pickle
import ThrusterLibrary as TH
import RPi.GPIO as gpio
from time import sleep
print("Started!")

HOST = '0.0.0.0'
PORT = 2015

STEPPER_DIR_PIN = 13
STEPPER_PULSE_PIN = 11
PUMP_ENABLE_PIN = 29
REFERENCE_PIN = 35

STEPPER_PULSE = 0
PUMP_STATE = False
MANIPULATOR_STATE = False
DELAYSTEP = 3
DUMPER_OPENPWM = 0.02
DUMPER_CLOSEPWM = 0.07
BOOST_DIV = 2

print("Attempting socket")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

print("Socket accepted")
print("Starting ESC's")

TH.start_ALL_ESC()

print("Setting up GPIO stuff")
gpio.setmode(gpio.BOARD)
gpio.setup(STEPPER_DIR_PIN, gpio.OUT)
gpio.setup(STEPPER_PULSE_PIN, gpio.OUT)
gpio.setup(PUMP_ENABLE_PIN, gpio.OUT) 
gpio.setup(REFERENCE_PIN, gpio.OUT)
gpio.output(REFERENCE_PIN, gpio.HIGH)

arrx = [
        [0.0, 0.0, 0.0, 0.0], [1.0, -1.0, -1.0, 1.0]  # x
    ]

arry = [
        [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, -1.0, -1.0]  # y
    ]

arrz = [
        [1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0]    # z
    ]

arrr = [
        [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 0.0, 0.0]    # r
    ]

arrp = [
        [1.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 0.0]    # p
    ]

arrc = [
        [0.0, 0.0, 0.0, 0.0], [1.0, -1.0, 1.0, -1.0]  # c
    ]

arr_corrective = [
        [1, -1, 1, -1], [-1, -1, 1, -1]
    ]

BOOST_ARR = [
        [False, False, False, False], [True, True, True, True]
    ]


def printarr(arra):
    print("{:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}".format(arra[0][0], arra[0][1], arra[0][2], arra[0][3], arra[1][0], arra[1][1], arra[1][2], arra[1][3]))


def arrmult(const, arra):
    return [
        [
            arra[0][0] * const,
            arra[0][1] * const,
            arra[0][2] * const,
            arra[0][3] * const
        ],
        [
            arra[1][0] * const,
            arra[1][1] * const,
            arra[1][2] * const,
            arra[1][3] * const
        ]
    ]


def arrdiv(arra, const):
    try:
        a = arra[0][0] / const
        b = arra[0][1] / const
        c = arra[0][2] / const
        d = arra[0][3] / const

        e = arra[1][0] / const
        f = arra[1][1] / const
        g = arra[1][2] / const
        h = arra[1][3] / const

        return [
            [
                a, b, c, d
            ],
            [
                e, f, g, h
            ]
        ]
    except ZeroDivisionError:
        print("0div")
        return [[0, 0, 0, 0], [0, 0, 0, 0]]

def arrdiv_boost(arra):
    a = 1 if BOOST_ARR[0][0] else BOOST_DIV
    b = 1 if BOOST_ARR[0][1] else BOOST_DIV
    c = 1 if BOOST_ARR[0][2] else BOOST_DIV
    d = 1 if BOOST_ARR[0][3] else BOOST_DIV
    e = 1 if BOOST_ARR[1][0] else BOOST_DIV
    f = 1 if BOOST_ARR[1][1] else BOOST_DIV
    g = 1 if BOOST_ARR[1][2] else BOOST_DIV
    h = 1 if BOOST_ARR[1][3] else BOOST_DIV

    return [
        [
            arra[0][0]/a,
            arra[0][1]/b,
            arra[0][2]/c,
            arra[0][3]/d
        ],
        [
            arra[1][0]/e,
            arra[1][1]/f,
            arra[1][2]/g,
            arra[1][3]/h
        ]
    ]


def arrmax(arra):
    rmax = -2
    for i in range(0, 3):
        rmax = max(arra[0][i], rmax)
    for i in range(0, 3):
        rmax = max(arra[1][i], rmax)
    return rmax


def arradd(arra, arrb):
    return [
        [
            arra[0][0] + arrb[0][0],
            arra[0][1] + arrb[0][1],
            arra[0][2] + arrb[0][2],
            arra[0][3] + arrb[0][3]
        ],
        [
            arra[1][0] + arrb[1][0],
            arra[1][1] + arrb[1][1],
            arra[1][2] + arrb[1][2],
            arra[1][3] + arrb[1][3]

        ]
    ]


def arrmultarr(arra, arrb):
    return [
        [
            arra[0][0] * arrb[0][0],
            arra[0][1] * arrb[0][1],
            arra[0][2] * arrb[0][2],
            arra[0][3] * arrb[0][3]
        ],
        [
            arra[1][0] * arrb[1][0],
            arra[1][1] * arrb[1][1],
            arra[1][2] * arrb[1][2],
            arra[1][3] * arrb[1][3]

        ]
    ]


def arraddint(arra, i):
    return [
        [
            arra[0][0] + i,
            arra[0][1] + i,
            arra[0][2] + i,
            arra[0][3] + i
        ],
        [
            arra[1][0] + i,
            arra[1][1] + i,
            arra[1][2] + i,
            arra[1][3] + i

        ]
    ]


def hatarr(hat):
    hatconst = 0.2
    if hat == 0:
        return [[0, 0, 0, 0], [0, 0, 0, 0]]
    if hat == 1:
        return [[hatconst, 0, 0, 0], [0, 0, 0, 0]]
    if hat == 2:
        return [[0, 0, 0, 0], [0, hatconst, 0, 0]]
    if hat == 3:
        return [[0, hatconst, 0, 0], [0, 0, 0, 0]]
    if hat == 4:
        return [[0, 0, 0, 0], [0, 0, hatconst, 0]]
    if hat == 5:
        return [[0, 0, hatconst, 0], [0, 0, 0, 0]]
    if hat == 6:
        return [[0, 0, 0, 0], [0, 0, 0, hatconst]]
    if hat == 7:
        return [[0, 0, 0, hatconst], [0, 0, 0, 0]]
    if hat == 8:
        return [[0, 0, 0, 0], [hatconst, 0, 0, 0]]


def motorrun(M):
    TH.move(11, M[0][0])
    TH.move(10, M[0][1])
    TH.move(4, M[0][2])
    TH.move(9, M[0][3])
    TH.move(8, M[1][0])
    TH.move(6, M[1][1])
    TH.move(7, M[1][2])
    TH.move(5, M[1][3])
    pass

try:
    sleep(1)
    for i in range(0, 15):
        TH.move(i, .5)

    while True:
        M = [
            [
                0.0, 0.0, 0.0, 0.0
            ],
            [
                0.0, 0.0, 0.0, 0.0
            ]
        ]
        data = conn.recv(4096)
        if not data: break
        fromsurface = pickle.loads(data)
    
        jha = fromsurface[0][0]
        jva = -1*fromsurface[0][1]
        jta = fromsurface[0][2]
        jla = -1*fromsurface[0][3]
    
        M = hatarr(fromsurface[2][0])
        if fromsurface[1][0] is 0:  # Disables input from joystick if trigger is held
            M = arradd(M, arrmult(jha, arrx))
            M = arradd(M, arrmult(jva, arry))
            M = arradd(M, arrmult(jta, arrc))
            M = arradd(M, arrmult(jla, arrz))
            
            # Use buttons on joystick face to handle roll, pitch
            if fromsurface[1][2] is 1:
                M = arradd(M, arrmult(.2, arrp))
            if fromsurface[1][3] is 1:
                M = arradd(M, arrmult(-.2, arrp))
            if fromsurface[1][4] is 1:
                M = arradd(M, arrmult(.2, arrr))
            if fromsurface[1][5] is 1:
                M = arradd(M, arrmult(-.2, arrr))
  
        # Use the thumb button as 'boost mode'
        if fromsurface[1][1] is not 1:
            M = arrdiv_boost(M)


        # Correct for things being backwards or poorly toleranced
        M = arrmultarr(arr_corrective, M)

        # Matrix normalization
        amax = arrmax(M)
        if arrmax(M) >= 1:
            M = arrdiv(M, amax)
        M = arraddint(M, 1)
        M = arrdiv(M, 2)

        # Display what we're about to try here
        printarr(M)

        # Matrix is now values of 0 to 1, with each index representing a thruster
        motorrun(M)

        # Open
        if fromsurface[1][6] is 1 or fromsurface[1][7] is 1:
            print("MANIP")
            gpio.output(STEPPER_DIR_PIN, fromsurface[1][6])
            if not MANIPULATOR_STATE:
                MANIPULATOR_STATE = True
                TH.send(15, .5)
        elif MANIPULATOR_STATE == True:
            print("NOMANIP")
            MANIPULATOR_STATE = False
            TH.send(15, 0)

#        # Close
#        if fromsurface[1][7] is 1:
#            gpio.output(STEPPER_DIR_PIN, gpio.LOW)
#            TH.send(15, .5)
#        else:
#            TH.send(15, 0)

        # Pump
        if fromsurface[1][10] is 1:
            print("PUMP")
            PUMP_STATE = True
            gpio.output(PUMP_ENABLE_PIN, gpio.HIGH)
        if fromsurface[1][10] is not 1 and PUMP_STATE == True:
            PUMP_STATE = False
            gpio.output(PUMP_ENABLE_PIN, gpio.LOW)

        # Dumper
        if fromsurface[1][11] is 1:
            TH.move(0, .45)
        else:
            TH.move(0, .85)

        conn.send(data)
except Exception as e:
    print("Shutting down!")
    print(e)
    for i in range(0, 15):
        TH.move(i, .5)
    conn.close()
