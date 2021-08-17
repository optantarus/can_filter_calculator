"""Test can_filter_calc.
"""

import unittest

import can_filter_calc


class can_filter_calc_test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_calc_11bit_ids(self):
        
        ref_lists = [['00000111111', '00000010101'], ['00000000010']]
        ref_filters = ['00000X1X1X1', '00000000010']
        ref_num = 6
        
        canCalc = can_filter_calc.CanFilterCalc(['', '-f=test_data/test_can_ids_11bit.txt', '-o=results/result_test_11bit_ids.txt', '-s=11', '-n=2'])
        test_lists, test_filters, test_num = canCalc.calc()
        
        self.assertEqual(ref_lists, test_lists, 'Error in calculated lists.')
        self.assertEqual(ref_filters, test_filters, 'Error in calculated filters.')
        self.assertEqual(ref_num, test_num, 'Error in calculated message number.')
        
        
    def test_calc_29bit_ids(self):
        
        ref_lists = [['01100111100000000010000000001'], ['11000000000000100000100000000', '11000000000000100000100000001']]
        ref_filters = ['01100111100000000010000000001', '1100000000000010000010000000X']
        ref_num = 0
        
        canCalc = can_filter_calc.CanFilterCalc(['', '-f=test_data/test_can_ids_29bit.txt', '-o=results/result_test_29bit_ids.txt', '-s=29', '-n=2'])
        test_lists, test_filters, test_num = canCalc.calc()
        
        self.assertEqual(ref_lists, test_lists, 'Error in calculated lists.')
        self.assertEqual(ref_filters, test_filters, 'Error in calculated filters.')
        self.assertEqual(ref_num, test_num, 'Error in calculated message number.')
        
        
    def test_calc_3_filters(self):
        
        ref_lists = [['00000111111'], ['00000010101'], ['00000000010']]
        ref_filters = ['00000111111', '00000010101', '00000000010']
        ref_num = 0
        
        with self.assertRaises(ValueError):
            canCalc = can_filter_calc.CanFilterCalc(['', '-f=test_data/test_can_ids_11bit.txt', '-o=results/result_test_calc_3_filters.txt', '-s=11', '-n=3'])
            test_lists, test_filters, test_num = canCalc.calc()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()