"""
Created on Apr 11, 2013

@author: Hans R Hammer
"""

from plotscripts.base.baseobject import BaseObject
from plotscripts.base.basecontainer import BaseContainer
from plotscripts.plotter.util.functions import axisDiv

import math
import numpy

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
    class Statistic(BaseContainer):
        """ Class to contain a statistic input
        :var input:
        :var weights:
        :var columns:
        :var method:
        :var basedata:
        """
        def __init__(self):
            super().__init__()
            self.input     = []
            self.weights   = []
            self.columns   = []
            self.method    = 'value'
            self.basedata  = None

            # internal
            self._sum      = {}
            self._avg      = {}
            self._stdDeviation = {}
            self._min      = {}
            self._max       = {}

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.xSteps     = []             # list for xValues

        self.xLabel     = ''
        self.yLabel     = ''

        self.statistics = {}             # index input for statistics views
        self.columns   = []              # columns to prepare statistics for

        self.defaults['normalize']    = 'max'   # normalization, sum | avg | max

        # internal
        self.data       = {}             # data storage



    def processData(self):
        """
        base method for data processing, called by inputArgs
        """
        self.out('Processing data')

        self.activateDefaults()
        # check the input
        self.checkInput()

        # call data executioner process method
        self.processClassData()

        # prepare statistics
        self.calcSpecialData()


    def processClassData(self):
        """ Virtual method to be overwritten by the implementation
        :return: None
        """
        raise self.exception('Data processing not implemented yet')

    def calcSpecialData(self):
        """
        function to calculate statistics
        """
        self.out('Preparing statistics')
        # loop over all inputs
        for key, statistic in self.statistics.items():
            try:
                for column in statistic.columns:
                    for idx, index in enumerate(statistic.input):
                        index = list(index) + [column]
                        tmpData = self.getData(index, statistic.method, statistic.basedata, None)
                        #TODO catch exceptions
                        # check for first data and create numpy array
                        if not column in statistic.avg:
                            statistic.avg[column] = numpy.zeros(tmpData.shape)
                            statistic.sum[column] = numpy.zeros(tmpData.shape)
                            statistic.min[column] = numpy.zeros(tmpData.shape)
                            statistic.max[column] = numpy.zeros(tmpData.shape)


                        # add values
                        statistic.sum[column] += tmpData
                        statistic.avg[column] += statistic.weights[idx] * tmpData
                        statistic.min[column] = numpy.minimum(statistic.min[column], tmpData)
                        statistic.max[column] = numpy.maximum(statistic.max[column], tmpData)

                    # create std deviation array
                    statistic.stdDeviation[column] = numpy.zeros(statistic.avg[column].shape)

                    # calculate std deviation
                    for index in statistic.input:
                        index = list(index) + [column]
                        tmpData = self.getData(index, 'value', None, None)
                        statistic.stdDeviation[column] += (statistic.avg[column] - tmpData)**2

                    # sqrt
                    statistic.stdDeviation[column] = numpy.sqrt(statistic.stdDeviation[column])
            except self.Exception as e:
                raise self.exception('Could not calculat statistic {0}'.format(key)) from e


    def getSpecialData(self, index):
        """
        Method for getting precalculated data like statistics
        """

        # no statistic
        if not index[0] in self.statistics:
            return False, None
        if len(index) < 3:
            raise self.exception('Index to short for statistics: {0}'.format(index))

        # get column
        column = index[-1]


        try:
            if index[1] == 'avg':
                return True, self.statistics[index[0]].avg[column]
            elif index[1] == 'sum':
                return True, self.statistics[index[0]].sum[column]
            elif index[1] == 'min':
                return True, self.statistics[index[0]].min[column]
            elif index[1] == 'max':
                return True, self.statistics[index[0]].max[column]
            elif index[1] == 'stdDeviation':
                return True, self.statistics[index[0]].stdDeviation[column]
            elif index[1] == 'avgMax':
                if len(index) > 3:
                    factor = index[2]
                else:
                    factor = 1
                return True, self.statistics[index[0]].avg[column] + factor * self.statistics[index[0]].stdDeviation[column]
            elif index[1] == 'avgMin':
                if len(index) > 3:
                    factor = index[2]
                else:
                    factor = 1
                return True, self.statistics[index[0]].avg[column] - factor * self.statistics[index[0]].stdDeviation[column]
        except KeyError as e:
            raise self.exception('Unknown key for statistics') from e
        except IndexError as e:
            raise self.exception('Wrong index for statistics') from e

        return False, None

    def getData(self, index, meth='value', base=None, x=None):
        """
        Get the data out of the database

        methods available are:
        value (default)
        diff (base needed)
        rel (base needed)
        grad () gradient of data, x values changed

        @param index: list with index of data
        @param meth: method for data processing, default = value
        @param base: list with index for base data needed for some methods, default = None
        @param x: x values for some methods, may be changed, default = None
        @return: numpy array with data
        """

        # check the length of index
        self.debug('Getting data for {0} {1}; base {2}'.format(index, meth, base))

        column = index[-1]

        # check and get special data
        check, values = self.getSpecialData(index)

        # we need to get data from the database
        if not check:
            # get normalized data
            if meth in ['rel_norm', 'diff_norm']:
                values = self.getData(index, 'norm', None)
            else:
                values = self.getClassData(index)

        if meth == 'grad':
            if x == None :
                raise self.exception('x values needed for gradient')
            x = self.enchantX(x)

            # which type of base data
        if meth in ['rel_norm', 'diff_norm']:
            baseMeth = 'norm'
        else:
            baseMeth = 'value'

        # try to get data and base data
        if base != None :
            self.debug('Getting base data')
            if base.__class__ == tuple:
                baseValues = self.getData(list(base[1]) + [column], baseMeth)
                baseX = self.getData(base[0])
            else:
                baseValues = self.getData(list(base) + [column], baseMeth)
                baseX = self.getXValues(base, column)
        else:
            baseValues = None

        if values.dtype == numpy.dtype('object'):
            raise self.exception('Data shape is not rectangular')
        if baseValues != None and baseValues.dtype == numpy.dtype('object'):
            raise self.exception('Base data shape is not rectangular')

        # check for base data, if we need it
        if meth in ['diff', 'rel', 'rel_norm', 'diff_norm'] :
            if base == None :
                raise self.exception('Base data needed for method: ' + str(meth))

            # try interpolations
            if x != None and baseValues.ndim > 0 and baseX != None:
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

            elif x == None:
                self.warning('Cannot interpolate')

        # calculate difference and deviations
        values = self.calc(x, values, meth, baseValues)

        return values

    def calc(self, x, y, meth, base_values):
        # decide what to do
        if meth == 'value':     # normal value
            pass
        elif meth == 'norm' :
            # normalize value if necessary
            if self.options['normalize'] == 'avg':
                y /= y[~numpy.isnan(y)].mean()
            elif self.options['normalize'] == 'max':
                y /= numpy.nanmax(y)
            elif self.options['normalize'] == 'sum':
                y /= numpy.nansum(y)
            else:
                raise self.exception('Unknown normalize function {0}'.format(self.options['normalize']))
        elif meth in ['diff', 'diff_norm'] :           # difference
            y = y - base_values
        elif meth in ['rel', 'rel_norm'] :             # relative deviation
            y = (y - base_values) / base_values * 100
        elif meth == 'grad' :           # gradient
            y = (y[:-1] - y[1:]) / (x[:-1] - x[1:])
        else :
            raise self.exception('Unknown method ' + str(meth))

        return y.squeeze()

    def enchantX(self, x):
        x1 = x.copy()
        # little bit magic to assign new values to x
        # not working at the moment correctly, if x is int array
        x_new = (x[:-1] + x[1:]) / 2.0
        x.resize(x_new.size, refcheck = False)
        x[:] = x_new[:]

        return x1

    def getSteps(self, values, numSteps, method, zeroFix = False):
        """
        base funciton to get value levels for map plots
        round to next nice level
        @param values: ndarray of values to calculate steps for
        @param numSteps: number of Steps
        @return: array with step values
        """
        valuesMax = numpy.nanmax(values)
        valuesMin = numpy.nanmin(values)

        # getting some stuff
        valuesRange = valuesMax - valuesMin                           # value range on axis
        if (not numpy.isnan(valuesRange) and valuesRange > 0):
            mag         = 10 ** (math.floor(math.log10(valuesRange)))    # magnitude of axis values
        elif not numpy.isnan(valuesRange) and valuesMax != 0:
            mag         = 10 ** (math.floor(math.log10(numpy.abs(valuesMax))))
            valuesMax = valuesMax + 1 * mag
            valuesMin = valuesMax - 1 * mag
        else:
            mag = 1
            valuesMax = 1
            valuesMin = -1

        valuesDiv   = axisDiv(valuesRange, mag)            # divider for axis

        # rescale values to rounded values
        mag    = mag / valuesDiv
        valuesMax    = math.ceil(valuesMax / mag) * mag
        valuesMin    = math.floor(valuesMin / mag) * mag

        # middle zeroFix
        if zeroFix == 'middle':
            if abs(valuesMax) > abs(valuesMin):
                valuesMin = valuesMax
            else:
                valuesMax = valuesMin
                # replace value nearer to zero with zero
        elif zeroFix:
            if valuesMax > 0 and valuesMin < 0:
                raise self.exception('Fixed zero not possible')
            elif valuesMax <= 0:
                valuesMax = 0
            elif valuesMin >= 0:
                valuesMin = 0

        return numpy.linspace(valuesMin, valuesMax, numSteps+1, True)


    def getXValues(self, index, column) :
        """
        get standard x values
        @return: numpy array with x values
        """
        if self.xSteps == None or self.xSteps == []:
            # self.warning('No x values available')
            return None

        return self.xSteps.copy()

    def getXLabel(self, column):
        """
        get x label for data
        @return: label as string
        """
        return self.xLabel

    def getYLabel(self, column, method = 'value'):
        """
        get y label for data
        @return: label as string
        """
        if self.yLabel == '' :
            return column
        else :
            return self.yLabel


    def checkInput(self):
        """
        check the input and convert if necessary
        """
        # test for files
        #if self.file == {} :
        #   raise self.exception('No data files')

        if self.xSteps != [] :
            self.xSteps = numpy.array(self.xSteps)

        # check statistic input
        # check dict
        if not self.statistics.__class__ == dict:
            raise self.exception('Statistics must be a dictionary!')

        if not self.columns.__class__ == list:
            raise self.exception('Columns must be a list')

        for key, statistic in self.statistics.items():
            if statistic.__class__ != self.Statistic:
                raise self.exception('Wrong class for statistic {0}'.format(key))
            if statistic.input.__class__ != list:
                raise self.exception('Statistic index must be a list for statistic {0}'.format(key))

            # test for column per statistic
            if statistic.columns.__class__ != list:
                raise self.exception('Column list must be a list')
            if statistic.columns == []:
                if self.columns != []:
                    statistic.columns = list(self.columns)
                else:
                    raise self.exception('No default and no statistic columns given for {0}'.format(key))
            if statistic.weights == []:
                statistic.weights = [1/len(statistic.input)] * len(statistic.input)