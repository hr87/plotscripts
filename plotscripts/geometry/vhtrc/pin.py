'''
Created on May 18, 2013

@author: hr87
'''

from .hexagonal import VHTRCHexagonal
import numpy, math

class VHTRCPin(VHTRCHexagonal):
   '''
   class doc
   '''
   
   radiusRod102   = 51.05      # taking hole radius, gap is part of xs
   radiusRod65    = 32.58
   radiusRod47    = 23.6
   fuelRodPitch   = 65
   posRod102      = 94
   posRod47       = 111
   
   def __init__(self):
      super().__init__()
      
   def setupClassGeometry(self):
      # create block geometry
      VHTRCHexagonal.setupClassGeometry(self)
      
      # create pin locations for blocks
      self.pinPoints    = []  # center points for rods
      self.pinRadii     = []  # rod diameters
      
      # 18-pin fuel block
      self.pinPoints.append(self.calcHexPoints(self.fuelRodPitch, 2, 0, True))
      self.pinRadii.append([self.radiusRod65] + [self.radiusRod47]*18)
      
      # 6 pin moderator block
      points         = numpy.zeros((6, 2))
      angles         = numpy.linspace(0, 4.0/3.0*math.pi, 3, True)
      points[[0,2,4], 0]   = numpy.cos(angles) * self.posRod102
      points[[0,2,4], 1]   = numpy.sin(angles) * self.posRod102
      points[[3,5,1], 0]   = -numpy.cos(angles) * self.posRod47
      points[[3,5,1], 1]   = numpy.sin(angles) * self.posRod47
      self.pinPoints.append(points)
      self.pinRadii.append([self.radiusRod102, self.radiusRod47]*3)
      
      # 1-pin moderator block
      self.pinPoints.append(numpy.zeros((1, 2)))
      self.pinRadii.append([self.radiusRod47])
      
      # 1-pin half block
      # angles of points
      angles = numpy.linspace(1.0/6.0*math.pi, 11.0/6.0*math.pi, 6, True)
      for angle in angles:
         # calc point for rod
         points = numpy.array([-1.0, 0.0]) * self.blockHexPitch / 4.0
         # rotate point
         
         points[0] *= math.cos(angle)
         points[1] *= math.sin(angle)
         self.pinPoints.append(points)
         self.pinRadii.append([self.radiusRod47])
         
         
         
   def getClassValuePaths(self):
      # get paths of blocks
      blockPaths = VHTRCHexagonal.getClassValuePaths(self)
      
      paths = []
      
      # add for every block the pins
      for idxBlock, block in enumerate(blockPaths):
         # add block path
         paths.append(block)
         
         
         
         # get block type
         blockType = self.blockTypes[idxBlock]
         for point, radius in zip(self.pinPoints[blockType], self.pinRadii[blockType]):
            tmpPath = numpy.zeros((2, 7))
            # add center point
            tmpPath[:, 0] = point + self._hexPoints[idxBlock]
            # add point and circle
            tmpPath[:, 1] = point + self._hexPoints[idxBlock] + numpy.array([radius, 0])
            # fill up with NaN
            tmpPath[:, 2:7] = float('NaN')
            
            # add pin list to path list
            paths.append(tmpPath)
      
      return numpy.array(paths) 
   
   def getClassPathTypes(self):
      blockTypes = VHTRCHexagonal.getClassPathTypes(self)
      
      pathTypes = []
           
      # add for every block the pins
      for idxBlock, block in enumerate(blockTypes):
         # add block path
         pathTypes.append(block)
         
         # get block type
         blockType = self.blockTypes[idxBlock]
         # add circle for each pin
         pathTypes += ['circle'] * len(self.pinPoints[blockType])
       
      return pathTypes 
            
   def getClassValuePoints(self):
      blockPoints = VHTRCHexagonal.getClassValuePoints(self)
      
      valuePoints = []
      
      for idxBlock, block in enumerate(blockPoints):
         valuePoints.append(block)
         
         # get block type
         blockType = self.blockTypes[idxBlock]
         tmpPath = []
         
         for point in self.pinPoints[blockType]:
            # add center point
            tmpPath.append(point)
         
         # add pin list to path list
         valuePoints.extend(tmpPath)
      
      print(valuePoints)   
      return numpy.array(valuePoints)
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      