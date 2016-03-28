#!/usr/bin/python 

import os
import sys
import re
import igraph
import random

if len(sys.argv) != 2:
    print "missing input var, correct usage:"
    print "python anomaly.py <dataset directory>"
    exit(1)
dataset_dir = sys.argv[1]
b_num = 512


def read_file(filename) :
    f = open(filename, "r")
    for line in f:
        yield line
        
def getdoc(number, filemapping):
    """
    Take a filemapping and a filenumber and output the edgelist.
    The filemapping is a dictionary that lets us grab the files in order.

    Example Input: getdoc(0, filemapping)
    Example Output: [(107, 13), (22, 3), (103, 3), ...]
    """
    filename = filemapping[number]
    edgelist = read_file(filename)
    edgelist = [re.findall(r'[0-9]+', line) for line in edgelist]
    edgelist = [(int(vertex1),int(vertex2)) for (vertex1, vertex2) in edgelist]
    return edgelist

def shingling(graph):
    """
    Take in a graph and produce a list of tuples using the walk algorithm.
    The first element of the tuple is the token (vertex ID) and the second
    element is the number of neighbors the vertex ID has, which in an 
    undirected graph, is the number of edges the vertex has. 
    """
    # We make a list of tuples (vertex ID, quality score, whether the vertex
    # has been visited) in decreasing order of quality.
    vertexQuality = [(vertexId, quality) for vertexId,quality in enumerate(graph.pagerank())]
    vertexQuality.sort(key=lambda(pair): (pair[1], random.random()) \
                        ,reverse=True)
    verticesSorted = [vertexId for (vertexId,quality) in vertexQuality]
    vertexQuality = dict(vertexQuality)
    vertexVisited = dict([(vertexId,False) for vertexId in verticesSorted])
    #print verticesSorted
    adjlist = graph.get_adjlist()
    #print adjlist
    output = []
    for vertex in verticesSorted:
        active = vertex
        takingWalk = True
        while takingWalk and not vertexVisited[active]:
            # Add vertex to list.
            neighbors = adjlist[active]
            output.append((active, len(neighbors)))
            vertexVisited[active] = True
            # Get unvisted neighbor of highest quality
            unvisitedNeighbors = [(node, vertexQuality[node])
                                  for node in neighbors
                                  if not vertexVisited[node]]
            if len(unvisitedNeighbors) > 0:
                unvisitedNeighbors.sort(key=lambda(pair): \
                                        (pair[1],random.random()) \
                                        ,reverse=True)
                active = unvisitedNeighbors[0][0]
            else: 
                takingWalk = False
    return output                
        
def doc2L(edgelist):
    """
    Initially, a document d is transformed to a set of weighted features 
    L = {(ti, wi)} where feature ti is a token of d and wi is its frequency in 
    d. Tokens are also obtained as in shingling and appear only once in set L. 
    This weighted set can be viewed as a multidimensional vector. 
    
    Output: list of tuples (ti, wi) for each i.
    """
    # Build up the graph from the edgelist.
    maxVertex = max([max(ofpair) for ofpair in edgelist])
    graph = igraph.Graph()
    graph.add_vertices(maxVertex+1)
    graph.add_edges(edgelist)
    # The edgelist uses vertex IDs and may not represent each vertex.
    # We therefore clean up the graph.
    emptyVertices = [vertexId   for (vertexId, adjacents)
                                in enumerate(graph.get_adjlist())
                                if 0 == len(adjacents)]
    graph.delete_vertices(emptyVertices)
    tokenWithWeights = shingling(graph)
    return tokenWithWeights

def hamming(vec1, vec2):
    """Performs the hamming distance on two equal length enumerable types.
    Input: any two enumerable objects (list, string, etc.)
    Output: hamming distance as an integer
    
    Following examples are for doctest:
    >>> hamming("hello", "world")
    4
    >>> hamming("karolin", "kathrin")
    3
    >>> hamming("karolin", "kerstin")
    3
    >>> hamming([0, 1, 1, 3, 4], [0, 1, 2, 3, 4])
    1
    >>> hamming([0, 1, 1, 3, 4], [0, 1, 2, 3])
    Traceback (most recent call last):
        ...
    Exception: vectors are not the same length
    """
    if len(vec1) != len(vec2):
        raise Exception("vectors are not the same length")

    return reduce(lambda x,y: x + y,
                  map(lambda (x,y): 0 if x==y else 1,
                      zip(vec1, vec2)), 0)

def simhash(L1, L2):
    """Performs the simhash function on two tuples defined as (ti, wi)
    where ti is a token of document d and wi is its frequency in d.
    simhash from equation (6): simhash(L1,L2) = 1 - hamming(h,h')/b

    Input: Two tuples (ti, wi)
    Output: simhash result

    >>> simhash(("token", 20), ("token2", 30))
    """
    (t1, w1) = L1
    (t2, w2) = L2
    doc1 = lookup(t1)
    doc2 = lookup(t2)

    for i in range(0, b_numl):
        h1 = doc1[random.randrange(-w1, w1, 1)]
        h2 = doc2[random.randrange(-w2, w2, 1)]
        result += 1 - hamming(h1, h2)/b_num
    return result


# takes a list of similarities between consecutive
# graphs and returns the outliers
def find_outliers(similarities):
#stub for now
    output=[]
    return output

def main():
    #print "Data directory is set to", dataset_dir
    random.seed(591)

    # Read all the files.
    absdir = os.path.abspath(dataset_dir)
    files = os.listdir(absdir)
    files = [os.path.join(absdir, filename) for filename in files]
    #print files

    # Create a dictionary that will map from file number to file.
    filenumbers = [int(re.findall(r'[0-9]+', rec)[0]) for rec in files]
    #print filenumbers
    filemapping = dict(zip(filenumbers, files))

    # Test doc2L
    testdoc = getdoc(0, filemapping)
    #print testdoc
    print doc2L(testdoc)

if __name__ == "__main__":
    import doctest
    #doctest.testmod()
    main()
