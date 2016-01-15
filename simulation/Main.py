#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main entry point. Starts the application."""

import sys

class Main(object):

    def usage(self):
        """Print usage information."""
        print (""" 
usage:
    %(name)s                       - start gui
    %(name)s doc nr                - generate docs for controller nr (variables/adjectives)
    %(name)s dot nr                - generate docs for controller nr (rules)
    %(name)s run nr1 nr2 [seconds] - run system with controller nr1 and process nr2 
                                     for certain time or forever
    """ % {"name":sys.argv[0]})

    def getControllers(self):
        """Get list with available controllers."""
        return \
        [ # available controllers
        ]

    def getProcesses(self):
        """Get list with available processes."""
        return \
        [ # available processes
        ]


    def make_doc(self,i):
        self.controllers[i][1].createDoc("../doc/%s" % self.controllers[i][0].lower())

    def make_dot(self,i):
        self.controllers[i][1].createDot("../doc/%s" % self.controllers[i][0].lower())

    def run_system(self,process,controller,t=None):
        self.system.controller = controller
        self.system.process = process
        import time
        self.system.start()
        sys.stderr.write("Started (%s) ...\n" % time.asctime())
        try:
            if t is not None:
                time.sleep(t) 
            else:
                while 1:
                    time.sleep(1)
        except KeyboardInterrupt:
            pass
        self.system.stop()
        sys.stderr.write("Stopped (%s).\n"  % time.asctime())
        plotxxx(self.system.controller)

    def start_gui(self):
        from simulation import MainWindow
        MainWindow.MainWindow(self.system,self.controllers,self.processes)

    def __init__(self):
        from simulation import System
        from simulation import Logger
        self.system = System.System()
        self.system.logger = Logger.Logger()
        self.controllers = self.getControllers()
        self.processes = self.getProcesses()

    def run(self):
        if len(sys.argv) > 1:
            # check if we want only generate docs
            if "doc" == sys.argv[1] and len(sys.argv) > 2:
                self.make_doc(int(sys.argv[2]))
            elif "dot" == sys.argv[1] and len(sys.argv) > 2:
                self.make_dot(int(sys.argv[2]))
            elif "run" == sys.argv[1] and len(sys.argv) > 3:
                t = None
                if len(sys.argv) > 4:
                    t = float(sys.argv[4])
                self.run_system(self.processes[int(sys.argv[3])][1],self.controllers[int(sys.argv[2])][1],t)
            else:
                self.usage()
        else: # no docs,... => start gui
            self.start_gui()

def plotxxx(controller):
    from fuzzy.doc.plot.gnuplot import doc
    from fuzzy.OutputVariable import OutputVariable
    directory = "../doc/fuzzy"
    d = doc.Doc(directory)
    for name,v in controller.system.variables.items():
        if isinstance(v, OutputVariable):
            d.createDocSets(v.defuzzify.activated_sets,name+"_activated_sets")
            d.createDocSets({"accumulate":v.defuzzify.accumulated_set},name+"_accumulate")
