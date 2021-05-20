import pickle as pickle

from Pool import Pool
from Member import Member

def appendPoolToFile(pool, file):
    with open(file, 'ab') as f:
        pickle.dump(pool, f)

def readPoolsFromFile(file):

    allPools = []
    with open(file, 'rb') as f:
        while True:
            try:
                pool = pickle.load(f)
                allPools.append(pool)
            except EOFError:
                break

    return allPools

def getPoolCount(file):
    return len(readPoolsFromFile(file))
