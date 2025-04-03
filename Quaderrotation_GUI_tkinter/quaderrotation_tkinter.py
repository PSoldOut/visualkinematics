from tkinter import RIGHT, Frame, TclError
import matplotlib
matplotlib.use('TkAgg')
import quader
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from tkinter import messagebox as m_box 
from quader import rotOrder

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

paused = False
played = False

root = Tk.Tk()
root.wm_title("Quaderrotation Animation")

orderRot = 1
koerperCoordSys = False


animationRangeX = np.linspace(start= 0, stop= 90,num=90) 
animationRangeY = np.linspace(start= 0, stop= -90,num=90) 
animationRangeZ = np.linspace(start= 0, stop= 90,num=90) 

f, linesArr = quader.initPlot(plt)


lenX = len(animationRangeX)
lenY = len(animationRangeY)
lenZ = len(animationRangeZ)

def animate(i):
    global played, paused, orderRot, koerperCoordSys
    if orderRot == 1:
        if(i < lenX):
            quader.getQuaderRotation1(animationRangeX[i], None, None, linesArr, rot_order=rotOrder.XYZ,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenY):
            quader.getQuaderRotation1(animationRangeX[lenX-1 if lenX != 0 else 0], animationRangeY[i-lenX], None, linesArr, rot_order=rotOrder.XYZ,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenY+lenZ):
            quader.getQuaderRotation1(animationRangeX[lenX-1 if lenX != 0 else 0], animationRangeY[lenY-1 if lenY != 0 else 0], animationRangeZ[i-(lenX+lenY)], linesArr, rot_order=rotOrder.XYZ,koerper_coord_sys=koerperCoordSys)
        else:
            anim.event_source.stop()
            paused = True
            played = True
    elif orderRot == 2:
        if(i < lenX):
            quader.getQuaderRotation1(animationRangeX[i], None, None, linesArr, rot_order=rotOrder.XZY,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenZ):
            quader.getQuaderRotation1(animationRangeX[lenX-1 if lenX != 0 else 0], None, animationRangeZ[i-lenX], linesArr, rot_order=rotOrder.XZY,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenY+lenZ):
            quader.getQuaderRotation1(animationRangeX[lenX-1 if lenX != 0 else 0], animationRangeY[i-(lenX+lenZ)], animationRangeZ[lenZ-1 if lenZ != 0 else 0], linesArr, rot_order=rotOrder.XZY,koerper_coord_sys=koerperCoordSys)
        else:
            anim.event_source.stop()
            paused = True
            played = True
    elif orderRot == 3:
        if(i < lenY):
            quader.getQuaderRotation1(None, animationRangeY[i], None, linesArr, rot_order=rotOrder.YXZ,koerper_coord_sys=koerperCoordSys)
        elif(i < lenY+lenX):
            quader.getQuaderRotation1(animationRangeX[i-lenY], animationRangeY[lenY-1 if lenY != 0 else 0], None, linesArr, rot_order=rotOrder.YXZ,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenY+lenZ):
            quader.getQuaderRotation1(animationRangeX[lenX-1 if lenX != 0 else 0], animationRangeY[lenY-1 if lenY != 0 else 0], animationRangeZ[i-(lenX+lenY)], linesArr, rot_order=rotOrder.YXZ,koerper_coord_sys=koerperCoordSys)
        else:
            anim.event_source.stop()
            paused = True
            played = True
    elif orderRot == 4:
        if(i < lenY):
            quader.getQuaderRotation1(None, animationRangeY[i], None, linesArr, rot_order=rotOrder.YZX,koerper_coord_sys=koerperCoordSys)
        elif(i < lenY+lenZ):
            quader.getQuaderRotation1(None, animationRangeY[lenY-1], animationRangeZ[i-lenY], linesArr, rot_order=rotOrder.YZX,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenY+lenZ):
            quader.getQuaderRotation1(animationRangeX[i-(lenY+lenZ)], animationRangeY[lenY-1 if lenY != 0 else 0], animationRangeZ[lenZ-1 if lenZ != 0 else 0], linesArr, rot_order=rotOrder.YZX,koerper_coord_sys=koerperCoordSys)
        else:
            anim.event_source.stop()
            paused = True
            played = True
    elif orderRot == 5:
        if(i < lenZ):
            quader.getQuaderRotation1(None, None, animationRangeZ[i], linesArr, rot_order=rotOrder.ZXY,koerper_coord_sys=koerperCoordSys)
        elif(i < lenZ+lenX):
            quader.getQuaderRotation1(animationRangeX[i-lenZ], None, animationRangeZ[lenZ-1 if lenZ != 0 else 0], linesArr, rot_order=rotOrder.ZXY,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenY+lenZ):
            quader.getQuaderRotation1(animationRangeX[lenX-1 if lenX != 0 else 0], animationRangeY[i-(lenX+lenZ)], animationRangeZ[lenZ-1 if lenZ != 0 else 0], linesArr, rot_order=rotOrder.ZXY,koerper_coord_sys=koerperCoordSys)
        else:
            anim.event_source.stop()
            paused = True
            played = True
    elif orderRot == 6:
        if(i < lenZ):
            quader.getQuaderRotation1(None, None, animationRangeZ[i], linesArr, rot_order=rotOrder.ZYX,koerper_coord_sys=koerperCoordSys)
        elif(i < lenZ+lenY):
            quader.getQuaderRotation1(None, animationRangeY[i-lenZ], animationRangeZ[lenZ-1 if lenZ != 0 else 0], linesArr, rot_order=rotOrder.ZYX,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenY+lenZ):
            quader.getQuaderRotation1(animationRangeX[i-(lenY+lenZ)], animationRangeY[lenY-1 if lenY != 0 else 0], animationRangeZ[lenZ-1 if lenZ != 0 else 0], linesArr, rot_order=rotOrder.ZYX,koerper_coord_sys=koerperCoordSys)
        else:
            anim.event_source.stop()
            paused = True
            played = True
    elif orderRot == 7:
        if(i < lenX):
            quader.getQuaderRotation1(animationRangeX[i], None, None, linesArr, rot_order=rotOrder.ZYZ,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenY):
            quader.getQuaderRotation1(animationRangeX[lenX-1 if lenX != 0 else 0], animationRangeY[i-lenX], None, linesArr, rot_order=rotOrder.ZYZ,koerper_coord_sys=koerperCoordSys)
        elif(i < lenX+lenY+lenZ):
            quader.getQuaderRotation1(animationRangeX[lenX-1 if lenX != 0 else 0], animationRangeY[lenY-1 if lenY != 0 else 0], animationRangeZ[i-(lenX+lenY)], linesArr, rot_order=rotOrder.ZYZ,koerper_coord_sys=koerperCoordSys)
        else:
            anim.event_source.stop()
            paused = True
            played = True

    # return line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12

