"""
Created on Apr 24, 2013

@author: Hans R Hammer
"""

import numpy
import math

from plotscripts.plotter.util.functions import axisDiv
from plotscripts.base.baseobject import BaseObject

class Colormap(BaseObject):
    """
    Class for creating a colormap
    """

    colors          = None      # numpy array with self.colors

    def __init__(self, cmType = 'hsv'):
        """
        Constructor
        """
        super().__init__()
        self.type = cmType.lower()

    def getColor(self, value):
        if math.isnan(value):
            return self.nanColor
        else :
            idx = self.lvls.searchsorted(value) - 1
            if(idx < 0):
                idx = 0
            try:
                return self.colors[idx, :]
            except IndexError as e:
                raise self.exception('Linking value {0} to color failed'.format(value)) from e

    def getTextColor(self, value):
        if value < self.fontMid:
            return self.fontColor[0]
        else :
            return self.fontColor[1]

    def getOverlayColor(self):
        return self.overlayColor

    def create(self, lvl, cmType = None):
        # assign new standard color map
        if not cmType == None :
            self.type = cmType.lower()

        if self.type == 'hsv':
            self.createHSV(lvl)
        else :
            raise self.exception('Color map type unknown')

    def createHSV(self, lvls):
        self.lvls = lvls
        self.numSteps = lvls.shape[0] - 1

        # calc http://en.wikipedia.org/wiki/HSL_and_HSV#From_HSV
        v = 1
        s = 1

        h = 360.0 / (lvls[-1] - lvls[0]) * lvls[0:-1] / 60.0
        h -= h[1]        # shift first value to 0
        c = v * s
        x = c * (1-numpy.absolute( (h-1) % 2 - 1))

        self.colors = numpy.zeros((self.numSteps, 3))

        for idx in range(self.numSteps):
            if h[idx] <= 1 :                      # dark blue
                self.colors[idx, :] = numpy.array([0, 0, (1.0 - x[idx]) / 2.0 + 0.5])
            elif h[idx] <= 2 :                 # blue
                self.colors[idx, :] = numpy.array([0, x[idx], c])
            elif h[idx] <= 3 :                  # green
                self.colors[idx, :] = numpy.array([0, c, x[idx]])
            elif h[idx] <= 4 :                  # yellow
                self.colors[idx, :] = numpy.array([x[idx], c, 0])
            elif h[idx] <= 5 :                  # red
                self.colors[idx, :] = numpy.array([c, x[idx], 0])
            else :                                 # dark red
                self.colors[idx, :] = numpy.array([(1.0 - x[idx]) / 2.0 + 0.5, 0, 0])

        # last step and scale to 0,255
        self.colors += (v - c);
        self.colors *= 255;

        self.nanColor = numpy.array([255, 255, 255])

        # setting up colors for font
        self.fontColor  = [[255, 0, 0], [0, 0, 0]]
        self.fontMid    = lvls[round((self.numSteps + 1.0) / 2.0)]

        # setting overlay color
        self.overlayColor   = numpy.array([255, 255, 255])

    def setupGeometry(self, upLeft, downRight, ticLength, vertical = True):
        self.xStart     = upLeft[0]
        self.xEnd       = downRight[0]
        self.yStart     = upLeft[1]
        self.yEnd       = downRight[1]
        self.xLength    = self.xStart - self.xEnd
        self.yLength    = self.yStart - self.yEnd

        self.ticLength  = ticLength
        self.range      = self.lvls.max() - self.lvls.min()
        self.mag        = 10 ** (math.floor(math.log10(self.range)))
        self.div        = axisDiv(self.range, self.mag)
        self.numLabels  = math.floor(self.range / self.mag * self.div)
        self.labels     = numpy.linspace(self.lvls.min(), self.lvls.max(), self.numLabels + 1, True);

        if vertical:
            self.height     = self.yLength / self.numSteps
            self.positions  = numpy.linspace(self.yStart, self.yEnd, self.numSteps + 1)
            self.legendPos  = numpy.linspace(self.yStart, self.yEnd, self.numLabels + 1);

        else:
            self.height     = self.xLength / self.numSteps
            self.positions  = numpy.linspace(self.xStart, self.xEnd, self.numSteps + 1)
            self.legendPos  = numpy.linspace(self.xStart, self.xEnd, self.Labels + 1)
