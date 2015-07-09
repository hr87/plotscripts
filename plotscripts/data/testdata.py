"""
Created on Jul 16, 2013

@author: Hans R Hammer

A class providing dummy test data, either increasing or random
"""

import numpy
import random

from plotscripts.data.basedata import BaseData


class TestData(BaseData):
    def _processClassData(self):
        pass

    def _getClassData(self, index, method='value', base=None, x=None):
        """
        creates dummmy data
        index: [type, num]

        type: rnd - random data, idx - increasing data
        num: number of data points
        """

        if len(index) < 2:
            raise self._exception('WTF, there are only two values necessary and you screwed it up')

        # get index
        num   = index[1]
        calc  = index[0]

        # init random generator
        random.seed()

        # create value array
        values = numpy.zeros(num)

        # fill it
        for idx in range(num):
            if calc == 'rnd':
                if len(index) == 2:
                    # get a random number
                    values[idx] = random.random()
                elif len(index) == 3:
                    values[idx] = random.uniform(0, index[2])
                else:
                    values[idx] = random.uniform(index[2], index[3])
            elif calc == 'num':
                values[idx] = idx
            else:
                raise self._exception('Unknown calculation type {0}'.format(calc))

        return values
