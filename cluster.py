#!/usr/bin/python3.4

from copy import deepcopy

def minAndIndex(l):

    """Finds the minimum of a list and returns the index where the minimum was 
       found

    Args:
        l (List(numeric)):	A list of numbers

    Returns:
        tuple (numeric,Int)	A tuple of minimum value and its index
    """

    return min( (l[i],i) for i in range(len(l)) )

def findMinimumDist(dm):

    """Finds the minimum distance of a distance matrix

    Args:
        dm (List(List(numeric)))	A list of lists representation of 
                                        distance matrix

    Returns:
        tuple (Int, Int, Int)		A tuple of (minimum value, col, (row-1)).
    """ 

    ((value, col), row_1) = minAndIndex(list(map(lambda x: minAndIndex(x), dm)))
    return (value, col, row_1+1)

def removeItem(distanceMatrix, item):

    """Removes an item from a distance matrix

    Args:
        distanceMatrix (List(List(numeric))	Distance matrix of a group of 
                                                items
        item (Int)				Index of the item to be 
                                                removed (0..)

    Returns:
        (List(List(numeric)))	A new distance matrix
    """

    N = len(distanceMatrix)
    returnValue = distanceMatrix[:(item-1)]
    for i in range(item,N):
        returnValue.append(distanceMatrix[i][:item]+distanceMatrix[i][(item+1):])
    return returnValue

def getIndices(item1, item2):

    """Get indices of distance values in distance matrix

    Args:
       item1, item2:	The two items of interest

    Returns:
        Indices for the distance matrix
    """

    if item2>item1:
        return (item2-1, item1)
    else:
        return (item1-1, item2)

def mergeLabels(labelList, item1, item2):

    """Merge item labels

    Args:
        labellist (List(String)):	List of labels of items
        item1 (Int):			The first item
        item2 (Int):                    The second item

    Returns:
        A new list with labels for item1 and item2 merged
    """

    returnValue = labelList[:item1]
    returnValue.append(labelList[item1]+"/"+labelList[item2])
    returnValue += labelList[(item1+1):item2]
    returnValue += labelList[(item2+1):]
    return returnValue

def mergeItems(distanceMatrix, labelList, item1, item2):

    """Merge two items in distance matrix

    Args:
        distanceMatrix (List(List)):	Distance matrix
        labellist (List(String)):	List of labels of items
        item1 (Int):			The first item
        item2 (Int):                    The second item

    Returns:
        A tuple with new distance matrix and list of labels

    """
    # Create a copy, so not to damage existing
    dm = deepcopy(distanceMatrix)
    N = len(labelList)
    ll = mergeLabels(labelList, item1, item2)
    for i in range(0, N):
        if ((i != item1) and (i != item2)):
            (r1, c1) = getIndices(item1,i)
            (r2, c2) = getIndices(item2,i)
            dm[r1][c1] = min(dm[r1][c1], dm[r2][c2])
    return (removeItem(dm, item2),ll)

def performClustering(distanceMatrix, labelList, noOfClusters):

    """Perform hierarchical clustering of a set of items

    Args:
       distanceMatrix (List(List)):	Distance matrix of items
       labelList (List(String):		Labels for identifying the items
       noOfClusters (Int):		Desired number of clusters

    Returns:
       A list of cluster labels

    """

    c = labelList[:]
    d = deepcopy(distanceMatrix)
    while len(c) > noOfClusters:
        (value, city1, city2) = findMinimumDist(d)
        print(value)
        (d, c) = mergeItems(d, c, city1, city2)
    return c


# Validation -----------------------------------------------------------------
"""
American cities example (from http://www.analytictech.com/networks/hiclus.htm, 
S. Borgatti: Connections 17(2):78-80)
Note that there are some typos in the tables on that page, so don't trust them 
indiscriminantly.
"""
print("""A wise man (Tom Lehrer) once sang:

        If you visit American city,
	You'll find it very pretty.
	There are just two things you must beware:
	Don't drink the water. And don't breathe the air.
""")

c1 = ['BOS', 'NY', 'DC', 'MIA', 'CHI', 'SEA', 'SF', 'LA', 'DEN']

d1 = [[206], 
 [429, 233], 
 [1504, 1308, 1075],
 [963, 802, 671, 1329], 
 [2976, 2815, 2684, 3273, 2013],
 [3095, 2934, 2799, 3053, 2142, 808], 
 [2979, 2786, 2631, 2687, 2054, 1131, 379], 
 [1949, 1771, 1616, 2037, 996, 1307, 1235, 1059]]

assert (performClustering(d1, c1, 2) ==
['BOS/NY/DC/CHI/DEN/SEA/SF/LA','MIA']), \
"American cities example failed. Did you breathe the air?"

"""
Italian cities example (from https://home.deib.polimi.it/matteucc/Clustering/tutorial_html/hierarchical.html) by Matteo Matteucci
"""

print("""
	"What did you learn in school today
	Dear little boy of mine?"
	"I learned how to cook the 'Zuppa minestrone'
	And I learned that an Italian man can make love all a-lon-e."
	
							Eddie Skoller	
""")

c2 = ['BA', 'FI', 'MI', 'NA', 'RM', 'TO']

d2 = [[662],
  [877, 295],
  [255, 468, 754],
  [412, 268, 564, 219],
  [996, 400, 138, 869, 669]]

assert (performClustering(d2, c2, 2) == ['BA/NA/RM/FI', 'MI/TO']), \
"Italian cities example failed."
