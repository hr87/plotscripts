"""
Created on Apr 11, 2013

@author: hammhr
"""

from ..base.baseobject import BaseObject


class BasePlotter(BaseObject):
    """
    Basic Plotter class
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.method     = []    # plot method
        self.columns    = []    # columns to be plotted
        self.basedata   = None  # base data for comparison
        self.title      = None  # plot title
        self.xLabel     = None  # x label
        self.yLabel     = None  # y label

        # default path and filename options
        self._addDefault('plotdir', '.', 'folder for plots')
        self._addDefault('title', True, 'Show title in plot', 'private')
        self._addDefault('size', [750, 500], 'pl,ot size in pixel', 'private')
        self._addDefault('xScale', 'linear', 'x axis scaling', 'private')
        self._addDefault('yScale', 'linear', 'y axis scaling', 'private')
        self._addDefault('fontSize', 12, 'plot font size', 'private')
        self._addDefault('use_dirs', True, 'creates folder hierarchy for plots', 'private')

        # internal
        self._data       = None  # storage for data

    def plot(self):
        """
        base method for plotting
        """
        raise self._exception('Plotting method not implemented yet in ' + self.__class__.__name__)

    def setTitle(self, title):
        if self.title == None :
            self.title = title
        else :
            self.title = str(self.title)

    def setData(self, data):
        """ Set data set
        :param data: data set
        :return: None
        """
        self._data = data
        
    def _checkInput(self):
        if self.method == [] :
            self.method = ['value']

        # setting columns
        if self.columns is None or self.columns == []:
            self.columns = [None]

        if self.columns.__class__.__name__ != 'list':
            self.columns = [self.columns]

