"""
Tool Name:  Export CSV
Source Name: ExportCSV.py
Version: 0.1
Author: Riccardo Plaia, Roxana Urdea,Giacomo Gasco

This script will create a space, comma, or semi-colon delimited CSV
file
"""

################ Imports ####################
import os
import arcpy

import unicodecsv
import SSUtilities as UTILS
import locale as LOCALE
LOCALE.setlocale(LOCALE.LC_ALL, '')

delimDict = {"TAB": '\t', "COMMA": ',', "SEMI-COLON": ";","PIPE" : "|"}

################### GUI Interface ###################
def setup():

    #### Get User Provided Inputs ####
    inputTable = arcpy.GetParameterAsText(0)
    delimiter = arcpy.GetParameterAsText(1)
    rowNumbers = arcpy.GetParameter(2)
    #headers = arcpy.GetParameterAsText(3)
    outputFile = arcpy.GetParameterAsText(4)


    #inputTable = r'D:\Strigari\Hilti\GIS\ToolData\Tooldata.gdb\VL_TRDGRP_SIMPLE'
    #delimiter = "TAB"
    #rowNumbers = -1
    headers = False
    #outputFile = 'sample'


    #### Set Delimiter ####
    try:
        delimiter = delimDict[delimiter]
    except:
        delimiter = " "

    #### Execute Function ####
    exportCSV(inputTable,delimiter,rowNumbers, outputFile, headers)

def writeFile(fileToWrite, cursor, rowsPerFile, delimiter):
    rowsWritten = 0
    with open(fileToWrite,'wb') as csvfile:
        writer = unicodecsv.writer(csvfile, encoding='utf-8', delimiter=delimiter)
        for row in cursor:
            writer.writerow(row)
            rowsWritten += 1
            if rowsWritten % rowsPerFile == 0:
                break
    return rowsWritten


def exportCSV(inputTable,delimiter, rowNumbers, outputFile, headers):

    #### Create Progressor Bar ####
    arcpy.AddMessage(arcpy.GetIDMessage(84012))
    #arcpy.SetProgressor("step", arcpy.GetIDMessage(84012), 0, cnt, 1)

    #### Process Field Values ####
    try:
        rows = arcpy.da.SearchCursor(inputTable,"*")

    except:
        arcpy.AddIDMessage("ERROR", 204)
        raise SystemExit()

    #### Create Output File ####

    number_table_rows = long(arcpy.GetCount_management(inputTable)[0])


    print(number_table_rows)
    filename = outputFile
    number_files = 1

    rowsPerFile = 5
    rowsWritten = 0

    if (rowNumbers != -1):
        with arcpy.da.SearchCursor(inputTable, "*") as cursor:
            while  (rowsWritten < number_table_rows):
                rowsWritten += writeFile(filename+'_'+str(number_files) + ".csv", cursor, rowsPerFile, delimiter)
                number_files +=1
    else:
        with arcpy.da.SearchCursor(inputTable, "*") as cursor:
            with open(outputFile+".csv",'wb') as csvfile:
                writer = unicodecsv.writer(csvfile, encoding='utf-8', delimiter=delimiter)
                for row in cursor:
                    writer.writerow(row)


        #### Write Field Names to File ####
        '''
        if headers:
            #allFieldNames = arcpy.Describe(inputTable).Fields
            allFieldNames = [str(f.name) for f in arcpy.Describe(inputTable).Fields]
            outRow = delimiter.join(allFieldNames)
            writer.writerow(outRow)
        '''


    arcpy.SetProgressorPosition()

    arcpy.AddMessage(outputFile)

if __name__ == '__main__':
    export = setup()