anim = FuncAnimation(f, animate, frames=3*360+1,  interval=50, repeat=False)
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)




def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def _playPause():
    global anim, paused, played
    if paused:
        if played:
            anim.event_source.start()
            anim.frame_seq = anim.new_frame_seq() 
            played = False
        else:
            anim.resume()
    else:
        anim.pause()
    paused = not paused


def _reload():
    try:
        x_val = int(x.get())
        y_val = int(y.get())
        z_val = int(z.get())
        if(x_val < -360 or x_val > 360 or y_val < -360 or y_val > 360 or z_val < -360 or z_val > 360):
            raise TclError("Numbers not between -360 and 360")
        global animationRangeX 
        animationRangeX = np.linspace(start= 0, stop= x_val,num=np.abs(x_val) if x_val != 0 else 1) #So that the Animation still works when Angle is set to 0 --> Array with one 0 in it and len=1
        global animationRangeY 
        animationRangeY = np.linspace(start= 0, stop= y_val,num=np.abs(y_val) if y_val != 0 else 1) 
        global animationRangeZ 
        animationRangeZ = np.linspace(start= 0, stop= z_val,num=np.abs(z_val) if z_val != 0 else 1) 

        global lenX
        lenX = len(animationRangeX)
        global lenY
        lenY = len(animationRangeY)
        global lenZ
        lenZ = len(animationRangeZ)


        global played, paused, dropDownVar, orderRot, values, koerperCoordSys, coordSysVar
        played = False
        paused = False
        orderRot = values[dropDownVar.get()]
        koerperCoordSys = coordSysVar.get()
        anim.event_source.start()
        anim.frame_seq = anim.new_frame_seq() 



    except TclError as error:
        m_box.showerror(title='Input Error', message=error)

