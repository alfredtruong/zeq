# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 13:45:44 2022

@author: ahkar

########################################################################
hand-written example :
########################################################################
'''
# assign leaf group 0
'A': [],            # 0
'B': ['A','D'],     # 
'C': [],            # 0
'D': ['C','E'],     # 
'E': [],            # 0
'F': ['B','G'],     # 
'G': ['I'],         # 
'H': [],            # 0
'I': ['H'],         # 

# gather group 0
peel = ['A','C','E','H']

# for remaining, identify next level that only contains stuff from peel
'A': [],            # 0
'B': ['A','D'],     # 
'C': [],            # 0
'D': ['C','E'],     # 1
'E': [],            # 0
'F': ['B','G'],     # 
'G': ['I'],         # 
'H': [],            # 0
'I': ['H'],         # 1

# add group 1 to peel
peel = ['A','C','E','H','D','I']

# for remaining, identify next level that only contains stuff from peel
'A': [],            # 0
'B': ['A','D'],     # 2
'C': [],            # 0
'D': ['C','E'],     # 1
'E': [],            # 0
'F': ['B','G'],     # 
'G': ['I'],         # 2
'H': [],            # 0
'I': ['H'],         # 1

# add group 2 to peel
peel = ['A','C','E','H','D','I','B','G']

# for remaining, identify next level that only contains stuff from peel
'A': [],            # 0
'B': ['A','D'],     # 2
'C': [],            # 0
'D': ['C','E'],     # 1
'E': [],            # 0
'F': ['B','G'],     # 3
'G': ['I'],         # 2
'H': [],            # 0
'I': ['H'],         # 1

# add group 3 to peel
peel = ['A','C','E','H','D','I','B','G','F']
'''
"""

########################################################
# complexity
########################################################
print('='*30)
print('memory complexity = O(N)')
print('='*30)
print('\t\t remaining_layers, peeled_layers and outer_skin at all at most the number of nodes')
print()

print('='*30)
print('runtime complexity = O(N^2)')
print('='*30)
print('\t\t I think the comparison in the for-loop runs at most N * (N+1) / 2 times')
print()

########################################################
# imports
########################################################
from typing import Dict,Callable

########################################################
# graph data
########################################################
# given example
graph = {
        'A': [],            # 3
        'B': ['A','D'],     # 1
        'C': [],            # 4
        'D': ['C','E'],     # 3
        'E': [],            # 4
        'F': ['B','G'],     # 0
        'G': ['I'],         # 1
        'H': [],            # 4
        'I': ['H'],         # 3
    }

'''
# example with a cycle
graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A'],
    }
'''

########################################################
# debugging
########################################################
DEBUG_LEVEL = 0 # no logging
#DEBUG_LEVEL = 1 # log container contents

########################################################
# top_sort
########################################################
def top_sort(graph : Dict, dependency_fn : Callable):
    '''
    idea : 
        liken a DAG to an onion
        the core of the onion -> terminal node
        the layer surrounding the core -> dependencies of the terminal node
        ...
        the outer skin of the onion -> nodes of the DAG with no dependencies
        
    logic:
        identify all nodes in the outer layer simultaneously
        `peel the onion` to reveal a new onion
        contents of the next layer CAN ONLY depend on nodes that have already been peeled
        `peel the onion` to reveal a new onion
        repeat until there is nothing left
    
    note:
        after implementing Kahn's algorithm I thought I'd try my own version
        turns out my onion idea is just Kahn in disguise
    '''
    remaining_layers = list(graph.keys()) # layers of unpeeled onion
    peeled_layers = [] # peeled layers of onion
    
    if DEBUG_LEVEL > 0: print('init phase')
    if DEBUG_LEVEL > 0: print('remaining',remaining_layers)
    if DEBUG_LEVEL > 0: print('peeled',peeled_layers)
    if DEBUG_LEVEL > 0: print()
    
    ##################################################################
    # initialize `peeled_layers` container with the outer skin / i.e. leaves
    ##################################################################
    
    # temp container for nodes that are on the skin
    outer_skin = [] 
    
    # populate outer_skin / what nodes that have NO dependencies
    for k in remaining_layers:
        if len(dependency_fn(k)) == 0:
            outer_skin.append(k)

    # check cycle at init
    if len(outer_skin) == 0:
        print('cycle detected') # remaining nodes depend on each other cyclicly
        return

    # update containers
    for k in outer_skin:
        remaining_layers.remove(k) # don't need to consider these nodes again
        peeled_layers.append(k) # remember what layers have been peeled
        
    # recursively peel until there's nothing left
    while remaining_layers: # while onion still exists

        if DEBUG_LEVEL > 0: print('while-loop')
        if DEBUG_LEVEL > 0: print('remaining',remaining_layers)
        if DEBUG_LEVEL > 0: print('peeled',peeled_layers)
        if DEBUG_LEVEL > 0: print()
        
        # temp container for nodes that are on the skin
        outer_skin = [] 
        
        # identify next layer, this new skin must `touch` only peeled layers (depend on only things in peeled_layers)
        found_something_to_peel = False
        for k in remaining_layers:
            if set(dependency_fn(k)).issubset(set(peeled_layers)):
                outer_skin.append(k)
                found_something_to_peel = True
        
        # check if cycle found, 
        # if remaining nodes depend on things other than the peeled stuff
        # it must mean they depend on themselves, i.e. a cycle
        if not found_something_to_peel:
            print('cycle found')
            break
            
        # update containers
        for k in outer_skin:
            remaining_layers.remove(k) # don't need to consider these nodes again
            peeled_layers.append(k) # update peeled_layers with contents of newly found outer_skin
                
    if DEBUG_LEVEL > 0: print('final result')
    if DEBUG_LEVEL > 0: print('remaining',remaining_layers)
    if DEBUG_LEVEL > 0: print('peeled',peeled_layers)
    if DEBUG_LEVEL > 0: print()
    
    # return result
    if len(peeled_layers) == len(graph):
        # onion was completely peeled away, i.e. no cycle
        return peeled_layers
    else:
        # remaining nodes depend on each other cyclicly
        print('cycle detected')

# return output
ordered = top_sort(graph,lambda key:graph[key])
print(ordered)

