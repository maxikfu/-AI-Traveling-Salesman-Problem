import sys
import math
import copy
import numpy as np
import time
import random
from random import shuffle
import os
#import psutil
from collections import deque
import heapq
#class with cost functions
class Cost_Function:
	def c1(x,y):
		if x==y:
			return 0
		elif (x<3 and y<3):
			return 1
		elif x<3:
			return 200
		elif y<3:
			return 200
		elif ((x%7)==(y%7)):
			return 2
		else:
			return abs(x-y)+3
	def c2(x,y):
		if x==y:
			return 0
		elif x+y<10:
			return abs(x-y)+4
		elif ((x+y)%11)==0:
			return 3
		else:
			return (abs(x-y)^2)+10
	def c3(x,y):
		if (x==y):
			return 0
		else:
			return (x+y)**2
	def cost(pathList,costType):
		#pathList = stringToList(pathString)
		result =0
		i=0
		if costType=='c1':
			while i<len(pathList)-1:
				result = result + Cost_Function.c1(int(pathList[i]),int(pathList[i+1]))
				i=i+1
			result=result+Cost_Function.c1(int(pathList[i]),int(pathList[0]))
		elif costType=='c2':
			while i<len(pathList)-1:
				result = result + Cost_Function.c2(int(pathList[i]),int(pathList[i+1]))
				i=i+1
			result=result+Cost_Function.c2(int(pathList[i]),int(pathList[0]))
		else:
			while i<len(pathList)-1:
				result = result + Cost_Function.c3(int(pathList[i]),int(pathList[i+1]))
				i=i+1
			result=result+Cost_Function.c3(int(pathList[i]),int(pathList[0]))
		return result
def main(costF,citiesN,searchType):
	return costF,citiesN,searchType
def randomSearch(inputList, costF):
	pathList=inputList[:]
	#cost of already existing route
	minCost = Cost_Function.cost(pathList,costF)
	maxMEB=0
	lastCostDelta=0
	productiveSwaps=0
	termination = False
	print("Initial Cost ",minCost)
	while (maxMEB < meb) and (not termination):
		swapNode=random.sample(pathList,2)
		i=pathList.index(swapNode[0])
		j=pathList.index(swapNode[1])
		pathList[i],pathList[j]=pathList[j],pathList[i]
		newCost =Cost_Function.cost(pathList,costF)
		#print(minCost)
		if (newCost >= minCost):
			pathList[j],pathList[i]=pathList[i],pathList[j]
		else:
			minCost = newCost 
			productiveSwaps=productiveSwaps+1
			lastCostDelta = maxMEB #the last time we found better solution
		if (maxMEB - lastCostDelta) >= 90000:#if minCost didn't change in 60000 iterations we can terminate
			termination = True
			#print("We stuck in local/global maximum ", minCost)
		maxMEB=maxMEB+1
	print("Productive swaps ",productiveSwaps)
	return minCost,maxMEB,pathList
#children node creator for DFS and BFS
def nodeExpansion(node):
	localstate="".join(str(s) for s in node)
	initialNode=localstate
	listOfChildren = []
	for n in range(int(citiesN)):
		if n not in node:
			localstate=localstate+str(n)
			listOfChildren.append(localstate)
			localstate = initialNode
	return listOfChildren
def isComplite(path):
	if int(citiesN)==len(set(path)):
		return True
	else:
		return False
#depth first search with partial solutions
def  depthFirstSearch(initialPath, costF):
	minCost = pow(10,10)
	alreadyWasRoot=''
	#running algortihm 3 times so we can choose root randomly
	for j in range(3):

		#randomly choosing what city will be the root, avoiding same root
		startState = str(random.sample(initialPath,1).pop())
		while startState in alreadyWasRoot:
			startState = str(random.sample(initialPath,1).pop())
		alreadyWasRoot=alreadyWasRoot+startState
		expandedNumber=0
		minPath=""
		#startState="0"
		#list of nodes what we are going to expand
		frontier =[]
		frontier.append(startState)
		#expandinf untill frontier is not empty
		while frontier and expandedNumber< meb:
			workNode =[]
			[workNode.append(int(s)) for s in frontier.pop()]
			if isComplite(workNode) and minCost>=Cost_Function.cost(workNode,costF):
				minCost = Cost_Function.cost(workNode,costF)
				minPath=""
				minPath = "".join(str(s) for s in workNode)
			elif not isComplite(workNode):#going to expand this node
				for child in nodeExpansion(workNode):
					expandedNumber=expandedNumber+1
					#why keep solutions if it wont be less?
					if not Cost_Function.cost(child,costF)>minCost:
						frontier.append(child)
	print("Nodes in frontier ",len(frontier))
	return minPath,minCost,expandedNumber
#breadth first search for partial solutions
def  breadthFirstSearch(initialPath, costF):
	minCost = pow(10,10)
	alreadyWasRoot=''
	#running algortihm 3 times so we can choose root randomly
	for j in range(1):

		#randomly choosing what city will be the root, avoiding same root
		startState = str(random.sample(initialPath,1).pop())
		while startState in alreadyWasRoot:
			startState = str(random.sample(initialPath,1).pop())
		alreadyWasRoot=alreadyWasRoot+startState
		expandedNumber=0
		minPath=""
		startState="0"
		#list of nodes what we are going to expand
		frontier =deque()
		frontier.append(startState)
		#expandinf untill frontier is not empty
		while frontier and expandedNumber< meb:
			workNode =[]
			[workNode.append(int(s)) for s in frontier.popleft()]
			if isComplite(workNode) and minCost>=Cost_Function.cost(workNode,costF):
				minCost = Cost_Function.cost(workNode,costF)
				minPath=""
			elif not isComplite(workNode):#going to expand this node
				for child in nodeExpansion(workNode):
					expandedNumber=expandedNumber+1
					#why keep solutions if it wont be less?
					if not Cost_Function.cost(child,costF)>minCost:
							frontier.append(child)
	print("Nodes in frontier ",len(frontier))
	return minPath,minCost,expandedNumber
