import networkx as nx
import os 
import numpy as np
import perm_matrix as pm
import perms as p
import sys
import math
import csv
from gensim.models import word2vec
from itertools import permutations
ret_start_val = -1


# In[8]:

#dir_name = os.listdir('../Data/all_graph10/')
#file_name = ["../Data/all_graph10/"+i  for i in dir_name]
#driver function for the program
'''for i in range(0,len(file_list)):
    present_neighbourhood = gen_neigbourhood(i)
    start_val = max(0,ret_start_val)
    total_neigh.append(present_neighbourhood)
    ret_hash_table,key_mid = populate_table(i,start_val,present_neighbourhood)
    #ret_start_val = max(list(ret_hash_table.values()))
    #full_hash_table.append(ret_hash_table)
    #create_partial_vocab(present_neighbourhood,ret_hash_table,key_mid,d,vocab)
''' 

# In[2]:

"""Create e-neigbourhood for any.. subgraph(e-neighbourhood is defined as 1 deletion(edge or node) as on dummy graph)"""
def e_neighbourhood_node_del(G):
    G_prime = G.copy()
    print type(G_prime)
    if len(G_prime.nodes()) > 0:
        G_prime.remove_node(np.random.choice(G_prime.nodes()))
    else:
        return None
    return G_prime
def e_neighbourhood_edge_del(G):
    G_prime = G.copy()
    print type(G_prime)
    edges = G.edges()
    #print np.random.choice(range(0,len(edges)-1))
    print len(edges)-1 
    if len(edges)-1 <= 0:
        return None
    else:
        G_prime.remove_edge(*edges[np.random.choice(range(0,len(edges)-1))])
    return G_prime
def e_neighbourhood_node_add(G):
    G_prime = G.copy()
    print type(G_prime)
    """choose some random nodes in the graph to which we have to add a edge"""
    label = len(G_prime)
    nodes_attach = np.random.randint(label)
    """node neigh computed before so no self loops"""
    node_neig = [np.random.choice(G_prime.nodes()) for _ in range(1,nodes_attach)]
    G_prime.add_node(label)
    a = [label for i in range(1,len(node_neig))]
    val = zip(a,node_neig)
    print val
    G_prime.add_edges_from(val)
    return G_prime
def e_neighbourhood_edge_add(G):
    G_prime = G.copy()
    print type(G_prime)
    """choose 2 random nodes and a edge"""
    n1 = np.random.choice(G_prime.nodes())
    n2 = np.random.choice(G_prime.nodes())
    if n1 is not n2:
        """graphs are simple so no self loop"""
        print "herer"
        G_prime.add_edge(n1,n2)
    return G_prime
        


# In[3]:

"""run some unit test"""
#neigbourhood = e_neighbourhood_node_del(file_list[2])#pass
#neigbourhood = e_neighbourhood_edge_del(file_list[2]) #pass
#neigbourhood = e_neighbourhood_edge_add(file_list[2])#pass
#neigbourhood = e_neighbourhood_node_add(file_list[2])#pass
#nx.draw_networkx(neigbourhood)
#add more boundary cases
"""Now randomly choose the choices we from 1 to 4 and apply the eps times"""
def gen_neigbourhood(k):
    eps = 3 #if eps is 3 we need 3 loops O(n^3)
    #num_eps = 10 #number of eps neigbour hoods you want
    neigbourhood = []
    for i in range(0,4):
        indermitate_graph = file_list[k]
        for j in range(0,4):
            for k in range(0,4):
                indermitate_graph = function_enumerate_all_neighb(indermitate_graph,i,j,k)
                if indermitate_graph is None:
                    indermitate_graph = file_list[k]
        neigbourhood.append(indermitate_graph)
    return neigbourhood


# In[4]:

