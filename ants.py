# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 12:39:29 2022

@author: OJ
"""

import random as r
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk


class Node:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index

class MyMap:
    def __init__(self, width, height, nodes, noSolutions):
        
        #making the actual "map"
        self.nodeList = []
        for i in range(0, nodes):
            self.nodeList.append(Node(r.randint(0, width), r.randint(0, height), i) )
        
        self.displayMap()
            
        #initialising stores of edge statistics
        self.topEdgeList = np.zeros( (int)(nodes * (nodes + 1) / 2) , dtype = int)
        self.edgeList = np.zeros( (int)(nodes * (nodes + 1) / 2) , dtype = int)
            
        #makes first round of solutions
        self.solutions = []
        for i in range(0, noSolutions):
            print("making solution in map: ",i)
            self.solutions.append(Solution(self))
            
        #should sort by distance travelled???
        self.solutions.sort(key = lambda x : x.distanceTravelled)
        
        #what fraction of solutions are significant, e.g 0.1 is top 10% of solutions
        significance = 0.1
        
        for i in range(0, len(self.solutions)):
            inTop = False
            if(i < len(self.solutions) * significance):
                inTop = True
            
            #for each node in solutions list of nodes
            for x in range(-1, nodes):
                #finds edge index of node and next node
                edgeIndex = MyMap.indexEdgeList(self.solutions[i].visitedNodes[x].index, self.solutions[i].visitedNodes[x +1].index, nodes)
                #increment edge index
                self.edgeList[edgeIndex] += 1
                if(inTop):
                    self.topEdgeList[edgeIndex] += 1
                
            
            
                
        #FIND OTHER HEURISTIC
            #make two arrays with integers for every edge
            #one counts number of times each edge is used
            #one counts number of times each edge is used in top x% of solutions
                #function that returns top edge frequency / edge frequency ** k
                #k determines how much separation between values
            #run function on all possible edges from node
            #sum heuristic values and divide each value by sum for fraction
            #do same for other heuristic
            #either add or multiply heuristics and use combined value to
            #determine next node
            
            
            
    def getNodeList(self):
        return self.nodeList
    
    #doesnt work!!!!!!!!!!!!!!!!!!!!
    def indexEdgeList(node1Index, node2Index, numberOfNodes):
        #ants indexing.png kind of explains it
        if(node2Index < node1Index):
            temp = node1Index
            node1Index = node2Index
            node2Index = temp
        
        index = node1Index * numberOfNodes
        index -= (node1Index * (node1Index +1)) /2
        index += node2Index - node1Index -1
        
        return index
    
    
    def heuristicA(current, nextt):
        """calculates heuristic value (estimation of how good of a choice 
        the next node is from the current)
        First:
        looks at distance between nodes
        uses value k to select how much closer nodes are prioritised, 0 treats 
        all nodes the same, bigger prioritises closer nodes more"""
        
        k = 1;
        # 1 / (distance between nodes) ^k
        return MyMap.calculateDistance(current, nextt) ** -k
        
    
    def calculateDistance(current, nextt):
        return ( ((current.x - nextt.x) **2) + ((current.y - nextt.y) **2) ) **0.5
    
    def displayMap(self):
        
        top = tk.Tk()

        canvas = tk.Canvas(top, bg = "blue", height = 250, width = 300)
        
        for node in self.nodeList:
            canvas.create_oval(node.x -3, node.y -3, node.x +3, node.y +3, fill = "black")
        
        canvas.pack()
        
    
#current have a class that generates decent random solutions
class Solution:
    def __init__(self, MyMap):
        self.unvisitedNodes = MyMap.getNodeList().copy()
        self.visitedNodes = []
        self.distanceTravelled = 0
        
        #gives a random starting node
        index = r.randint(0, len(self.unvisitedNodes) -1)
        print("unvisited: ",len(self.unvisitedNodes))
        print("visited: ",len(self.visitedNodes))
        self.exploreNode(index)
        
        #continue path until all nodes are visited
        while(len(self.unvisitedNodes) != 0):
            print("picking node")
            print("unvisited: ",len(self.unvisitedNodes))
            print("visited: ",len(self.visitedNodes))
            print("distance travelled: ",self.distanceTravelled)
            self.pickNextNode()
        
        
    
    def pickNextNode(self):
        """chooses a random next node weighted by the heuristic function"""
        print("PICKING")
        current = self.visitedNodes[len(self.visitedNodes) -1]
        
        #sums all heuristics
        heuristicSum = 0
        for i in range(0, len(self.unvisitedNodes)):
            heuristicSum += MyMap.heuristicA(current, self.unvisitedNodes[i])
            
        #chooses random next node weighted on heuristic function
        randomPoint = heuristicSum * r.random()
        print("r: ",randomPoint," sum: ",heuristicSum)
        index = -1
        while(randomPoint < heuristicSum and index < len(self.unvisitedNodes)):
            index += 1
            heuristicSum -= MyMap.heuristicA(current, self.unvisitedNodes[index])
        
        self.exploreNode(index)
        
        
    def exploreNode(self, index):
        #print("exploring: ",index)
        #moves node from unvisited to visited
        self.visitedNodes.append(self.unvisitedNodes[index])
        del self.unvisitedNodes[index]
        #adds on distance travelled
        self.distanceTravelled += MyMap.calculateDistance(
            self.visitedNodes[len(self.visitedNodes) -1], self.visitedNodes[len(self.visitedNodes) -2])

            
            
mapp = MyMap(800, 600, 10, 100)
distances = []

#for i in range(0, 1000):
 #   print("making solution ",i)
  #  solution = Solution(mapp)
   # distances.append(solution.distanceTravelled)

#bad plot
distances.sort()
#index = range(0, 100)

#time = [0, 1, 2, 3]
#position = [0, 100, 200, 300]

#plt.plot(index, distances)
#plt.xlabel('index')
#plt.ylabel('distances')

#better plot (hopefully)
#basically makes a histogram
#splits distances into sections with upper and lower distance boundaries of equal size
#records frequency of data in each boundary and plots
raange = distances[len(distances) -1] - distances[0]
sections = []
section = 0
totalSections = 25
for i in range(0, totalSections):
    sections.append(0)
    
for i in range(0, len(distances)):
    if(distances[i] < distances[0] + (raange * (section + 1) / totalSections)):
        sections[section] += 1
    else:
        section += 1
        
index = range(0, totalSections)
plt.plot(index, sections)
plt.xlabel('section')
plt.ylabel('frequency')
