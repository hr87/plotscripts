"""
Created on May 12, 2013

@author: Hans R Hammer
"""

from ..basexygeometry import BaseXYGeometry as _BaseXYGeometry
from .hexagonal import Hexagonal as _Hexagonal


class HexagonalXY(_BaseXYGeometry, _Hexagonal):
    """ Creates a hexagonal geometry with xy points from a file for center points """

    def __init__(self):
        """ Constructor """
        super().__init__(self)

    def setupClassGeometry(self):
        self.readPoints(self.fileName)

    def getClassValuePaths(self):
        _Hexagonal.getClassValuePaths(self)

    def getClassOverlayPaths(self):
        _Hexagonal.getClassOverlayPaths(self)

    def getClassTextPoints(self):
        _Hexagonal.getClassTextPoints(self)

    def getClassValuePoints(self):
        _Hexagonal.getClassValuePoints(self)

    def getClassPathTypes(self):
        _Hexagonal.getClassPathTypes(self)

    def getClassOverlayTypes(self):
        _Hexagonal.getClassOverlayTypes(self)

    def _checkInput(self):
        super()._checkInput(self)