def function_enumerate_all_neighb(graph,i,j,k):
    indermitate_graph = graph
    if i is 0:
        indermitate_graph = e_neighbourhood_edge_del(indermitate_graph)
        if indermitate_graph is None:
            return None
        else:
            indermitate_graph = indermitate_graph.copy()
    elif i is 1:
        indermitate_graph = e_neighbourhood_node_del(indermitate_graph)
        if indermitate_graph is None:
            return None
        else:
            indermitate_graph = indermitate_graph.copy()
    elif i is 2:
        indermitate_graph = e_neighbourhood_node_add(indermitate_graph).copy()
    elif i is 3:
        indermitate_graph = e_neighbourhood_edge_add(indermitate_graph).copy()
    elif j is 0:
        indermitate_graph = e_neighbourhood_edge_del(indermitate_graph)
        if indermitate_graph is None:
            return None
        else:
            indermitate_graph = indermitate_graph.copy()
    elif j is 1:
        indermitate_graph = e_neighbourhood_node_del(indermitate_graph)
        if indermitate_graph is None:
            return None
        else:
            indermitate_graph = indermitate_graph.copy()
    elif j is 2:
        indermitate_graph = e_neighbourhood_node_add(indermitate_graph).copy()
    elif j is 3:
        indermitate_graph = e_neighbourhood_edge_add(indermitate_graph).copy()
    elif k is 0:
        indermitate_graph = e_neighbourhood_edge_del(indermitate_graph)
        if indermitate_graph is None:
            return None
        else:
            indermitate_graph = indermitate_graph.copy()
    elif k is 1:
        indermitate_graph = e_neighbourhood_node_del(indermitate_graph)
        if indermitate_graph is None:
            return None
        else:
            indermitate_graph = indermitate_graph.copy()
    elif k is 2:
        indermitate_graph = e_neighbourhood_node_add(indermitate_graph).copy()
    elif k is 3:
        indermitate_graph = e_neighbourhood_edge_add(indermitate_graph).copy()

    return indermitate_graph



# In[5]:

dict1 = {}
def seralize_matrix(matrix):
    serialized_matrix = []
    new_matrix = []
    for i in range(0,len(matrix)) :
        serialized_matrix.append(matrix[i][:])
    #print serialized_matrix
    for i in serialized_matrix:
        i = i.tolist()
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
    all_strings = list(map("".join, permutations("".join(string))))
    #all_strings =  p.perms("".join(string))
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
def hashmap(graph,dictionary,counter):
    if seralize_matrix(graph) in dictionary:
        for key in dictionary.keys():
            if seralize_matrix(graph) == key:
                print "already exists"
                dictionary[key] = counter
    else:
        keys = generate_all_isomorphic(graph)
        keys_serilized = []
        for i in keys:
            keys_serilized.append(seralize_matrix(i))
        for i in keys_serilized:
            print i
            dictionary[i] = counter


# In[6]:

def populate_table(k,starting_val,neigbourhood):
    hash_table = {}
    """create a enrty for all neighbourhoods you found"""
    for i in neigbourhood:
        if len(hash_table.values()) is 0:
            counter = starting_val + 1
        else:
            counter = max(hash_table.values()) + 1
        hashmap(np.array(nx.to_numpy_matrix(i)),hash_table,counter)


# In[8]:

"""okay so my idea is to create a new hashtable for all these subgraphs and generate corpus and then destroy them"""
def create_partial_vocab(neigbourhood,hash_table,key_mid,d,vocab):
    """take 2*len(neigbourhood) such samples"""
    for i in range(1,2*len(neigbourhood)):
        choices = [np.random.choice(hash_table.values()) for i in range(1,d)]
        choices.insert(int(math.floor(d/2)),hash_table[key_mid])
        choices = map(str,choices)
        vocab.append(" ".join(choices))
    print vocab



if __name__ == "__main__":
    i = 3
    file_name = "/home/kris/Desktop/ML_DeppWalk/Data/all_graph10/graph4.g6"
    full_hash_table = []
    print file_name
    file_list = nx.read_graph6(file_name)
    d = 5 #context window size
    vocab = [] #vocab """we migh have to save it to the disk and start again if size too big"""
    ret_start_val = 0
    total_neigh = []
    present_neighbourhood = gen_neigbourhood(i)
    start_val = max(0,ret_start_val)
    total_neigh.append(present_neighbourhood)
    ret_hash_table,key_mid = populate_table(i,start_val,present_neighbourhood)



