'''
Created on Mar 7, 2014

@author: Hans R Hammer
'''

import plotscripts
import plotscripts.data.testdata as testdata
import plotscripts.data.multidataset as multifile
import plotscripts.plotter.matplotlib.lineplotter as plotter

print('I am alive')

# create object
inputArg = plotscripts.InputArgs()
# set a few options, will be passed to sub objects
# this options are global, options also can be set in the sub objects
inputArg._options['debug'] = True
inputArg._options['plotdir'] = 'plot/data/'

inputArg._data = multifile.MultiDataSet()
inputArg._data.files['test1'] = testdata.TestData()
inputArg._data.files['test2'] = testdata.TestData()

inputArg._plots['test'] = plotter.LinePlotter()
inputArg._plots['test'].input    = [['test1', 'rnd', 10], ['test2', 'rnd', 10]]
inputArg._plots['test'].xValues  = list(range(10))
inputArg._plots['test'].column   = ['column']

#run the stuff
inputArg.run()
print('done')
