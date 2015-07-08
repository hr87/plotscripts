"""
Created on Jun 26, 2013

@author: Hans R Hammer
"""

from plotscripts.geometry.hexagonal.hexagonalthird import HexagonalThird
from plotscripts.geometry.hexagonal.triangular import Triangular

class TriangularThird(Triangular, HexagonalThird):
    """ Provides a third hexagonal core with triangles """

    def __init__(self):
        """ Constructor """
        super().__init__()

    def setupClassGeometry(self):
        """ Set up the geometry for this object

        :return: None
        """
        HexagonalThird.setupClassGeometry(self)
        self._triPoints = self.calcTriPoints(self._hexPoints, self.pitch, self.shuffleTris)
