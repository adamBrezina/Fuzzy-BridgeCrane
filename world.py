from visual import *

class World:

    pillar1 = None
    floor = None
    rail1 = None
    rail2 = None

    rail1a = None
    rail2a = None

    def __init__(self):
        #floor
        self.floor = box(size=(25,0.1,40), pos = (0,-0.05,0), color=color.white)

        #static bridge crane
        self.pillar1 = box(size = (0.3,10,1), pos = (-1.05,5,14.5),material=materials.rough, color=color.blue)
        self.pillar1 = box(size = (0.3,10,1), pos = (-1.05,5,-14.5),material=materials.rough, color=color.blue)
        self.pillar1 = box(size = (0.3,10,1), pos = (1.05,5,14.5),material=materials.rough, color=color.blue)
        self.pillar1 = box(size = (0.3,10,1), pos = (1.05,5,-14.5),material=materials.rough, color=color.blue)

        self.rail1 = box(size=(0.3,0.01,30), pos = (-1.05, 10.01, 0), material=materials.silver)
        self.rail2 = box(size=(0.3,0.01,30), pos = (1.050, 10.010, 0), material=materials.silver)

        self.rail1a = box(size=(0.3,0.3,30), pos = (-1.05, 9.85, 0), material=materials.rough, color=color.blue)
        self.rail2a = box(size=(0.3,0.3,30), pos = (1.05, 9.85, 0), material=materials.rough, color=color.blue)








