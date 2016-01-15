# -*- coding: utf-8 -*-

try:
    import Tkinter
except ImportError:
    import tkinter
    Tkinter = tkinter

class MainWindow(object):
    """Main window of application."""

    def __init__(self,system,controllers,processes):
        self.system = system
        self.root = Tkinter.Tk()
        self.root.title("Controller")
        self.root.minsize(400,200)

        self.controller_nr = Tkinter.IntVar(0)
        self.controllers = controllers
        def Controller_Changed(name,index,mode):
            self.Controller_Changed()
        self.controller_nr.trace_variable('w',Controller_Changed)

        self.process_nr = Tkinter.IntVar(0)
        self.processes = processes
        def Process_Changed(name,index,mode):
            self.Process_Changed()
        self.process_nr.trace_variable('w',Process_Changed)

        menubar = Tkinter.Menu(self.root)

        file_menu = Tkinter.Menu(menubar,tearoff=0)
        file_menu.add_command(label="Quit",underline=0,command=self.File_Quit,accelerator="Ctrl+Q")
        menubar.add_cascade(label="File",underline=0,menu=file_menu)
        self.root.bind('<Control-q>',self.File_Quit)

        self.run_menu = Tkinter.Menu(menubar,tearoff=0)
        self.run_menu.add_command(label="Start", command=self.Run_Start,accelerator="F5")
        self.run_menu.add_command(label="Step", command=self.Run_Step,accelerator="F11")
        self.run_menu.add_command(label="Stop", command=self.Run_Stop,accelerator="Shift+F5")
        menubar.add_cascade(label="Run",underline=0,menu=self.run_menu)
        self.root.bind('<F5>',self.Run_Start)
        self.root.bind('<F11>',self.Run_Step)
        self.root.bind('<Shift-F5>',self.Run_Stop)

        process_menu = Tkinter.Menu(menubar,tearoff=0)
        process_menu.add_command(label="View",underline=0, command=self.Process_View,accelerator="V")
        self.root.bind('<v>',self.Process_View)
        i = 0
        for process in processes:
            process_menu.add_separator()
            process_menu.add_radiobutton(label=process[0],underline=0, variable=self.process_nr,value=i)
            if process[2]:
                # needed to save the current value of process
                def Show(process=process):
                    process[2](process[1])
                process_menu.add_command(label="... Parameter",underline=4, command=Show)
            i = i + 1
        menubar.add_cascade(label="Process",underline=0,menu=process_menu)

        controller_menu = Tkinter.Menu(menubar,tearoff=0)
        i = 0
        for controller in controllers:
            controller_menu.add_radiobutton(label=controller[0],underline=0, variable=self.controller_nr,value=i)
            i = i + 1
        menubar.add_cascade(label="Controller",underline=0,menu=controller_menu)


        help_menu = Tkinter.Menu(menubar,tearoff=0)
        help_menu.add_command(label="About",underline=0, command=self.Help_About,accelerator="F1")
        menubar.add_cascade(label="Help",underline=0,menu=help_menu)
        self.root.bind('<F1>',self.Help_About)

        self.controller_nr.set(0)
        self.process_nr.set(0)

        self.root.config(menu=menubar)
        
        Tkinter.Label(self.root,text=
"""
The following keys are defined:

Ctrl+Q   Exit
V         Show visualization
F5        Start simulation
Shift+F5  Stop simulation
F11       Single step of simulation
""",justify=Tkinter.LEFT).pack()

        self.root.mainloop()

    # menu callbacks
    def File_Quit(self,event=None):
        self.root.quit()

    def Run_Start(self,event=None):
        self.system.start()

    def Run_Stop(self,event=None):
        self.system.stop()

    def Run_Step(self,event=None):
        self.system.step()

    def Process_View(self,event=None):
        import ProcessView
        ProcessView.Open(self.system)

    def Help_About(self,event=None):
        import About
        About.Open()

    def Controller_Changed(self):
        nr = self.controller_nr.get()
        print ("Set controller %d: %s %s" % (nr,self.controllers[nr][0],self.controllers[nr][1]))
        self.system.controller = self.controllers[nr][1]

    def Process_Changed(self):
        nr = self.process_nr.get()
        print ("Set process %d: %s %s" % (nr,self.processes[nr][0],self.processes[nr][1]))
        self.system.process = self.processes[nr][1]
