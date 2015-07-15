'''
Created on Mar 7, 2014

@author: Hans R Hammer
'''

import plotscripts
import plotscripts.data as data
import plotscripts.plotter.matplotlib as plotter

print('I am alive')

# create object
inputArg = plotscripts.InputArgs()
# set a few options, will be passed to sub objects
# this options are global, options also can be set in the sub objects
inputArg.setOption('debug', True)
inputArg.setOption('plotdir', 'plot/data/')

mulitFile = inputArg.setData(data.MultiDataSet)
inputArg._data.files['test1'] = data.TestData()
inputArg._data.files['test2'] = data.TestData()

inputArg.addPlot('test', plotter.LinePlotter())
# TODO use index
inputArg._plots['test'].input    = [['test1', 'rnd', 10], ['test2', 'rnd', 10]]
inputArg._plots['test'].xValues  = list(range(10))
inputArg._plots['test'].column   = ['column']

#run the stuff
inputArg.run()
print('done')
