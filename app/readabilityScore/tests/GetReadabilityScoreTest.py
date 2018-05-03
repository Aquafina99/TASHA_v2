import os
from TempFileChecker import *
import GetReadabilityScore

if (fileCheck("temp/test.txt.txt")): 
    os.remove("temp/test.txt.txt")

if (fileCheck("temp/blanktest.txt.txt")): 
    os.remove("temp/blanktest.txt.txt")

try:
    fopen = open("test.txt")
    print(GetReadabilityScore.getReadabilityScore("test.txt",fopen.read()))
    fopen.close()
    print ("Test Successful!")
except:
    print ("Test Failed!")

try:
    fopen = open ("blanktest.txt")
    print(GetReadabilityScore.getReadabilityScore("blanktest.txt",fopen.read()))
    fopen.close()
    print ("Error Expected!")
except:
    print ("Test Successful!")
