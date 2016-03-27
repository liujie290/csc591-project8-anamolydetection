import sys

if len(sys.argv) != 2:
    print "missing input var, correct usage:"
    print "python anomaly.py <dataset directory>"
    exit(1)
dataset_dir = sys.argv[1]


def read_file(filename) :
    f = open(filename, "r")
    for line in f:
        yield line
        
def doc2L(doc):
    """
    Initially, a document d is transformed to a set of weighted features L = {(ti, wi)} where feature ti
    is a token of d and wi is its frequency in d. Tokens are also obtained as in shingling and appear only 
    once in set L. This weighted set can be viewed as a multidimensional vector. 
    """
    # FILL IN CODE HERE
        
def simhash(L1, L2):
    """
    simhash from equation (6): simhash(L1,L2) = 1 - hamming(h,h')/b
    """
    # FILL IN CODE HERE
    
    



def main():
    print "Data directory is set to", dataset_dir

if __name__ == "__main__":
    main()
