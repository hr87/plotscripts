"""
Created on Apr 11, 2013

@author: Hans R Hammer
"""

import math
import numpy

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

    class Index(BaseContainer):
        """ Class to create an index
        :var columns: list or single column
        """

        def __init__(self):
            """ Constructor """
            super().__init__()
            self.column = None

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

    def statisticIndex(self):
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

    def getData(self, index, method='value', baseIndex=None, x=None):
        """
        Get the data out of the database

        methods available are:
        value (default)
        diff (base needed)
        rel (base needed)
        grad () gradient of data, x values changed

        :param index: list with index of data
        :param method: method for data processing, default = value
        :param baseIndex: list with index for base data needed for some methods, default = None
        :param x: x values for some methods, may be changed, default = None
        :return: numpy array with data
        """
        from plotscripts.data.statisticdata import StatisticData
        # check the length of index
        self._debug('Getting data for {0} {1}; base {2}'.format(index, method, baseIndex))

        # check for statistic
        if (not isinstance(self, StatisticData)) and isinstance(index, StatisticData.StatisticIndex):
            try:
                return self._statistics[index.name].getData(index, method, baseIndex, x)
            except KeyError:
                raise self._exception('No statistic with name "{0}"'.format(index.name))

        # get normalized data
        if method in ['rel_norm', 'diff_norm']:
            values = self.getData(index, 'norm', None)
        else:
            values = self._getClassData(index)

        if method == 'grad':
            if x is None:
                raise self._exception('x values needed for gradient')
            x = self._enchantX(x)

            # which type of base data
        if method in ['rel_norm', 'diff_norm']:
            baseMeth = 'norm'
        else:
            baseMeth = 'value'

        # try to get data and base data
        if baseIndex is not None:
            self._debug('Getting base data')
            if baseIndex.__class__ == tuple:
                baseValues = self.getData(baseIndex[0], baseMeth)
                baseX = self.getData(baseIndex[1])
            else:
                baseValues = self.getData(baseIndex, baseMeth)
                baseX = self.getXValues(baseIndex, index.column)
        else:
            baseValues = None
            baseX = None

        if values.dtype == numpy.dtype('object'):
            raise self._exception('Data shape is not rectangular')
        if baseValues is not None and baseValues.dtype == numpy.dtype('object'):
            raise self._exception('Base data shape is not rectangular')

        # check for base data, if we need it
        if method in ['diff', 'rel', 'rel_norm', 'diff_norm']:
            if baseIndex is None:
                raise self._exception('Base data needed for method: ' + str(method))

            # try interpolations
            if x is not None and baseValues.ndim > 0 and baseX is not None:
                # sort x and base values increasing
                sortX = numpy.argsort(x)
                x = x[sortX]
                sortBase = numpy.argsort(baseX)
                baseX = baseX[sortBase]
                baseValues = baseValues[sortBase]

                # interpolate
                baseValues = numpy.interp(x, baseX, baseValues)

                # undo sort
                baseValues = baseValues[numpy.argsort(sortBase)]

            elif x is None:
                self._warning('Cannot interpolate')

        # calculate difference and deviations
        values = self._calc(x, values, method, baseValues)

        return values

    def _calc(self, x, y, method, base_values):
        # decide what to do
        if method == 'value':  # normal value
            pass
        elif method == 'norm':
            # normalize value if necessary
            normMethod = self._getOption('normalize')
            if normMethod == 'avg':
                y /= y[~numpy.isnan(y)].mean()
            elif normMethod == 'max':
                y /= numpy.nanmax(y)
            elif normMethod == 'sum':
                y /= numpy.nansum(y)
            else:
                raise self._exception('Unknown normalize function {0}'.format(normMethod))
        elif method in ['diff', 'diff_norm']:  # difference
            y = y - base_values
        elif method in ['rel', 'rel_norm']:  # relative deviation
            y = (y - base_values) / base_values * 100
        elif method == 'grad':  # gradient
            y = (y[:-1] - y[1:]) / (x[:-1] - x[1:])
        else:
            raise self._exception('Unknown method ' + str(method))

        return y.squeeze()

    def _enchantX(self, x):
        x1 = x.copy()
        # little bit magic to assign new values to x
        # not working at the moment correctly, if x is int array
        x_new = (x[:-1] + x[1:]) / 2.0
        x.resize(x_new.size, refcheck=False)
        x[:] = x_new[:]

        return x1

    def getSteps(self, values, numSteps, method, zeroFix=False):
        """
        base funciton to get value levels for map plots
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
            if statistic.__class__ != StatisticData:
                raise self._exception('Wrong class for statistic {0}'.format(key))
                # if statistic.input.__class__ != list:
                #     raise self._exception('Statistic index must be a list for statistic {0}'.format(key))
                #
                # # test for column per statistic
                # if statistic.columns.__class__ != list:
                #     raise self._exception('Column list must be a list')
                # if statistic.columns == []:
                #    if self.columns != []:
                #        statistic.columns = list(self.columns)
                #    else:
                #        raise self._exception('No default and no statistic columns given for {0}'.format(key))
                # if statistic.weights == []:
                #     statistic.weights = [1/len(statistic.input)] * len(statistic.input)
