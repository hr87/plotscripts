#!/bin/python3

import unittest

# import test suits
import tests.plotter

testSuite = unittest.TestSuite()
testSuite.addTest(tests.plotter.plotterSuite)

# run tests
unittest.main(defaultTest='testSuite', buffer=True)
