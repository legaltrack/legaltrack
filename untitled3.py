# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 13:06:36 2020

@author: Ghulam Mursaleen
"""

# Python3 Program to print BFS traversal 
# from a given source vertex. BFS(int s) 
# traverses vertices reachable from s. 
from collections import defaultdict 


# Create a graph given in 
# the above diagram 

graph = {'A': set(['B', 'C']),
         'B': set([ 'D', 'E']),
         'D':set([ ]),
         'E': set(['H', 'I']),
         'F':set([ ]),
         'H':set([ ]),
         'I':set([ ]),
         'J':set([ ]),
         'C': set(['F','G']),
         'G': set(['J'])
         }

def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited

print("visited", bfs(graph, 'A')) # {'B', 'C', 'A', 'F', 'D', 'E'}

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

print("path of BFS",list(bfs_paths(graph, 'A', 'J')))


def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None

print("shortes path",shortest_path(graph, 'A', 'J'))
 

