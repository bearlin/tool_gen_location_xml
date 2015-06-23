#!/usr/bin/python

from sys import argv
import codecs

print "Start."

if len(argv) < 5:
  print "Usage : " + argv[0] + " CoordinatesFilename LocationNamePrefix countryName CityName"
  print "Example : ./gen_jv_xml.py raw.txt FakePrefix Taiwan Taipei"
  exit(0)

currentScript, inputFilename, inputLocationNamePrefix, inputCountry, inputCity = argv
print "currentScript: %r" % currentScript
print "inputFilename: %r" % inputFilename
print "inputLocationNamePrefix: %r" % inputLocationNamePrefix
print "inputCountry: %r" % inputCountry
print "inputCity: %r" % inputCity

print "Opening the rawfile..."
rawfile = codecs.open(inputFilename, 'r', encoding='utf-8')
xmlfile = codecs.open(inputFilename + ".xml", 'w', encoding='utf-8')

currentDataState = 0; # 0:Initialize state; 1: We are now handling departure data; 2: We are now handling destination data;
departureLatList = []
departureLonList = []
destinationLatList = []
destinationLonList = []

# Processing all lines in rawfile
lineCount=0
for string in rawfile:
  lineCount = lineCount + 1
  #print "Processing[%d]:%s" % (lineCount, string)

  # Skip the header (first line)
  if (lineCount == 1) :
    continue

  strtmp1 = string

  # Find '('
  keyIdxNext = strtmp1.find('(', 0)
  while (keyIdxNext != -1):
    # Initialize departure/destination state
    if (currentDataState == 0) :
      currentDataState = 1

    startIdx = keyIdxNext + 1
    # Find ','
    keyIdxEnd = strtmp1.find(',', startIdx)
    endIdx = keyIdxEnd
    strtmp2 = strtmp1[startIdx:endIdx]
    #print "Found latitute:%s" % (strtmp2)

    # Save latitute
    if (currentDataState == 1) :
      departureLatList.append(strtmp2);
    elif (currentDataState == 2) :
      destinationLatList.append(strtmp2);

    # Find ','
    keyIdxNext = strtmp1.find(',', endIdx)
    startIdx = keyIdxNext + 2
    # Find ')'
    keyIdxEnd = strtmp1.find(')', startIdx)
    endIdx = keyIdxEnd
    strtmp2 = strtmp1[startIdx:endIdx]
    #print "Found longitute:%s" % (strtmp2)

    # Save longitute
    if (currentDataState == 1) :
      departureLonList.append(strtmp2);
    elif (currentDataState == 2) :
      destinationLonList.append(strtmp2);

    # Try to find next keyIdxNext
    keyIdxNext = strtmp1.find('(', endIdx)

    # Toggle departure/destination state
    if (currentDataState == 1) :
      currentDataState = 2
    elif (currentDataState == 2) :
      currentDataState = 1

# After all lines in rawfile was parsed
for index in range(len(departureLatList)):
  depLat = departureLatList[index]
  depLon = departureLonList[index]
  desLat = destinationLatList[index]
  desLon = destinationLonList[index]
  #print "%s,%s\t%s,%s" % (depLat, depLon, desLat, desLon)

  # Write xml results to xmlfile
  # Prepare datas
  locationNameDeparture = inputLocationNamePrefix + "_Departure_" + str(index)
  locationNameDestination = inputLocationNamePrefix + "_Destination_" + str(index)
  country = inputCountry
  city = inputCity
  postalCode=""
  street=""
  houseNumber=""
  crossing=""
  # Write departure
  print "Writing : %s(%s,%s), %s(%s,%s)" % (locationNameDeparture, depLat, depLon, locationNameDestination, desLat, desLon)
  xmlfile.write("  <!-- For jv test -->\n")
  xmlfile.write("  <Location name=\"" + locationNameDeparture + "\">\n")
  xmlfile.write("    <address country=\"" + country + "\" city=\"" + city + "\" postalCode=\"" + postalCode + "\" street=\"" + street + "\" houseNumber=\"" + houseNumber + "\" crossing=\"" + crossing + "\" />\n")
  xmlfile.write("    <position latitude=\"" + depLat + "\" longitude=\"" + depLon + "\" />\n")
  xmlfile.write("  </Location>\n")
  # Write destination
  xmlfile.write("  <Location name=\"" + locationNameDestination + "\">\n")
  xmlfile.write("    <address country=\"" + country + "\" city=\"" + city + "\" postalCode=\"" + postalCode + "\" street=\"" + street + "\" houseNumber=\"" + houseNumber + "\" crossing=\"" + crossing + "\" />\n")
  xmlfile.write("    <position latitude=\"" + desLat + "\" longitude=\"" + desLon + "\" />\n")
  xmlfile.write("  </Location>\n")

xmlfile.close()
rawfile.close()

print "Done."
