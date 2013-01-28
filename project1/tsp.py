import sys
import os
import itertools
import math
import random


class Point :
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __str__(self):
		return "(" + self.x + ", " + self.y + ")"
	
	def getX(self):
		return self.x
	
	def getY(self):
		return self.y
	
	def distanceFrom(self, point):
		return math.sqrt(math.pow((self.x - point.getX()), 2) + math.pow((self.y - point.getY()), 2))
	

sampleSet = [Point(0,0), Point(2,1), Point(3,4), Point(5,3), Point(7,5), Point(8,1)]
#returns a list in folowing fomat [path, distance, timeFromClock]
def exhaustive(setOfPoints, n):
	itertoolsPermutations=itertools.permutations(setOfPoints, n)
	return doExhaustive(itertoolsPermutations, n)

def doExhaustive(permutations, n):
	shortestDistance = 99999999999999 #relativly large num
	shortestPath = None
	try:
		while True:
			currentPath = permutations.next()
			distance = 0
			for i in range(n-1):
				distance = distance + currentPath[i].distanceFrom(currentPath[i+1])# cals all except the last point going back to start
			distance = distance + currentPath[n-1].distanceFrom(currentPath[0])#go back to start
			if shortestDistance > distance:
				shortestDistance = distance
				shortestPath = currentPath

	except StopIteration:
		print "we have stoped" #will remove later
		return [shortestPath, shortestDistance]


"""
My nearest neighbor algo will do the following:
1. Randomly pick a point from the set as the start. This may cause problems with special cases, but the average tsp seems to be unaffected by this move
2. start will be set as current point, calcs the closest point from the set of remaining points
3. sets the new point as current, repeats until there no more points remaining in set
4. last point will calc distance back to start

in the case of tie in terms of who is closer, it will pick the point with the lowest x value ie the left most point, and then a the lowest y value if they have same x. This should at least make it harder for the worst case to occur, but is not going to fix the worst case


"""




#returns a list in folowing fomat [path, distance, timeFromClock]
def nearest(setOfPoints, n):
	path = setOfPoints #this is the set of all points used
	distance = 0 #distance is 0 at start
	start = random.randint(0, n-1) #picks a random point to start in the set, this causes less pre-iterations for better results in the average case, but potentially leads to the worst case scenario
	startPoint = setOfPoints[start] #holds the start so when the last point is calculated, the distance can be added for the return trip
	usedPath = [] # the list that will hold the path that is followed
	currentPoint = startPoint # set current point to calc distance form remaining points
	del path[start] #remove the start point from the list of points, this way it wont try and be used later in the loop
	while len(path) > 0: # visted points are removed from list during loop, so when there are no more points to loop over, it will stop
		pointIndex = 0
		nearestPoint = path[0] # start out by setting the first point in the set as nearest
		for i in range(len(path)): # range should return all ints from 0 to n-1, so there should be no index problems
			if currentPoint.distanceFrom(nearestPoint) > currentPoint.distanceFrom(path[i]):
				nearestPoint = path[i] # if the 'nearest' point is farther than the point in iteration, set the iteration point as nearest
				pointIndex = i
			elif currentPoint.distanceFrom(nearestPoint) == currentPoint.distanceFrom(path[i]):
				if nearestPoint.getX() > path[i].getX(): # handels if there are ties
					nearestPoint = path[i] # give the lower x value the 'closest point'
					pointIndex = i
				else:
					if nearestPoint.getY() > path[i].getY():
						nearestPoint = path[i] # if there are equadistant points with the same x value, picks the point with lowest y
						pointIndex = i
		distance = distance + currentPoint.distanceFrom(nearestPoint)# add the distance, should have closest point out of loop
		usedPath.append(currentPoint) # add point to path
		currentPoint = nearestPoint # move the current point to the nearest
		del path[pointIndex] # remove the point that is now the current point
	distance = distance + currentPoint.distanceFrom(startPoint) # once the loop is done, we need to go back to the start
	usedPath.append(currentPoint)
	return [usedPath, distance] # will add clock later


def loadInputs():
	numberOfPoints = random.randint(5, 20) # should provide a sufficent number of points to analyize, but not cause a lot of problems on the upperbound of exhausive search
	listOfXValues = generateRandomPoints(numberOfPoints)# will gen the x values of the points
	listOfYValues = generateRandomPoints(numberOfPoints)# will gen the y values of the points
	listOfPoints = []
	for i in range(n):
		listOfPoints.append(Point(listOfXValues[i], listOfYValues[i]))
	removeDuplicates(listOfPoints)
	numberOfPoints = len(listOfPoints)#duplicates may have been removed, lowering number of points from before
	nearestResult = nearest(listOfPoints, numberOfPoints)
	exhaustiveResult = exhaustive(listOfPoints, numberOfPoints)

#genrates random ints between 0 and 30
def generateRandomPoints(n):
	listOfVals = []
	numVals = n
	while numVals > 0:
		listOfVals.append(random.randint(0, 30))
		numVals = numVals - 1
	return listOfVals

#removes duplicate points 
def removeDuplicates(listOfPoints):
	listOfPotential = [] #contains list of potential duplicates
	for i in range(len(listOfPoints)): # will find all points with the same x value
		for j in range(i+1, len(listOfPoints)):
			if listOfPoints[i].getX() == listOfPoints[j].getX():
				if listOfPoints[i].getY() == listOfPoints[j].getY():
					if i != j: #just a check to make sure im not comparing the same index
						del listOfPoints[j] #remove duplicate point
	return listOfPoints

#func used to for testing only, uses a set group of points to test accuracy
def test():
	print "the points used in the sample are "
	for i in range(len(sampleSet)):
		print "(%i, %i)" % (sampleSet[i].getX(), sampleSet[i].getY())

	exhaustiveResult = exhaustive(sampleSet, 6)
	nearestResult = nearest(sampleSet, 6)
	print "nearest result"
	for i in range(len(nearestResult[0])):
		print "(%i, %i)" % (nearestResult[0][i].getX(), nearestResult[0][i].getY())
	print nearestResult[1]
	print "exhaustive result"
	for i in range(len(exhaustiveResult[0])):
		print "(%i, %i)" % (exhaustiveResult[0][i].getX(), exhaustiveResult[0][i].getY())
	print exhaustiveResult[1]
	

#loadInputs() this func will be used on final version, sample set is used turing test
test()