def _rotOrderChanged(input):
    global values, x_rot
    if values[input] == 7:
        x_rot.config(text="Z-Rot in °")
    else:
        x_rot.config(text="X-Rot in °")

# field options
options = {'padx': 5, 'pady': 5}

dropDownRahmen = Frame(master=root)
dropDownRahmen.pack(side=Tk.TOP, **options)

rot_order = Tk.Label(master = dropDownRahmen, text='Rot-Order: ')
rot_order.pack(side=Tk.LEFT)


values = {
    "X, Y, Z" : 1,
    "X, Z, Y" : 2,
    "Y, X, Z" : 3,
    "Y, Z, X" : 4,
    "Z, X, Y" : 5,
    "Z, Y, X" : 6,
    "Z, Y, Z" : 7
}

# for (text, value) in values.items(): 
# 	Tk.Radiobutton(master=radioButtonRahmen, text = text, variable = radioButtonVar, 
# 				value = value).pack(side = Tk.LEFT, ipady = 3) 
dropDownVar= Tk.StringVar(root, list(values.keys())[0]) #Variable that determins in what Order the Rotations should happen


dropDownMenu = Tk.OptionMenu(dropDownRahmen, dropDownVar,*values.keys(), command=_rotOrderChanged)
dropDownMenu.pack(side=Tk.LEFT, ipady=3)

coordSysVar = Tk.BooleanVar(root, value=False)
coordinate_system = Tk.Checkbutton(dropDownRahmen, text="Körperkoordinatensystem",variable=coordSysVar)
coordinate_system.pack(side=Tk.LEFT, ipady=3)
quit_button = Tk.Button(master=root, text='Quit', command=_quit)
quit_button.pack(side=Tk.BOTTOM, **options)

buttonRahmen = Frame(master=root)
buttonRahmen.pack(side=Tk.BOTTOM, **options)

setData_button = Tk.Button(master=buttonRahmen, text='Set Data', command=_reload)
setData_button.pack(side=Tk.LEFT, **options)
start_stop_button = Tk.Button(master=buttonRahmen, text='Play/Pause', command=_playPause)
start_stop_button.pack(side=Tk.LEFT, **options)




labelRahmen = Frame(master=root)
labelRahmen.pack(side=Tk.TOP, **options)

x = Tk.IntVar()
x.set('90')

x_rot = Tk.Label(master=labelRahmen, text='X-Rot in °')
x_rot.pack(side=Tk.LEFT, **options)

x_entry = Tk.Entry(master=labelRahmen, textvariable=x)
x_entry.pack(side=Tk.LEFT, **options)


y = Tk.IntVar()
y.set('-90')

y_rot = Tk.Label(master=labelRahmen, text='Y-Rot in °')
y_rot.pack(sid=Tk.LEFT, **options)

y_entry = Tk.Entry(master=labelRahmen, textvariable=y)
y_entry.pack(side=Tk.LEFT, **options)

z = Tk.IntVar()
z.set('90')

z_rot = Tk.Label(master=labelRahmen, text='Z-Rot in °')
z_rot.pack(sid=Tk.LEFT, **options)

z_entry = Tk.Entry(master=labelRahmen, textvariable=z)
z_entry.pack(side=Tk.LEFT, **options)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.