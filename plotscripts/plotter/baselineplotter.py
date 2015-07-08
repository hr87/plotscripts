"""
Created on Jun 27, 2013

@author: Hans R Hammer
"""

import os
import numpy
from plotscripts.plotter.baseplotter import BasePlotter
from plotscripts.base.baseobject import BaseObject

class Line(BaseObject):
    """ Class describing a line in a line plot. Holds information about values, color etc

    :var color:
    :var lineStyle:
    :var markerStyle:
    :var data:
    :var title:
    :var lineWidth:
    :var xValues:
    """
    from enum import Enum, unique

    @unique
    class ColorList(Enum):
        auto     = 0
        red      = 1
        blue     = 2
        green    = 3
        yellow   = 4
        magenta  = 5
        cyan     = 6
        black    = 7

    @unique
    class LineStyleList(Enum):
        none        = 0
        solid       = 1
        dashed      = 2
        pointed     = 3
        dashpoint   = 4

    @unique
    class MarkerStyleList(Enum):
        none        = 0
        dot         = 1
        square      = 2
        star        = 3
        circle      = 4

    def __init__(self):
        super().__init__()
        self.color = self.ColorList.auto
        self.lineStyle = self.LineStyleList.solid
        self.markerStyle = self.MarkerStyleList.none

        self.data   = []
        self.title  = ''

        self.lineWidth = 1
        self.markerSize = 1

        self.xValues = None

    def checkInput(self):
        super()._checkInput()
        if self.lineWidth < 0:
            self._warning("Line width smaller 0, set to 0")
            self.lineWidth = 0
        if self.markerSize < 0:
            self._warning("Marker size smaller 0, set to 0")
            self.markerSize = 0
        if self.xValues is not None:
            self.xValues = numpy.array(self.xValues)


class BaseLinePlotter(BasePlotter):
    """ Base class for all line plotters

    :var xValues:

    """
    def __init__(self):
        super().__init__()
        self.xValues = None

        # default options
        self._addDefault('legendPos', 'upper right', 'legend position', 'private')
        self._addDefault('grid', 'major', 'background grid', 'private')

        # internal
        self._lines = []

    def addLine(self):
        """Returns a line object with default settings

        :return reference to new line object
        """
        newLine = Line()
        self._lines.append(newLine)
        return newLine

    def plot(self):
        """ Plot function, create all the lines from the data.

        This function prepares all data for the plots. The data is then passed to the writeFile method. This
        method is overwritten by the plotters and produces the final files.

        :return: None
        """
        # test for input
        self._out('Plotting {0}'.format(self.title))
        self._checkInput()
        self._activateDefaults()

        for method in self.method:
            # create path
            path = self._getOption('plotdir')
            if self._getOption('use_dirs'):
                # create path
                 path += self._cleanPath('/{0}/{1}/'.format(self.title, method))

            # create dir for output
            try:
                os.makedirs(path, exist_ok=True)
            except OSError as e:
                raise self._exception('Could not create directory ' + path ) from e

            for column in self.columns:
                # create filename
                filename = self._cleanFileName('{0}_{1}_{2}'.format(self.title, method, column)) + '.' + self._getOption('format')

                # create title
                if column:
                    title = ('{0} - {1}'.format(self.title, column))
                else:
                    title = self.title

                # get all data
                for idx, line in enumerate(self._lines):
                    datakey = line.data

                    # get data values and add to line
                    if datakey.__class__ == tuple:
                        # create copy
                        datakey = tuple(datakey)
                        # append column if necessary
                        if column is not None:
                            datakey[1].append(column)

                        line.xValues = self._data.getData(datakey[0], 'value', None)
                        line.yValues = self._data.getData(datakey[1], method, self.basedata, line.xValues)

                    else:
                        # create copy
                        datakey = list(datakey)
                        # append column
                        if column is not None:
                            datakey.append(column)

                        if line.xValues is not None:
                            pass
                        elif self.xValues is not None:
                            line.xValues = self.xValues
                        else:
                            line.xValues = self._data.getXValues(datakey, column)
                            if line.xValues is None:
                                raise self._exception('No default x values found')
                        line.yValues = self._data.getData(datakey, method, self.basedata, line.xValues)

                    # set legend to default, if not provided
                    if not line.title:
                        line.title = 'Plot {0}'.format(idx)

                self.writeFile(path, filename, title, self._lines, column, method)

    def writeFile(self, path, filename, title, lines, column, method = 'value'):
        """ Virtual method, must be overwritten by the implementations of the plotter

        :param path: relative file path
        :param filename: file name
        :param title: title of the plot
        :param lines: list of line objects
        :param column: current column
        :param method: current method
        :return: None
        """
        raise self._exception('Not implemented in base class')

    def _checkInput(self):
        super()._checkInput()
        if self.xValues is not None:
            self.xValues = numpy.array(self.xValues)

        for line in self._lines:
            line.checkInput()
