# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 00:45:20 2022

@author: ahkar
"""

########################################################
# complexity
########################################################
print('='*30)
print('memory complexity = O(N)')
print('='*30)
print('\t\t we maintain 3 lists (in_degree_count, q and top_sort, could use 2 tbh)')
print('\t\t each list is at most N (count of nodes) long')
print()

print('='*30)
print('runtime complexity = O(N+E)')
print('='*30)
print('\t\t the while-loop runs at least N (count of nodes) times')
print('\t\t within the while-loop we do a for-loop at most E (count of edges) times')
print()

########################################################
# imports
########################################################
from typing import List,Dict,Callable

########################################################
# debugging
########################################################
DEBUG_LEVEL = 0 # no logs
#DEBUG_LEVEL = 1 # log at outer while-loop level
#DEBUG_LEVEL = 2 # log at inner for-loop level

########################################################
# top sort a la Kahn's Algorithm
########################################################
def top_sort(graph : Dict, dependencies_fn : Callable):
    '''
    perform topological sort of some directed acyclic graph
    
    args:
        keys
            list of hashable objects representing nodes of the graph dependencies_fn
            function taking a key and returning a list of dependencies
                
    returns:
        list of keys in top sort order
        
    approach:
        Kahn's Algorithm
        https://en.wikipedia.org/wiki/Topological_sorting
        
        components
            (a) list  = in_degree_counter / enumerates # dependencies for each node of graph
            (b) queue = q / list of nodes that are no dependencies
            (c) list  = top_sort / final topological sorting order found via algo
        idea
            (1) simulate removing non-dependent nodes from graph
            (2) gather non-dependent nodes into `q` whenever they are found
            (3) pop from `q` into results container `top_sort` using non-emptiness of `q` to drive loop
            (4) nodes NOT accounted for in `top_sort` thus must be cyclic as cannot "bite off"
            
    '''

    # initialize dependency count tracker
    in_degree_count : Dict = {node:len(dependencies_fn(node)) for node in graph}
    
    # initialize queue with non-dependent nodes
    q               : List = [k for k,v in in_degree_count.items() if v == 0]
            
    # populate top_sort by
    # (1) popping from q
    # (2) adjusting in_degree_count to simulated simplifying the graph due to (1)
    # (3) add newly non-dependent nodes that subsequently appear due to (1)
    q_handled_index : int  = 0 # progression pointer
    top_sort        : List = [] # initialize Kahn topological sort output container
    
    # keep running until no "loose ends" are found
    while len(q):
    
        if DEBUG_LEVEL > 0: print('='*20)
        if DEBUG_LEVEL > 0: [print('in_degree_count',node,'\t',dependencies_fn(node)) for node in in_degree_count]
        if DEBUG_LEVEL > 0: print('q',q)

        # (1) popping from q
        pushed_node : object = q.pop(0) # grab popped node
        top_sort.append(pushed_node) # populate top_sort with said node
        q_handled_index += 1 # increment progression pointer
        
        if DEBUG_LEVEL > 0: print('top_sort',top_sort)
            
        # (2) adjusting in_degree_count to simulated simplifying the graph due to (1)
        for node in graph:
            if pushed_node in dependencies_fn(node):

                if DEBUG_LEVEL > 1: print('[amend in_degree_count] node',node,':','found',pushed_node,'in',dependencies_fn(node))

                # augment in_degree_count to simulate removal of this arrow / dependency
                in_degree_count[node] -= 1
                
                # (3) add newly non-dependent nodes that subsequently appear due to (1)
                if in_degree_count[node] == 0:
                    q.append(node) # (3)
                    if DEBUG_LEVEL > 1: print('q',q,'added',node)
    # at this point len(q) = 0, i.e. algo found no more non-dependent nodes

    # return result
    if q_handled_index != len(graph):
        # if there are nodes still NOT been handled by Kahn, they must contain cycle(s)
        print('cycle detected')
    else:
        # otherwise algo traversed all nodes, we're good, i.e. no cycle
        return top_sort

########################################################
# example given
########################################################
graph = {
        'A': [],
        'B': ['A','D'],
        'C': [],
        'D': ['C','E'],
        'E': [],
        'F': ['B','G'],
        'G': ['I'],
        'H': [],
        'I': ['H'],
    }

assert top_sort(
    graph,
    lambda key: graph[key]
    )==list('ACEHDIBGF')

'''
# validate
graph = {
        1: [],
        'B': [1,(True,False)],
        int: [],
        (True,False): [int,2.1],
        2.1: [],
        float: ['B',(1,2)],
        (1,2): ['I'],
        'H': [],
        'I': ['H'],
    }
top_sort(graph,lambda key: graph[key])
'''
