"""
Created on Mar 7, 2014

@author: Hans R Hammer
"""

from plotscripts.data.basedata import BaseData
from plotscripts.base.exception import PlotscriptException

class MultiDataSet(BaseData):
    """ Allows to handle multiple data sets
    """
    def __init__(self):
        """ Constructor """
        super().__init__()
        self._dataSets = {}

    def addDataSet(self, name, dataClass):
        """

        :param name:
        :param dataClass:
        :return: reference to data set
        """
        if not issubclass(dataClass, BaseData):
            self._error(dataClass.__name__ + 'is not a valid data set')
        newData = dataClass()
        self._dataSets[name] = newData
        return newData

    def _processClassData(self):
        for name, dataSet in self._dataSets.items():
            try:
                dataSet.copyOptions(self._options)
                dataSet.processData()
                self.getOptions(dataSet)
            except PlotscriptException as e:
                raise self._exception('Could not process file {0}'.format(name)) from e

    def getClassData(self, index, method='value', base=None, x=None):
        key = index[0]
        fileIndex = index[1:]

        try:
            values = self._dataSets[key].getClassData(fileIndex, method, base, x)
        except KeyError:
            raise self._exception('Could not find {0}'.format(key))
        except PlotscriptException as e:
            raise self._exception('Error fetching data from {0}'.format(key)) from e

        return values

    def _checkInput(self):
        super()._checkInput()

        for name, dataSet in self._dataSets.items():
            if not issubclass(dataSet.__class__, BaseData):
                raise self._exception('{0} is not a compatible data set'.format(name))

            try:
                dataSet._checkInput()
            except PlotscriptException as e:
                raise self._exception('Error in file {0}'.format(name)) from e
