'''
Created on Aug 18, 2013

@author: Hans R Hammer
'''

import math
import numpy
from plotscripts.geometry.basegeometry import BaseGeometry


class Rectangular(BaseGeometry):

    def __init__(self):
        super().__init__()

        self.pitch     = None   # pitch, single value or list with [x, y] pitch
        self.numBlocks = None   # number of block, single value or list with [x, y] num

        self._defaults['centered'] = True    # flag if geometry centered to 0,0 or left lower corner

        # internal
        self.centerPoints = None

    def setupClassGeometry(self):
        self.centerPoints = self.calcCenterPoints(self.pitch, self.numBlocks, self._options['centered'])

    def calcCenterPoints(self, pitch, numBlocks, centered = True):
        centerPoints = numpy.zeros((numBlocks[0] * numBlocks[1], 2))

        # some math to create center points
        if math.floor(numBlocks[0] / 2.0) == numBlocks[0] / 2.0:
            offsetX = 0.5
        else:
            offsetX = 0.0
        if math.floor(numBlocks[1] / 2.0) == numBlocks[1] / 2.0:
            offsetY = 0.5
        else:
            offsetY = 0.0

        # start y at the top
        if centered:
            y = - pitch[1] * (math.floor(numBlocks[1]/2.0) - offsetY)
        else:
            y = 0

        # iterate over all positions and create center points
        for idxY in range(numBlocks[1]):
            # restart x in on left
            if centered:
                x = -pitch[0] * (math.floor(numBlocks[0]/2.0) - offsetX)
            else:
                x = 0

            for idxX in range(numBlocks[0]):
                # assign point to array
                centerPoints[(idxX + idxY * numBlocks[0]), :] = numpy.array((x, y))
                # decrease x with pith
                x += pitch[0]

            # increase y with pitch
            y += pitch[1]

        return centerPoints

    def getClassValuePaths(self):
        paths = numpy.zeros((self.centerPoints.shape[0], 2, 5))

        # that's easy
        for idx in range(self.centerPoints.shape[0]):
            paths[idx, 0, 0] = self.centerPoints[idx, 0] - 0.5 * self.pitch[0]
            paths[idx, 1, 0] = self.centerPoints[idx, 1] - 0.5 * self.pitch[1]

            paths[idx, 0, 1] = self.centerPoints[idx, 0] + 0.5 * self.pitch[0]
            paths[idx, 1, 1] = self.centerPoints[idx, 1] - 0.5 * self.pitch[1]

            paths[idx, 0, 2] = self.centerPoints[idx, 0] + 0.5 * self.pitch[0]
            paths[idx, 1, 2] = self.centerPoints[idx, 1] + 0.5 * self.pitch[1]

            paths[idx, 0, 3] = self.centerPoints[idx, 0] - 0.5 * self.pitch[0]
            paths[idx, 1, 3] = self.centerPoints[idx, 1] + 0.5 * self.pitch[1]

            paths[idx, 0, 4] = paths[idx, 0, 0]
            paths[idx, 1, 4] = paths[idx, 1, 0]

        return paths

    def getClassOverlayPaths(self):
        return Rectangular.getClassValuePaths(self)

    def getClassValuePoints(self):
        return self.centerPoints

    def getClassTextPoints(self):
        return Rectangular.getClassValuePoints(self)

    def getClassPathTypes(self):
        return ['path'] * self.centerPoints.shape[0]

    def getClassOverlayTypes(self):
        return ['path'] * self.centerPoints.shape[0]

    def _checkInput(self):
        super()._checkInput()
        if self.pitch is None:
            raise self._exception('No pitch provided')
        if self.pitch.__class__ != list:
            self.pitch = [self.pitch, self.pitch]
        else:
            if len(self.pitch) != 2:
                raise self._error('Pitch must be a list of 2 elements')

        if self.numBlocks is None:
            raise self._exception('Number of blocks missing')
        if self.numBlocks.__class__ != list:
            self.numBlocks = [self.numBlocks, self.numBlocks]
        else:
            if len(self.numBlocks) != 2:
                raise self._error('Pitch must be a list of 2 elements')