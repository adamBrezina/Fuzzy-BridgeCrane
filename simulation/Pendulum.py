# -*- coding: utf-8 -*-

"""
 Realizes the simulation of a pendulum.

 Calculates the simulation in steps of about 10ms.
 (So we don't need the correct differential equations.)

 Beside the movement is also tries to model static and slipping friction.
 Both values are set to the same value and simply modeled as force against 
 the movement direction. If the friction force is larger then the driving 
 force (external or own mass in movement) the movement stops.

 Also contains some modifiable parameters.
"""
import math
import random


class Pendulum(object):
    """Simulation of a pendulum."""

    #: lower limit of velocity. Smaller values of velocity are considered as no movement.
    NO_MOVEMENT = 0.00001

    def __init__(self):
        """Initialize the simulation."""
        self.X = 0.0  #: position [m]
        self.dX_dT = 0.0 #: velocity [m/s]
        self.Phi = math.radians(270.0) #: angle [rad]
        self.dPhi_dT = 0.0 #: angle velocity [rad/s]

        self.a = 0.0 #: acceleration [m/s²]

        self.l = 1.0 #: length of pendulum [m]
        self.m = 1.0 #: mass of pendulum [kg]
        self.M_P = 0.1 #: friction of bearing of pendulum expressed as torque [kgm²/s²=Nm]
        self.a_W = 0.1 #: friction of car expressed as acceleration [m/s²]

        self.W = 1.0 #: gain for incoming acceleration value
        self.Z = 0.01 #: disturbance

        self.pendulum_moves = 0
        self.car_moves = 0


    def doStep(self,dT):
        """Do one step of time dT.
          If dT is too large it is subdivided in smaller steps."""
        n = 1
        dT_n = dT

        # dT is larger than 0.02 ?
        if dT/0.01 >= 2.0:
            # divide dT into smaller steps
            n = round(dT/0.01)
            dT_n = dT/float(n)

        for _ in range(n): # calculate steps
            self.doSmallStep(dT_n)

    def doSmallStep(self,dT):
        """Simulate a small step of not more than 0.02s."""

        while dT > 0.0:
            time_left = 0.0

            a = self.a * self.W # calculate used acceleration

            # XXX wiederanlauf
            if (self.car_moves==0) and (abs(a) > self.a_W):
                self.car_moves = 1
                if a > 0: self.dX_dT = +Pendulum.NO_MOVEMENT
                else:     self.dX_dT = -Pendulum.NO_MOVEMENT

            # XXX Reibung zu gross => Stop
            if (abs(self.dX_dT) < Pendulum.NO_MOVEMENT) and (abs(a) <= self.a_W):
                self.car_moves = 0
                self.dX_dT = 0.0
                a = 0.0

            # XXX Wirkungsrichtung Reibung ?
            if self.car_moves == 1:
                if self.dX_dT > 0: a = a - self.a_W
                else:              a = a + self.a_W

                if self.dX_dT * (self.dX_dT + a * dT) < 0.0: # XXX Nulldurchgang ?
                    # Zeiteinheit teilen
                    dT_ = - self.dX_dT/a
                    if abs(dT_) > 1.0E-5 and abs(dT-dT_) > 1.0E-5: 
                        time_left = dT - dT_ # XXX Restzeit
                        dT = dT_

            while dT > 0.0:
                time_left2 = 0.0

                M_D = self.l/2.0 * self.m * (
                        9.81 * -math.cos(self.Phi) # momentum of gravity
                      + a *  math.sin(self.Phi) # momentum of car movement
                      + (self.Z * random.gauss(0.0,1.0)) * math.sin(self.Phi) # disturbance
                      )

                if (self.pendulum_moves == 0) and (abs(M_D) > self.M_P):
                    # XXX Wiederanlauf
                    self.pendulum_moves = 1
                    if M_D > 0.0: self.dPhi_dT = +Pendulum.NO_MOVEMENT
                    else:       self.dPhi_dT = -Pendulum.NO_MOVEMENT
                if (abs(self.dPhi_dT) < Pendulum.NO_MOVEMENT) and (abs(M_D)<=self.M_P):
                    # XXX Reibung zu groß => Stop
                    self.pendulum_moves = 0
                    self.dPhi_dT = 0.0
                    M_D = 0.0

                # Reibung im Lager beachten 
                # Reibung verrechnen
                if self.pendulum_moves:
                    # Wirkrichtung Reibung ?
                    if self.dPhi_dT > 0: M_D = M_D - self.M_P
                    else:                M_D = M_D + self.M_P

                    d2Phi_dT2 = M_D/(4.0/3.0 * self.m * self.l*self.l/4.0) # inertia

                    if self.dPhi_dT * (self.dPhi_dT + d2Phi_dT2 * dT) < 0.0: # XXX Nulldurchgang ?
                        # Zeiteinheit teilen
                        dT_ = - self.dPhi_dT/d2Phi_dT2
                        if abs(dT_) > 1.0E-5 and abs(dT-dT_) > 1.0E-5: 
                            time_left2 = dT - dT_ # XXX Restzeit
                            dT = dT_

                    # XXX neuer Winkel 
                    self.Phi += self.dPhi_dT * dT + d2Phi_dT2 * dT*dT
                    while self.Phi < 0.0: self.Phi = self.Phi + 2.0*math.pi
                    while self.Phi >= 2.0*math.pi: self.Phi = self.Phi - 2.0*math.pi

                    # XXX neue Winkelgeschwindigkeit
                    self.dPhi_dT += d2Phi_dT2 * dT

                # new position
                self.X += self.dX_dT * dT + a*dT*dT

                # new speed
                self.dX_dT += a*dT

                dT = time_left2
            dT = time_left
