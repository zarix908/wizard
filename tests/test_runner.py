import unittest
from tests.invalid_args_tests import InvalidArgsTests

calcTestSuite = unittest.TestSuite()
calcTestSuite.addTest(unittest.makeSuite(InvalidArgsTests))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(calcTestSuite)
