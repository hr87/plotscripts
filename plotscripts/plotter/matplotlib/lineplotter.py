"""
Created on Apr 11, 2013

@author: Hans R Hammer
"""

import matplotlib.pyplot as plt
from plotscripts.plotter.baselineplotter import BaseLinePlotter, Line


class LinePlotter(BaseLinePlotter):
    """
    Basic plotter for two 2D plots using matplotlib
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        # add options
        self._addDefault('dpi', 300, 'plot resolution', 'private')
        self._addDefault('format', 'svg', 'plot file format', 'private')

    def getStyle(self, line):
        """ Function to translate line object into necessary style strings

        :param line: line object to translate
        :return keyword dict for pyplot.plot
        """
        colors = {Line.ColorList.auto: None,
                  Line.ColorList.red: 'r',
                  Line.ColorList.blue: 'b',
                  Line.ColorList.green: 'g',
                  Line.ColorList.yellow: 'y',
                  Line.ColorList.magenta: 'm',
                  Line.ColorList.cyan: 'c',
                  Line.ColorList.black: 'k'
                  }
        lineStyles = {Line.LineStyleList.none: 'None',
                      Line.LineStyleList.solid: '-',
                      Line.LineStyleList.dashed: '--',
                      Line.LineStyleList.pointed: ':',
                      Line.LineStyleList.dashpoint: '-.'
                      }
        markerStyles = {Line.MarkerStyleList.none: None,
                        Line.MarkerStyleList.dot: '.',
                        Line.MarkerStyleList.square: 's',
                        Line.MarkerStyleList.star: '*',
                        Line.MarkerStyleList.circle: 'o'}

        plotargs = {'label': line.title,
                    'linewidth': line.lineWidth,
                    'markersize': line.markerSize,
                    'marker': markerStyles[line.markerStyle],
                    'linestyle': lineStyles[line.lineStyle]
                    }
        if colors[line.color]:
            plotargs['color'] = colors[line.color]

        return plotargs

    def writeFile(self, path, filename, title, lines, column, method = 'value'):
        self._out('Creating plot {0}'.format(filename))

        # create figure
        fig = plt.figure()
        fig.set_dpi(self._getOption('dpi'))
        fig.set_size_inches(self._getOption('size')[0] / self._getOption('dpi')*5/1.5,
                            self._getOption('size')[1] / self._getOption('dpi')*5/1.5,
                            forward=True)

        axes = fig.add_subplot(1, 1, 1)

        idx = 0

        # plot graphs
        for line in lines:
            try:
                # get style
                style = self.getStyle(line)
                # plot data
                axes.plot(line.xValues, line.yValues, **style)
            except ValueError as e:
                raise self._exception('Mismatching vector: x: {0}, y: {1}'.format(line.xValues.shape,
                                                                                  line.yValues.shape)) from e
            idx += 1

        # set labels
        if self.xLabel is None:
            plt.xlabel(self._data.getXLabel(column))
        else:
            plt.xlabel(self.xLabel)

        if self.yLabel is None:
            plt.ylabel(self._data.getYLabel(column, method))
        else:
            plt.ylabel(self.yLabel)

        # set legend location
        axes.legend(loc = self._getOption('legendPos'))

        # set axis scale
        axes.set_xscale(self._getOption('xScale'))
        axes.set_yscale(self._getOption('yScale'))

        if self._getOption('grid') is not None:
            axes.grid(True, self._getOption('grid'))

        # set title
        if self._getOption('title'):
            plt.title(title)

        # save figure
        fig.savefig(path + filename, format = self._getOption('format'))
