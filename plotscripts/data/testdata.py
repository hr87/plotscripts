"""
Created on Jul 16, 2013

@author: Hans R Hammer

A class providing dummy test data, either increasing or random
"""

import numpy
import random

from plotscripts.data.basedata import BaseData

class TestData(BaseData):
    def processClassData(self):
        pass

    def getClassData(self, index, meth='value', base=None, x=None):
        """
        creates dummmy data
        index: [type, num]

        type: rnd - random data, idx - increasing data
        num: number of data points
        """

        if len(index) < 2:
            raise self.exception('WTF, there are only two values necessary and you screwed it up')

        # get index
        num   = index[1]
        calc  = index[0]

        # init random generator
        random.seed()

        # create value array
        values = numpy.zeros((num))

        # fill it
        for idx in range(num):
            if calc == 'rnd':
                # get a random number
                values[idx] = random.random()
            else:
                values[idx] = idx

        return values