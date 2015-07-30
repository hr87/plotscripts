"""
Created on Apr 24, 2013

@author: Hans R Hammer
"""

from plotscripts.plotter.basemapplotter import BaseMapPlotter as BaseMap
from plotscripts.plotter.util.colormap import Colormap
from plotscripts.plotter.util.axis import Axis

import math


class MapPlotter(BaseMap):
    """
    classdocs
    """

    def __init__(self, name):
        """
        Constructor
        """
        super().__init__(name)
        self._addDefault('lineWidth', 0.5, 'width of frame lines', 'private')
        self._addDefault('stroke', None, 'stroke color for data fields', 'private')
        self._addDefault('strokeWidth', 1, 'strocke width', 'private')
        self._addDefault('overlayWidth', 1, 'overlay stroke width', 'private')

        # setting for text overlay
        self._addDefault('text_lim_low', 0.01, 'lower limit for value format strings', 'private')
        self._addDefault('text_lim_mid', 1, 'middle limit for value format strings', 'private')
        self._addDefault('text_lim_up', 1000, 'upper limit for value format strings', 'private')

        self._addDefault('text_for_low', '{0:.2e}', 'lower value format string', 'private')
        self._addDefault('text_for_mlow', '{0:.1f}', 'lower middle value format string', 'private')
        self._addDefault('text_for_mup', '{0:.2f}', 'upper middle value format string', 'private')
        self._addDefault('text_for_up', '{0:.2e}', 'upper value format string', 'private')

        # setting for axis and legend
        self._addDefault('leg_lim_low', 0.01, 'lower limit for value format strings', 'private')
        self._addDefault('leg_lim_mid', 1, 'middle limit for value format strings', 'private')
        self._addDefault('leg_lim_up', 1e4, 'upper limit for value format strings', 'private')

        self._addDefault('leg_for_low', '{0:.2e}', 'lower value format string', 'private')
        self._addDefault('leg_for_mlow', '{0:g}', 'lower middle value format string', 'private')
        self._addDefault('leg_for_mup', '{0:g}', 'upper middle value format string', 'private')
        self._addDefault('leg_for_up', '{0:.2e}', 'upper value format string', 'private')

    def writeFile(self, path, filename, values, lvls, assign, title=None):
        self._out('Writing file {0}'.format(filename))
        # setting up some vars
        pos_title       = [0.5, 0.03]
        pos_x_label     = 0.98
        pos_y_label     = 0.02
        pos_x_tics      = 0.95
        pos_y_tics      = 0.08
        pos_cb_labels   = 0.02

        # setting up axis
        x_size          = self._getOption('size')[0]
        y_size          = self._getOption('size')[1]

        xAxis           = Axis(x_size, 0.1, 0.75, 0.0125)
        yAxis           = Axis(y_size, 0.1, 0.9, 0.0125, True)

        # get necessary points from geometry
        valuePaths     = self._geometry.getValuePaths()
        overlayPaths   = self._geometry.getOverlayPaths()
        textPoints     = self._geometry.getTextPoints()
        pathTypes      = self._geometry.getPathTypes()
        overlayTypes   = self._geometry.getOverlayTypes()

        # select assignment
        if assign != []:
            try:
                valuePaths  = valuePaths[assign, :, :]
                textPoints  = textPoints[assign, :]
                pathTypes   = [pathTypes[idx] for idx in assign]
            except IndexError as e:
                raise self._exception('Wrong assignment to blocks') from e

        if values.shape[0] != valuePaths.shape[0]:
            values = values.T
            # try transposed values
            if values.shape[0] != valuePaths.shape[0]:
                raise self._exception('Non matching number of values for geometry. Values {0}, geometry {1}'
                                      .format(values.T.shape, valuePaths.shape[0]))

        if self._getOption('extrema') == []:
            # get extrema with or without the nan regions
            if self._getOption('nanRegions'):
                extrema = self._geometry.getExtrema(valuePaths, None)
            else:
                extrema = self._geometry.getExtrema(valuePaths, values)

            if self._getOption('sameExtrema'):
                extrema[0] = min(extrema[0], extrema[2])
                extrema[1] = max(extrema[1], extrema[3])
                extrema[2] = extrema[0]
                extrema[3] = extrema[1]
        else:
            extrema = self._getOption('extrema')

        xAxis.setAxis(extrema[0], extrema[1])
        yAxis.setAxis(extrema[2], extrema[3])

        # set up color map
        colormap = Colormap(self._getOption('colormap'))
        colormap.create(lvls)
        colormap.setupGeometry([0.83, 0.1], [0.88, 0.9], 0.0125)

        # font size
        #TODO get scale from axis
        fontSize = self._getOption('fontSize')
        mapFontSize = self._getOption('mapFontSize')
        fontOffset = fontSize / 4
        if mapFontSize <= 0:
            self._warning('Map font size = {0}, setting to 1!'.format(mapFontSize))
            mapFontSize = 1

        # scale points
        valuePaths[:, 0, :] = xAxis.convertPoints(valuePaths[:, 0, :])
        valuePaths[:, 1, :] = yAxis.convertPoints(valuePaths[:, 1, :])
        overlayPaths[:, 0, :] = xAxis.convertPoints(overlayPaths[:, 0, :])
        overlayPaths[:, 1, :] = yAxis.convertPoints(overlayPaths[:, 1, :])
        textPoints[:, 0] = xAxis.convertPoints(textPoints[:, 0])
        textPoints[:, 1] = yAxis.convertPoints(textPoints[:, 1])

        # open file
        try :
            svgFile = open(path + '/' + filename + '.svg', 'w')
        except IOError as e:
            raise self._exception('Could not open file ' + filename + '.svg' ) from e

        # write file
        try:
            # write header
            svgFile.write('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n\
              <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" \
              "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
            svgFile.write('<svg  xmlns="http://www.w3.org/2000/svg" \nwidth="{0}" height="{1}" viewBox = "0 0 {0} {1}" version = "1.1">\n'
                          .format(x_size, y_size))

            # plot data
            svgFile.write('<g id="data">\n')
            for idx in range(values.shape[0]):
                color = colormap.getColor(values[idx])

                tmpStr = self.createPath(pathTypes[idx], valuePaths[idx, :, :], color,
                                         self._getOption('stroke'), self._getOption('strokeWidth'))

                svgFile.write(tmpStr)
            svgFile.write('</g>\n')

            # write overlay
            if self._getOption('overlay'):
                svgFile.write('<g id="overlay">\n')
                for idx in range(overlayPaths.shape[0]):
                    color = colormap.getOverlayColor()

                    tmpStr = self.createPath(overlayTypes[idx], overlayPaths[idx, :, :],
                                             None, color, self._getOption('overlayWidth'))

                    svgFile.write(tmpStr)
                svgFile.write('</g>\n')

            # write text overlay
            if self._getOption('overlayText'):
                svgFile.write('<g id="overlay_text">\n')
                for idx in range(textPoints.shape[0]):
                    if not math.isnan(values[idx]):
                        color = colormap.getTextColor(values[idx])
                        value = self.formatValue('text', values[idx])
                        textStr = '<text x="{0:.0f}" y="{1:.0f}" font-size = "{2}" text-anchor="middle" fill="rgb({3}, {4}, {5})">{6}</text>\n'.format(
                            textPoints[idx, 0], textPoints[idx, 1] + fontOffset,
                            mapFontSize,
                            color[0], color[1], color[2],
                            value)

                        svgFile.write(textStr)
                svgFile.write('</g>\n')

            # write title
            if self._getOption('title') and title is not None:
                tmpStr = '<text x="{0:.0f}" y="{1:.0f}" font-size = "{2}" text-anchor="middle" fill="black">{3}</text>\n'.format(
                    pos_title[0] * x_size,
                    pos_title[1] * y_size + fontOffset,
                    fontSize,
                    title)
                svgFile.write(tmpStr)

            # write x axis tics
            tics        = xAxis.getTics()
            ticPos      = xAxis.getTicPos()
            ticStart    = yAxis.getStart()
            ticEnd      = ticStart + xAxis.tic_length * yAxis.size
            ticStart2   = yAxis.getEnd()
            ticEnd2     = ticStart2 - xAxis.tic_length * yAxis.size

            svgFile.write('<g id="axis">\n')
            for idx in range(tics.shape[0]):
                tmpStr = '<path d = "M {0:.0f} {1:.0f} L {2:.0f} {3:.0f}" stroke = "black" stroke-width = "{4}" fill = "none"/>\n'.format(
                    ticPos[idx], ticStart,
                    ticPos[idx], ticEnd,
                    self._getOption('lineWidth'))
                svgFile.write(tmpStr)
                tmpStr = '<path d = "M {0:.0f} {1:.0f} L {2:.0f} {3:.0f}" stroke = "black" stroke-width = "{4}" fill = "none"/>\n'.format(
                    ticPos[idx], ticStart2,
                    ticPos[idx], ticEnd2,
                    self._getOption('lineWidth'))
                svgFile.write(tmpStr)

                value = self.formatValue('leg', tics[idx])
                tmpStr = '<text x="{0:.0f}" y="{1:.0f}" font-size = "{2}" text-anchor="middle">{3}</text>\n'.format(
                    ticPos[idx], pos_x_tics * yAxis.size,
                    fontSize,
                    value)
                svgFile.write(tmpStr)

            # write y axis tics
            tics        = yAxis.getTics()
            ticPos      = yAxis.getTicPos()
            ticStart    = xAxis.getStart()
            ticEnd      = ticStart + yAxis.tic_length * xAxis.size
            ticStart2   = xAxis.getEnd()
            ticEnd2     = ticStart2 - yAxis.tic_length * xAxis.size

            for idx in range(tics.shape[0]):
                tmpStr = '<path d = "M {0:.0f} {1:.0f} L {2:.0f} {3:.0f}" stroke = "black" stroke-width = "{4}" fill = "none"/>\n'.format(
                    ticStart, ticPos[idx],
                    ticEnd, ticPos[idx],
                    self._getOption('lineWidth'))
                svgFile.write(tmpStr)
                tmpStr = '<path d = "M {0:.0f} {1:.0f} L {2:.0f} {3:.0f}" stroke = "black" stroke-width = "{4}" fill = "none"/>\n'.format(
                    ticStart2, ticPos[idx],
                    ticEnd2, ticPos[idx],
                    self._getOption('lineWidth'))
                svgFile.write(tmpStr)

                value = self.formatValue('leg', tics[idx])
                tmpStr = '<text x="{0:.0f}" y="{1:.0f}" font-size = "{2}" text-anchor="middle">{3}</text>\n'.format(
                    pos_y_tics * yAxis.size, ticPos[idx] + fontOffset,
                    fontSize,
                    value)
                svgFile.write(tmpStr)

            # write axis frame
            tmpStr = '<path d = "M {0:.0f} {1:.0f} L {2:.0f} {1:.0f} L {2:.0f} {3:.0f} L {0:.0f} {3:.0f} L {0:.0f} {1:.0f}" stroke = "black" stroke-width = "{4}" fill = "none"/>\n'.format(
                xAxis.getStart(), yAxis.getStart(),
                xAxis.getEnd(), yAxis.getEnd(),
                self._getOption('lineWidth'))

            svgFile.write(tmpStr)

            # write axis label
            tmpStr = '<text x="{0:.0f}" y="{1:.0f}" font-size = "{2}" text-anchor="middle">{3}</text>\n'.format(
                xAxis.mid * xAxis.size,
                pos_x_label * yAxis.size,
                fontSize,
                self._geometry.getXLabel())

            svgFile.write(tmpStr)

            tmpStr = '<text x="{1:.0f}" y="{0:.0f}" font-size = "{2}" text-anchor="middle" transform="rotate(-90)">{3}</text>\n'.format(
                pos_y_label * xAxis.size,
                -yAxis.mid * yAxis.size,
                fontSize,
                self._geometry.getYLabel())

            svgFile.write(tmpStr)
            svgFile.write('</g>\n')

            # write color bar
            svgFile.write('<g id="colorbar">\n')
            for idx in range(colormap.numSteps):
                tmpStr = '<path d = "M {0:.0f} {1:.0f} L {2:.0f} {1:.0f} L {2:.0f} {3:.0f} L {0:.0f} {3:.0f} L {0:.0f} {1:.0f}" stroke = "none" fill = "rgb({4:.0f}, {5:.0f}, {6:.0f})"/>\n'.format(
                    colormap.xStart * x_size,
                    colormap.positions[idx] * y_size,
                    colormap.xEnd * x_size,
                    colormap.positions[idx + 1] * y_size,
                    colormap.colors[colormap.numSteps - idx - 1, 0],
                    colormap.colors[colormap.numSteps - idx - 1, 1],
                    colormap.colors[colormap.numSteps - idx - 1, 2])

                svgFile.write(tmpStr)

            # write color bar tics
            for idx in range(colormap.numLabels + 1):
                tmpStr = '<path d = "M {0:.0f} {1:.0f} L {2:.0f} {1:.0f} " stroke = "black" stroke-width = "{3}" fill = "none"/>\n'.format(
                    colormap.xStart * x_size,
                    colormap.legendPos[idx] * y_size,
                    (colormap.xStart + colormap.ticLength) * x_size,
                    self._getOption('lineWidth'))
                svgFile.write(tmpStr)

                tmpStr = '<path d = "M {0:.0f} {1:.0f} L {2:.0f} {1:.0f} " stroke = "black" stroke-width = "{3}" fill = "none"/>\n'.format(
                    (colormap.xEnd  - colormap.ticLength) * x_size,
                    colormap.legendPos[idx] * y_size,
                    colormap.xEnd * x_size,
                    self._getOption('lineWidth'))
                svgFile.write(tmpStr)

            # legend
            for idx in range(colormap.numLabels + 1):
                value = self.formatValue('leg', colormap.labels[colormap.numLabels - idx])
                tmpStr = '<text x="{0:.0f}" y="{1:.0f}" font-size = "{2}" text-anchor="start">{3}</text>\n'.format(
                    (colormap.xEnd + pos_cb_labels) * x_size,
                    colormap.legendPos[idx] * y_size + fontOffset,
                    fontSize,
                    value)
                svgFile.write(tmpStr)

            # write color bar frame
            tmpStr = '<path d = "M {0:.0f} {1:.0f} L {2:.0f} {1:.0f} L {2:.0f} {3:.0f} L {0:.0f} {3:.0f} L {0:.0f} {1:.0f}" stroke = "black" stroke-width = "{4}" fill = "none"/>\n'.format(
                colormap.xStart * x_size,
                colormap.yStart * y_size,
                colormap.xEnd * x_size,
                colormap.yEnd * y_size,
                self._getOption('lineWidth'))

            svgFile.write(tmpStr)
            svgFile.write('</g>\n')

            # close tag
            svgFile.write('</svg>\n')

        except IOError as e:
            raise self._exception('Error writing file ' + filename ) from e
        finally:
            # close file
            svgFile.close()

    def createPath(self, pathType, path, color, strokeColor, width):
        # get path type
        if  pathType == 'path':
            # write beginning of path
            tmpStr = '<path d = "M {0:.0f} {1:.0f}'.format(path[0, 0],
                                                           path[1, 0])

            # writing points
            for idx2 in range(1, path.shape[1]):
                # test for more points
                if math.isnan(path[0, idx2]):
                    break
                tmpStr += ' L {0:.0f} {1:.0f}'.format(path[0, idx2],
                                                      path[1, idx2])

            tmpStr += '"'

        # circle
        elif pathType == 'circle':
            # calc radius
            tmp = path[:, 0] - path[:, 1]
            radius = math.sqrt(tmp[0]**2 + tmp[1]**2)
            tmpStr = '<circle cx="{0}" cy="{1}" r="{2}"'.format(path[0, 0], path[1, 0], radius)
        elif pathType.__class__ == list:
            # path with different types
            tmpStr = '<path d = "M {0:.0f} {1:.0f}'.format(path[0, 0],
                                                           path[1, 0])

            raise self._exception('Work in progress')

        # and gone
        else:
            raise self._exception('Unknown overlay type')

        # write design attributes
        if strokeColor is None:
            tmpStr += ' stroke="none"'
        else:
            tmpStr += ' stroke="rgb({0}, {1}, {2})"'.format(int(strokeColor[0]), int(strokeColor[1]), int(strokeColor[2]))

        tmpStr += ' stroke-width = "{0}"'.format( width)

        if color is None:
            tmpStr += ' fill="none"'
        else:
            tmpStr += ' fill="rgb({0}, {1}, {2})"'.format(int(color[0]), int(color[1]), int(color[2]))

        tmpStr += '/>\n'

        return tmpStr

    def formatValue(self, valueType, value):
        """
        Function to format values according to the options
        """
        if value == 0.0:
            value = self._getOption(valueType + '_for_mlow').format(value)
        elif abs(value) < self._getOption(valueType + '_lim_low'):
            value = self._getOption(valueType + '_for_low').format(value)
        elif abs(value) < self._getOption('leg_lim_mid') :
            value = self._getOption(valueType + '_for_mlow').format(value)
        elif abs(value) < self._getOption('leg_lim_up'):
            value = self._getOption(valueType + '_for_mup').format(value)
        else:
            value = self._getOption(valueType + '_for_up').format(value)

        return value
