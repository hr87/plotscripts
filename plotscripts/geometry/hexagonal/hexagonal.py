"""
Created on Apr 22, 2013

@author: Hans R Hammer
"""

import numpy
import math

from plotscripts.geometry.basegeometry import BaseGeometry

class Hexagonal(BaseGeometry):
    """
    Provides a hexagonal geometry. The numbering of the sections is starting
    at the center and going then mathematical outwards.
    :var ringStart: Start ring, default = 0
    :var ringEnd: End Ring
    :var pitch: Pitch of one hexagon
    
    """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.ringStart      = 0         # start ring 0 = center block
        self.ringEnd        = None      # end rings
        self.pitch          = None      # block pitch

        # internal
        self._calculated     = False     # flag if points are already calculated
        self._hexPoints      = None      # hex center points

    def setupClassGeometry(self):
        self._hexPoints = self.calcHexPoints(self.pitch, self.ringEnd, self.ringStart)

    def getClassValuePoints(self):
        return self._hexPoints

    def getClassValuePaths(self) :
        # calc inner and outer radius
        r = self.pitch / 2.0
        a = 2.0 / numpy.sqrt(3) * r

        # prepare array
        points = numpy.zeros((1, 2, 7))

        # calc corner  points of hex
        angles = numpy.linspace(0, 2.0*math.pi, 7, True)
        points[0, 0, :] = numpy.cos(angles) * a
        points[0, 1, :] = numpy.sin(angles) * a

        # get value points
        tmp = self._hexPoints[:, :, numpy.newaxis].repeat(7, 2)
        # resize array to all hex points
        points = points.repeat(tmp.shape[0], 0)
        # translate all corner points
        points += tmp

        return points

    def getClassOverlayPaths(self):
        return Hexagonal.getClassValuePaths(self)

    def getClassTextPoints(self):
        return Hexagonal.getClassValuePoints(self)

    def getClassPathTypes(self):
        return ['path'] * self._hexPoints.shape[0]

    def getClassOverlayTypes(self):
        return ['path'] * self._hexPoints.shape[0]

    def calcHexPoints(self, pitch, ringEnd, ringStart = 0, rotate = False):
        """ calculating center points of an hexagonal grid
        :param pitch: block pitch
        :param ringEnd: number of final ring
        :param ringStart: number of first ring
        :param rotate: rotate core for 30 degrees
        :return: ndarray with center points
        """
        self._debug('Calculating points')

        # calc inner and outer radius
        r = pitch / 2.0
        a = 2.0 / numpy.sqrt(3) * r

        # calc number of points
        numPoints = 3 * ringEnd**2 + 3 * ringEnd + 1

        # see if we have a hole
        if (ringStart != 0) :
            missingPoints = 3 * (ringStart - 1)**2 + 3 * (ringStart - 1) + 1
            numPoints -= missingPoints
            idx = 0
            start = ringStart
        else :
            idx = 1
            start = 1

        # init matrix
        hexPoints = numpy.zeros((numPoints, 2))

        for ring in range(start, ringEnd + 1) :
            pos = numpy.arange(0, ring)

            # seems to work, but how
            hexPoints[idx: idx + ring,:] = numpy.array([ring - pos, ring + pos]).T
            idx += ring
            hexPoints[idx: idx + ring,:] =  numpy.array([-pos, 2*ring - pos]).T
            idx += ring
            hexPoints[idx: idx + ring,:] =  numpy.array([-ring*numpy.ones(ring), ring - 2*pos]).T
            idx += ring
            hexPoints[idx: idx + ring,:] =  numpy.array([-ring + pos, -ring - pos]).T
            idx += ring
            hexPoints[idx: idx + ring,:] =  numpy.array([pos, -2*ring + pos]).T
            idx += ring
            hexPoints[idx: idx + ring,:] =  numpy.array([ring*numpy.ones(ring), -ring + 2*pos]).T
            idx += ring

        # scale point matrix
        hexPoints[:, 0] = hexPoints[:, 0] * 1.5 * a
        hexPoints[:, 1] = hexPoints[:, 1] * r

        # rotate by 30 degree
        if rotate:
            alpha = math.pi / 6
            # create rotation matrix
            rot = numpy.array([[math.cos(alpha), math.sin(alpha)],
                               [-math.sin(alpha), math.cos(alpha)]])

            hexPoints = hexPoints.dot(rot)

        return hexPoints

    def _checkInput(self):
        BaseGeometry._checkInput(self)

        if self.ringEnd is None:
            raise self._exception('No end ring number')

        if self.pitch is None :
            raise self._exception('No pitch')
