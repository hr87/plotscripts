import plotscripts.data
import plotscripts.plotter.matplotlib as mplplotter

inputArgs = plotscripts.InputArgs()
inputArgs.setData(plotscripts.data.TestData)

plot = inputArgs.addPlot('matplotlib_1', mplplotter.LinePlotter)
plot.setOption('use_dirs', False)               # do not generate folder structure
plot.setOption('plotdir', '.')                  # set folder to test folder
plot.setOption('format', 'png')                 # output format to png

line = plot.addLine()                           # add a line
line.data = (['num', 10], ['num', 10])          # setting x and y values
line.color = line.ColorList.red                 # set line color
line.lineStyle = line.LineStyleList.dashed      # set line style
line.markerStyle = line.MarkerStyleList.dot     # set marker style
line.markerSize = 1.1                           # set marker size

line = plot.addLine()                           # add second line
line.data = (['num', 10], ['rnd', 10, 10])      # setting x and y values
line.color = line.ColorList.blue                # set line color
line.lineStyle = line.LineStyleList.solid       # set line style

inputArgs.run()                                 # execute
