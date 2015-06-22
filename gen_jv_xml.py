#!/usr/bin/python

from sys import argv
import codecs

print "Start."
script, filename = argv
print "script: %r." % script
print "filename: %r." % filename

print "Opening the rawfile..."
rawfile = codecs.open(filename, 'r', encoding='utf-8')
xmlfile = codecs.open(filename + ".xml", 'w', encoding='utf-8')

isDepartureData=2; # 0: We are now NOT handling departure data, 1: We are now handling departure data, 2:Initialize state
departureLatList = []
departureLonList = []
destinationLatList = []
destinationLonList = []

# Processing all lines in rawfile
lineCount=0
for string in rawfile:
  lineCount = lineCount + 1
  print "Processing[%d]:%s" % (lineCount, string)

  # skip the header (first line)
  if (lineCount == 1) :
    continue

  strtmp1 = string
  # print "len(strtmp1):%r" % (len(strtmp1))
  keyIdxNext = strtmp1.find('(', 0)
  while (keyIdxNext != -1):
    # Initialize departure/destination state
    if (isDepartureData == 2) :
      isDepartureData = 1

    startIdx = keyIdxNext + 1
    keyIdxEnd = strtmp1.find(',', startIdx)
    endIdx = keyIdxEnd
    # print "keyIdxNext01:%r" % (keyIdxNext)
    # print "keyIdxEnd:%r" % (keyIdxEnd)
    # print "startIdx:%r" % (startIdx)
    # print "endIdx:%r" % (endIdx)
    strtmp2 = strtmp1[startIdx:endIdx]
    print "Found latitute:%s" % (strtmp2)
    if (isDepartureData == 1) :
      departureLatList.append(strtmp2);
    elif (isDepartureData == 0) :
      destinationLatList.append(strtmp2);

    keyIdxNext = strtmp1.find(',', endIdx)
    startIdx = keyIdxNext + 2
    keyIdxEnd = strtmp1.find(')', startIdx)
    endIdx = keyIdxEnd
    strtmp2 = strtmp1[startIdx:endIdx]
    print "Found longitute:%s" % (strtmp2)
    if (isDepartureData == 1) :
      departureLonList.append(strtmp2);
    elif (isDepartureData == 0) :
      destinationLonList.append(strtmp2);

    # Try to find next keyIdxNext
    keyIdxNext = strtmp1.find('(', endIdx)
    # print "keyIdxNext02:%r" % (keyIdxNext)

    # Toggle departure/destination state
    if (isDepartureData == 0) :
      isDepartureData = 1
    elif (isDepartureData == 1) :
      isDepartureData = 0

# After all lines in rawfile was parsed
for index in range(len(departureLatList)):
  depLat = departureLatList[index]
  depLon = departureLonList[index]
  desLat = destinationLatList[index]
  desLon = destinationLonList[index]
  print "%s,%s\t%s,%s" % (depLat, depLon, desLat, desLon)
  # dumpfile.write(wstr)
  # dumpfile.write("\n")

  # if (lineCount == 3) :
  #   break

xmlfile.close()
rawfile.close()

print "Done."
