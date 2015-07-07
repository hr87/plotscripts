"""
Created on Apr 23, 2013

@author: Hans R Hammer
"""

import numpy
import math

from plotscripts.geometry.hexagonal.hexagonal import Hexagonal

class Triangular(Hexagonal):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.triPoints      = None

        self.shuffleTris = False          # shuffle tris in different order
        # self.activateDefaults()

    def setupClassGeometry(self):
        super().setupClassGeometry()
        self.triPoints = self.calcTriPoints(self._hexPoints, self.pitch, self.shuffleTris)

    def getClassValuePoints(self):
        return self.triPoints

    def getClassValuePaths(self):
        # init array
        points = numpy.zeros((self._hexPoints.shape[0]*6, 2, 4))

        # corner number of tr in hex and tri keys
        keys = numpy.arange(0, self._hexPoints.shape[0]).repeat(6)

        # get hex corner points
        cornerPoints = Hexagonal.getClassValuePaths(self)

        # set start end point
        points[:, :, 0] = self._hexPoints[keys, :]
        points[:, :, 3] = self._hexPoints[keys, :]

        # get indices for tris
        indices = numpy.arange(self._hexPoints.shape[0]) * 6

        for idx in range(6) :
            if self.shuffleTris:
                points[indices + idx, :, 1] = cornerPoints[:, :, self.shuffleTris[idx]]
                points[indices + idx, :, 2] = cornerPoints[:, :, (self.shuffleTris[idx]+1)%6]
            else:
                points[indices + idx, :, 1] = cornerPoints[:, :, idx]
                points[indices + idx, :, 2] = cornerPoints[:, :, (idx+1)%6]

        return points

    def getClassTextPoints(self):
        return Triangular.getClassValuePoints(self)

    def getClassPathTypes(self):
        return ['path'] * self.triPoints.shape[0]

    def getClassOverlayTypes(self):
        return ['path'] * self._hexPoints.shape[0]

    def calcTriPoints(self, hexPoints, pitch, shuffle = False):
        self.out('Calculating points')

        # prepare tri point array
        triPoints = numpy.zeros((6, 2))

        angles = numpy.linspace(1.0/6.0*math.pi, 11.0/6.0*math.pi, 6, True)

        # shuffle tris
        if shuffle:
            angles[:] = angles[shuffle]

        triPoints[:, 0] = numpy.cos(angles)
        triPoints[:, 1] = numpy.sin(angles)

        triPoints *= pitch/3.0
        triPoints  = numpy.tile(triPoints, (hexPoints.shape[0], 1))

        keys = numpy.arange(0, hexPoints.shape[0]).repeat(6)

        triPoints += hexPoints[keys, :]

        return triPoints

    def checkInput(self):
        super().checkInput()

        if self.shuffleTris:
            if len(self.shuffleTris) != 6:
                raise self.exception('Shuffling list not correct')
