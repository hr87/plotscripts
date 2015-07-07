"""
Created on Apr 11, 2013

@author: Hans R Hammer
"""

import matplotlib.pyplot as plt
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

        self._defaults['dpi']         = 300
        self._defaults['format']      = 'svg'

    def getStyle(self, line):
        """
        Function to translate line object into necessary style strings
        """
        return ''

    def writeFile(self, path, filename, title, lines, column, method = 'value'):
        self._out('Creating plot {0}'.format(filename))

        # create figure
        fig = plt.figure()
        fig.set_dpi(self._options['dpi'])
        fig.set_size_inches(self._options['size'][0] / self._options['dpi']*5/1.5,
                            self._options['size'][1] / self._options['dpi']*5/1.5,
                            forward=True)

        axes = fig.add_subplot(1, 1, 1)

        idx = 0

        # plot graphs
        for line in lines:
            try:
                # get style
                style = self.getStyle(line)
                # plot data
                axes.plot(line.xValues, line.yValues, style, label = line.title)
            except ValueError as e:
                raise self._exception('Missmatching vector: x: {0}, y: {1}'.format(line.xValues.shape,
                                                                                  line.yValues.shape)) from e

            #TODO set configs
            idx += 1

        # set labels
        if self.xLabel == None :
            plt.xlabel(self.data.getXLabel(column))
        else :
            plt.xlabel(self.xLabel)

        if self.yLabel == None :
            plt.ylabel(self.data.getYLabel(column, method))
        else :
            plt.ylabel(self.yLabel)

        # set legend location
        axes.legend(loc = self._options['legendPos'])

        # set axis scale
        axes.set_xscale(self._options['xScale'])
        axes.set_yscale(self._options['yScale'])

        if self._options['grid'] != None:
            axes.grid(True, self._options['grid'])

        # set title
        if self._options['title']:
            plt.title(title)

        # save figure
        fig.savefig(path + filename, format = self._options['format'])
