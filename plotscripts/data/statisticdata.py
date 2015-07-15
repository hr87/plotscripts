""" Module for statistics
"""

import numpy
from plotscripts.data.basedata import BaseData


class StatisticData(BaseData):
    """ Class to contain a statistic input
    :var input:
    :var weights:
    :var columns:
    :var method:
    :var basedata:
    """

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
        self.columns   = None
        self.method    = 'value'
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
        self._input.append(index)
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
                    if index.column is None:
                        index.column = column
                    tmpData.append(self.ref.getData(index, self.method, self.basedata, None))

                # convert to numpy array
                tmpData = numpy.array(tmpData)

                if tmpData.dtype == numpy.object:
                    raise self._exception('Data is not rectangular for statistic "{0}"'.format(self.name))

                # add values
                self._data[column] = {}
                self._data[column]['sum'] = tmpData.sum(axis=0)
                self._data[column]['avg'] = (tmpData * self._weights).mean(axis=0)
                self._data[column]['min'] = tmpData.min(axis=0)
                self._data[column]['max'] = tmpData.max(axis=0)
                self._data[column]['var'] = tmpData.var(axis=0)
                self._data[column]['sigma'] = numpy.sqrt(tmpData.var(axis=0))
                self._data[column]['avgMax'] = self._data[column]['avg'] + self._data[column]['sigma']
                self._data[column]['avgMin'] = self._data[column]['avg'] - self._data[column]['sigma']

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
