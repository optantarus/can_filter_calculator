#!/usr/bin/env python3

'''can_filter_calc.py: Calculate CAN filter.

This little script takes a text file with CAN IDs and calculate the required
CAN filter.
'''

import sys
import argparse
import math
import more_itertools
import itertools

import time

from typing import List, Tuple
from operator import iand, ior
from functools import reduce

class CanFilterCalc:

    def __init__(self, argv: List[str]):

        self.canIds: List[int] = []
        self.canIdsStrings: List[str] = []
        self.passMessagesMin: List[int] = []
        self.idBitSize: int = 0
        self.numFilter: int = 0
        self.minLength: int = 0
        self.bestLists: List[List[int]] = []
        self.bestListsStr: List[List[str]] = []
        self.bestFilters: List[int] = []
        self.bestMasks: List[int] = []
        self.bestFiltersStr: List[str] = []
        self.outputFile: str = ""

        # parse comand line arguments and set canIds, idBitSize and numFilter
        self._parseArguments(argv)

    def calc(self) -> Tuple[List[List[str]], List[str], int] :
        '''Calculate CAN Filter.
        '''

        # initialize variables to store best filter values
        self.minLength = self.numFilter*pow(2, self.idBitSize)
        self.bestLists = []
        self.bestFilters = []
        self.passMessagesMin = []
        self.bestFiltersStr = []
        self.bestListsStr = []

        # loop through all variants to partition the CAN IDs to the given filter number
        for part in more_itertools.set_partitions(self.canIds, self.numFilter):
            lengthPart = 0
            filtersPart = []
            masksPart = []
            passMessages = []

            # loop through lists for all CAN filters
            for idList in part:
                lengthList, canMask, canFilter = self.calcFilter(idList)
                
                lengthPart += lengthList
                passMessages.append(lengthList)
                filtersPart.append(canFilter)
                masksPart.append(canMask)

            if(self.minLength > lengthPart):
                self.minLength = lengthPart
                self.bestFilters = filtersPart
                self.bestMasks = masksPart
                self.bestLists = part
                self.passMessagesMin = passMessages
        
        for mask, fil in zip(self.bestMasks, self.bestFilters):
            self.bestFiltersStr.append(self._filterStr(mask, fil))   
        
        tempList = []
        
        for idList in self.bestLists:
            for canId in idList:
                tempList.append("{num:0{length}b}".format(num = canId, length = self.idBitSize))
            self.bestListsStr.append(tempList)
            tempList = []
                
        if self.outputFile:
            self._writeToFile()
                
        return self.bestListsStr, self.bestFiltersStr, self.minLength


    def calcFilter(self, idList: List[int]) -> Tuple[int, int]:
        '''Calculate canFilter for list of CAN IDs.
        
        The canFilter is representated as a mask and a filter.
        
        @param[in]   idList      list of CAN IDs as ints
        @retval      numPassIds  number of CAN IDs that pass canFilter
        @retval      canMask     represensation of can mask
        @retval      canFilter   represensation of can filter
        '''
        canMask = 0
        canFilter = 0
        numPassIds = 0

        # calculate mask with xor over all IDs in list
        canFilter = reduce(iand, idList)
        canMask = reduce(ior, idList) ^ canFilter
       
        # number of unwanted messages that pass filter
        if(len(idList) > 1):
            numPassIds = pow(2, str(bin(canMask)).count('1')) - len(idList)
        else:
            numPassIds = 0

        return numPassIds, canMask, canFilter

    def _filterStr(self, canMask: int, canFilter: int) -> str:
        '''Create string representation of can mask and can filter.
        
        '0' or '1' means an ID has to have that value. 'X' means don't care
        
        @param[in]   canMask      can mask
        @param[in]   canFilter    can filter
        @retval      canFilterRep represensation of can filter
        '''
        
        canFilterRep = ""
        canMaskStr = "{num:0{length}b}".format(num = canMask, length = self.idBitSize)
        canFilterStr = "{num:0{length}b}".format(num = canFilter, length = self.idBitSize)
        
        # loop through all bits of the ID size
        for x in range(0, self.idBitSize):

            if canMaskStr[x] == '1':
                canFilterRep = canFilterRep + 'X'
            elif canFilterStr[x] == '1':
                canFilterRep = canFilterRep + '1'
            else:
                canFilterRep = canFilterRep + '0' 
        
        return canFilterRep

    def _writeToFile(self):
        '''Write result of execution of calc to file.
        '''

        # calculate length of CAN identifier in hex
        idLength = math.ceil(self.idBitSize / 4)
        stringLists = []
        headers = []
    
        # create list of lists with strings of all CAN messages IDs used for each filter
        for idList in self.bestLists:
            tempList = []
            for canId in idList:
                # create string with CAN ID in binary and hex format
                tempList.append("0b{num:0{length}b}".format(num = canId, length = self.idBitSize) + " : " + "0x{num:0{length}x}".format(num = canId, length = idLength))
                
            stringLists.append(tempList)
    
        # create list with strings of all CAN filters
        for fil, msg in zip(self.bestFiltersStr, self.passMessagesMin):
            # create string with CAN filter and number of messages that pass filter
            headers.append("0b" + fil + " : " + "{num:{length}d}".format(num = msg, length = idLength + 2))
    
        # add fill entries so that all lists of CAN message IDs have same length to easy print a table
        tableList = list(itertools.zip_longest(*stringLists, fillvalue=" "*(self.idBitSize + 3 + idLength + 4)))
        
        # print created strings to file
        with open(self.outputFile, 'w') as file:
            file.write("Calculated CAN Filters [ filter : number of unwanted passing messages ]:\n")
            file.write(" | ".join(headers) + "\n")
            file.write("\n")
            
            file.write("CAN messages assigned to filters [ bin : hex ]:\n")
            for line in tableList:
                file.write(" | ".join(line) + "\n")


    def _parseArguments(self, argv: List[str]) -> None:
        '''Parse comand line arguments.
        '''

        cmdParser = argparse.ArgumentParser(description="Calculate filter for given CAN IDs")
        cmdParser.add_argument("-f", "--file", required=True, help="name of file with CAN ids")
        cmdParser.add_argument("-s", "--size", required=True, help="bit size of CAN IDs")
        cmdParser.add_argument("-n", "--num", required=True, help="number of filters")
        cmdParser.add_argument("-o", "--out", required=False, help="file to write results to")

        self.cmdArgs = cmdParser.parse_args(argv[1:])

        self.idBitSize = int(self.cmdArgs.size)
        self.numFilter = int(self.cmdArgs.num)
        
        self.outputFile = self.cmdArgs.out

        self._readIdsFromFile(self.cmdArgs.file)


    def _readIdsFromFile(self, fileName: str) -> None:
        '''Open given file and read CAN IDs.
        '''

        with open(fileName, 'r') as file:
            for line in file:
                self.canIds.append(int(line, 16))

           
    def _convertIdsToStrings(self) -> None:
        '''convert CAN ID numbers into binary strings with width of bitsize.
        '''
        
        for num in self.canIds:
            self.canIdsStrings.append('{num:0{bitSize}b}'.format(num = num, bitSize = self.idBitSize)) 

def main():
    
    begin = time.time()
    
    canCalc = CanFilterCalc(sys.argv)
    bestLists, bestFilters, minLength = canCalc.calc()
    
    end = time.time()
    
    print("\nResult:\n")
    print("Lists: ", bestLists, "\n")
    print("Filters: ", bestFilters, "\n")
    print("Sum messages pass: ", minLength, "\n\n")
    
    print("Time:", end - begin, "s")

    
if __name__ == '__main__':
    main()
    
        
