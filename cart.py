from visual import *
from visual.graph import *
from visual.controls import *


class Cart:
    
    
    x = 0
    rotation = 0
    a = None
    line = None
    load = None
    wheel1 = None
    wheel4 = None
    wheel3 = None
    wheel2 = None
    weight = None
    cartLine = None
    mass = 2.0
    length = 4.0
    cartMass = 1.0
    

    def __init__(self):
    
        self.a = box(size=(1.9,0.1,0.8), pos=(0,10.2,0), color=color.orange)
        self.line = cylinder(axis=(0,self.length/2,0), radius = 0.035, pos=(0,10.15,0), color=color.red)
        self.line.rotate(angle=self.rotation, axis=(0,0,1), origin=(0,10.15,0))
        self.wheel1 = cylinder(axis=(0.1,0,0), radius = 0.2, pos=(-1.05, 10.225, 0.4), color=color.orange)
        self.wheel2 = cylinder(axis=(0.1,0,0), radius = 0.2, pos=(0.95, 10.225, 0.4), color=color.orange)
        self.wheel3 = cylinder(axis=(0.1,0,0), radius = 0.2, pos=(-1.05, 10.225, -0.4), color=color.orange)
        self.wheel4 = cylinder(axis=(0.1,0,0), radius = 0.2, pos=(0.95, 10.225, -0.4), color=color.orange)

        self.load = box(size=(self.mass, self.mass, self.mass), pos=(0, 10 - self.length,0), color=color.green)
        self.weight = cylinder(axis=(0,self.cartMass,0), radius = 0.5, pos=(0,10.25,0), color=color.green)
        self.cartLine = cylinder(axis=(0,1.2,0), radius = 0.08, pos=(0,10.25,0), color=color.orange)
    def setPos(self,y):
        self.x = y
        self.a.pos = vector (0,10.2,self.x)
        
        self.wheel1.pos = vector (-1.05, 10.225, 0.4 + self.x)
        self.wheel2.pos = vector (0.95, 10.225, 0.4 + self.x)
        self.wheel3.pos = vector (-1.05, 10.225, -0.4 + self.x)
        self.wheel4.pos = vector (0.95, 10.225, -0.4 + self.x)
        self.line.pos = vector (0,10.15,self.x)
        self.load.pos = vector(0, 10 - self.length * cos(self.rotation),self.x - self.length * sin(self.rotation))
        self.weight.pos = vector(0,10.25,self.x)
        self.cartLine.pos = vector(0, 10.25, self.x)

    def getPos(self):
        return(self.x)

    
    def setRot(self,alfa):
        self.line.rotate(angle=alfa-self.rotation, axis=(1,0,0), origin=(0,10.15,self.x))
        self.load.rotate(angle=(alfa-self.rotation), axis=(1,0,0), origin=(0,10.15,self.x))
        self.rotation = alfa
        
    def setLength(self,x):
        self.length = x
        self.line.axis = (0,-self.length,0)

    def setMass(self,mass):
        self.mass = mass
        self.load.length = self.mass
        self.load.height = self.mass
        self.load.width = self.mass
        print self.mass, mass

    def setCartMass(self, mass):
        self.cartMass = mass/1.6
        self.weight.axis = (0,self.cartMass,0)
   