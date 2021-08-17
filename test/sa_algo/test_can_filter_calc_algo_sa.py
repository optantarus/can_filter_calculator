"""Test can_filter_calc sa algorithm.
"""

import unittest

import can_filter_calc


class can_filter_calc_algo_sa_test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_calc_11bit_ids_2_filters(self):
        
        referencePassMessages = []
        
        with open('test_data/output/result_list_fil_2_messages_pass.txt', 'r') as file:
            for line in file:
                referencePassMessages.append(int(line))
        
        for testData in range(0, 5):
            with self.subTest(description = "Test " + str(testData)):
                canCalc = can_filter_calc.CanFilterCalc(['', '-f=test_data/input/test_can_ids_11bit_' + str(testData) + '.txt', '-o=results/result_test_11bit_ids_2_fil_' + str(testData) + '.txt', '-s=11', '-n=2', '-a=SA'])
                test_lists, test_filters, test_num = canCalc.calc()
            
                self.assertLessEqual(test_num, referencePassMessages[testData], "Optimum not found")

                
    def test_calc_11bit_ids_3_filters(self):
        
        referencePassMessages = []
        
        with open('test_data/output/result_list_fil_3_messages_pass.txt', 'r') as file:
            for line in file:
                referencePassMessages.append(int(line))
        
        for testData in range(0, 5):
            with self.subTest(description = "Test " + str(testData)):
                canCalc = can_filter_calc.CanFilterCalc(['', '-f=test_data/input/test_can_ids_11bit_' + str(testData) + '.txt', '-o=results/result_test_11bit_ids_3_fil_' + str(testData) + '.txt', '-s=11', '-n=3', '-a=SA'])
                test_lists, test_filters, test_num = canCalc.calc()
            
                self.assertLessEqual(test_num, referencePassMessages[testData], "Optimum not found")

                
    def test_calc_11bit_ids_4_filters(self):
        
        referencePassMessages = []
        
        with open('test_data/output/result_list_fil_4_messages_pass.txt', 'r') as file:
            for line in file:
                referencePassMessages.append(int(line))
        
        for testData in range(0, 5):
            with self.subTest(description = "Test " + str(testData)):
                canCalc = can_filter_calc.CanFilterCalc(['', '-f=test_data/input/test_can_ids_11bit_' + str(testData) + '.txt', '-o=results/result_test_11bit_ids_4_fil_' + str(testData) + '.txt', '-s=11', '-n=4', '-a=SA'])
                test_lists, test_filters, test_num = canCalc.calc()
            
                self.assertLessEqual(test_num, referencePassMessages[testData], "Optimum not found")

               
    def test_calc_large_number_11bit_ids_4_filters(self):
        
        referencePassMessages = []
        
        with open('test_data/output/result_list_large_fil_4_messages_pass.txt', 'r') as file: # this list contains only boundary value, no optimal ones
            for line in file:
                referencePassMessages.append(int(line))
        
        for testData in range(0, 5):
            with self.subTest(description = "Test " + str(testData)):
                canCalc = can_filter_calc.CanFilterCalc(['', '-f=test_data/input/test_large_can_ids_11bit_' + str(testData) + '.txt', '-o=results/result_test_large_11bit_ids_4_fil_' + str(testData) + '.txt', '-s=11', '-n=4', '-a=SA'])
                test_lists, test_filters, test_num = canCalc.calc()
            
                self.assertLessEqual(test_num, referencePassMessages[testData], "Optimum not found")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()