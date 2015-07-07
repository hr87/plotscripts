'''
Created on Apr 11, 2013

@author: hammhr
'''

from ..base.baseobject import BaseObject

class BasePlotter(BaseObject):
   '''
   Basic Plotter class
   '''
   



   def __init__(self):
      '''
      Constructor
      '''
      super().__init__()
      self.input      = []    # plot data
      self.method     = []    # plot method
      self.columns    = []    # columns to be plotted
      self.basedata   = None  # base data for comparison
      self.title      = None  # plot title
      self.xLabel     = None  # x label
      self.yLabel     = None  # y label
  
      # default path and filename options
      self.defaults['plotdir']     = '.'
      self.defaults['title']       = True
      self.defaults['size']        = [750, 500]
      self.defaults['xScale']      = 'linear'
      self.defaults['yScale']      = 'linear'
      self.defaults['fontSize']    = 12
      
      # internal 
      self.data       = None  # storage for data
      
      
   def plot(self):
      '''
      base method for plotting
      '''
      raise self.exception('Plotting method not implemented yet in ' + self.__class__.__name__)
   
   def setTitle(self, title):
      if self.title == None :
         self.title = title
      else :
         self.title = str(self.title)
             
   def checkInput(self):
      if self.input == [] :
         raise self.exception('No input data specified')
      
      if self.method == [] :
         self.method = ['value']
      
      # setting columns
      if self.columns == None or self.columns == []:
         self.columns = [None]
         
      if self.columns.__class__.__name__ != 'list':
         self.columns = [self.columns]
        
      for tmpInput in self.input:
         tmpInput.checkInput()
      
