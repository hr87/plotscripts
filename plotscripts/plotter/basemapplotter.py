"""
Created on Apr 22, 2013

@author: Hans R Hammer
"""

from plotscripts.base.baseobject import BaseObject
from plotscripts.plotter.baseplotter import BasePlotter
from plotscripts.geometry.basegeometry import BaseGeometry

import os
import numpy


class BaseMapPlotter(BasePlotter):
    """ Basic for all map plotters """
    class Map(BaseObject):
        """ Class to store a map

        :var input: index of input data
        :var title: legend string of map
        :var select: select only partial or shuffled data
        :var assign: select only partial or shuffled blocks
        """

        def __init__(self):
            """ Constructor """
            super().__init__()
            self.input = []                 # data index
            self.legend = None              # description
            self.select    = []             # select the values in 2d
            self.assign    = []             # select the blocks
            self.transpose = False          # transpose data array

        def _checkInput(self):
            super()._checkInput()
            #TODO check input here

    def __init__(self):
        """ Constructor """
        super().__init__()

        # options
        self._addDefault('extrema', [], 'manual set for extrema, [x_min, x_max, y_min, y_max]', 'private')
        self._addDefault('mapFontSize', 6, 'font size for values in map', 'private')
        self._addDefault('colormap', 'hsv', 'type of color map, hsv only one at this time', 'private')
        self._addDefault('sameLvls', False, 'flag to put the same levels on every plot', 'private')
        self._addDefault('numLvls', 20, 'number of color steps in color map', 'private')
        self._addDefault('zeroFix', False, 'True, fixes nearest value to zero, middle fixes middle to zero', 'private')
        self._addDefault('overlay', True, 'overlay lines', 'private')
        self._addDefault('overlayText', True, 'text value overlay', 'private')
        self._addDefault('nanRegions', False, 'cut outer NaN regions', 'private')
        self._addDefault('sameExtrema', False, 'x and y the same', 'private')

        # internal
        self._geometry = None           # geometry class
        self._maps = []                 # dict of input maps

    def setGeometry(self, geometryClass):
        """ sets the geometry for the map plotter

        :param geometryClass: class of geometry
        :return: reference to geometry object
        """
        if not issubclass(geometryClass, BaseGeometry):
            raise self._exception(geometryClass.__name__ + 'is not a valid geometry')
        newGeometry = geometryClass()
        self._geometry = newGeometry
        return newGeometry

    def addMap(self, name):
        """ Adds a new map input and returns reference
        :param name: name of map plot
        :return: reference to map plot
        """
        newMap = self.Map()
        self._maps.append(newMap)
        return newMap

    def plot(self):
        """ function getting data from executioner and calls write file """
        # test for input
        self._checkInput()

        self._out('Plotting {0}'.format(self.title))

        # the defaults
        self._activateDefaults()
        # setting options in geometry
        self._geometry.copyOptions(self._options)
        # setup geometry
        self._geometry.setupGeometry()
        # getting defaults from geometry
        #TODO self._retrieveOptions(self._geometry.getOptions)

        for method in self.method:
            for column in self.columns:

                values = []

                for map in self._maps:
                    datakey = map.input
                    # check for x values
                    if datakey.__class__.__name__ == 'tuple':
                        # useless poke
                        raise self._exception('No x values allowed in map plot')

                    # create copy
                    datakey = list(datakey)

                    # check column 
                    if column is not None:
                        datakey.append(column)

                    # get values
                    tmp = self._data.getData(datakey, method, self.basedata, None)
                    # transpose values if wanted
                    if map.transpose:
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
                if not map.select == []:
                    try:
                        values = values[:, :, map.select]
                    except IndexError as e:
                        raise self._exception('Non valid selection of data') from e

                # calculate levels for all values at once
                if self._getOption('sameLvls'):
                    lvls = self._data.getSteps(values, self._getOption('numLvls'), method, self._getOption('zeroFix'))

                for idxData, map in enumerate(self._maps):   # check column
                    datakey = map.input
                    # use legend strings for name if possible
                    if map.legend:
                        tmpName = map.legend
                    else:
                        tmpName = datakey[0]

                    path = self._getOption('plotdir')
                    if self._getOption('use_dirs'):
                        if column is not None:
                            path += self._cleanPath('/{0}/{1}/{2}/{3}'.format(self.title, method, tmpName, column))
                        else:
                            path += self._cleanPath('/{0}/{1}/{2}'.format(self.title, method, tmpName))
                    # create dir for output
                    try:
                        os.makedirs(path, exist_ok=True)
                    except OSError as e:
                        raise self._exception('Could not create directory ' + path) from e

                    for idxSelect in range(values.shape[2]):
                        # get levels for each single values
                        if not self._getOption('sameLvls'):
                            lvls = self._data.getSteps(values[idxData, :, idxSelect], self._getOption('numLvls'), method, self._getOption('zeroFix'))

                        # create filename dependent on number of values
                        #TODO get map title
                        if values.shape[2] > 1:
                            title = self.title + ' {0}'.format(idxSelect)
                            filename = self._cleanFileName('{0}_{1}_{2}_{3}_{4}'.format(self.title, tmpName, method, column, idxSelect))
                        else:
                            title = self.title
                            filename = self._cleanFileName('{0}_{1}_{2}_{3}'.format(self.title, tmpName, method, column))

                        self.writeFile(path, filename, values[idxData, :, idxSelect], lvls, map.assign, title)

    def writeFile(self, path, filename, values, lvls, assign, title=None):
        raise self._exception('Not implemented in base class')

    def _checkInput(self):
        BasePlotter._checkInput(self)

        if self._geometry.__class__ == type:
            raise self._exception('I need a instance and not a class defenition. Add () to the geometry')

        if not issubclass(self._geometry.__class__, BaseGeometry):
            raise self._exception(self._geometry.__class__.__name__ + ' is no compatible geometry')

