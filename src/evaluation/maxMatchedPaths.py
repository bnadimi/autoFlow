# In this evaluation method, we start with the longest path first and try to find all the instances of that path. Then it will check the second-largest 
# path and try to find all instances of it in the trace file. It goes like this until no instances are left in the trace file.
import networkx as nx 
import matplotlib.pyplot as plt
import numpy as np
import sys
import joblib
from datetime import datetime
import scipy as sp

class maxMatchedPaths:
	def __init__ (self, traceFilePath, availablePaths, initialNodes, terminalNodes, resultFileName):
		self.availablePaths = availablePaths
		self.availablePathsUsage = [[0 for x in range(len(y))] for y in self.availablePaths] 
		self.traceFilePath = traceFilePath
		self.fileName = resultFileName
		self.sizeOfAdMatrix = 100 #8
		self.adMatrix    = [[0 for x in range(self.sizeOfAdMatrix)] for y in range(self.sizeOfAdMatrix)] 
		self.arrayOfActivePaths = [0] * self.sizeOfAdMatrix
		self.toBePrinted = ""
		self.maxIndexNode = 0
		self.tracesArray = []
		self.traceUnderEvaluation = []
		self.starting_nodes = initialNodes
		self.ending_nodes = terminalNodes
		self.all_paths_sorted = [[] for x in range(max(self.starting_nodes)+1)]  # = []
		self.startAndEnds = [[] for x in range(max(self.starting_nodes)+1)]
		self.counterForTest = 0

		# for i in self.availablePathsUsage:
		# 	for j in i:
		# 		print ("0 ", end="")
		# 	print ("")

	def read_synthetic_traces(self, path):
		tempTraceArray = []
		flag = False
		try:
			with open(path, 'r') as File:
				infoFile = File.readlines() 
				eachFile = []
				for line in infoFile: 
					words = line.split(" ")
					for i in words:
						if (i != '' and i != '\n' and i != '-1' and i != '-2'):
							flag = True
							tempTraceArray.append(int(i))
						elif (i == '-2'):
							flag = False
							self.tracesArray.append(tempTraceArray)
							tempTraceArray = []
					if flag == True:
						self.tracesArray.append(tempTraceArray)
						tempTraceArray = []
		except FileNotFoundError as e:
			print ("\tError Reading Traces File!")
			exit()

	def read_jbl_traces (self, path):
		file = joblib.load(path)

		for i, j in enumerate(file):
			tempTrace = []
			for each in file[j]:
				tempTrace.append(int(each))
			self.tracesArray.append(tempTrace) 

	def read_inputs(self, traceFilePath):
		trace_file_type = traceFilePath.split('.')
		if trace_file_type[-1] == "txt":
			self.read_synthetic_traces(traceFilePath)
		else:
			self.read_jbl_traces(traceFilePath)

	def write_to_file (self, fileName, writeString):
		with open(fileName, 'a') as f:
    			f.write(writeString)

	def checkIfPathIsAvailable(self, sub_trace):
		# print ("Length of sub_trace = ", len(sub_trace))
		# print (sub_trace)
		shouldBeRemoved = []
		# print("Sub trace = ", sub_trace)
		for path_under_test in self.availablePaths[sub_trace[0]]:
			if set(path_under_test).issubset(set(sub_trace)):
				lastIndex = 0
				shouldBeRemoved = []
				# print("Path under test = ", path_under_test)
				for anEvent in path_under_test:
					# print("last index = ", lastIndex, " / index = ", sub_trace[lastIndex:].index(anEvent))
					# if sub_trace.index(anEvent) >= lastIndex:
					if anEvent in sub_trace[lastIndex:]:
						self.counterForTest += 1
						# shouldBeRemoved.append(sub_trace.index(anEvent))
						# lastIndex = sub_trace.index(anEvent)
						shouldBeRemoved.append(sub_trace[lastIndex:].index(anEvent)+lastIndex)
						lastIndex = sub_trace[lastIndex:].index(anEvent)
					else:
						# print("")
						break
			if len(shouldBeRemoved) == len(path_under_test):
				self.availablePathsUsage[sub_trace[0]][self.availablePaths[sub_trace[0]].index(path_under_test)] += 1
				# print("\t\tAccepted path = ", path_under_test)
				return shouldBeRemoved
			else:
				shouldBeRemoved = []
		return 0

		# shouldBeRemoved = []
		# for path_under_test in availablePaths[sub_trace[0]]:
		# 	lastIndex = 0
		# 	for anEvent in path_under_test:
		# 		if anEvent in sub_trace and sub_trace.index(anEvent) >= lastIndex:
		# 		# if anEvent in sub_trace: 
		# 			self.counterForTest += 1
		# 			shouldBeRemoved.append(sub_trace.index(anEvent))
		# 			lastIndex = sub_trace.index(anEvent)
		# 		else:
		# 			break
		# 	if len(shouldBeRemoved) == len(path_under_test):
		# 		# print ("\t", end="")
		# 		# for items in shouldBeRemoved:
		# 		# 	print(sub_trace[items], " ", end="")
		# 		return shouldBeRemoved
		# 	else:
		# 		shouldBeRemoved = []
		# return 0

	def find_path (self, inputPath):
		# print("Length = ", len(inputTrace))
		# toBeremoved = 0
		# totalNumberOfEvents = 0 
		# totalNumberOfAccepted = 0
		# arrayOfActivePaths = [0] * self.sizeOfAdMatrix
		# checkFlag = False
		# ratio = 0
		# numberofRatios = 0

		i = 0
		lastIndex = 0
		deletedMessages = 0
		while i < len(self.traceUnderEvaluation):
			if self.traceUnderEvaluation[i] == inputPath[0]:
				lastIndex = i
				shouldBeRemoved = []
				for anEvent in inputPath:
					if anEvent in self.traceUnderEvaluation[lastIndex:]:
						shouldBeRemoved.append(self.traceUnderEvaluation[lastIndex:].index(anEvent)+lastIndex)
						lastIndex += self.traceUnderEvaluation[lastIndex:].index(anEvent)
						print("Found ", anEvent, "at index ", lastIndex, " length of trace now is ", len(self.traceUnderEvaluation))
					else:
						i += 1
						break
				if len(shouldBeRemoved) == len(inputPath):
					deletedMessages += len(shouldBeRemoved)
					for k in reversed(shouldBeRemoved):
						del self.traceUnderEvaluation[k]#+i
					print("Removed and i = ", i)
			else:
				i += 1

		return deletedMessages





		# test = 0
		# i = 0
		# foundPathFlag = False
		# while i < len(inputTrace):
		# 	foundPathFlag = False
		# 	if inputTrace[i] in self.starting_nodes:
		# 		# print ("i = ", i, " inputTrace size = ", len(inputTrace))
		# 		for terminal in self.startAndEnds[inputTrace[i]]:
		# 			if terminal in inputTrace[i:len(inputTrace)]:
		# 				j = inputTrace[i:len(inputTrace)].index(terminal)
		# 				sub_trace = inputTrace[i:i+j+1]
		# 				remove = self.checkIfPathIsAvailable(sub_trace)
		# 				if remove != 0:
		# 					foundPathFlag = True
		# 					totalNumberOfAccepted += len(remove)
		# 					# test = []
		# 					for k in reversed(remove):
		# 						# test.append(inputTrace[k+i])
		# 						del inputTrace[k+i]
		# 					# print("Finale accepted = ", end="")
		# 					# for t in reversed(test):
		# 					# 	print(t, end=" ")
		# 					# print("")
		# 					# print("Test length = ", test)
		# 					break
		# 				else:
		# 					foundPathFlag = False
		# 	if foundPathFlag == False:
		# 		i += 1


		# old_method_accepted_events_number = 0


		# ############################################################################ For test only
		# notAccepted = [0 for x in range(self.sizeOfAdMatrix)]
		# totalNotAccepted = 0
		# for i in inputTrace:
		# 	notAccepted[i] += 1
		# # print("Not Accepted")
		# for i in range(len(notAccepted)):
		# 	if notAccepted[i]:
		# 		# print (i, " : ", notAccepted[i])
		# 		totalNotAccepted += notAccepted[i]
		# # print ("In total = ", totalNotAccepted)
		# # print ("input trace = ", inputTrace)

		# # for i in range(len(self.availablePathsUsage)):
		# 	# if self.availablePathsUsage[i]:
		# 		# for j in range(len(self.availablePathsUsage[i])):
		# 			# if self.availablePathsUsage[i][j]:
		# 				# print(self.availablePaths[i][j], ": ", self.availablePathsUsage[i][j])
		# 				# print (j, end=" ")
		# 		# print ("")
		# ############################################################################ For test only

		# self.toBePrinted += "\n\tAccepted Events Number = " + str(totalNumberOfAccepted + old_method_accepted_events_number)
		# # print ("\tAccepted Events Number = ", totalNumberOfAccepted + old_method_accepted_events_number)
		# return totalNumberOfAccepted + old_method_accepted_events_number

	def Evaluate(self):
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		self.toBePrinted += "\nStart Time =" + current_time
		# print("\nStart Time =", current_time)

		self.read_inputs(self.traceFilePath)

		self.toBePrinted += "\n\t------------------------------------------------------------------Creating the Finite State Machine------------------------------------------------------------------"
		# print ("\t------------------------------------------------------------------Creating the Finite State Machine------------------------------------------------------------------")


		################################################################################################################### For Efficiency
		# print("Starting nodes = ", self.starting_nodes)
		# print("Ending nodes = ", self.ending_nodes)

		for pathCases in self.availablePaths:
			for paths in pathCases:
				if paths[-1] not in self.startAndEnds[paths[0]]:
					self.startAndEnds[paths[0]].append(paths[-1])
		# print ("test startAndEnds: ", self.startAndEnds)		
		################################################################################################################### For Efficiency

		self.toBePrinted += "\n\tDone creating the Finite State Machine!"
		self.toBePrinted += "\n\t----------------------------------------------------------------From now on we are testing the parser----------------------------------------------------------------"
		# print ("\tDone creating the Finite State Machine!")
		# print ("\t----------------------------------------------------------------From now on we are testing the parser----------------------------------------------------------------")


		# finalRatio = 0
		finalNumberofRatios = 0
		totalCountOfEvents = 0
		totalAcceptedEventsNumber = 0

		# print ("\n")
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		# print("\tCurrent Time =", current_time)
		self.toBePrinted += "\n\n\tCurrent Time =" + current_time


		for traceIndex in range(len(self.tracesArray)):

			totalCountOfEvents += len(self.tracesArray[traceIndex])
			self.traceUnderEvaluation = self.tracesArray[traceIndex]
			acceptedEventsNumber = 0
			for pathClass in self.availablePaths:
				for path in pathClass:
					print("Working on path: ", path)	
					acceptedEventsNumber += self.find_path(path)
					print("Test = \t\t", acceptedEventsNumber)

			totalAcceptedEventsNumber += acceptedEventsNumber
			finalNumberofRatios += 1

		# for i in range(len(self.availablePathsUsage)):
		# 	if self.availablePathsUsage[i]:
		# 		for j in range(len(self.availablePathsUsage[i])):
		# 			if self.availablePathsUsage[i][j]:
		# 				print(self.availablePaths[i][j], ": ", self.availablePathsUsage[i][j])
		# 				# print (j, end=" ")
		# 		print ("")

		# for traceIndex in range(len(self.tracesArray)):

		# 	totalCountOfEvents += len(self.tracesArray[traceIndex])
		# 	self.toBePrinted += "\n\tTrace number " + str(traceIndex) + " : "
		# 	# print ("\tTrace number ", traceIndex, " : ")
		# 	acceptedEventsNumber = self.find_path(self.tracesArray[traceIndex])
		# 	# acceptedEventsNumber = find_path_old_method(tracesArray[traceIndex])

		# 	totalAcceptedEventsNumber += acceptedEventsNumber
		# 	# finalRatio += R
		# 	finalNumberofRatios += 1




		self.toBePrinted += "\n\tTotal number of events = " + str(totalCountOfEvents)
		self.toBePrinted += "\n\tNumber of traces = " + str(finalNumberofRatios)
		self.toBePrinted += "\n\tThe final answer is : " + str(totalAcceptedEventsNumber/totalCountOfEvents)
		# toBePrinted += "\n\tThe final answer is : " + str(finalRatio/finalNumberofRatios)
		# print ("\tTotal number of events = ", totalCountOfEvents)
		# print ("\tNumber of traces = ", finalNumberofRatios)
		# print ("\tThe final answer is : ", (totalAcceptedEventsNumber/totalCountOfEvents) )
		# print ("\tThe final answer is : ", (finalRatio/finalNumberofRatios) )


		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		# print("\nEnd Time =", current_time)
		# print ("")
		self.toBePrinted += "\n\nEnd Time =" + current_time + "\n\n\n\n\n\n\n\n"


		# FSMSize = 0
		# for i in range(sizeOfAdMatrix):
		# 	for j in range(sizeOfAdMatrix):
		# 			if FSMadMatrix[i][j] == 1:
		# 				FSMSize += 1
		# print ("FSM Size = ", FSMSize)
		# toBePrinted += "\n FSM Size =" + str(FSMSize) + "\n\n\n\n\n\n\n\n"

		self.write_to_file(self.fileName, self.toBePrinted)
		# print("Counter for test = ", self.counterForTest)
		return (totalAcceptedEventsNumber/totalCountOfEvents), (totalAcceptedEventsNumber/totalCountOfEvents)  
