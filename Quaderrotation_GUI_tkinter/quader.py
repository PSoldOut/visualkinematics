from turtle import color
from matplotlib import animation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox
from matplotlib.patches import FancyArrowPatch
from enum import Enum
# Wie die einzelnen Punkte zu Geraden verbunden Werden:
#A - 1, B - 2, C - 2, D - 3, E - 4, F - 5, G - 6, H - 7
# [A,B] -> [0,1]
arangement = [[0,1],[0,3],[0,4],[1,2],[1,5],[2,3],[2,6],[3,7],[4,5],[4,7],[5,6],[6,7]]

class rotOrder(Enum):
    XYZ = 1
    XZY = 2
    YXZ = 3
    YZX = 4
    ZXY = 5
    ZYX = 6
    ZYZ = 7

def getxyz(lineP):
    z = [lineP[0][0],lineP[1][0]]
    x = [lineP[0][1],lineP[1][1]]
    y = [lineP[0][2],lineP[1][2]]
    return z,x,y



def getQuaderRotation1(phiX, phiY, phiZ, lines, rot_order=rotOrder.XYZ, koerper_coord_sys=False):
    
    #Grundlängen des Würfels
    Bz = np.array([0,0,1])
    Bx = np.array([3,0,0])
    By = np.array([0,2,0])
    
    if rot_order == rotOrder.ZYZ: #Euler Case Two Rotations around Z and one around Y Axis
        if(phiX is not None): #Interprete phiX as phiZ by Exchanging the Rot Matrix from PhiX to the rot matrix of PhiZ
            phiX = phiX*np.pi/180 
            rotMatrixX = np.array([
                [np.cos(phiX), -np.sin(phiX), 0],
                [np.sin(phiX), np.cos(phiX), 0],
                [0, 0, 1]
            ])
        else:
            rotMatrixX = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
            ])

        #Rotation entlang der Y-Achse anhand der Rot-Matrix und dem gegebenen Winkel
        if(phiY is not None):

            phiY = phiY*np.pi/180 

            rotMatrixY = np.array([
            [np.cos(phiY), 0, np.sin(phiY)],
            [0, 1, 0],
            [-np.sin(phiY), 0, np.cos(phiY)]
            ])
        else:
            rotMatrixY = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
            ])

        #Rotation entlang der Z-Achse anhand der Rot-Matrix und dem gegebenen Winkel
        if(phiZ is  not None):
            phiZ = phiZ*np.pi/180 

            rotMatrixZ = np.array([
                [np.cos(phiZ), -np.sin(phiZ), 0],
                [np.sin(phiZ), np.cos(phiZ), 0],
                [0, 0, 1]
            ])
        else:
            rotMatrixZ = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
            ])

    else:# Normal Case (Every Axes is displayed ones)
        #Rotation entlang der X-Achse anhand der Rot-Matrix und dem gegebenen Winkel
        if(phiX is not None):
            phiX = phiX*np.pi/180 
            rotMatrixX = np.array([
            [1, 0, 0],
            [0, np.cos(phiX), -np.sin(phiX)],
            [0, np.sin(phiX), np.cos(phiX)]
            ])
        else:
            rotMatrixX = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
            ])

        #Rotation entlang der Y-Achse anhand der Rot-Matrix und dem gegebenen Winkel
        if(phiY is not None):

            phiY = phiY*np.pi/180 

            rotMatrixY = np.array([
            [np.cos(phiY), 0, np.sin(phiY)],
            [0, 1, 0],
            [-np.sin(phiY), 0, np.cos(phiY)]
            ])
        else:
            rotMatrixY = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
            ])

        #Rotation entlang der Z-Achse anhand der Rot-Matrix und dem gegebenen Winkel
        if(phiZ is  not None):
            phiZ = phiZ*np.pi/180 

            rotMatrixZ = np.array([
                [np.cos(phiZ), -np.sin(phiZ), 0],
                [np.sin(phiZ), np.cos(phiZ), 0],
                [0, 0, 1]
            ])
        else:
            rotMatrixZ = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
            ])
    


    if not koerper_coord_sys:
        if rot_order == rotOrder.XYZ:
            gesamtRotMatrix = np.matmul(rotMatrixX, rotMatrixY)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixZ)
        elif rot_order == rotOrder.XZY:
            gesamtRotMatrix = np.matmul(rotMatrixX, rotMatrixZ)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixY)
        elif rot_order == rotOrder.YXZ:
            gesamtRotMatrix = np.matmul(rotMatrixY, rotMatrixX)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixZ)
        elif rot_order == rotOrder.YZX:
            gesamtRotMatrix = np.matmul(rotMatrixY, rotMatrixZ)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixX)
        elif rot_order == rotOrder.ZXY:
            gesamtRotMatrix = np.matmul(rotMatrixZ, rotMatrixX)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixY)
        elif rot_order == rotOrder.ZYX:
            gesamtRotMatrix = np.matmul(rotMatrixZ, rotMatrixY)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixX)
        elif rot_order == rotOrder.ZYZ:
            gesamtRotMatrix = np.matmul(rotMatrixX, rotMatrixY)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixZ)
    else:
        if rot_order == rotOrder.XYZ:
            gesamtRotMatrix = np.matmul(rotMatrixZ, rotMatrixY)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixX)
        elif rot_order == rotOrder.XZY:
            gesamtRotMatrix = np.matmul(rotMatrixY, rotMatrixZ)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixX)
        elif rot_order == rotOrder.YXZ:
            gesamtRotMatrix = np.matmul(rotMatrixZ, rotMatrixX)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixY)
        elif rot_order == rotOrder.YZX:
            gesamtRotMatrix = np.matmul(rotMatrixX, rotMatrixZ)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixY)
        elif rot_order == rotOrder.ZXY:
            gesamtRotMatrix = np.matmul(rotMatrixY, rotMatrixX)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixZ)
        elif rot_order == rotOrder.ZYX:
            gesamtRotMatrix = np.matmul(rotMatrixX, rotMatrixY)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixZ)
        elif rot_order == rotOrder.ZYZ:
            gesamtRotMatrix = np.matmul(rotMatrixZ, rotMatrixY)
            gesamtRotMatrix = np.matmul(gesamtRotMatrix, rotMatrixX)


    Bz = gesamtRotMatrix.dot(Bz)
    Bx = gesamtRotMatrix.dot(Bx)
    By = gesamtRotMatrix.dot(By)




    #Die Einzelnen Punkte des Quaders anhand des Grundvektors und den Rotierten Richtungsvektoren bestimmen
    zero_vec = np.array([0,0,0])

    A = zero_vec
    B = zero_vec+Bx
    C = zero_vec+Bx+By
    D = zero_vec+By
    E = zero_vec+Bz
    F = zero_vec+Bz+Bx
    G = zero_vec+Bz+Bx+By
    H = zero_vec+Bz+By

    points = np.array([A,B,C,D,E,F,G,H])

    #Die Punktkombinationen anhand dessen, wie in "arrangement" festgelegt in ein Array schreiben 
    linePoints = np.empty((0,2,3))
    for x in arangement:
        linePoints = np.append(linePoints, [[points[x[0]], points[x[1]]]], axis=0) 

    #Die Linienplots mit den neuen Punktkoordinaten aktualisieren 
    for x in range(len(arangement)):
        lines[x].set_data_3d(getxyz(linePoints[x]))



def initPlot(plt):

    plt.title("Quaderrotation Animation")
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')


    #Initial View of the Rectangle
    ax.view_init(elev=20., azim=45)

    # ax.quiver(0,0,0,0,0,4,length=4.0, normalize=True)
    ax.plot([0,0], [0,0], [0,4], color='black', label= '$Z$')
    ax.plot([0,4], [0,0], [0,0], color='black', label= '$X$')
    ax.plot([0,0], [0,4], [0,0], color='black', label= '$Y$')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # getQuaderRotation2(ax,0)
    # getQuaderRotation1(ax,90)

    z,x,y = [0,0], [0,0], [0,4]
    line1, = ax.plot(z,x,y) 
    line2, = ax.plot(z,x,y) 
    line3, = ax.plot(z,x,y) 
    line4, = ax.plot(z,x,y) 
    line5, = ax.plot(z,x,y) 
    line6, = ax.plot(z,x,y) 
    line7, = ax.plot(z,x,y) 
    line8, = ax.plot(z,x,y) 
    line9, = ax.plot(z,x,y) 
    line10, = ax.plot(z,x,y) 
    line11, = ax.plot(z,x,y) 
    line12, = ax.plot(z,x,y) 

    lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12]



    return fig, lines

