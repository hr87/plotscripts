import plotscripts.data
import plotscripts.plotter.matplotlib as mplplotter

inputArgs = plotscripts.InputArgs()
inputArgs.setData(plotscripts.data.TestData)

plot = inputArgs.addPlot('matplotlib_1', mplplotter.LinePlotter)
plot.setOption('use_dirs', False)               # do not generate folder structure
plot.setOption('plotdir', '.')                  # set folder to test folder
plot.setOption('format', 'png')                 # output format to png

index = plotscripts.data.TestData.index()
index.calcType = 'num'
index.num = 10

line = plot.addLine('num')                      # add a line
line.setIndex((index, index))                    # setting x and y values
line.color = line.ColorList.red                 # set line color
line.lineStyle = line.LineStyleList.dashed      # set line style
line.markerStyle = line.MarkerStyleList.dot     # set marker style
line.markerSize = 1.1                           # set marker size

index2 = plotscripts.data.TestData.index()
index2.calcType = 'rnd'
index2.num = 10
index2.max = 10

line = plot.addLine('rnd')                      # add second line
line.setIndex((index, index2))                   # setting x and y values
line.color = line.ColorList.blue                # set line color
line.lineStyle = line.LineStyleList.solid       # set line style
inputArgs.run()                                 # execute
