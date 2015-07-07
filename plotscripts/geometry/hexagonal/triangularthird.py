"""
Created on Jun 26, 2013

@author: Hans R Hammer
"""

from plotscripts.geometry.hexagonal.hexagonalthird import HexagonalThird
from plotscripts.geometry.hexagonal.triangular import Triangular

class TriangularThird(Triangular, HexagonalThird):
    """

    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()

    def setupClassGeometry(self):
        """

        :return: None
        """
        HexagonalThird.setupClassGeometry(self)
        self.triPoints = self.calcTriPoints(self._hexPoints, self.pitch, self.shuffleTris)
