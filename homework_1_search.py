from queue import PriorityQueue
from pprint import pprint
# Graph of cities with connections to each city. Similar to our class exercises,
# you can draw it on a piece of paper
# with step-by-step node inspection for better understanding


graph = {
'San Bernardino': ['Riverside', 'Rancho Cucamonga'],
'Riverside': ['San Bernardino', 'Ontario', 'Pomona'],
'Rancho Cucamonga': ['San Bernardino', 'Azusa', 'Los Angeles'],
'Ontario': ['Riverside', 'Whittier', 'Los Angeles'],
'Pomona': ['Riverside', 'Whittier', 'Azusa', 'Los Angeles'],
'Whittier': ['Ontario','Pomona', 'Los Angeles'],
'Azusa': ['Rancho Cucamonga', 'Pomona', 'Arcadia'],
'Arcadia': ['Azusa', 'Los Angeles'],
'Los Angeles': ['Rancho Cucamonga', 'Ontario', 'Pomona', 'Whittier', 'Arcadia']
}

# Weights are treated as g(n) function as we studied in our class lecture which
# represents the backward cost.
# In the data structure below, the key represents the cost from a source to target
# node. For example, the first
# entry shows that there is a cost of 2 for going from San Bernardino to Riverside.

weights = {
('San Bernardino', 'Riverside'): 2,
('San Bernardino', 'Rancho Cucamonga'): 1,
('Riverside', 'Ontario'): 1,
('Riverside', 'Pomona'): 3,
('Rancho Cucamonga', 'Los Angeles'): 5,
('Pomona', 'Los Angeles'): 2,
('Ontario', 'Whittier'): 2,
('Ontario', 'Los Angeles'): 3,
('Rancho Cucamonga', 'Azusa'): 3,
('Pomona', 'Azusa'): 2,
('Pomona', 'Whittier'): 2,
('Azusa', 'Arcadia'): 1,
('Whittier', 'Los Angeles'): 2,
('Arcadia', 'Los Angeles'): 2
}

# heurist is the h(n) function as we studied in our class lecture which represents
# the forward cost.
# In the data structure below, each entry represents the h(n) value. For example,
# the second entry
# shows that h(Riverside) is 2 (i.e., h value as forward cost for eaching at
# Riverside assuming that
# your current/start city is San Bernardino)

heuristic = {
'San Bernardino': 4,
'Riverside': 2,
'Rancho Cucamonga': 1,
'Ontario': 1,
'Pomona': 3,
'Whittier': 4,
'Azusa': 3,
'Arcadia': 2,
'Los Angeles': 0
}

