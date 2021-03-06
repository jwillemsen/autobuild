#!/usr/bin/python

# ******************************************************************
#      Author: Heather Drury
#              Justin Michel
#        Date: 7/06/2004
# ******************************************************************

import sys
sys.path.append("../matrix_database")

from HTMLScoreboard import *
from TestPlatform import *
from utils import *
from TestDBFileHandle import *
import string

#Uncomment when you need save the test results to database
# from TestDB import *


def ReadLogFiles ():
	fh=open(infile,"r")
	builds = []
	# read in text files containing test results for each platform
        for line in fh.readlines():
            name, file = line.split()
            build = TestPlatform (name, file)
            if (build.valid_raw_file == 1):
               print "********* BUILD", name
               builds.append (build)
            else:
               print "ERROR: invalid log file:", name, file
	fh.close()	
	return builds

def SaveBuildResults2HTML (directory, fname):
	# now print the results to an HTML file
	for n in range (0, len(builds)):
		builds[n].HTMLtestResults = HTMLPlatformTestTable(builds[n].name, directory)

		# print out the failed tests
		for m in range (0, len(builds[n].test_results)):
			if builds[n].test_results[m].passFlag == FAIL:
				builds[n].HTMLtestResults.addData2 (n, builds[n].test_results[m].passFlag, \
					builds[n].test_results[m].time, \
					builds[n].test_results[m].name)
		# print out the successful tests
		for m in range (0, len(builds[n].test_results)):
			if builds[n].test_results[m].passFlag == PASS:
				builds[n].HTMLtestResults.addData2 (n, builds[n].test_results[m].passFlag, \
					builds[n].test_results[m].time, \
					builds[n].test_results[m].name)
		builds[n].HTMLtestResults.writeHTML()

# build up test matrix
def BuildTestMatrix (builds, directory, fname, filename):
	testMatrix = TestMatrix (len(builds))
	for n in range (0, len(builds)):
		for m in range (0, len(builds[n].test_results)):
			testMatrix.addTestResult (n, builds[n].test_results[m].name, \
					builds[n].test_results[m].passFlag)

	# write out the HTML
	HTMLtestMatrix = HTMLTestMatrix2 (fname, directory)
	for n in range (0, len(testMatrix.testNames)):
		HTMLtestMatrix.addTestData (testMatrix.testNames [n], testMatrix.testResults[n], \
					testMatrix.fileNames [n], builds)

	totalPass = 0
	totalFail = 0
	totalSkip = 0
	for n in range (0, len(builds)):
		builds[n].npass, builds[n].nfail, builds[n].nskip = testMatrix.getTestResults(n)
		totalPass = totalPass + builds[n].npass
		totalFail = totalFail + builds[n].nfail
		totalSkip = totalSkip + builds[n].nskip
	HTMLtestMatrix.writeBriefs (totalPass, totalFail, totalSkip)

	for n in range (0, len(builds)):
		HTMLtestMatrix.writeBuildSummary (n, builds[n])
	getSummaryResults(HTMLtestMatrix, builds, filename)
	HTMLtestMatrix.writeHTML()
	HTMLtestMatrix.writeHTMLsummary()
	return testMatrix

# Write one HTML file for each test with each row representing a platform
def WriteTestHTML (testMatrix, builds):
	# print out HTML file for each test with results for all platforms
	for n in range (0, len(builds)):
		print "\tPlatform: ", builds[n].name, builds[n].ACEtotal, builds[n].ACEfail, builds[n].TAOtotal, builds[n].TAOfail
	for m in range (0, len(testMatrix.testNames)):
		fname = testMatrix.fileNames[m] + '.html'
		html = HTMLTestFile (fname)
		for n in range (0, len(builds)):
			html.addData2 (testMatrix.testResults[m][n], builds[n].name)
		html.writeHTML()

def getSummaryResults (HTMLtestMatrix, builds, fname):
	ACEtotal = 0
	TAOtotal = 0
	ACEfail = 0
	TAOfail = 0
        ACEpass = 0
        TAOpass = 0
        ACEperc = 0
        TAOperc = 0
        overall = 0
	skip = 0
	for n in range (0, len(builds)):
		print "\tPlatform: ", builds[n].name, builds[n].ACEtotal, builds[n].ACEfail, builds[n].TAOtotal, builds[n].TAOfail
		ACEtotal = ACEtotal+builds[n].ACEtotal
		TAOtotal = TAOtotal+builds[n].TAOtotal
		ACEfail = ACEfail+builds[n].ACEfail
		TAOfail = TAOfail+builds[n].TAOfail
		skip = skip+builds[n].nskip
		ACEpass = ACEtotal-ACEfail
		TAOpass = TAOtotal-TAOfail
		ACEperc = ComputePercentage(ACEpass, ACEtotal)
		TAOperc = ComputePercentage(TAOpass, TAOtotal)
		overall = ComputePercentage((TAOpass+ACEpass), (TAOtotal+ACEtotal))
	print "ACE tests ****", ACEtotal, ACEfail, ACEperc
	print "TAO tests ****", TAOtotal, TAOfail, TAOperc
	file = "/tmp/matrix_output." + fname + ".txt"
	fh=open(file,"w")
	percent='%\n'
	str = "# of ACE tests passed: %d\n" % (ACEtotal)
	fh.write (str)
	str = "# of ACE tests failed: %d\n" % (ACEfail)
	fh.write (str)
	str = "ACE percentage: %.2f" % ACEperc
	str = str+percent
	fh.write (str)
	fh.write("\n")

	str = "# of TAO tests passed: %d\n" % (TAOtotal)
	fh.write (str)
	str = "# of TAO tests failed: %d\n" % (TAOfail)
	fh.write (str)
	str = "TAO percentage: %.2f" % TAOperc
	str = str+percent
	fh.write (str)
	fh.write("\n")

	str = "# of tests passed: %d\n" % (TAOtotal+ACEtotal)
	fh.write (str)
	str = "# of tests failed: %d\n" % (TAOfail+ACEfail)
	fh.write (str)
	str = "# of tests skipped: %d\n" % (skip)
	fh.write (str)

	str = "Overall percentage: %.0f" % overall
	str = str+percent
	fh.write (str)
	fh.close()
#
	fname = outfile + ".TestMatrix"
	HTMLtestMatrix.writeSummary (ACEpass, ACEtotal, ACEperc, TAOpass, TAOtotal, TAOperc)

option=string.atoi(sys.argv[1])
infile=sys.argv[2]
directory=sys.argv[3]
outfile=sys.argv[4]
fname=outfile + ".matrix"

builds = ReadLogFiles ()
testMatrix = BuildTestMatrix (builds, directory, fname, outfile)
SaveBuildResults2HTML(directory,outfile)

if option == 1:
   WriteTestDBFiles(builds)

# Temporary comment out to avoid the requirement of MySQLdb.
# Uncomment when you need save the test results to database.
#if option == 2:
#   database_name = sys.argv[5]
#   SaveTestResults2DB(builds, database_name)

if option > 2:
   print "ERROR: invalid option", option
# there is no standardization of how the test names are created for ACE, TAO, until there is,
# we shouldn't do this HAD 2.11.04
#WriteTestHTML (testMatrix, builds)
print "Normal execution!"

