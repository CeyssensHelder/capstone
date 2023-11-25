import unittest
import getopt
import sys
import os

from ApiTest import *
from ModelTests import *
from LoggerTests import *


try:
    optlist, args = getopt.getopt(sys.argv[1:],'v')
except getopt.GetoptError:
    print(getopt.GetoptError)
    print(sys.argv[0] + "-v")
    print("... the verbose flag (-v) may be used")
    sys.exit()

VERBOSE = False
RUNALL = False

sys.path.append(os.path.realpath(os.path.dirname(__file__)))

for o, a in optlist:
    if o == '-v':
        VERBOSE = True

ApiTestSuite = unittest.TestLoader().loadTestsFromTestCase(ApiTest)
ModelTestSuite = unittest.TestLoader().loadTestsFromTestCase(ModelTest)
LoggerTestSuite = unittest.TestLoader().loadTestsFromTestCase(LoggerTest)

MainSuite = unittest.TestSuite([LoggerTestSuite,ModelTestSuite,ApiTestSuite])
