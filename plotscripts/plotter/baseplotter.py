"""
Created on Apr 11, 2013

@author: hammhr
"""

import copy
from plotscripts.base.baseobject import BaseObject
from plotscripts.data.basedata import BaseData


class BasePlotter(BaseObject):
    """
    Basic Plotter class
    """

    def __init__(self, name):
        """
        Constructor
        """
        super().__init__()
        self.methods = [None]  # plot method
        self.columns = [None]  # columns to be plotted
        self.title = name  # plot title
        self.xLabel = None  # x label
        self.yLabel = None  # y label

        # default path and filename options
        self._addDefault('plotdir', '.', 'folder for plots')
        self._addDefault('title', True, 'Show title in plot', 'private')
        self._addDefault('size', [750, 500], 'pl,ot size in pixel', 'private')
        self._addDefault('xScale', 'linear', 'x axis scaling', 'private')
        self._addDefault('yScale', 'linear', 'y axis scaling', 'private')
        self._addDefault('fontSize', 12, 'plot font size', 'private')
        self._addDefault('use_dirs', True, 'creates folder hierarchy for plots', 'private')

        # internal
        self._data = None  # storage for data
        self._basedata = None  # base data for comparison
        self._name = name

    def plot(self):
        """
        base method for plotting
        """
        raise self._exception('Plotting method not implemented yet in ' + self.__class__.__name__)

    def setData(self, data):
        """ Set data set
        :param data: data set
        :return: None
        """
        self._data = data

    def setBaseIndex(self, index):
        """ Set the index for the base data
        :param index: index object
        :return: None
        """
        if not isinstance(index, BaseData.Index):
            raise self._exception('Invalid index object "{0}"'.format(index))
        self._basedata = copy.deepcopy(index)

    def _checkInput(self):
        # setting columns
        if not isinstance(self.methods, list):
            self.methods = [self.methods]
        if not isinstance(self.columns, list):
            self.columns = [self.columns]

