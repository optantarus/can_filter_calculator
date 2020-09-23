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

from typing import List, Tuple

class CanFilterCalc:

    def __init__(self, argv: List[str]):

        self.canIds: List[int] = []
        self.canIdsStrings: List[str] = []
        self.passMessagesMin: List[int] = []
        self.idBitSize: int = 0
        self.numFilter: int = 0
        self.minLength: int = 0
        self.bestLists: List[List[str]] = []
        self.bestFilters: List[str] = []
        self.outputFile: str = ""

        # parse comand line arguments and set canIds, idBitSize and numFilter
        self._parseArguments(argv)

    def calc(self) -> Tuple[List[List[str]], List[str], int] :
        '''Calculate CAN Filter.
        '''

        self._convertIdsToStrings()

        # initialize variables to store best filter values
        self.minLength = self.numFilter*pow(2, self.idBitSize)
        self.bestLists = []
        self.bestFilters = []
        self.passMessagesMin = []

        # loop through all variants to partition the CAN IDs to the given filter number
        for part in more_itertools.set_partitions(self.canIdsStrings, self.numFilter):
            lengthPart = 0
            filtersPart = []
            passMessages = []

            # loop through lists for all CAN filters
            for idList in part:
                lengthList, canFilter = self.calcFilter(idList)
                
                lengthPart += lengthList
                passMessages.append(lengthList)
                filtersPart.append(canFilter)

            if(self.minLength > lengthPart):
                self.minLength = lengthPart
                self.bestFilters = filtersPart
                self.bestLists = part
                self.passMessagesMin = passMessages
                
        if self.outputFile:
            self._writeToFile()
                
        return self.bestLists, self.bestFilters, self.minLength


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
                tempList.append('0b' + canId + ' : ' + '0x{num:0{length}x}'.format(num = int(canId, 2), length = idLength))
                
            stringLists.append(tempList)
    
        # create list with strings of all CAN filters
        for fil, msg in zip(self.bestFilters, self.passMessagesMin):
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
    canCalc = CanFilterCalc(sys.argv)
    bestLists, bestFilters, minLength = canCalc.calc()
    
    print("\nResult:\n")
    print("Lists: ", bestLists, "\n")
    print("Filters: ", bestFilters, "\n")
    print("Sum messages pass: ", minLength)

    
if __name__ == '__main__':
    main()
    
        
