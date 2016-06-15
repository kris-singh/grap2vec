__author__ =  'kris singh'
__date__ = '10/06/2016'
__filename__ = 'perm_matrix.py'
__descripition__ = 'generate all permutation matricies of any given size'
__email__ = 'cs15mtech11007@iith.ac.in'
#refrences : http://math.stackexchange.com/questions/7840/finding-all-n%C3%97n-permutation-matrices
import numpy as np
import perms as p
import sys
def seralize_matrix(matrix):
    serialized_matrix = []
    new_matrix = []
    for i in range(0,len(matrix)) :
        serialized_matrix.append(matrix[i][:])
    print serialized_matrix
    for i in serialized_matrix:
        i = i.tolist()
        print i
        i = map(int,i)
        i = map(str,i)
        string = ''.join(i)
        new_matrix.append(string)
    return ''.join(new_matrix)
def generate_all_isomorphic(graph):
    """
    source for explanation math.stackexchange.com/questions/331233/showing-two-graphs-isomorphic-using-their-adjacency-matrices
    """
    perm_matrix_list = perm_matrix(len(graph))
    result = []
    for i in perm_matrix_list:
        result.append(np.dot(np.dot(i,graph),np.transpose(i)))
    return result
def perm_matrix(size):
    """
    __params__:
    size : size of the matrix you want to create
    """
    org_matrix = np.identity(size)
    string = [str(i) for i in range(0,size)]
    all_strings =  p.perms("".join(string))
    all_matrix = []
    for k,v in enumerate(all_strings):
        matrix = np.zeros((size,size))
        #perm matrix is square in cases of graphs adj matrix
        #do this with list comprehension
        for key,i in enumerate(v):
            matrix[key][int(i)] = 1
        all_matrix.append(matrix)
    #print all_matrix[2]
    return all_matrix
def hashmap(graph,dictionary):
    if seralize_matrix(graph) in dictionary:
        pass
    else:
        keys = generate_all_isomorphic(graph)
        num = np.random.randint(low = 0,high = sys.maxint)
        for k,v in enumerate(keys):
            dictionary[seralize_matrix(v)] = num
        return dictionary

if __name__ == '__main__':
    matrix = np.array([[0,1],[1,0]])
    dict1 = dict()
    print hashmap(matrix,dict1)
