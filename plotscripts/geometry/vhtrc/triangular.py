"""
Created on May 18, 2013

@author: hr87
"""

from plotscripts.geometry.vhtrc.hexagonal import VHTRCHexagonal
from plotscripts.geometry.hexagonal.triangular import Triangular

class VHTRCTriangular(VHTRCHexagonal, Triangular):
    """
    classdoc
    """
    halfTris       = [[2, 3, 4],
                      [3, 4, 5],
                      [0, 4, 5],
                      [0, 1, 5],
                      [0, 1, 2],
                      [1, 2, 3]]

    boundaryTris   = [[2, 4],
                      [3, 5],
                      [0, 4],
                      [1, 5],
                      [0, 2],
                      [1, 3]]

    def __init__(self):
        super().__init__()
        self._options['fontSizeOffset'] = 0
        self._activateDefaults()
        self.select = None

    def setupClassGeometry(self):
        VHTRCHexagonal.setupClassGeometry(self)

        # get tri points
        self.triPoints = Triangular.calcTriPoints(self, self._hexPoints, self.pitch)

        # delete tris on the outside
        # select list
        self.select = []
        for idxBlock in range(self.numBlocks):
            if idxBlock not in self.halfBlocks:
                # select all tris
                self.select.extend([idxBlock*6 + idx for idx in range(6)])
            else:
                for idxSide, side in enumerate(self.boundaryBlocks):
                    # test if block i in side
                    if idxBlock in side:
                        # get tris in core
                        for tri in self.halfTris[idxSide]:
                            # append tri
                            self.select.append(idxBlock*6 + tri)

                        # leave loop
                        break

        # select tris from all tris
        self.triPoints = self.triPoints[self.select]

    def getClassValuePaths(self):
        paths = Triangular.getClassValuePaths(self)
        return paths[self.select].copy()

    def getClassTextPoints(self):
        return Triangular.getClassTextPoints(self)

    def getClassValuePoints(self):
        return Triangular.getClassValuePoints(self)
