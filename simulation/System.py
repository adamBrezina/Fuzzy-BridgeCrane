# -*- coding: utf-8 -*-

"""Models the whole thing.
    Process, controller and a main loop."""

import threading
import time
import logging

class System(object):
    """
    Manages the whole system.
    
    process is the current controlled process.
    controller is the current controller.
    
    The whole system is executed in a separate thread.
    The timer is also realized as separate thread.
    """

    def __init__(self,stepsize=0.01,process=None,controller=None,logger=None):
        self.process = process #: process to control
        self.controller = controller #: controller for calculating control values
        self.logger = logger #: logging instance
        self.stepsize = stepsize #: step size of loop for simulations in seconds
        self.run = 0 #: main loop in in continuous run mode
        self.run_event = threading.Event() #: controls the main loop's turn (if set make another turn)
        self.main_thread = threading.Thread(target=self.main_loop) #: the main loop thread
        self.main_thread.setDaemon(1)
        self.main_thread.start()
        self.timer_event = threading.Event() #: periodic trigger for main loop
        self.timer_thread = threading.Thread(target=self.timer_loop) #: calculation time independent periodic trigger generator
        self.timer_thread.setDaemon(1)
        self.timer_thread.start()

    def main_loop(self):
        """Realize main control loop as separate thread, so it can be
           running independently of the GUI timers"""
        while 1:
            self.run_event.wait() # wait for start impulse
            if not self.run: # if only a step reset start impulse
                self.run_event.clear()
            try:
                if self.process:
                    input = self.process.getStateValues()
                    output = self.process.getDefaultControlValues()
                    t0 = time.time()
                    if self.controller:
                        self.controller.calculate(input,output)
                    t1 = time.time()
                    self.process.doStep(self.stepsize)
                    t2 = time.time()
                    self.process.setControlValues(output)
                    if self.logger:
                        self.logger.log(input,output)
                    logging.warn("Time for controller %fms, Time for process %fms",(t1-t0)*1000,(t2-t1)*1000)
                else:
                    self.run = 0
                    self.run_event.clear()
            except:
                self.run = 0
                self.run_event.clear()
                import traceback
                traceback.print_exc()

            # if run mode and is simulated, wait for next activation
            if self.run:# and not self.process.no_timer: 
                self.timer_event.wait()
                self.timer_event.clear()

    def timer_loop(self):
        """Realize a timer, using sleep is usually more precise
           than using the GUI timer"""
        while 1:
            self.run_event.wait() # only when running
            time.sleep(self.stepsize) # wait until next impulse 
            self.timer_event.set() # activate timer impulse

    def start(self):
        """Start the main loop."""
        self.run = 1
        self.run_event.set()

    def stop(self):
        """Stop the main loop."""
        self.run = 0
        self.run_event.clear()

    def step(self):
        """Make a single step of the main loop. ( = stop after one step)"""
        self.run = 0
        self.run_event.set()
