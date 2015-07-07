'''
Created on Apr 22, 2013

@author: Hans R Hammer
'''

from .baseplotter import BasePlotter
from ..geometry.basegeometry import BaseGeometry

import os
import numpy

class BaseMapPlotter(BasePlotter):
   '''
   Basic for all map plotters
   '''

   
   def __init__(self):
      '''
      Constructor
      '''
      super().__init__()
      self.geometry  = None         # geometry class
      self.select    = []           # select the values in 2d
      self.assign    = []           # select the blocks
      self.transpose = False        # transpose data array
      
      self._defaults['extrema']      = []        # manual set for extrema, [x_min, x_max, y_min, y_max]
      self._defaults['mapFontSize']  = 6
      self._defaults['colormap']     = 'hsv'     # type of color map, hsv only one at this time
      self._defaults['sameLvls']     = False     # flag to put the same levels on every plot
      self._defaults['numLvls']      = 20        # number of color steps in color map
      self._defaults['zeroFix']      = False     # True, fixes nearest value to zero, middle fixes middle to zero
      self._defaults['overlay']      = True      # overlay lines
      self._defaults['overlayText']  = True      # text value overlay
      self._defaults['nanRegions']   = False     # cut outer NaN regions
      self._defaults['sameExtrema']  = False     # x and y the same


   def plot(self):
      '''
      function getting data from executioner and calls write file
      '''
      # test for input
      self._checkInput()
      
      self._out('Plotting {0}'.format(self.title))
      
      # setting options in geometry
      self.geometry.setOptions(self._options)
      # setup geometry
      self.geometry.setupGeometry()
      # getting defaults from geometry
      self.getOptions(self.geometry)
      # and the defaults
      self._activateDefaults()
      
      for method in self.method:       
         for column in self.columns:
            
            values = []
            
            for datakey in self.input:
               # check for x values
               if datakey.__class__.__name__ == 'tuple' :
                  # useless poke
                  raise self._exception('No x values allowed in map plot')
               
               # create copy
               datakey = list(datakey)
               
               # check column 
               if column != None:
                  datakey.append(column)
                  
               # get values
               tmp = self.data.getData(datakey, method, self.basedata, None)
               # transpose values if wanted
               if self.transpose:
                  tmp = tmp.transpose()
               
               # add values to list
               values.append(tmp)
            
            # convert into numpy array
            try:
               values = numpy.array(values)
            except ValueError as e:
               for value in values:
                  print(value.shape)
               raise self._exception('Results have not the same shape, array not rectangular') from e
            
            # add third axis
            if values.ndim < 3:
               values = values[:, :, numpy.newaxis]
               
            # check for dims
            if values.ndim > 3:
               raise self._exception('To many dimensions in value array: {0}'.format(values.ndim))
            
            # select data to plot from 2d values
            if not self.select == []:
               try:
                  values = values[:, :, self.select]
               except IndexError as e:
                  raise self._exception('Non valid selection of data') from e
               
            # calculate levels for all values at once
            if(self._options['sameLvls']):
               lvls = self.data.getSteps(values, self._options['numLvls'], method, self._options['zeroFix'])
               
            for idxData, datakey in enumerate(self.input): # check column 
               # use legend strings for name if possible
               if self.legend:
                  tmpName = self.legend[idxData]
               else:
                  tmpName = datakey[0]
                  
               if column != None:
                  path = self._options['plotdir'] + self._cleanPath('/{0}/{1}/{2}/{3}'.format(self.title, method, tmpName, column))
               else:
                  path = self._options['plotdir'] + self._cleanPath('/{0}/{1}/{2}'.format(self.title, method, tmpName))
               # create dir for output
               try :
                  os.makedirs(path, exist_ok=True)
               except OSError as e:
                  raise self._exception('Could not create directory ' + path ) from e
               
               for idxSelect in range(values.shape[2]):
                  # get levels for each single values
                  if not self._options['sameLvls']:
                     lvls = self.data.getSteps(values[idxData, :, idxSelect], self._options['numLvls'], method, self._options['zeroFix'])
                   
                  # create filename dependent on number of values
                  if values.shape[2] > 1:
                     title = self.title + ' {0}'.format(idxSelect)
                     filename = self._cleanFileName('{0}_{1}_{2}_{3}_{4}'.format(self.title, tmpName, method, column, idxSelect))
                  else:
                     title = self.title
                     filename = self._cleanFileName('{0}_{1}_{2}_{3}'.format(self.title, tmpName, method, column))
                  
                  self.writeFile(path, filename, values[idxData, :, idxSelect], lvls, title)
   
   def writeFile(self, path, filename, values, lvls, title = None):
      raise self._exception('Not implemented yet')
   
   def _checkInput(self):
      BasePlotter._checkInput(self)
      
      if self.geometry.__class__ == type:
         raise self._exception('I need a instance and not a class defenition. Add () to the geometry')
      
      if not issubclass(self.geometry.__class__, BaseGeometry):
         raise self._exception(self.geometry.__class__.__name__ + ' is no compatible geometry')
      
      self.geometry.checkInput()
           
      
      