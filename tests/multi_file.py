'''
Created on Mar 7, 2014

@author: Hans R Hammer
'''

import plotscripts
import plotscripts.data.testdata as testdata
import plotscripts.data.multifile as multifile
import plotscripts.plotter.matplotlib.lineplotter as plotter

print('I am alive')

# create object
inputArg = plotscripts.InputArgs()
# set a few options, will be passed to sub objects
# this options are global, options also can be set in the sub objects
inputArg.options['debug'] = True
inputArg.options['plotdir'] = 'plot/data/' 

inputArg.data = multifile.MultiFile()
inputArg.data.files['test1'] = testdata.TestData()
inputArg.data.files['test2'] = testdata.TestData()

inputArg.plot['test'] = plotter.LinePlotter()
inputArg.plot['test'].input    = [['test1', 'rnd', 10], ['test2', 'rnd', 10]]
inputArg.plot['test'].xValues  = list(range(10))
inputArg.plot['test'].column   = ['column']

#run the stuff
inputArg.run()
print('done')
