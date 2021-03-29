# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 01:27:12 2021

@author: SAYED & SANTANA
"""

import sys
import time



class Node():
    def __init__(self, state, parent=None, action=None, cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth


class StackFringe():
    def __init__(self):
        self.fringe = []

    def add(self, node):
        self.fringe.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.fringe)

    def empty(self):
        return len(self.fringe) == 0
    
    def size(self):
        return len(self.fringe)

    def remove(self):
        if self.empty():
            raise Exception("empty fringe")
        else:
            node = self.fringe[-1]
            self.fringe = self.fringe[:-1]
            return node


class QueueFringe(StackFringe):

    def remove(self):
        if self.empty():
            raise Exception("empty fringe")
        else:
            node = self.fringe[0]
            self.fringe = self.fringe[1:]
            return node
        


class Path_Finder():

    def __init__(self, file_name):
        
        # Map for save graph
        self.maps = {}
        
        # Load data from files into memory
        print("Loading Map...")
        self.load_data(file_name)
        print("Map loaded...")
        
        
        
        # Keep track of number of states explored
        self.num_explored = 0
        
        # Initialize an empty explored set
        self.explored = set()
        
        # Initialize cost to zero
        self.cost = 0
        
        # Initialize cost to zero
        self.running_time = 0
        
        # Initialize path to none
        self.path = None
        
        # Initialize maximum number of nodes to zero
        self.maximum_number_of_nodes = 0

    


    def load_data(self, file_name):
    
        with open(file_name, 'r') as f:
            line  = f.readline()
            line  = line.rstrip('\n').split(' ')
            
            # Scan number of rows and columns and stote them in map
            self.maps["rows"] = int(line[0])
            self.maps["columns"] = int(line[1])
            
            # Scan source and stote them in map
            line  = f.readline()
            self.maps["source"] = tuple(int(i) for i in line.rstrip('\n').split(' '))
            
            # Scan goal and stote them in map
            line  = f.readline()
            self.maps["goal"] = tuple(int(i) for i in line.rstrip('\n').split(' '))
    
            # Scan cost from graph and stote them in map
            self.maps["cost"] = []
            for line in f.readlines():
                self.maps["cost"].append([int(i) for i in line.rstrip('\n').split(' ')])    
        

    def print(self):
        
        # First check is there any path exist
        if self.path == None:
            print("The cost of the path found: -1")
            print("The path as a sequence of actions and coordinates : NULL")
        else:  
            path_sequence = []
            node = self.path
            
            # Calculating path
            while node.parent is not None:
                r, c = node.state
                path_sequence.append((node.action, (r, c)))
                node = node.parent
            path_sequence.append(("Start", self.maps['source']))
            path_sequence.reverse()
            print("The cost of the path found : ", self.cost)
            print("The path as a sequence of actions and coordinates : ", path_sequence)
        
        print("The number of nodes expanded : ", self.num_explored)
        print("The maximum number of nodes held in memory: ", self.maximum_number_of_nodes)
        print("The runtime of the algorithm in milliseconds: ", self.running_time * 1000)


    def generate_successor(self, state):
        row, col = state
        candidates = [
            ("Up", (row - 1, col)),
            ("Down", (row + 1, col)),
            ("Left", (row, col - 1)),
            ("Right", (row, col + 1))
        ]
        
        
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.maps["rows"] and 0 <= c < self.maps["columns"] and self.maps["cost"][r][c] != 0:
                result.append((action, (r, c)))
        return result


    def  Breadth_First_Search(self):
        
        self.running_time = time.time()
        
        # Initialize fringe to just the starting position
        start = Node(state=self.maps['source'])
        fringe = QueueFringe()
        fringe.add(start)

        

        # Keep looping until solution found
        while True:
            # Check whether 3 minutes over!!            
            if time.time() > self.running_time + 180:
                self.running_time = time.time() - self.running_time
                return
            
            # If nothing left in fringe, then no path
            if fringe.empty():
                self.running_time = time.time() - self.running_time
                return
            # Update maximum number of nodes
            self.maximum_number_of_nodes = max(self.maximum_number_of_nodes, fringe.size())
            
            # Choose a node from the fringe(Queue)
            node = fringe.remove()
            
            # Update total number of explored node 
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.maps["goal"]:
                self.path = node
                self.running_time = time.time() - self.running_time
                self.cost = node.cost
                return

            # Mark node as explored
            self.explored.add(node.state)
            
            # Add neighbors to fringe
            for action, state in self.generate_successor(node.state):
                if not fringe.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action, cost=self.maps["cost"][state[0]][state[1]])
                    child.cost += child.parent.cost
                    child.depth = child.parent.depth + 1
                    fringe.add(child)
                    

def main():
    
    file_name = sys.argv[1]
    algorithm_name = sys.argv[2]
    
    
    PF = Path_Finder(file_name)
    print("Path Finder Search Algorithm: ", algorithm_name)
    if algorithm_name =="BFS":
        PF.Breadth_First_Search()
    PF.print()
    
if __name__ == "__main__":
    main()