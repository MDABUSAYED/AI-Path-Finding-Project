# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 01:27:12 2021

@author: SAYED & SANTANA
"""

import sys
import time
from queue import PriorityQueue

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
        
class AStarFringe(QueueFringe):
    
    def __init__(self):
        self.fringe = PriorityQueue()

    def add(self, index, node):
        self.fringe.put((index, id(node), node))

    def contains_state(self, state):
        return any(node.state == state for index, i, node in self.fringe.queue)

    def empty(self):
        return len(self.fringe.queue) == 0
    
    def size(self):
        return len(self.fringe.queue)

    def remove(self):
        if self.empty():
            raise Exception("empty fringe")
        else:
            index, i, node = self.fringe.get()
            return node
        
    def manhattan_heuristic(self, node, goal):
        return abs(node.state[0] - goal[0]) + abs(node.state[1] - goal[1]) 
    

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
                #self.cost += node.cost
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
                    child = Node(state=state, parent=node, action=action, cost=self.maps["cost"][state[0]][state[1]] + node.cost)
                    child.depth = child.parent.depth + 1
                    fringe.add(child)
                    
                    
    def Iterative_Deepening_Search(self):
        
        def Total_Number_of_Explorable_Node(self):
            
            # Initialize fringe to just the starting position
            start = Node(state=self.maps['source'])
            fringe = QueueFringe()
            fringe.add(start)
            

            # Keep looping until the exploration of the whole graph
            while True:
               
            
                # If nothing left in fringe, then exploration of the map is complete and we need to return total explorable node
                if fringe.empty():
                    self.explored = set()
                    a = self.num_explored
                    self.num_explored = 0
                    return a
            
            
                # Choose a node from the fringe(Queue)
                node = fringe.remove()
            
                # Update total number of explored node 
                self.num_explored += 1


                # Mark node as explored
                self.explored.add(node.state)
            
                # Add neighbors to fringe
                for action, state in self.generate_successor(node.state):
                    if not fringe.contains_state(state) and state not in self.explored:
                        child = Node(state=state)
                        fringe.add(child)
            
        
        def Depth_First_Search(self, depth):
                
                
            # Initialize fringe to just the starting position
            start = Node(state=self.maps['source'])
            fringe = StackFringe()
            fringe.add(start)
            
        
            # Keep looping until solution found
            while True:
                
                # If nothing left in fringe, then need to return
                if fringe.empty():
                    return
                
                # Update maximum number of nodes
                self.maximum_number_of_nodes = max(self.maximum_number_of_nodes, fringe.size())
                
                # Choose a node from the fringe(Stack)
                node = fringe.remove()
                
                # Update total number of explored node 
                self.num_explored += 1
                
                # If node is the goal, then we have a solution
                if node.state == self.maps["goal"]:
                    self.path = node
                    self.cost = node.cost
                    return

                # Mark node as explored
                self.explored.add(node.state)
                
                # When we reached our limited depth, we need to continue, no need to add new node at fringe or no need to explore new node
                if node.depth == depth:
                    continue
                
        
                # Add neighbors to fringe
                for action, state in self.generate_successor(node.state):
                    if not fringe.contains_state(state) and state not in self.explored:
                        child = Node(state=state, parent=node, action=action, cost=self.maps["cost"][state[0]][state[1]] + node.cost)
                        child.depth = child.parent.depth + 1
                        fringe.add(child)
        
        # Start timer to calculate running time of IDS
        self.running_time = time.time()
        
        # Calculate total explorable node on a map 
        total_explorable_node = Total_Number_of_Explorable_Node(self)
        
        
        
        # Initialize depth
        d = 0
        # Node explore at current depth
        node_explore_this_depth = 0
        # Total node explore upto previous depth or before dfs call
        current = 0 
        
        
        while True:
            
            # Before calling DFS initialize explored set
            self.explored = set()
            
            # Total explored node on depth d
            node_explore_this_depth = self.num_explored - current
            
            

            # Check whether 3 minutes running time over!!            
            if time.time() > self.running_time + 180:
                self.running_time = time.time() - self.running_time
                return
            
            # On a particular depth if node explore current depth is equal to total explorable node then we need to stop calling DFS
            if node_explore_this_depth == total_explorable_node:
                self.running_time = time.time() - self.running_time
                return
            # If no path found for depth d, we should call DFS with depth d + 1
            if self.path == None:
                d += 1
                current = self.num_explored
                Depth_First_Search(self, depth=d)
            # If there is a path then need to stop calling DFS        
            else:
                self.running_time = time.time() - self.running_time
                return
                    
    def  AStar_Search(self):
        
        self.running_time = time.time()
        
        node_list = set()
        # Initialize fringe to just the starting position
        start = Node(state=self.maps['source'])
        fringe = AStarFringe()
        fringe.add(fringe.manhattan_heuristic(node=start, goal=self.maps["goal"]), start)
        

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
                if state not in node_list and state not in self.explored:
                    child = Node(state=state, parent=node, action=action, cost=self.maps["cost"][state[0]][state[1]] + node.cost)
                    fringe.add(child.cost + fringe.manhattan_heuristic(node=child, goal=self.maps["goal"]), child)
                    node_list.add(state)
                    
            
def main():
    
    file_name = sys.argv[1]
    algorithm_name = sys.argv[2]
    
    # Creare a path finder class
    PF = Path_Finder(file_name)
    print("Path Finder Search Algorithm: ", algorithm_name)
    if algorithm_name =="BFS":
        PF.Breadth_First_Search()
    elif algorithm_name =="IDS":
        PF.Iterative_Deepening_Search()
    elif algorithm_name =="A*":
        PF.AStar_Search()
    PF.print()
    
if __name__ == "__main__":
    main()