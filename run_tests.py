#!/bin/python3

import unittest

import tests

print('Running plotscripts test suite:')
testSuite = unittest.TestSuite()
testSuite.addTest(tests.testSuite())

# run tests
unittest.main(defaultTest='testSuite', buffer=True)
