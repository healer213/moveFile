#--------------------------------------------------------------------------------------------------
#                                      MOVEFILE
#--------------------------------------------------------------------------------------------------
#   This script will find all files of a specified type in one directory and move them to another.
#   This will prove useful when moving files on the Linux systems to help organize them quickly.
#
#   Instructions:
#
#   When typing directory names, include the "/" at the end or else you end up with this:
#       New destination file names:
#          /home/astral/testTargettxtfile_5-2.txt
#          /home/astral/testTargettxtfile_5-1.txt
#          /home/astral/testTargettxtfile_5-3.txt
#          /home/astral/testTargettxtfile_5-4.txt
#          /home/astral/testTargettxtfile_5-5.txt
#       Total 5 new destinations ready.
#
#   Uncomment (remove the # from the beginning of the lines) which method/function you wish to use.
#   Different ones are better for different number of iterations.
#
#   Extensions will be concatenated with the * wildcard prior to execution.
#
#
#==================================================================================================

import os
import glob
from pathlib import Path
import shutil
movers = []
tarMoves = []
#--------------------------------------------------------------------------------------------------
#=======VAR CLEAR - THIS CLEARS ALL THE GLOBAL VARIABLES
#--------------------------------------------------------------------------------------------------
def varClear():
    movers.clear()
    #print("Movers list: " + str(len(movers)))
    tarMoves.clear()
    #print("tarMoves list: " + str(len(tarMoves)))
    srcDir = ""
    tarDir = ""
    fType = ""
    print("Variables cleared. Ready to start again...\n")
#--------------------------------------------------------------------------------------------------
#   DEFINE MULTI-USE FUNCTIONS
#--------------------------------------------------------------------------------------------------
#=======SHOW MOVES - PRINTS THE FILES AND TOTAL TO BE MOVED
#--------------------------------------------------------------------------------------------------
def showMoves(movers):
    for i in movers:
        print("\t" + i)
    print("\nTotal found: " + str(len(movers)))
#--------------------------------------------------------------------------------------------------
#=======COPY MOVES - COPIES THE FILES TO BE MOVED
#--------------------------------------------------------------------------------------------------
def cpMoves(movers,tarMoves):
    if len(movers)!=len(tarMoves):
        print("ERROR: Lists aren't the same")
    else:
        #print("Lists are same length")
        srcChk = []
        tarChk = []
        for i in movers:
            srcSpl = i.split("/")
            srcLen = len(srcSpl) - 1
            srcAdd = srcSpl[srcLen]
            srcChk.append(srcAdd)
        for j in tarMoves:
            tarSpl = j.split("/")
            tarLen = len(tarSpl) - 1
            tarAdd = tarSpl[tarLen]
            tarChk.append(tarAdd)
        #print("source check: " + str(srcChk))
        #print("target check: " + str(tarChk))
        if srcChk==tarChk:
            print("Proceeding with copy...\n")
            fileCt = len(tarMoves) - 1
            while fileCt > -1:
                shutil.copy2(movers[fileCt],tarMoves[fileCt])
                print("Copied: " + str(tarMoves[fileCt]))
                fileCt = fileCt - 1
            print("\nCopy completed for " + str(len(tarMoves)) + " files.")
#--------------------------------------------------------------------------------------------------
#=======MOVE MOVES - ACTUALLY RELOCATES THE FILES INSTEAD OF COPYING
#--------------------------------------------------------------------------------------------------
def mvMoves(movers,tarMoves):
    print("Move function called.\n")
    if len(movers)!=len(tarMoves):
        print("ERROR: Lists aren't the same")
    else:
        #print("Lists are same length")
        srcChk = []
        tarChk = []
        for i in movers:
            srcSpl = i.split("/")
            srcLen = len(srcSpl) - 1
            srcAdd = srcSpl[srcLen]
            srcChk.append(srcAdd)
        for j in tarMoves:
            tarSpl = j.split("/")
            tarLen = len(tarSpl) - 1
            tarAdd = tarSpl[tarLen]
            tarChk.append(tarAdd)
        #print("source check: " + str(srcChk))
        #print("target check: " + str(tarChk))
        if srcChk==tarChk:
            print("Proceeding with move...\n")
            fileCt = len(tarMoves) - 1
            while fileCt > -1:
                shutil.move(movers[fileCt],tarMoves[fileCt])
                print("Moved: " + str(tarMoves[fileCt]))
                fileCt = fileCt - 1
            print("\nMove completed for " + str(len(tarMoves)) + " files.")
