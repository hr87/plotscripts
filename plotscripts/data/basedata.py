"""
Created on Apr 11, 2013

@author: Hans R Hammer
"""

import math
import numpy
import enum

from plotscripts.base.baseobject import BaseObject
from plotscripts.base.basecontainer import BaseContainer
from plotscripts.plotter.util.functions import axisDiv


class BaseData(BaseObject):
    """
    Base class for all executioner
    :var dir: base input directory for the data, default = '.'
    :var file: dic with files, key is used as index
    :var xSteps: list with default x steps for data
    :var xLabel: x label for plots, default = ''
    :var yLabel: y label, default = ''
    :var statistics: input for statistic calculations, different sets possible, same input syntax like plooter input
    """

    @enum.unique
    class Methods(enum.Enum):
        value = 0
        difference = 1
        deviation = 2
        normalized = 3
        normalizedDifference = 4
        normalizedDeviation = 5

    class Index(BaseContainer):
        """ Class to create an index
        :var columns: list or single column
        """

        def __init__(self):
            """ Constructor """
            super().__init__()
            self.column = None
            self.method = BaseData.Methods.value

        def getIndex(self):
            """ Create and return index
            :return: index list
            """
            self._exception("Not implemented in base class")

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.xSteps = []  # list for xValues TODO think about that
        self.xLabel = ''  # TODO that too
        self.yLabel = ''
        self.columns = []  # columns to prepare statistics for

        # set default options
        self._addDefault('normalize', 'max',
                         'Normalization method: sum, avg, max', 'private')  # normalization,

        # internal
        self._data = {}  # data storage
        self._statistics = {}  # index input for statistics views

    def addStatistic(self, name):
        """ Add a statistic input
        :param name: name of the statistic
        :return: reference to statistic object
        """
        from plotscripts.data.statisticdata import StatisticData

        newStatistic = StatisticData(name)
        self._statistics[name] = newStatistic
        return newStatistic

    @staticmethod
    def index():
        """ Create and return a data index
        :return: an object of StatisticIndex
        """
        raise BaseObject.Exception('BaseData', 'index', "Not implemented in base class")

    @staticmethod
    def statisticIndex():
        """ Create and return a statistic index
        :return: an object of StatisticIndex
        """
        from plotscripts.data.statisticdata import StatisticData

        return StatisticData.StatisticIndex()

    def processData(self):
        """
        base method for data processing, called by inputArgs
        """
        self._out('Processing data')

        self._activateDefaults()
        # check the input
        self._checkInput()

        # call data executioner process method
        self._processClassData()

        # prepare statistics
        self._calcSpecialData()

    def _processClassData(self):
        """ Virtual method to be overwritten by the implementation
        :return: None
        """
        raise self._exception('Data processing not implemented in base class')

    def _getClassData(self, index):
        """ Virtual method to retrieve class data
        :param index: data index
        :return: data as ndarray
        """
        raise self._exception("Data retrieving not implemented in base class")

    def _calcSpecialData(self):
        """
        function to calculate statistics
        """
        self._out('Preparing statistics')
        # loop over all inputs
        for key in self._statistics:
            self._statistics[key].ref = self
            self._statistics[key].processData()

    def getData(self, index, baseIndex=None, x=None):
        """
        Get the data out of the database

        methods available are:
        value (default)
        diff (base needed)
        rel (base needed)
        grad () gradient of data, x values changed

        :param index: list with index of data
        :param baseIndex: list with index for base data needed for some methods, default = None
        :param x: x values for some methods, may be changed, default = None
        :return: numpy array with data
        """
        from plotscripts.data.statisticdata import StatisticData
        # check the length of index
        self._debug('Getting data for {0}; base {1}'.format(index, baseIndex))

        # check for statistic
        if (not isinstance(self, StatisticData)) and isinstance(index, StatisticData.StatisticIndex):
            try:
                return self._statistics[index.name].getData(index, baseIndex, x)
            except KeyError:
                raise self._exception('No statistic with name "{0}"'.format(index.name))

        # get normalized data
        values = self._getClassData(index)

        # try to get base data
        if baseIndex is not None:
            self._debug('Getting base data')
            if isinstance(baseIndex, tuple):
                baseValues = self.getData(baseIndex[0])
                baseX = self.getData(baseIndex[1])
            else:
                baseValues = self.getData(baseIndex)
                baseX = self.getXValues(baseIndex)
        else:
            baseValues = None
            baseX = None

        if values.dtype == numpy.dtype('object'):
            raise self._exception('Data shape is not rectangular')
        if baseValues is not None and baseValues.dtype == numpy.dtype('object'):
            raise self._exception('Base data shape is not rectangular')

        # calculate difference and deviations
        values = self._calc(x, values, index.method, baseValues, baseX)

        return values

    def _calc(self, x, y, method, base_values, baseX):
        # check method
        if method not in self.Methods:
            raise self._exception('Unknown method ' + str(method))

        # nothing to do for values
        if method == self.Methods.value:  # normal value
            pass
        # normalize values
        if method in [self.Methods.normalized, self.Methods.normalizedDifference,
                      self.Methods.normalizedDeviation]:
            normMethod = self._getOption('normalize')
            if normMethod == 'avg':
                y = y / y[~numpy.isnan(y)].mean()
            elif normMethod == 'max':
                y = y / numpy.nanmax(y)
            elif normMethod == 'sum':
                y = y / numpy.nansum(y)
            else:
                raise self._exception('Unknown normalization function {0}'.format(normMethod))
        # calculate difference
        if method in [self.Methods.difference, self.Methods.normalizedDifference]:
            if base_values is None:
                raise self._exception('Base data needed for difference')
            base_values = self._interpolate(x, baseX, base_values)
            y = y - base_values
        # calculate deviation in percent
        if method in [self.Methods.deviation, self.Methods.normalizedDeviation]:
            if base_values is None:
                raise self._exception('Base data needed for deviation')
            base_values = self._interpolate(x, baseX, base_values)
            y = (y - base_values) / base_values * 100

        return y.squeeze()

    def _interpolate(self, x1, x2, y):
        if x1 is not None and y.ndim > 0 and x2 is not None:
            # sort x and base values increasing
            sortX = numpy.argsort(x1)
            x = x1[sortX]
            sortBase = numpy.argsort(x2)
            baseX = x2[sortBase]
            y = y[sortBase]
            # interpolate
            y = numpy.interp(x, baseX, y)
            # undo sort
            y = y[numpy.argsort(sortBase)]

        elif x1 is None or x2 is None:
            self._warning('Cannot interpolate')
        return y

    def getSteps(self, values, numSteps, method, zeroFix=False):
        """
        base function to get value levels for map plots
        round to next nice level
        :param values: ndarray of values to calculate steps for
        :param numSteps: number of Steps
        :return: array with step values
        """
        valuesMax = numpy.nanmax(values)
        valuesMin = numpy.nanmin(values)

        # getting some stuff
        valuesRange = valuesMax - valuesMin  # value range on axis
        if not numpy.isnan(valuesRange) and valuesRange > 0:
            mag = 10 ** (math.floor(math.log10(valuesRange)))  # magnitude of axis values
        elif not numpy.isnan(valuesRange) and valuesMax != 0:
            mag = 10 ** (math.floor(math.log10(numpy.abs(valuesMax))))
            valuesMax += 1 * mag
            valuesMin -= 1 * mag
        else:
            mag = 1
            valuesMax = 1
            valuesMin = -1

        valuesDiv = axisDiv(valuesRange, mag)  # divider for axis

        # rescale values to rounded values
        mag = mag / valuesDiv
        valuesMax = math.ceil(valuesMax / mag) * mag
        valuesMin = math.floor(valuesMin / mag) * mag

        # middle zeroFix
        if zeroFix == 'middle':
            if abs(valuesMax) > abs(valuesMin):
                valuesMin = valuesMax
            else:
                valuesMax = valuesMin
                # replace value nearer to zero with zero
        elif zeroFix:
            if valuesMax > 0 and valuesMin < 0:
                raise self._exception('Fixed zero not possible')
            elif valuesMax <= 0:
                valuesMax = 0
            elif valuesMin >= 0:
                valuesMin = 0

        return numpy.linspace(valuesMin, valuesMax, numSteps + 1, True)

    def getXValues(self, index):
        """
        get standard x values
        @return: numpy array with x values
        """
        if self.xSteps is None or self.xSteps == []:
            # self.warning('No x values available')
            return None

        return self.xSteps.copy()

    def getXLabel(self, column):
        """
        get x label for data
        @return: label as string
        """
        return self.xLabel

    def getYLabel(self, column, method='value'):
        """
        get y label for data
        @return: label as string
        """
        if self.yLabel == '':
            return column
        else:
            return self.yLabel

    def _checkInput(self):
        """
        check the input and convert if necessary
        """
        from plotscripts.data.statisticdata import StatisticData
        # test for files
        # if self.file == {} :
        #   raise self.exception('No data files')

        if self.xSteps != []:
            self.xSteps = numpy.array(self.xSteps)

        # check statistic input
        # check dict
        if not self._statistics.__class__ == dict:
            raise self._exception('Statistics must be a dictionary!')

        if not self.columns.__class__ == list:
            raise self._exception('Columns must be a list')

        for key, statistic in self._statistics.items():
            if not isinstance(statistic, StatisticData):
                raise self._exception('Wrong class for statistic {0}'.format(key))
