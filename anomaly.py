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


def main():
    print "Data directory is set to", dataset_dir

if __name__ == "__main__":
    main()