#--------------------------------------------------------------------------------------------------
#=======SPLIT NAMES - REMOVES THE FILE NAMES FROM THEIR PATHS
#--------------------------------------------------------------------------------------------------
def splName(movers,tarDir):
    print("Converting source names to target names...\n")
    for i in movers:
        splitter = i.split("/")
        #print(splitter)
        lastSpl = len(splitter) - 1
        #print(lastSpl)
        fName = splitter[lastSpl]
        #print("fName is: " + fName)
        fName = tarDir + fName
        #print("tarName is now: " + fName)
        tarMoves.append(fName)

    print("New destination file names:")
    for j in tarMoves:
        print("\t" + j)
    print("Total " + str(len(tarMoves)) + " new destinations ready.\n")
    print("Original file names:")
    for i in movers:
        print("\t" + i)
#--------------------------------------------------------------------------------------------------
#=======ITERATE USING GLOB [UNTESTED]
#--------------------------------------------------------------------------------------------------
def runGlob(srcDir,fType):
    print("Finding all files ending in ." + fType + " in " + srcDir + "\n")
    for name in glob.glob(srcDir+"**/*."+fType, recursive=True):
        print(name)
        movers.append(name)
    showMoves(movers)

    if len(movers) == 0:
        print("No files found.\n\nReturning to start.\n-----------------------\n")
        varClear()
        mvStart()
#--------------------------------------------------------------------------------------------------
#=======ITERATE USING PATHLIB [UNTESTED]
#--------------------------------------------------------------------------------------------------
def runPathLib(srcDir,fType):
    print("Finding all files ending in ." + fType + " in " + srcDir + "\n")
    for path in Path(srcDir).glob("**/*."+fType):
        movers.append(str(path))
    showMoves(movers)

    if len(movers) == 0:
        print("No files found.\n\nReturning to start.\n------------------------\n")
        varClear()
        mvStart()
#--------------------------------------------------------------------------------------------------
#=======ITERATE USING SCANDIR [UNTESTED]
#--------------------------------------------------------------------------------------------------
def scanRecurse(srcDir,fType):
    print("Finding all files ending in ." + fType + " in " + srcDir + "\n")
    for entry in os.scandir(srcDir):
        if entry.name.endswith("."+fType) and entry.is_file():
            yield os.path.join(entry.name, entry.path)
        elif entry.is_dir():
            yield from scanRecurse(entry.path,fType)
def runScandir(srcDir,fType):
    for i in scanRecurse(srcDir,fType):
        print(i)
        movers.append(i)
    showMoves(movers)

    if len(movers) == 0:
        print("No files found.\n\nReturning to start.\n----------------------\n")
        varClear()
        mvStart()
#--------------------------------------------------------------------------------------------------
#=======ITERATE USING WALK [UNTESTED]
#--------------------------------------------------------------------------------------------------
def runWalk(srcDir,fType):
    print("Finding all files ending in ." + fType + " in " + srcDir + "\n")
    for root,dirs,files in os.walk(srcDir, topdown=True):
        for file in files:
            if file.endswith("."+fType):
                print(os.path.join(root,file))
                movers.append(os.path.join(root,file))
        for dir in dirs:
            print(os.path.join(root,dir+"/"))
    showMoves(movers)

    if len(movers) == 0:
        print("No files found.\n\nReturning to start.\n----------------------\n")
        varClear()
        mvStart()
#--------------------------------------------------------------------------------------------------
#=======METHOD CHOOSE - ALLOWS USER TO CHOOSE WHICH METHOD TO USE (IF THEY CARE).
#--------------------------------------------------------------------------------------------------
def methodChoose(srcDir,fType):
    print("Seeking " + fType + " files.\n")
    methodSelect = input("Which method would you like to use?\n\t1. (G)lob\n\t2. (W)alk\n\t3. (P)athLib\n\t4. (S)canDir\nSelection: ")
    match methodSelect:
        case ("G"|"g"|"1"):
            runGlob(srcDir,fType)
        case ("W"|"w"|"2"):
            runWalk(srcDir,fType)
        case ("P"|"p"|"3"):
            runPathLib(srcDir,fType)
        case ("S"|"s"|"4"):
            runScandir(srcDir,fType)
        case _:
            print("Invalid option. Please try again.\n")
            methodChoose()
