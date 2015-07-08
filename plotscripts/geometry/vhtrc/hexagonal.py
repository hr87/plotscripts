"""
Created on May 12, 2013

@author: Hans R Hammer

Geometry module for the vhtrc benchmark
"""

from ..hexagonal.hexagonal import Hexagonal


import math as _math
import numpy
import math


class VHTRCHexagonal(Hexagonal):
    """ Geometry class for VHTRC core """

    # a few constants for the vhtrc geometry
    outerHexPitch  = 2400.8

    blockTypes     = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                      1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 3, 2, 2, 2, 4,
                      2, 2, 2, 5, 2, 2, 2, 6, 2, 2, 2, 7, 2, 2, 2, 8, 2, 2, 2, 3, 4,
                      4, 5, 5, 6, 6, 7, 7, 8, 8, 3]

    cornerBlocks   = [2, 3, 7, 8, 12, 13, 17, 18, 22, 23, 27, 28]

    boundaryBlocks = [[37, 38, 60, 61, 72],
                      [40, 41, 42, 62, 63],
                      [44, 45, 46, 64, 65],
                      [48, 49, 50, 66, 67],
                      [52, 53, 54, 68, 69],
                      [56, 57, 58, 70, 71]]

    halfBlocks     = [37, 41, 45, 49, 53, 57, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]

    # calculating geometry vars
    numBlocks      = len(blockTypes)
    blockHexPitch  = outerHexPitch / 8
    blockHexRadius = blockHexPitch / _math.sqrt(3)
    triRadius = blockHexRadius * _math.sqrt(3) / 3

    def __init__(self):
        super().__init__()

        self.ringEnd = 4
        self.ringStart = 0
        self.pitch = self.blockHexPitch

    def setupClassGeometry(self):
        # create points
        self._hexPoints = numpy.zeros((73, 2))
        # normal rings
        self._hexPoints[0:61, :]    = self.calcHexPoints(self.pitch, self.ringEnd, self.ringStart)
        # corner ring
        self._hexPoints[61:73, :]   = self.calcHexPoints(self.pitch, self.ringEnd+1, self.ringEnd+1)[self.cornerBlocks]

    def getClassValuePaths(self):
        # get hexagonal path
        paths = Hexagonal.getClassValuePaths(self)

        # calc inner and outer radius
        r = self.pitch / 2.0
        a = 2.0 / numpy.sqrt(3) * r

        # prepare array
        points = numpy.zeros((2, 7))

        # calc corner  points of hex
        angles = numpy.linspace(0, 2.0*math.pi, 7, True)
        points[0, :] = numpy.cos(angles) * a
        points[1, :] = numpy.sin(angles) * a

        # change half block paths
        # get side and boundary blocks for side
        for idxSide, side in enumerate(self.boundaryBlocks):
            # get block
            for block in side:
                # check if we
                if not block in self.halfBlocks:
                    continue

                # create array
                tmpPoints = numpy.zeros((2, 7))

                # get points for four path thing
                for idx in range(4):
                    # assign corner point
                    tmpPoints[:, idx] = points[:, (idxSide+idx+2)%6] + self._hexPoints[block, :]

                # assign last point
                tmpPoints[:, 4] = points[:, (idxSide+2)%6] + self._hexPoints[block, :]
                # setting remaining point to NaN
                tmpPoints[:, 5:7] = float('NaN')

                # replace block path
                paths[block, :, :] = tmpPoints

        return paths.copy()
