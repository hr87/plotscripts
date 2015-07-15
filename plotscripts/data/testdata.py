"""
Created on Jul 16, 2013

@author: Hans R Hammer

A class providing dummy test data, either increasing or random
"""

import numpy
import numpy.random

from plotscripts.data.basedata import BaseData


class TestData(BaseData):
    def __init__(self):
        super().__init__()

    class TestIndex(BaseData.Index):
        """ Index class for TestData
        :var calcType: calculation type, 'num' or 'rnd'
        :var num: number of elements
        :var min: minimal value
        :var max: maximal value, 'rnd' only
        :var step: step size for num only
        """
        def __init__(self):
            """ Constructor """
            super().__init__()
            self.calcType = None
            self.num = None
            self.min = 0
            self.max = 1
            self.step = 1

    @staticmethod
    def index():
        """ Create a test data index
        :return: index object
        """
        return TestData.TestIndex()

    def _processClassData(self):
        pass

    def _getClassData(self, index, method='value', base=None, x=None):
        """
        creates dummy data
        index: [type, num]

        type: rnd - random data, idx - increasing data
        num: number of data points
        """

        # get index
        try:
            # fill it
            if index.calcType == 'rnd':
                values = numpy.random.uniform(index.min, index.max, index.num)
            elif index.calcType == 'num':
                maxValue = index.min + index.num * index.step
                values = numpy.arange(index.min, maxValue, index.step)
            else:
                raise self._exception('Unknown calculation type {0}'.format(index.calcType))
        except IndexError:
            raise self._exception('Invalid index "{0}"'.format(index))

        return values
