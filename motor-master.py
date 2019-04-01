# motor-master
# @cst <chris thierauf chris@cthierauf.com>
import socket, pickle
import ThrusterLibrary as TH

TH.start_ALL_ESC()

HOST = 'localhost'
PORT = 2013
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

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
    if const is 0.0:
        return [[0, 0, 0, 0], [0, 0, 0, 0]]

    try:
        a = 0 if arra[0][0] == 0 else arra[0][0] / const
        b = 0 if arra[0][1] == 0 else arra[0][0] / const
        c = 0 if arra[0][2] == 0 else arra[0][0] / const
        d = 0 if arra[0][3] == 0 else arra[0][0] / const

        e = 0 if arra[1][0] == 0 else arra[0][0] / const
        f = 0 if arra[1][1] == 0 else arra[0][0] / const
        g = 0 if arra[1][2] == 0 else arra[0][0] / const
        h = 0 if arra[1][3] == 0 else arra[0][0] / const

        return [
            [
                a, b, c, d
            ],
            [
                e, f, g, h
            ]
        ]
    except ZeroDivisionError:
        return [[0, 0, 0, 0], [0, 0, 0, 0]]


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


def hatarr(hat):
    if hat == 0:
        return [[0, 0, 0, 0], [0, 0, 0, 0]]
    if hat == 1:
        return [[0.1, 0, 0, 0], [0, 0, 0, 0]]
    if hat == 2:
        return [[0, 0, 0, 0], [0, 0.1, 0, 0]]
    if hat == 3:
        return [[0, 0.1, 0, 0], [0, 0, 0, 0]]
    if hat == 4:
        return [[0, 0, 0, 0], [0, 0, 0.1, 0]]
    if hat == 5:
        return [[0, 0, 0.1, 0], [0, 0, 0, 0]]
    if hat == 6:
        return [[0, 0, 0, 0], [0, 0, 0, 0.1]]
    if hat == 7:
        return [[0, 0, 0, 0.1], [0, 0, 0, 0]]
    if hat == 8:
        return [[0, 0, 0, 0], [0.1, 0, 0, 0]]


def motorrun(M):
    TH.move(1, M[0][1])
    TH.move(2, M[0][2])
    TH.move(3, M[0][3])
    TH.move(4, M[0][4])
    TH.move(5, M[1][1])
    TH.move(6, M[1][2])
    TH.move(7, M[1][3])
    TH.move(8, M[1][4])


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
        M = arradd(M, arrmult(jta, arrr))
        M = arradd(M, arrmult(jla, arrz))

    # print(arrmax(M))
    M = arrdiv(M, arrmax(M))
    printarr(M)
    motorrun(M)
    conn.send(data)

conn.close()
