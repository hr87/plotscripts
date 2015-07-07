"""
Created on May 5, 2013

@author: hr87
"""

import numpy

from plotscripts.geometry.hexagonal.hexagonal import Hexagonal

class HexagonalThird(Hexagonal):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

    def setupClassGeometry(self):
        super().setupClassGeometry()

        idxStart = 0
        selection = []

        # calc selection list
        for idxRing in range(self.ringStart, self.ringEnd):
            tmp = numpy.arange(2*idxRing) + idxStart
            # increase the index of the starting block for next ring
            if idxRing == 0:
                idxStart = 1
                tmp = numpy.array([0])
            else:
                idxStart += idxRing * 6

            selection.extend(tmp.tolist())

        # select third hex points
        #selection = list(range(0, 90))
        self._hexPoints = self._hexPoints[selection, :]
