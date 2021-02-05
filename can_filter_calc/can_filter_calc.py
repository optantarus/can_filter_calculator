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
import copy

import time
import random

import matplotlib.pyplot

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
        self.algorithm: str = "OPT"

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

        # choose algorithm to use
        if self.algorithm == "SA":
            self.simulatedAnnealing()
        else:
            self.optimalFilter()
            
        
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

    def simulatedAnnealing(self):
        '''Calculate an filter by using the simulated annealing algorithm
        '''
        
        # initialize values
        newLists = []
        mumPassMsgMax = self.numFilter*pow(2, self.idBitSize)
        
        lastTempUpdate = 0
        
        # parameters
        repetitions= 5000
        epochs = 100
        temp = 1.0
        coolingFactor = 0.95
        repWithSameTemp = 100
        decTemp = temp / repetitions
        
        curTemp = temp
        
        # graph data
        xAxis = range(0, repetitions*epochs)
        diff = 0
        accept = 0
        acceptList = []
        bestValue = []
        searchValue = []
        tempValue = []
        diffValue = []
        
        #initialize random number generator with system time (default)
        random.seed()
        
        # create start solution
        filtersList = self.createStartSolution()
        
        # set start values as best values
        self.bestLists = filtersList
        self.minLength, self.passMessagesMin, self.bestFilters, self.bestMasks  = self.calcFilters(filtersList)
        
        # initial set of old value
        lengthPartOld = self.minLength
        lengthPartOldStart = lengthPartOld
        
        for j in range(0, epochs):
        # repetitions of simulated annealing algorithm
            for i in range(0, repetitions):
    
                # create new variant based on current
                newLists = self.createNeighbour(filtersList)
                
                # calculate ranking values for new variant
                lengthPart, passMessages, filtersPart, masksPart = self.calcFilters(newLists)
                
                # new variant lets equal or less messages pass
                if(lengthPartOld >= lengthPart):
                    filtersList = newLists
                # new variant lets more messages pass
                else:
                    # accept new variant if a certain propablility
                    diff = (lengthPart - lengthPartOld) / mumPassMsgMax
                    expo = diff / temp
                    #expoVal = random.expovariate(expo)
                    expoVal = math.exp(-expo/temp)
                    uniVal = random.random()
                    
                    if expoVal >= uniVal:
                        filtersList = newLists
                        accept += 1
                
                # new variant let less messages pass -> save as new best solution        
                if(self.minLength > lengthPart):
                    self.minLength = lengthPart
                    self.bestFilters = filtersPart
                    self.bestMasks = masksPart
                    self.bestLists = newLists
                    self.passMessagesMin = passMessages
                
                # save value for graph view
                bestValue.append(self.minLength)
                searchValue.append(lengthPart)
                diffValue.append(diff)
                tempValue.append(temp)
                acceptList.append(accept)
                
                # decrease temperature
                if repWithSameTemp > (i-lastTempUpdate):
                    lastTempUpdate = i  
                    curTemp = curTemp * coolingFactor
                 
                #temp = temp - decTemp
                
            lastTempUpdate = 0
            curTemp = temp
            filtersList = self.createStartSolution()
            lengthPartOld = lengthPartOldStart
        
        # draw plots    
        matplotlib.pyplot.plot(xAxis, bestValue, label = "best")
        matplotlib.pyplot.plot(xAxis, searchValue, label = "search")
        matplotlib.pyplot.legend()
        
        matplotlib.pyplot.figure()
        matplotlib.pyplot.plot(xAxis, tempValue, label = "temp")
        matplotlib.pyplot.plot(xAxis, diffValue, label = "diff")
        
        matplotlib.pyplot.figure()
        matplotlib.pyplot.plot(xAxis, acceptList, label = "accept")
        matplotlib.pyplot.legend()
        
        #matplotlib.pyplot.show()
            
        
    def createStartSolution(self):
        '''Create an initial solution for simulated annealing algorithm.
        '''
        
        # calculate number of messages per filter if equally spread across all filters
        numFil = math.ceil(len(self.canIds) / self.numFilter)
        
        # sort CAN ID list
        self.canIds.sort()
        # assign equal number of CAN IDs to each filter
        lists = [self.canIds[i:i + numFil] for i in range(0, len(self.canIds), numFil)]
        
        return lists

        
    def createNeighbour(self, lists):
        '''Create variant of given lists.
        
        Randomly chose an element from a list and move it to another.
        
        @param[in]   lists      list of list of CAN IDs for each filter
        @retval      newLists   modified list of lists
        '''
        
        newLists = copy.deepcopy(lists)
        
        # chose random filter to pick element from
        randomSourceFilter = random.randint(0, (self.numFilter-1))
        # only use number if that list is not empty after removing one element
        while len(newLists[randomSourceFilter]) < 2:
            randomSourceFilter = random.randint(0, (self.numFilter-1))
        
        # chose random filter to move element to
        randomDestFilter = randomSourceFilter
        # only use filter if not identical to source
        while randomSourceFilter == randomDestFilter:
            randomDestFilter = random.randint(0, (self.numFilter-1))
        
        # chose source element
        randomElement = random.randint(0, (len(newLists[randomSourceFilter])-1))
        
        # move element
        newLists[randomDestFilter].append(newLists[randomSourceFilter][randomElement])
        newLists[randomSourceFilter].pop(randomElement)
        
        return newLists
        

    def optimalFilter(self):
        '''Calculate optimal CAN filter.
        
        Iterates through all possible filters and finds optimal one.
        '''
        # loop through all variants to partition the CAN IDs to the given filter number
        for part in more_itertools.set_partitions(self.canIds, self.numFilter):
            lengthPart = 0
            filtersPart = []
            masksPart = []
            passMessages = []

            lengthPart, passMessages, filtersPart, masksPart = self.calcFilters(part)

            if(self.minLength > lengthPart):
                self.minLength = lengthPart
                self.bestFilters = filtersPart
                self.bestMasks = masksPart
                self.bestLists = part
                self.passMessagesMin = passMessages

    def calcFilters(self, idLists):
        lengthPart = 0
        filtersPart = []
        masksPart = []
        passMessages = []


        # loop through lists for all CAN filters
        for idList in idLists:
            lengthList, canMask, canFilter = self.calcFilter(idList)
            
            lengthPart += lengthList
            passMessages.append(lengthList)
            filtersPart.append(canFilter)
            masksPart.append(canMask)
            
        return lengthPart, passMessages, filtersPart, masksPart


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
        lenList = len(idList)
        # calculate mask with xor over all IDs in list
        if(lenList > 0):
            canFilter = reduce(iand, idList)
            canMask = reduce(ior, idList) ^ canFilter
       
        # number of unwanted messages that pass filter
        if(lenList > 1):
            numPassIds = pow(2, bin(canMask).count('1')) - lenList
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
        
        cmdParser.add_argument("-a", "--algorithm", choices=["OPT","SA"], default="OPT", required=False, help="algorithm to use (default: OPT)")

        self.cmdArgs = cmdParser.parse_args(argv[1:])

        self.idBitSize = int(self.cmdArgs.size)
        self.numFilter = int(self.cmdArgs.num)
        
        self.outputFile = self.cmdArgs.out
        
        self.algorithm = self.cmdArgs.algorithm

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
    
        
