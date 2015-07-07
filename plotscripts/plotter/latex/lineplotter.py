"""
Created on Mar 7, 2014

@author: Hans R Hammer
"""

from plotscripts.plotter.baselineplotter import BaseLinePlotter

class LinePlotter(BaseLinePlotter):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()

    def getStyle(self, line):
        """
        Function to translate line object into necessary style strings
        """
        return ''

    def writeFile(self, path, filename, title, lines, column, method = 'value'):
        self.out('Creating plot {0}'.format(filename))

        # open file
        try :
            texFile = open(path + '/' + filename + '.tex', 'w')
        except IOError as e:
            raise self.exception('Could not open file ' + filename ) from e