""" Module for statistics
"""

import numpy
import copy
import enum

from plotscripts.data.basedata import BaseData


class StatisticData(BaseData):
    """ Class to contain a statistic input
    :var input:
    :var weights:
    :var columns:
    :var method:
    :var basedata:
    """

    @enum.unique
    class Fields(enum.Enum):
        """ Enum class that holds all available statistics and the according calculations

        Add the calculation function in _calcMethods
        """
        avg = 0
        sum = 1
        min = 2
        max = 3
        variance = 4
        sigma = 5
        avgMin = 6
        avgMax = 7

    _calcMethods = {            # dict with all functions to calc statistic
        Fields.avg: lambda a, w: (w * a).mean(axis=0),
        Fields.sum: lambda a, w: a.sum(axis=0),
        Fields.min: lambda a, w: a.min(axis=0),
        Fields.max: lambda a, w: a.max(axis=0),
        Fields.variance: lambda a, w: (w * a).var(axis=0),
        Fields.sigma: lambda a, w: numpy.sqrt((w * a).var(axis=0)),
        Fields.avgMax: lambda a, w: (w * a).mean(axis=0) + numpy.sqrt((w * a).var(axis=0)),
        Fields.avgMin: lambda a, w: (w * a).mean(axis=0) - numpy.sqrt((w * a).var(axis=0))
    }

    class StatisticIndex(BaseData.Index):
        """ Class for a statistic index, used to retrieve data from a statistic
        :var name: statistic name
        :var field: statistic field, e.g. 'avg'
        :var weight: the weight for the average
        """
        def __init__(self):
            """ Constructor """
            super().__init__()
            self.name = None
            self.field = None

    def __init__(self, name):
        super().__init__()
        self.name      = name
        self.columns   = [None]
        self.method    = None
        self.basedata  = None

        # internal
        self._input     = []
        self._weights   = []
        self._data      = {}
        self.ref        = None

    def addInput(self, index, weight=1.0):
        """ Add an input to this statistic
        :param index: index object
        :return:
        """
        if not isinstance(index, self.Index):
            raise self._exception('Invalid index object "{0}"'.format(index))
        self._input.append(copy.deepcopy(index))
        self._weights.append(weight)

    def _processClassData(self):
        """
        function to calculate statistics
        """
        self._out('Preparing statistic "{0}"'.format(self.name))
        # set up weights
        self._weights = numpy.array(self._weights).reshape(len(self._weights), 1)
        # loop over all inputs
        try:
            for column in self.columns:
                tmpData = []
                for idx, index in enumerate(self._input):
                    if column is not None:
                        index.column = column
                    if self.method is not None:
                        index.method = self.method
                    tmpData.append(self.ref.getData(index, self.basedata, None))

                # convert to numpy array
                tmpData = numpy.array(tmpData)

                if tmpData.dtype == numpy.object:
                    raise self._exception('Data is not rectangular for statistic "{0}"'.format(self.name))

                # add values
                self._data[column] = {}
                for calc in self.Fields:
                    self._data[column][calc] = self._calcMethods[calc](tmpData, self._weights)

        except self.Exception as e:
            raise self._exception('Could not calculate statistic "{0}"'.format(self.name)) from e

    def _getClassData(self, index):
        """
        Method for getting precalculated data like statistics
        :param index: the search index for the data
        """
        try:
            columnData = self._data[index.column]
        except KeyError as e:
            raise self._exception('Unknown column "{0}" for statistics'.format(index.column)) from e
        try:
            return columnData[index.field]
        except KeyError as e:
            raise self._exception('Unknown field "{0}" for statistics'.format(index.field)) from e

    def _checkInput(self):
        """
        check the input and convert if necessary
        """
        # TODO complete check input
        # check statistic input
        if not self._input:
            raise self._exception('No input given for statistic "{0}"'.format(self.name))

        if self.columns is not None:
            if not self.columns.__class__ == list:
                raise self._exception('Columns must be a list')
        else:
            self.columns = [None]

    @staticmethod
    def index():
        return StatisticData.StatisticIndex()
