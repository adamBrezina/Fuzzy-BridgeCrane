# -*- coding: utf-8 -*-

class Process(object):
    """Base class for any kind of process"""

    def __init__(self):
        pass

    def getStateValues(self,dict):
        pass

    def setControlValues(self,dict):
        pass

    def getDefaultControlValues(self):
        pass
