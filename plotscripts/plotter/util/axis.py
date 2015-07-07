"""
Created on Apr 24, 2013

@author: Hans R Hammer
"""

import math
import numpy

from plotscripts.plotter.util.functions import axisDiv
from plotscripts.base.baseobject import BaseObject

class Axis(BaseObject):
    """
    Class providing an axis
    """

    def __init__(self, size, start, end, tic_length, swap = False):
        """
        Constructor
        """
        super().__init__()

        self.size = size
        self.start      = start
        self.end        = end
        self.length     = self.end - self.start
        self.mid        = self.length / 2.0 + self.start
        self.tic_length = tic_length

        self.swap = swap

    def setAxis(self, minValue, maxValue):
        self.min = minValue
        self.max = maxValue

        # getting some stuff
        self.range  = self.max - self.min                           # value range on axis

        # test for negative values
        self.mag    = 10 ** (math.floor(math.log10(self.range)))    # magnitude of axis values
        self.mag    = 10 ** (math.floor(math.log10(self.range)))    # magnitude of axis values
        self.div    = axisDiv(self.range, self.mag)            # divider for axis

        # rescale values to rounded values
        self.mag    = self.mag / self.div
        self.max    = math.ceil(self.max / self.mag) * self.mag
        self.min    = math.floor(self.min / self.mag) * self.mag
        self.range  = self.max - self.min

        self.num    = self.range / self.mag + 1                     # number of tics
        self.tics   = numpy.linspace(self.min, self.max, self.num,)   # vector with tic values
        self.ticPos = (self.length / self.range) * (self.tics - self.min) + self.start

        self.zero   = self.start + (self.end - self.start) / (self.max - self.min) * (- self.min)

    def convertPoints(self, points):
        # swap axis?
        if self.swap:
            points = -(points - (self.max + self.min) / 2 ) + (self.max + self.min) / 2

        points = (points * self.length / self.range + self.zero) * self.size

        return points

    def getStart(self):
        return self.start * self.size

    def getEnd(self):
        return self.end * self.size

    def getTics(self):
        if self.swap:
            return self.tics[::-1]

        return self.tics

    def getTicPos(self):
        return self.ticPos * self.size

    def getFactor(self):
        return (self.length * self.size) / self.range