#--------------------------------------------------------------------------------------------------
#=======ACTION CHOOSE - ALLOWS USER TO CHOOSE COPY OR MOVE.
#--------------------------------------------------------------------------------------------------
def actionChoose():
    actionChoice = input("Would you like to copy these files or move them?\n\t1. (C)opy\n\t2. (M)ove\nSelection: ")
    print("User has chosen: " + actionChoice + "\n")
    match actionChoice:
        case ("C"|"c"|"1"):
            cpMoves(movers,tarMoves)
        case ("M"|"m"|"2"):
            mvMoves(movers,tarMoves)
        case _:
            print("Invalid selection. Please try again.\n")
            actionChoose()
#--------------------------------------------------------------------------------------------------
#=======RESTART MENU - LETS THE USER DO ANOTHER COPY/MOVE OPERATION W/O RESTARTING MANUALLY
#--------------------------------------------------------------------------------------------------
def restartMenu():
    restartChoice = input("Would you like to perform another copy/move operation?\n\t1. (Y)es\n\t2. (N)o\nSelection: ")
    match restartChoice:
        case ("Y"|"y"|"1"):
            varClear()
            mvStart()
        case ("N"|"n"|"2"):
            quit()
#--------------------------------------------------------------------------------------------------
#                               ****RUNNING PROGRAM****
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#=======MV START - THIS IS THE INITIAL PORTION OF THE PROGRAM. USE THIS FUNCTION TO RESET.
#--------------------------------------------------------------------------------------------------
def mvStart():
    #===SOURCE DIRECTORY
    srcDir = input("Input source:")
    if srcDir == "":
        srcDir = os.getcwd()
        print("Source directory set as current directory:\n\t" + srcDir + "\n")

    # Convert possible relative paths
    # USER HOME
    if srcDir.startswith("~"):
        srcDir = os.path.expanduser(srcDir)
        print("Converted source directory to: " + srcDir + "\n")
    # REL TO CURRENT WORKING DIRECTORY
    if srcDir.startswith("./"):
        dir1 = srcDir.split("/")
        #print(dir1)
        srcDir = os.getcwd() + "/" + dir1[1]
        print("Converted relative directory to: \n\t" + srcDir + "\n")
    if srcDir.startswith("../"):
        dir1 = srcDir.split("/")
        #print(dir1)
        cwd = os.getcwd().split("/")
        #print("cwd = ")
        #print(cwd)
        cwd.pop()
        cwdLen = len(cwd)
        newSrc = []
        for x in cwd:
            newSrc.append(x)
        newSrc.append(dir1[1])
        #print("newSrc = ")
        #print(newSrc)
        srcDir = "/".join(newSrc)
        print("Source directory is: " + srcDir + "\n")

    # Ensure the source directory exists.
    if not os.path.isdir(srcDir):
        print("Source directory does not exist. Please try again.\n")

    #===FILE TYPE
    fType = input("Input file extension to search for.\n\tInput: ")
    print("Seeking files typed as: " + fType + "\n")

    #===TARGET DIRECTORY
    tarDir = input("Input path of the TARGET directory.\n\tInput: ")
    if tarDir == "":
        tarDir = os.getcwd()
        print("Target directory set as current directory:\n\t" + tarDir + "\n")

    # Convert possible relative paths
    if tarDir.startswith("~"):
        tarDir = os.path.expanduser(tarDir)
        print("Converted target directory to: " + tarDir + "\n")
    if tarDir.startswith("."):
        dir2 = tarDir.split("/")
        #print(dir2)
        tarDir = os.getcwd() + "/" + dir2[1]
        print("Converted relative directory to: \n\t" + tarDir + "\n")

    # Ensure the target directory exists.
    if not os.path.isdir(tarDir):
        makeDir = input("Target directory does not exist. Would you like to create it now?\n\n\t(Y)es\n\t(N)o\nSelection: ")
        if makeDir == "Y" or "y":
            os.mkdir(tarDir)
        else:
            print("Please try again.")


    # Ask the user which method to use.
    #print("Debug: fType == " + fType + "\n")
    #print("Debug: srcDir == " + srcDir + "\n")
    #print("Debug: tarDir == " + tarDir + "\n")
    methodChoose(srcDir,fType)
    # Now we split the strings and redifine the destination paths.
    splName(movers,tarDir)
    # Menu to ask user whether to copy or move files.
    actionChoose()
    # Menu to ask user to repeat process
    restartMenu()
mvStart()
#--------------------------------------------------------------------------------------------------
#   TO DO LIST:
#       - Create GUI with browsing capability to make easier to use for non-programmers?
#--------------------------------------------------------------------------------------------------
