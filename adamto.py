from visual import *
from visual.graph import *

from scipy.integrate import odeint
from fuzzy import *

from cart import *
from world import *

import fuzzy.storage.fcl.Reader
import numpy as np
import scipy as sp
import visual.controls as cntrl

global angles
global position
isPaused = False
isStarted = False


def uhol(y, x):
    y0 = y[0]
    y1 = y[1]
    y2 = (-a12/z)*y0 - Fk/mk
    return y1, y2

def poloha(y, x):
    global i
    i = 0
    x0 = y[0]
    x1 = y[1]
    x2 = (a11/z)*angles[i,0] + Fk/mk
    i = i + 1
    return x1, x2

def initSystem():
    global cart1,distance,l,mk,mg,s1,s2,s3,s4
    s1.value = 50
    s2.value = 50
    s3.value = 50
    s4.value = 50
    cart1.setPos(50/100 * 15 - 8)
    cart1.setLength(50/200*5+5)
    cart1.setCartMass(50/100)
    cart1.setMass(75/100 * 1.9 + 0.1)
    distance = s1.value/100 * 15 + 5
    l = s2.value/100 * 5 + 5
    mk = s3.value/100 * 850 + 150
    mg =  s4.value/1000 * 2500 + 500
    
def setStart():
    global isPaused, isStarted
    if not(isPaused):
        isStarted = True
    if isPaused:
        isPaused = False

def setReset():
    global isPaused,isStarted
    global a,b,x,Fk,init1,init2
    isPaused = False
    isStarted = False
    a = 0
    b = 0
    x = 0
    Fk = 0
    init1 = 0.0, 0.0
    init2 = 0.0, 0.0

def setPause():
    global isPaused
    isPaused = True

def setExit():
    exit()

# init parameters
mk = 150.0
mg = 500.0
l = 10
g = 9.81
a11 = mg / mk
a12 = 1 + mg / mk
z = l / g
dest = 3
lengthL = 2

# create fuzzy regulator
system = fuzzy.storage.fcl.Reader.Reader().load_from_file("modifiedRules.fcl")
#system = fuzzy.storage.fcl.Reader.Reader().load_from_file("diplomovkaRules.fcl")

#control window
c = cntrl.controls(x=0, y=600, width=920, height=210, background = color.black, range=60)

s1 = slider(pos=(-25,6), width=3, length=30, axis=(1,0,0), color = color.blue)
s2 = slider(pos=(-25,2), width=3, length=30, axis=(1,0,0), color = color.blue)
s3 = slider(pos=(-25,-2), width=3, length=30, axis=(1,0,0), color = color.blue)
s4 = slider(pos=(-25, -6), width=3, length=30, axis=(1,0,0), color = color.blue)

m1 = menu(pos=(-43,6), width=30, height=3, text = 'DESTINATION:')
m2 = menu(pos=(-43,2), width=30, height=3, text = 'ROPE LENGTH:')
m3 = menu(pos=(-43,-2), width=30, height=3, text = 'CART MASS:')
m4 = menu(pos=(-43,-6), width=30, height=3, text = 'LOAD MASS:')

bl = button(pos=(15,5), height=8, width=13, text='START', action=lambda: setStart())
b2 = button(pos=(15,-5), height=8, width=13, text='RESET', action=lambda: setReset())
b3 = button(pos=(30,5), height=8, width=13, text='PAUSE', action=lambda: setPause())
b4 = button(pos=(30,-5), height=8, width=13, text='EXIT', action=lambda: setExit())
#main scene
scene = display(title='Fuzzy GantryCrane Simulator',
x=0, y=0, width=920, height=600, center=(0,0,0), background=color.black)
scene.fov = 1.5


#create objects in scene
world1 = World()
cart1 = Cart()
cart1.setPos(-13)
cart1.setLength(l/2)

# set scene camera position
scene.forward = (10,-8,10)

# graph for position of cart
gd1 = gdisplay(x = 920, y = 0, width = 920, height = 270, 
title = 'Position of cart', xtitle = 'time',ytitle = 'position', ymax = 25)
f1 = gcurve(color = color.red)
f1a = gcurve(color = color.yellow)

# graph of angle of rope
gd2 = gdisplay(x = 920, y = 270, width = 920, height = 270,
title = 'Angle', xtitle = 'time',ytitle = 'angle(degrees)', ymax = 30, ymin = -30)
f2 = gcurve(color = color.cyan)

# graph for power output
gd3 = gdisplay(x = 920, y = 270*2, width = 920, height = 270,
title = 'Power for pushing the cart', xtitle = 'time',ytitle = 'Power')
f3 = gcurve(color = color.green)

while 1:
    # preallocate input and output values
    my_input = {
            "Range" : 0.0,
            "Speed" :0.0,
            "Alfa" : 0.0,
            "AngularVelocity" : 0.0
            }
    my_output = {
            "Power" : 0.0
            }

    initSystem()
    while isStarted == False:
        rate(20)
        #set graphic model
        cart1.setPos(s1.value/100 * 15 - 8)
        cart1.setLength(s2.value/200*5+5)
        cart1.setMass(s4.value/100 + 1)
        cart1.setCartMass(s3.value/80 + 0.2)
        #set physical model parameters   
        distance = s1.value/100 * 15 + 5
        l = s2.value/100 * 5 + 5
        mk = s3.value/100 * 850 + 150
        mg =  s4.value/1000 * 2500 + 500

    a = 0
    b = 0
    x = 0
    Fk = 0
    init1 = 0.0, 0.0
    init2 = 0.0, 0.0

    goback = 0
    while goback < distance:
        cart1.setPos(distance-goback-13)
        goback = goback + 0.2
        rate(20)

    while isStarted:
        rate(50)
        if not(isPaused):
            x = np.linspace(a, b, 2)

            a = b
            b = b + 0.025
            angles = odeint(uhol, init1, x)
            position = odeint(poloha, init2, x)
            init1 = angles[1, 0], angles[1, 1]
            init2 = position[1, 0], position[1, 1]

            #set cart position
            cart1.setPos(position[1, 0]-13)
            cart1.setRot(-angles[1, 0]);
            my_input = {
                    "Range" : distance - position[1,0],
                    "Speed" :position[1,1],
                    "Alfa" : angles[1,0],
                    "AngularVelocity" : angles[1,1]
            
                    }
            my_output = {
                    "Power" : Fk
                    }
            temp = angles[1,0]*180/3.14
            f2.plot(pos = (b,temp))
            f1.plot(pos = (b,position[1,0]))
            f1a.plot(pos = (b, distance))
            f3.plot(pos = (b,Fk))

            system.calculate(my_input, my_output)
           # if position[1,0] < KAM + 0.5 and position[1,0] > KAM - 0.5 : gain = 20
           # else : gain=2220
    
            Fk= my_output["Power"]*125

