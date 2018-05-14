"""
Created on Apr 24, 2013

@author: Hans R Hammer
"""

import numpy
import math

from plotscripts.plotter.util.functions import axisDiv
from plotscripts.base.baseobject import BaseObject

import matplotlib.colors
import matplotlib.cm

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
        self.cmap = None

    def getColor(self, value):
        if math.isnan(value):
            return self.nanColor
        else :
            return numpy.round(numpy.array(self.cmap.to_rgba(value)[:-1]) * 255)

    def getTextColor(self, value):
        if value < self.fontMid:
            return self.fontColor[0]
        else :
            return self.fontColor[1]

    def getOverlayColor(self):
        return self.overlayColor

    def create(self, lvls, cmType=None):
        self.lvls = lvls
        self.numSteps = lvls.shape[0] - 1

        # assign new standard color map
        c_norm = matplotlib.colors.Normalize(vmin=lvls[0], vmax=lvls[-1])
        self.cmap = matplotlib.cm.ScalarMappable(norm=c_norm, cmap=matplotlib.cm.viridis)

        self.nanColor = numpy.array([255, 255, 255])

        # setting up colors for font
        self.fontColor  = [self.getColor(lvls[-1]), self.getColor(lvls[0])]
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
