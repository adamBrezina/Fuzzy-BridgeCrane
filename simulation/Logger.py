# -*- coding: utf-8 -*-

import sys

class Logger(object):
    """A simple logging class. It just prints the values as table to stdout."""

    def __init__(self):
        self.__initialized = 0
        self.__inputs = []
        self.__outputs = []
        self.out = None

    def __init(self,inputs,outputs,out=sys.stdout):
        if self.__initialized == 0:
            self.__inputs = sorted(inputs)
            self.__outputs = sorted(outputs)
            self.__initialized = 1
        if not (self.out is out):
            self.out = out
            self.out.write("#%s\t%s\n" % ('\t'.join(self.__inputs),'\t'.join(self.__outputs)))

    def log(self,inputs,outputs,out=sys.stdout):
        self.__init(inputs,outputs,out)
        self.out.write("%s\t%s\n" % ('\t'.join([str(inputs[x]) for x in self.__inputs]),'\t'.join([str(outputs[x]) for x in self.__outputs])))
