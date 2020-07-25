"""Test can_filter_calc.
"""

import unittest

import can_filter_calc


class can_filter_calc_test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_calc(self):
        
        ref_lists = [['00000111111', '00000010101'], ['00000000010']]
        ref_filters = ['00000X1X1X1', '00000000010']
        ref_num = 6
        
        canCalc = can_filter_calc.CanFilterCalc(['', '-f=can_ids.txt', '-s=11', '-n=2'])
        test_lists, test_filters, test_num = canCalc.calc()
        
        self.assertEqual(ref_lists, test_lists, 'Error in calculated lists.')
        self.assertEqual(ref_filters, test_filters, 'Error in calculated filters.')
        self.assertEqual(ref_num, test_num, 'Error in calculated message number.')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()