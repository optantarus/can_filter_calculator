#!/usr/bin/env python3

'''can_filter_calc.py: Calculate CAN filter.

This little script takes a text file with CAN IDs and calculate the required
CAN filter.
'''

import argparse
import more_itertools

from typing import List, Tuple

class CanFilterCalc:

    def __init__(self):

        self.canIds: List[int] = []
        self.canIdsStrings: List[str] = []
        self.idBitSize: int = 0
        self.numFilter: int = 0

        # parse comand line arguments and set canIds, idBitSize and numFilter
        self._parseArguments()

    def calc(self) -> None:
        '''Calculate CAN Filter.
        '''

        # convert CAN ID numbers into binary strings with width of bitsize
        for num in self.canIds:
            self.canIdsStrings.append('{num:0{bitSize}b}'.format(num = num, bitSize = self.idBitSize)) 

        # initialize variables to store best filter values
        minLength = self.numFilter*pow(2, self.idBitSize)
        bestLists = []
        bestFilters = []

        # loop through all variants to partition the CAN IDs to the given filter number
        for part in more_itertools.set_partitions(self.canIdsStrings, self.numFilter):
            lengthPart = 0
            filtersPart = []

            # loop through lists for all CAN filters
            for idList in part:
                lengthList, canFilter = self.calcFilter(idList)
                
                lengthPart += lengthList
                filtersPart.append(canFilter)

            if(minLength > lengthPart):
                minLength = lengthPart
                bestFilters = filtersPart
                bestLists = part

        print("\nResult:\n")
        print("Lists: ", bestLists, "\n")
        print("Filters: ", bestFilters, "\n")
        print("Sum messages pass: ", minLength)

    def calcFilter(self, idList: List[str]) -> Tuple[int, str]:
        '''Calculate canFilter for list of CAN IDs.
        
        The canFilter is representated as a string. '0' or '1' means
        an ID has to have that value. 'X' means don't care.
        
        @param[in]   idList      list of CAN IDs as binary strings
        @retval      numPassIds  number of CAN IDs that pass canFilter
        @retval      canFilter      represensation of canFilter
        '''
        canFilter = ''
        numPassIds = 0

        # loop through all bits of the IDs
        for x in range(0, self.idBitSize):
            allZeros = True
            allOnes = True

            # loop through all IDs
            for item in idList:
                if item[x] == '0':
                    allOnes = False
                    
                if item[x] == '1':
                    allZeros = False

            if allZeros:
                canFilter = canFilter + '0'
            elif allOnes:
                canFilter = canFilter + '1'
            else:
                canFilter = canFilter + 'X'        
        # number of unwanted messages that pass filter
        numPassIds = pow(2, canFilter.count('X')) - len(idList)

        return numPassIds, canFilter


    def _parseArguments(self) -> None:
        '''Parse comand line arguments.
        '''

        cmdParser = argparse.ArgumentParser()
        cmdParser.add_argument("-f", "--file", required=True, help="name of file with CAN ids")
        cmdParser.add_argument("-s", "--size", required=True, help="bit size of CAN IDs")
        cmdParser.add_argument("-n", "--num", required=True, help="number of filters")

        self.cmdArgs = cmdParser.parse_args()

        self.idBitSize = int(self.cmdArgs.size)
        self.numFilter = int(self.cmdArgs.num)

        self._readIdsFromFile(self.cmdArgs.file)


    def _readIdsFromFile(self, fileName: str) -> None:
        '''Open given file and read CAN IDs.
        '''

        with open(fileName, 'r') as file:
            for line in file:
                self.canIds.append(int(line, 16))


if __name__ == '__main__':

    canCalc = CanFilterCalc()
    canCalc.calc()
