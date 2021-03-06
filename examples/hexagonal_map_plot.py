import plotscripts.data
import plotscripts.plotter.svg as svgplotter
import plotscripts.geometry.hexagonal as geometry

inputArgs = plotscripts.InputArgs()
inputArgs.setData(plotscripts.data.TestData)

plot = inputArgs.addPlot('svgmap_1', svgplotter.MapPlotter)
plot.setOption('use_dirs', False)       # do not create folder structure
plot.setOption('plotdir', '.')          # output folder

geometry = plot.setGeometry(geometry.Hexagonal)   # add gemoetry information
geometry.pitch = 10                     # set width of blocks
geometry.ringEnd = 10             # set up number of rings

index = plotscripts.data.TestData.index()
index.calcType = 'num'
index.num = 331

mapPlot = plot.addMap('test')           # add a map
mapPlot.setData(index)                  # set map data

inputArgs.run()                         # execute
