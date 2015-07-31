""" Example to use all geometries
"""

# import necessary packages
import plotscripts
import plotscripts.data as data
import plotscripts.plotter.svg as plotter
import plotscripts.geometry.hexagonal as hexagonal
import plotscripts.geometry.rectangular as rectangular
import math

print('I am alive')

# create object
inputArg = plotscripts.InputArgs()
# set a few options, will be passed to sub objects
# this options are global, options also can be set in the sub objects
inputArg.setOption('debug', True)
inputArg.setOption('plotdir', 'plot/geometry/')

inputArg.setOption('text_for_low', '{0:.0f}') # lower value format string
inputArg.setOption('text_for_mlow', '{0:.0f}') # lower middle value format string
inputArg.setOption('text_for_mup', '{0:.0f}') # upper middle value format string
inputArg.setOption('text_for_up', '{0:.0f}') # upper value format string

# create test data executioner
dataset = inputArg.setData(data.TestData)

# plot all available geometries
plot = inputArg.addPlot('rectangular', plotter.MapPlotter)
geometry = plot.setGeometry(rectangular.Rectangular)
geometry.pitch = 10
geometry.numBlocks = [5, 5]

index = dataset.index()
index.calcType = 'num'
index.num = 25


import plotscripts.geometry.rectangular.rectangular
inputArg._plots['rectangular']                    = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['rectangular'].geometry           = plotscripts.geometry.rectangular.rectangular.Rectangular()
inputArg._plots['rectangular'].geometry.numBlocks = [5, 7]
inputArg._plots['rectangular'].geometry.pitch     = [30, 10]
inputArg._plots['rectangular'].input              = [ ['idx', 35]]


import plotscripts.geometry.hexagonal.hexagonal
inputArg._plots['hexmap']                      = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['hexmap'].geometry             = plotscripts.geometry.hexagonal.hexagonal.Hexagonal()
inputArg._plots['hexmap'].geometry.ringEnd     = 3
inputArg._plots['hexmap'].geometry.ringStart   = 0
inputArg._plots['hexmap'].geometry.pitch       = 30
inputArg._plots['hexmap'].input                = [ ['idx', 37]]


import plotscripts.geometry.hexagonal.triangular
inputArg._plots['trimap']                      = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['trimap'].geometry             = plotscripts.geometry.hexagonal.triangular.Triangular()
inputArg._plots['trimap'].geometry.ringEnd     = 3
inputArg._plots['trimap'].geometry.ringStart   = 0
inputArg._plots['trimap'].geometry.pitch       = 30
inputArg._plots['trimap'].input                = [ ['idx', 222]]


import plotscripts.geometry.hexagonal.hexagonalthird
inputArg._plots['hexthird']                    = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['hexthird'].geometry           = plotscripts.geometry.hexagonal.hexagonalthird.HexagonalThird()
inputArg._plots['hexthird'].geometry.ringEnd   = 5
inputArg._plots['hexthird'].geometry.ringStart = 0
inputArg._plots['hexthird'].geometry.pitch     = 30
inputArg._plots['hexthird'].input              = [ ['idx', 21]]


import plotscripts.geometry.hexagonal.triangularthird
inputArg._plots['trithird']                    = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['trithird'].geometry           = plotscripts.geometry.hexagonal.triangularthird.TriangularThird()
inputArg._plots['trithird'].geometry.ringEnd   = 5
inputArg._plots['trithird'].geometry.ringStart = 0
inputArg._plots['trithird'].geometry.pitch     = 30
inputArg._plots['trithird'].input              = [ ['idx', 126]]


#import plotscripts.geometry.hexagonal.hexagonalxy
# rectangular xy

# special geometries fot the vhtrc experiment
import plotscripts.geometry.vhtrc.hexagonal
inputArg._plots['vhtrc_hex']           = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['vhtrc_hex'].geometry  = plotscripts.geometry.vhtrc.hexagonal.VHTRCHexagonal()
inputArg._plots['vhtrc_hex'].input     = [ ['idx', 73]]
inputArg._plots['vhtrc_hex'].method    = ['value']


import plotscripts.geometry.vhtrc.triangular
inputArg._plots['vhtrc_tri']           = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['vhtrc_tri'].geometry  = plotscripts.geometry.vhtrc.triangular.VHTRCTriangular()
inputArg._plots['vhtrc_tri'].input     = [ ['idx', 384]]
inputArg._plots['vhtrc_tri'].method    = ['value']


import plotscripts.geometry.vhtrc.pin
inputArg._plots['vhtrc_pin']           = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['vhtrc_pin'].geometry  = plotscripts.geometry.vhtrc.pin.VHTRCPin()
inputArg._plots['vhtrc_pin'].input     = [ ['idx', 613]]
inputArg._plots['vhtrc_pin'].method    = ['value']

# this shows the use of the transformation abilities
# possible is flipping at X and Y
# rotation around z
# translate before and after rotation
inputArg._plots['rectangular_trans']                       = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['rectangular_trans'].geometry              = plotscripts.geometry.rectangular.rectangular.Rectangular()
inputArg._plots['rectangular_trans'].geometry.numBlocks    = [5, 7]
inputArg._plots['rectangular_trans'].geometry.pitch        = [30, 10]
inputArg._plots['rectangular_trans'].input                 = [ ['idx', 35]]
inputArg._plots['rectangular_trans'].options['rotation']   = math.pi / 4  # rotate
inputArg._plots['rectangular_trans'].options['offsetX']    = 10     # translate after rotation x
inputArg._plots['rectangular_trans'].options['offsetY']    = -50    # translate after rotation y
inputArg._plots['rectangular_trans'].options['offsetXRot'] = 0      # translation before rotation x
inputArg._plots['rectangular_trans'].options['offsetYRot'] = 0      # translation before rotation y

# this shows possibility of select blocks from the geometry to show details 
# or leaving some stuff blank, can also be used to shuffle blocks in different sequence
# assign takes a list of blocks to use 
inputArg._plots['assign']                      = plotscripts.plotter.svg.svgmapplotter.SvgMapPlotter()
inputArg._plots['assign'].geometry             = plotscripts.geometry.hexagonal.hexagonal.Hexagonal()
inputArg._plots['assign'].geometry.ringEnd     = 3
inputArg._plots['assign'].geometry.ringStart   = 0
inputArg._plots['assign'].geometry.pitch       = 30
inputArg._plots['assign'].input                = [ ['idx', 16]]
inputArg._plots['assign'].assign               = [2*idx for idx in range(16)]

inputArg.run()
print('done')