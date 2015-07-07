'''
Created on Aug 29, 2013

@author: Hans R Hammer

test file for all geometries
'''

# import necessary packages
import plotscripts.data.testdata
import plotscripts.plotter.svg.mapplotter
import math

print('I am alive')

# create object
inputArg = plotscripts.InputArgs()
# set a few options, will be passed to sub objects
# this options are global, options also can be set in the sub objects
inputArg.options['debug'] = True
inputArg.options['plotdir'] = 'plot/geometry/' 

inputArg.options['text_for_low'] = '{0:.0f}' # lower value format string
inputArg.options['text_for_mlow']= '{0:.0f}' # lower middle value format string
inputArg.options['text_for_mup'] = '{0:.0f}' # upper middle value format string
inputArg.options['text_for_up']  = '{0:.0f}' # upper value format string

# create test data executioner
inputArg.data = plotscripts.data.testdata.TestData()

# plot all available geometries
import plotscripts.geometry.rectangular.rectangular
inputArg.plot['rectangular']                    = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['rectangular'].geometry           = plotscripts.geometry.rectangular.rectangular.Rectangular()
inputArg.plot['rectangular'].geometry.numBlocks = [5, 7]
inputArg.plot['rectangular'].geometry.pitch     = [30, 10]
inputArg.plot['rectangular'].input              = [ ['idx', 35]]


import plotscripts.geometry.hexagonal.hexagonal
inputArg.plot['hexmap']                      = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['hexmap'].geometry             = plotscripts.geometry.hexagonal.hexagonal.Hexagonal()
inputArg.plot['hexmap'].geometry.ringEnd     = 3
inputArg.plot['hexmap'].geometry.ringStart   = 0
inputArg.plot['hexmap'].geometry.pitch       = 30
inputArg.plot['hexmap'].input                = [ ['idx', 37]]


import plotscripts.geometry.hexagonal.triangular
inputArg.plot['trimap']                      = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['trimap'].geometry             = plotscripts.geometry.hexagonal.triangular.Triangular()
inputArg.plot['trimap'].geometry.ringEnd     = 3
inputArg.plot['trimap'].geometry.ringStart   = 0
inputArg.plot['trimap'].geometry.pitch       = 30
inputArg.plot['trimap'].input                = [ ['idx', 222]]


import plotscripts.geometry.hexagonal.hexagonalthird
inputArg.plot['hexthird']                    = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['hexthird'].geometry           = plotscripts.geometry.hexagonal.hexagonalthird.HexagonalThird()
inputArg.plot['hexthird'].geometry.ringEnd   = 5
inputArg.plot['hexthird'].geometry.ringStart = 0
inputArg.plot['hexthird'].geometry.pitch     = 30
inputArg.plot['hexthird'].input              = [ ['idx', 21]]


import plotscripts.geometry.hexagonal.triangularthird
inputArg.plot['trithird']                    = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['trithird'].geometry           = plotscripts.geometry.hexagonal.triangularthird.TriangularThird()
inputArg.plot['trithird'].geometry.ringEnd   = 5
inputArg.plot['trithird'].geometry.ringStart = 0
inputArg.plot['trithird'].geometry.pitch     = 30
inputArg.plot['trithird'].input              = [ ['idx', 126]]


#import plotscripts.geometry.hexagonal.hexagonalxy
# rectangular xy

# special geometries fot the vhtrc experiment
import plotscripts.geometry.vhtrc.hexagonal
inputArg.plot['vhtrc_hex']           = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['vhtrc_hex'].geometry  = plotscripts.geometry.vhtrc.hexagonal.VHTRCHexagonal()
inputArg.plot['vhtrc_hex'].input     = [ ['idx', 73]]
inputArg.plot['vhtrc_hex'].method    = ['value']


import plotscripts.geometry.vhtrc.triangular
inputArg.plot['vhtrc_tri']           = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['vhtrc_tri'].geometry  = plotscripts.geometry.vhtrc.triangular.VHTRCTriangular()
inputArg.plot['vhtrc_tri'].input     = [ ['idx', 384]]
inputArg.plot['vhtrc_tri'].method    = ['value']


import plotscripts.geometry.vhtrc.pin
inputArg.plot['vhtrc_pin']           = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['vhtrc_pin'].geometry  = plotscripts.geometry.vhtrc.pin.VHTRCPin()
inputArg.plot['vhtrc_pin'].input     = [ ['idx', 613]]
inputArg.plot['vhtrc_pin'].method    = ['value']

# this shows the use of the transformation abilities
# possible is flipping at X and Y
# rotation around z
# translate before and after rotation
inputArg.plot['rectangular_trans']                       = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['rectangular_trans'].geometry              = plotscripts.geometry.rectangular.rectangular.Rectangular()
inputArg.plot['rectangular_trans'].geometry.numBlocks    = [5, 7]
inputArg.plot['rectangular_trans'].geometry.pitch        = [30, 10]
inputArg.plot['rectangular_trans'].input                 = [ ['idx', 35]]
inputArg.plot['rectangular_trans'].options['rotation']   = math.pi / 4  # rotate
inputArg.plot['rectangular_trans'].options['offsetX']    = 10     # translate after rotation x
inputArg.plot['rectangular_trans'].options['offsetY']    = -50    # translate after rotation y
inputArg.plot['rectangular_trans'].options['offsetXRot'] = 0      # translation before rotation x
inputArg.plot['rectangular_trans'].options['offsetYRot'] = 0      # translation before rotation y

# this shows possibility of select blocks from the geometry to show details 
# or leaving some stuff blank, can also be used to shuffle blocks in different sequence
# assign takes a list of blocks to use 
inputArg.plot['assign']                      = plotscripts.plotter.svg.mapplotter.MapPlotter()
inputArg.plot['assign'].geometry             = plotscripts.geometry.hexagonal.hexagonal.Hexagonal()
inputArg.plot['assign'].geometry.ringEnd     = 3
inputArg.plot['assign'].geometry.ringStart   = 0
inputArg.plot['assign'].geometry.pitch       = 30
inputArg.plot['assign'].input                = [ ['idx', 16]]
inputArg.plot['assign'].assign               = [2*idx for idx in range(16)]

inputArg.run()
print('done')