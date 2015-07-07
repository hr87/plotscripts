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

        self.defaults['dpi']         = 300
        self.defaults['format']      = 'svg'

    def getStyle(self, line):
        """
        Function to translate line object into necessary style strings
        """
        return ''

    def writeFile(self, path, filename, title, lines, column, method = 'value'):
        self.out('Creating plot {0}'.format(filename))

        # create figure
        fig = plt.figure()
        fig.set_dpi(self.options['dpi'])
        fig.set_size_inches(self.options['size'][0] / self.options['dpi']*5/1.5,
                            self.options['size'][1] / self.options['dpi']*5/1.5,
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
                raise self.exception('Missmatching vector: x: {0}, y: {1}'.format(line.xValues.shape,
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
        axes.legend(loc = self.options['legendPos'])

        # set axis scale
        axes.set_xscale(self.options['xScale'])
        axes.set_yscale(self.options['yScale'])

        if self.options['grid'] != None:
            axes.grid(True, self.options['grid'])

        # set title
        if self.options['title']:
            plt.title(title)

        # save figure
        fig.savefig(path + filename, format = self.options['format'])
