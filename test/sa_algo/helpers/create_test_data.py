#!/usr/bin/env python3

'''create_test_data.py: Create test data for Calculate CAN filter.

This little script creates textfiles with random number of random CAN IDs.
'''

import random

import can_filter_calc

def createCanIdList():
    '''Create random CAN id list.
    '''
    
    canIdList = []
    
    random.seed()
    
    numberOfIds = random.randint(5, 11)
    
    for i in range(0, numberOfIds):
        canIdList.append("0x{num:0x}".format(num = random.randint(0, 2048)))
    
    return canIdList


def writeToFile(stringList, fileName, folder):
    '''Write string list to file.
    '''
    
    # print created strings to file
    with open(folder + fileName + ".txt", 'w') as file:
        for listItem in stringList:
            file.write(listItem + "\n")

def main():
    
    numberOfFiles = 5
    filterMin = 2
    filterMax = 4
    canIdList = []
    results = [[] for i in range(0, filterMax + 1)]
    
    for i in range(0, numberOfFiles):
        
        fileName = "test_can_ids_11bit_" + str(i)
        folderName = "../test_data/input/"
        
        # create test data
        canIdList = createCanIdList()
        writeToFile(canIdList, fileName, folderName)
        
        for fil in range(filterMin, filterMax + 1): 
            # calculate optimal solution
            canCalc = can_filter_calc.CanFilterCalc(['', '-f='+folderName+fileName+'.txt', '-o=../test_data/output/result_opt_11bit_ids_' + str(fil) + '_fil_' + str(i) + '.txt', '-s=11', '-n=' + str(fil)])
            test_lists, test_filters, test_num = canCalc.calc()
        
            results[fil].append(str(test_num))
        
    # write results file
    for fil in range(filterMin, filterMax + 1):
        fileName = "result_list_fil_" + str(fil) + "_messages_pass"
        folderName = "../test_data/output/"
        
        writeToFile(results[fil], fileName, folderName)

    
if __name__ == '__main__':
    main()
    