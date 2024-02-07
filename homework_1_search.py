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
    """
    Search the shallowest nodes in the search tree first.
    Your search algorithm needs to return (i) a list of cities the algorithm
    will propose to go to to reach the
    goal, and (ii) set of expanded cities (visited nodes). Make sure to
    implement a graph search algorithm.
    """
    "*** YOUR CODE HERE ***"
    # You can delete the line below once you have implemented your solution
    # above
    return {"Returned solution: [], Expanded cities: []"}
 
 
 
 
  def depthFirstSearch(self, start, goal, graph):
    stack = [start]      #setting out our data structure. Remember to use only Stack.pop() and stack.append()
    stackVisited = []    #this will just hold everything we went through

    while start != goal:
      if start not in stackVisited:
        stackVisited.append(start)
        
        children = graph.get(start, [])                #grab the children of the starting point...
        children.reverse()                             #we have to reverse it so that it is in proper order
        if children != []:                             #only pop if we have things to pop
            firstChild = children.pop()                #grab the first item in the list DFS style
            while firstChild in stackVisited:          #if child is in visited stack, we continue till we find a new start position
              firstChild = children.pop()
        stack.append(firstChild)                       #add child to current route
        start = firstChild


      




      """
      Search the deepest nodes in the search tree first.
      Your search algorithm needs to return (i) a list of cities the algorithm
      will propose to go to to reach the
      goal, and (ii) set of expanded cities (visited nodes). Make sure to
      implement a graph search algorithm.
      Please be very careful when you expand the neighbor nodes in your code when
      using stack. In case of using
      normal list or a data structure other than the Stack, you might need to
      reverse the order of the neighbor nodes
      before you push them in the stack to get correct results
      """
      "*** YOUR CODE HERE ***"
    # You can delete the line below once you have implemented your solution
    #above
    return "Returned solution: ", stack , "Expanded cities: " , stackVisited
  def uniformCostSearch(self, start, goal, graph, weights):
    """Search the node of least total cost first.
    Important things to remember
    1 - Use PriorityQueue with .put() and .get() functions
    2 - In addition to putting the start or current node in the queue, also put
    the cost (g(n)) using weights data structure
    3 - When you're expanding the neighbor of the current you're standing at,
    get its g(neighbor) by weights[(node, neighbor)]
    4 - Calling weights[(node, neighbor)] may throw KeyError exception which is
    due to the fact that the weights data structure
    only has one directional weights. In the class, we mentioned that there
    is a path from Arad to Sibiu and back. If the
    exception occurs, you will need to get the weight of the nodes in
    reverse direction (weights[(neighbor, node)])
    """
    "*** YOUR CODE HERE ***"
    # You can delete the line below once you have implemented your solution
    #above
    return {"Returned solution: [], Expanded cities: []"}
  def AStar(self, start, goal, graph, weights, heuristic):
    """Search the node that has the lowest combined cost and heuristic first.
    Important things to remember
    1 - Use PriorityQueue with .put() and .get() functions
    2 - In addition to putting the start or current node in the queue, and the
    g(n), also put the combined cost (i.e., g(n) + h(n))
    using weights and heuristic data structure
    3 - When you're expanding the neighbor of the current you're standing at,
    get its g(neighbor) by weights[(node, neighbor)]
    4 - Calling weights[(node, neighbor)] may throw KeyError exception which is
    due to the fact that the weights data structure
    only has one directional weights. In the class, we mentioned that there
    is a path from Arad to Sibiu and back. If the
    exception occurs, you will need to get the weight of the nodes in
    reverse direction (weights[(neighbor, node)])
    """
    "*** YOUR CODE HERE ***"
    # You can delete the line below once you have implemented your solution
    #above
    return {"Returned solution: [], Expanded cities: []"}

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
