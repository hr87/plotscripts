"""
Created on May 12, 2013

@author: hr87
"""

from ..basexygeometry import BaseXYGeometry
from .hexagonal import Hexagonal

class HexagonalXY(BaseXYGeometry, Hexagonal):
   """
   Creates a hexagonal geometry with xy points from a file for center points 
   """
   
   
   def __init__(self):
      """
      Constructor
      """
      super().__init__(self)

   def setupClassGeometry(self):
      self.readPoints(self.fileName)
      
   def getClassValuePaths(self):
      Hexagonal.getClassValuePaths(self)
   
   def getClassOverlayPaths(self):
      Hexagonal.getClassOverlayPaths(self)
   
   def getClassTextPoints(self):
      Hexagonal.getClassTextPoints(self)
   
   def getClassValuePoints(self):
      Hexagonal.getClassValuePoints(self)
   
   def getClassPathTypes(self):
      Hexagonal.getClassPathTypes(self)
   
   def getClassOverlayTypes(self):
      Hexagonal.getClassOverlayTypes(self)
   
   def _checkInput(self):
      super()._checkInput(self)
   
      