"""
Created on Apr 22, 2013

@author: Hans R Hammer
"""

from plotscripts.plotter.baseplotter import BasePlotter
from plotscripts.geometry.basegeometry import BaseGeometry

import os
import numpy


class BaseMapPlotter(BasePlotter):
    """ Basic for all map plotters """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.select    = []           # select the values in 2d
        self.assign    = []           # select the blocks
        self.transpose = False        # transpose data array

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
        self._geometry = None         # geometry class

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

    def plot(self):
        """ function getting data from executioner and calls write file """
        # test for input
        self._checkInput()

        self._out('Plotting {0}'.format(self.title))

        # the defaults
        self._activateDefaults()
        # setting options in geometry
        self._geometry.setOptions(self._options)
        # setup geometry
        self._geometry.setupGeometry()
        # getting defaults from geometry
        self.getOptions(self._geometry)

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
                    tmp = self._data.getData(datakey, method, self.basedata, None)
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
                    lvls = self._data.getSteps(values, self._options['numLvls'], method, self._options['zeroFix'])

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
                            lvls = self._data.getSteps(values[idxData, :, idxSelect], self._options['numLvls'], method, self._options['zeroFix'])

                        # create filename dependent on number of values
                        if values.shape[2] > 1:
                            title = self.title + ' {0}'.format(idxSelect)
                            filename = self._cleanFileName('{0}_{1}_{2}_{3}_{4}'.format(self.title, tmpName, method, column, idxSelect))
                        else:
                            title = self.title
                            filename = self._cleanFileName('{0}_{1}_{2}_{3}'.format(self.title, tmpName, method, column))

                        self.writeFile(path, filename, values[idxData, :, idxSelect], lvls, title)

    def writeFile(self, path, filename, values, lvls, title = None):
        raise self._exception('Not implemented in base class')

    def _checkInput(self):
        BasePlotter._checkInput(self)

        if self._geometry.__class__ == type:
            raise self._exception('I need a instance and not a class defenition. Add () to the geometry')

        if not issubclass(self._geometry.__class__, BaseGeometry):
            raise self._exception(self._geometry.__class__.__name__ + ' is no compatible geometry')

