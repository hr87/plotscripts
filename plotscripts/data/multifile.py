"""
Created on Mar 7, 2014

@author: Hans R Hammer
"""

from plotscripts.data.basedata import BaseData
from plotscripts.base.exception import PlotscriptException

class MultiFile(BaseData):
    def __init__(self):
        super().__init__()

        self.files = {};


def processClassData(self):
    for name, currentFile in self.files.items():
        try:
            currentFile.setOptions(self.options)
            currentFile.processData()
            self.getOptions(currentFile)
        except PlotscriptException as e:
            raise self.exception('Could not process currentFile for file {0}'.format(name)) from e

def getClassData(self, index, meth='value', base=None, x=None):
    key = index[0]
    fileIndex = index[1:]

    try:
        values = self.files[key].getClassData(fileIndex, meth, base, x)
    except KeyError:
        raise self.exception('Could not find {}'.format(key))
    except PlotscriptException as e:
        raise self.exception('Error fetching data from {}'.format(key)) from e

    return values

def checkInput(self):
    super().checkInput()

    for name, executioner in self.files.items():
        if not issubclass(executioner.__class__, BaseData):
            raise self.exception('{0} is not a campatible data executioner'.format(name))

        try:
            executioner.checkInput()
        except PlotscriptException as e:
            raise self.exception('Error in file {0}'.format(name)) from e

