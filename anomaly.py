#!/usr/bin/python 

import os
import sys
import re

if len(sys.argv) != 2:
    print "missing input var, correct usage:"
    print "python anomaly.py <dataset directory>"
    exit(1)
dataset_dir = sys.argv[1]


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
        
def doc2L(doc):
    """
    Initially, a document d is transformed to a set of weighted features L = {(ti, wi)} where feature ti
    is a token of d and wi is its frequency in d. Tokens are also obtained as in shingling and appear only 
    once in set L. This weighted set can be viewed as a multidimensional vector. 
    
    Output: list of tuples (ti, wi) for each i.
    """
    # FILL IN CODE HERE
        
def simhash(L1, L2):
    """
    simhash from equation (6): simhash(L1,L2) = 1 - hamming(h,h')/b
    """
    # FILL IN CODE HERE
    
    



def main():
    print "Data directory is set to", dataset_dir
    
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
    #doc2L(testdoc)

if __name__ == "__main__":
    main()