# Data structure to implement search algorithms. Each function below currently has
# one line of code
# returning empty solution with empty expanded cities. You can remove the current
# return statement and
# implement your code to complete the functions.
class SearchAlgorithms:
  def breadthFirstSearch(self, start, goal, graph):
    Queue = [(start, [start])]  # The queue holds tuples of (node, path)
    Visited = [start]  # This will hold the overall exploration of the algorithm
    
    
    while Queue:  # While there are nodes to explore and we haven't found the goal...
        (next, path) = Queue.pop(0)  # Dequeue the next node and its path; dequeue here is done with .pop(0)
        # Note, tuple will allow us to keep track of the path that was taken for the current "next"
        children = graph.get(next, [])   # Grab the children of the current node
        for child in children:  # For each child...
           if child not in Visited:  # If they aren't marked visited...
            Visited.append(child)  # Mark child as visited
            Queue.append((child, path + [child]))  # Add them to the queue with the current path
            if child == goal:  # If we've reached the goal...
              path = path + [child]    #current path has not been updated through loop, and wont be, therefore must be done in condition of goal check
              return "Returned solution: ", path, "Expanded cities: ", Visited  # this will allow us to break out the loop ASAP and return answers

    return "Nothing found" #back up in case nothing is found
 
 
 
 
  def depthFirstSearch(self, start, goal, graph):
    stack = [start]      #setting out our data structure. Remember to use only Stack.pop() and stack.append()
    stackVisited = []    #this will just hold everything we went through

    while start != goal:
      if start not in stackVisited:
        stackVisited.append(start)
        
        children = list(graph.get(start, []))                #grab the children of the starting point...
        children.reverse()                             #we have to reverse it so that it is in proper order
        if children != []:                             #only pop if we have things to pop
            firstChild = children.pop()                #grab the first item in the list DFS style
            while firstChild in stackVisited:          #if child is in visited stack, we continue till we find a new start position
              firstChild = children.pop()
        stack.append(firstChild)                       #add child to current route
        start = firstChild
    return "Returned solution: ", stack , "Expanded cities: " , stackVisited
  

  def uniformCostSearch(self, start, goal, graph, weights):
    pQueue = PriorityQueue()
    #NOTE: I AM GOING TO USE A THREE TUPLE FOR THIS IMPLEMENTATION
    #REASON: We can keep cost, and city name within [0] and [1] but this would not keep track of the path. Therefore we will use [2] to hold the path taken to reach the node stored.
    pQueue.put((0,start,[start])) #in our priority queue, we will have a tuple, the cost and the child, and route to child
    Visited = [start] #we start from start therefore it is automatically visited
    #NOTE: the weight is given in the data struct weights above. This means for ex: if we insert Riverside into the queue, you would do .put(2, Riverside) since we are coming from San Bernardino
    #FURTHERNOTE: THE COSTS ADD ONTO EACHOTHER...
    while pQueue:                   #while our queue is not empty
      currentTuple = pQueue.get()     #assign current to be the highest priority tuple (this ensures us that we always explore cheapest path)
      node = currentTuple[1]          #this will grab the city from tuple
      children = graph.get(node, [])  #grab the children of the current highest priority

      #Our goal will eventually be the node being viewed from priority queue. This is checked only when the node is popped out to ensure that all possible least cost paths were considered
      if node == goal:
              return "Returned Solution: ", currentTuple[2], "Expanded Cities: ", Visited  #Since we search through cheapest routes, once goal is found, it is our immediate answer as more expensive routes were filtered out.

      for child in children:           #For each child...
        if child not in Visited:       #If not marked visited...
            Visited.append(child)      #Mark the child as visited...
            pQueue.put((weights[(node, child)] + currentTuple[0], child, currentTuple[2] + [child]))    #And put the child, along with its weight + previous cost, and updated path, into our priority queue .

    return "Nothing Found" #backup if no route was found.
  

  def AStar(self, start, goal, graph, weights, heuristic):
    pQueue = PriorityQueue()
    pQueue.put((0, start, [start]))   #We will utilize the same 3-tuple structure utilized in UCS. cost, start, and path.
    Visited = [start]                 #we start from start therefore it is automatically visited

    while pQueue:                     #structure of UCS will be replicated, only difference will be the cost that is calculated.
       currentTuple = pQueue.get()
       node = currentTuple[1]
       children = graph.get(node, [])

       if node == goal:    #again, we note that if the current node (which was just dequeued from the priority queue) is our goal, then it is our lowest possible cost route to the goal
          return "Returned Solution: ", currentTuple[2], "Expanded Cities: ", Visited
       
       for child in children:
          if child not in Visited:
             Visited.append(child)
             pQueue.put((weights[(node, child)] + currentTuple[0] + heuristic[(child)], child, currentTuple[2] + [child]))    #difference here is that we are also adding on to the cost, the heuristic

    return "Nothing Found" #backup if no route was found.

# Call to create the object of the above class
search = SearchAlgorithms()
# Call to each algorithm to print the results
print("Breadth First Search Result") # ['San Bernardino', 'Rancho Cucamonga', 'Los Angeles']
pprint(search.breadthFirstSearch('San Bernardino', 'Los Angeles', graph))
print("Depth First Search Result") # ['San Bernardino', 'Riverside', 'Ontario', 'Whittier', 'Pomona', 'Azusa', 'Rancho Cucamonga', 'Los Angeles']
pprint(search.depthFirstSearch('San Bernardino', 'Los Angeles', graph))
print("Uniform Cost Search Result") # ['San Bernardino', 'Rancho Cucamonga', 'Los Angeles']
pprint(search.uniformCostSearch('San Bernardino', 'Los Angeles', graph, weights))
print("A* Search Result") # ['San Bernardino', 'Rancho Cucamonga', 'Los Angeles']
pprint(search.AStar('San Bernardino', 'Los Angeles', graph, weights, heuristic))
