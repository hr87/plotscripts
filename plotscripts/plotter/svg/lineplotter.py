"""
Created on Apr 11, 2013

@author: hammhr
"""

import os
from plotscripts.plotter.baselineplotter import BaseLinePlotter

class LinePlotter(BaseLinePlotter):
    """
    Basic plotter for two 2D plots
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

    def plot(self) :
        # test for input
        self._checkInput()

        for method in self.method :
            # create path
            path = self._cleanPath('/{0}/{1}/'.format(self.title, method))

            # create dir for output
            try :
                os.makedirs(path, exist_ok=True)
            except OSError as e:
                raise self._exception('Could not create directory ' + path ) from e

            for column in self.column :
                # open file
                filename = self._cleanFileName('{0}_{1}_{2}'.format(self.title, method, column)) + '.svg'
                try :
                    f_plot = open(path + filename, 'w')
                except IOError as e:
                    raise self._exception('Could not open file ' + filename ) from e

                try :
                    # write svg header
                    self.writeHead(f_plot)

                    for datakey in self.input :
                        # get arrays
                        values = self._data.getData(datakey, column, method, self.basedata)
                        self.writeData(f_plot, values)

                        # write legend
                    self.writeLegend(f_plot)

                    #write axis
                    self.writeAxix(f_plot)

                except IOError as e:
                    raise self._exception('Error writing file ' + filename ) from e
                finally:
                    f_plot.close()

    def writeHead(self, f_plot) :
        f_plot.write('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n\
               <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" \
               "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
        f_plot.write('<svg width="{0}" height="{1}" viewBox = "0 0 {0} {1}" \
               version = "1.1">\n')

    def writeData(self, f_plot, values):
        pass

    def writeAxix(self, f_plot) :
        f_plot.write('</svg>\n')

    def writeLegend(self, f_plot):
        pass
