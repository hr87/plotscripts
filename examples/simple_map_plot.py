import plotscripts.data
import plotscripts.plotter.svg as svgplotter
import plotscripts.geometry.rectangular as geometry

inputArgs = plotscripts.InputArgs()
inputArgs.setData(plotscripts.data.TestData)

plot = inputArgs.addPlot('svgmap_1', svgplotter.SvgMapPlotter)
plot.setOption('use_dirs', False)       # do not create folder structure
plot.setOption('plotdir', '.')          # output folder
plot.setOption('show_ticks', False)     # no axis ticks

geometry = plot.setGeometry(geometry.Rectangular)   # add gemoetry information
geometry.pitch = 10                     # set width of blocks
geometry.numBlocks = [5, 5]             # set up number of blocks

index = plotscripts.data.TestData.index()
index.calcType = 'num'
index.num = 25

mapPlot = plot.addMap('test')           # add a map
mapPlot.setIndex(index)                  # set map data

inputArgs.run()                         # execute
