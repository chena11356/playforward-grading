import sys
import json
import os

# Part 1: add all sessions to the same file
""" folders = [x[0] for x in os.walk('logfiles')]
folders.remove('logfiles')

for folder in folders:
  # open combined file with name of studentID
  fWrite = open('logfiles/'+folder.split('/')[1]+'.txt', 'w+')

  # grab number of files in directory
  files = os.listdir(folder)
  if '.DS_Store' in files:
    files.remove('.DS_Store')
  numFiles = len(files)
  
  i = 0
  while (i < numFiles):
    fRead = open(folder + '/' + str(i) + '.log', "r")
    for line in fRead:
      fWrite.write(line)
    fRead.close()
    i += 1
  
  fWrite.close() """

# Part 2: combine all studentID files into one

allFiles = os.listdir('logfiles')
logFiles = []
for fileName in allFiles:
  if '.txt' in fileName:
    logFiles.append(fileName)

fWrite = open('all.txt', 'w+')

for logFile in logFiles:
  fRead = open('logfiles/' + logFile, "r")
  for line in fRead:
      fWrite.write(line)
  fRead.close()

fWrite.close()