#simulated annealing
def probabilityAcceptance(d,t):
	if d<=0:
		return 1
	else:
		return math.exp(-d/t)

def simulatedAnnealing(pathList,costF):
	#print("Simulated Annealing Results for cost function =",costF)
	temperatureStart=10
	temperatureEnd=0.0001
	coolingFactor = 0.9999
	temperature=temperatureStart
	x=0
	lastCostDelta=0
	prevCost=Cost_Function.cost(pathList,costF)
	maxMEB=0
	print("Initial Cost ",prevCost)
	while temperature>temperatureEnd and maxMEB<meb:
		maxMEB=maxMEB+1
		swapNode=random.sample(pathList,2)
		i=pathList.index(swapNode[0])
		j=pathList.index(swapNode[1])
		pathList[i],pathList[j]=pathList[j],pathList[i]
		newCost =Cost_Function.cost(pathList,costF)
		difference=(newCost-prevCost)/prevCost
		#print(probabilityAcceptance(difference,temperature))
		if probabilityAcceptance(difference,temperature)>=random.random():
			prevCost=newCost
			lastCostDelta = maxMEB
			x=x+1
			# if x==100:
			# 	print(newCost)
			# 	x=0
		else:
			pathList[j],pathList[i]=pathList[i],pathList[j]
			if (maxMEB - lastCostDelta) >= 10000:#if minCost didn't change in 60000 iterations we can terminate
				termination = True
		temperature=temperature*coolingFactor
		#print(temperature, prevCost
	return prevCost,maxMEB,pathList

################################################

#getting parameters from cmd line
parameters=[]
param=[]
if __name__ == "__main__":
	#print(len(sys.argv))
	if len(sys.argv) > 1:
		costF,citiesN,searchType = main(sys.argv[1],sys.argv[2],sys.argv[3])
		param.append(costF)
		param.append(citiesN)
		param.append(searchType)
		parameters.append(param)
	else:
		with open('input.txt', 'r') as f:
			for line in f:
				parameters.append(line.rstrip('\n').split(","))
		f.close()
#output option
orig_stdout = sys.stdout
fout = open('output.txt', 'w')
sys.stdout = fout
for l in parameters:
	#generating set of cities
	costF=l[0]
	searchType=l[2]
	cities = [];
	citiesN=l[1]
	[cities.append(int(s)) for s in range(int(citiesN))]
	#suffling initial path
	#shuffle(cities)
	#output into file
	
	start_time = time.time()
	#setting up MEB
	meb=200000
	initialCities = cities[:]
	costs=0
	iniCosts=0
	paths=[]
	mebList=0

	if searchType=='SIM':
		print("SIM - Random Swap algorithm for cost function ",costF," Number of cities = ",citiesN)
		print()
		for i in range(3):#running 3 times because randomized algorithm
			print("Iteration Number=",i)
			start_time = time.time()
			initialCities = cities[:]
			shuffle(initialCities)
			iniCosts=iniCosts+Cost_Function.cost(initialCities,costF)
			cost,maxMEB,path = randomSearch(initialCities,costF)
			runningTime= time.time() - start_time
			costs=costs+cost
			mebList=mebList+maxMEB
			print("End Cost=",cost)
			print("Number of swaps=",maxMEB)
			print("Shortest path found ",path)
			print("Running time=",runningTime)
			print()
		#print(costs/3,mebList/3,iniCosts/3)
		print()
		print()	
	elif searchType=='SOPH':
		print("SOPH - Simulated Annealing algorithm for cost function ",costF," Number of cities = ",citiesN)
		print()
		for i in range(3):#running 3 times because randomized algorithm
			print("Iteration Number=",i)
			start_time = time.time()
			initialCities = cities[:]
			shuffle(initialCities)
			iniCosts=iniCosts+Cost_Function.cost(initialCities,costF)
			cost,maxMEB,path = simulatedAnnealing(initialCities,costF)
			runningTime= time.time() - start_time
			costs=costs+cost
			mebList=mebList+maxMEB
			print("End Cost=",cost)
			print("Number of swaps=",maxMEB)
			print("Shortest path found ",path)
			print("Running time=",runningTime)
			print()
		#print(costs/3,mebList/3,iniCosts/3)
		print()
		print()	
	elif searchType=='DFS':
		print("Depth First Search algorithm for cost function ",costF," Number of cities = ",citiesN)
		print()
		path,cost,expNodes = depthFirstSearch(cities,costF)
		print("End Cost=",cost)
		print("Number nodes expanded",expNodes)
		print("Shortest path found ",path)
		print("Running time=",time.time() - start_time)
		print()
		print()
	elif searchType=='BFS':
		print("Breadth First Search algorithm for cost function ",costF," Number of cities = ",citiesN)
		print()
		path,cost,expNodes =  breadthFirstSearch(cities,costF)
		print("End Cost=",cost)
		print("Number nodes expanded",expNodes)
		print("Shortest path found ",path)
		print("Running time=",time.time() - start_time)
		print()
		print()
fout.close()
