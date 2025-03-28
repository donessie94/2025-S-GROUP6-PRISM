'''
    Created by Daniel Levy, 3/17/2025

    This is an Error class to handle any errors from PRISM's data
    ingestion. The likelihood of errors is low, especially since
    we are trying to automate it. However, it doesn't mean we
    should have a safety net in case something unexpected happens.
'''
import json

class DataIngestionError:

    __fileName = None # Input file error was found in
    __line = None     # Specific line in file with issue
    __msg = None      # Error message we should output

    def __init__(self):
        self.__fileName = ""
        self.__line = ""
        self.__msg = ""

    '''
        If we encounter any errors, then this method will create a JSON
        file containing all the errors that can then be parsed/displayed
        to the user however we want.
    '''
    @staticmethod
    def createErrorJSON(fileName,errors):
        errorCount = len(errors)
        with open(f"{fileName}.json",'w') as oFile:
            oFile.write('{\n\t"errors": [\n')
            for i,e in enumerate(errors):
                json.dump(e.__dict__,oFile,indent=4)
                if(i != errorCount-1):
                    oFile.write(',\n')
            oFile.write('\t]\n')
            oFile.write('}\n')

    def setFileName(self,fileName):
        self.__fileName = fileName

    def setLine(self,line):
        self.__line = line

    def setMsg(self,msg):
        self.__msg = msg

    def getFileName(self):
        return self.__fileName

    def getLine(self):
        return self.__line

    def getMsg(self):
        return self.__msg
