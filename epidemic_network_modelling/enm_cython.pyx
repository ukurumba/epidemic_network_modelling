from cython.parallel import prange
from math import exp 
# from libc.math cimport exp as c_exp
import numpy as np
cimport openmp 


cdef double cfib(int n):
    cdef int i
    cdef double a=0.0,b=1.0
    for i in range(n):
        a, b = a+b, a
    return a

def fib(x):
    return cfib(x)


def array_f(X):
    
    Y = np.zeros(X.shape)
    index = X > 0.5
    Y[index] = np.exp(X[index])

    return Y

def c_array_f(X):

    cdef int N = X.shape[0]
    cdef double[:] Y = np.zeros(N)
    cdef int i

    for i in range(N):
        if X[i] > 0.5:
            Y[i] = X[i] * 2 
        else:
            Y[i] = 0

    return Y

cdef c_array_f_multi(long[:] X):

    cdef int N = X.shape[0]
    cdef double[:] Y = np.zeros(N)
    cdef int i

    cdef int num_threads 
    cdef int thread_num = openmp.omp_get_num_threads()





    for i in prange(N, nogil=True):
        if X[i] > 0.5:
            Y[i] = X[i] * 2 
        else:
            Y[i] = 0

    return Y


def array_f_multi_wrapper(Y):
    X = Y

    return c_array_f_multi(X)

def cython_wrapper_sri_mc(adjacency_matrix, age,transmission_probability,recovery_probability,occupation_probability,init_distrib = 0, num_its = 0):
    if init_distrib == 0:
        num_people = len(adjacency_matrix)
        graph_attributes = np.transpose(np.vstack((np.vstack((np.ones(num_people),np.zeros(num_people))), np.zeros(num_people)))) 
    
        #first column is susceptible, second infected, third resistant. Each row is a person
        num_susceptible = [0 for i in range(num_its+1)] #creating our return array. First value in array is the initial distribution
        num_infected = [0 for i in range(num_its+1)]
        num_recovered = [0 for i in range(num_its+1)]
        graph_attributes[0,0] = 0
        graph_attributes[0,1] = 1 
        num_susceptible[0] = num_people - 1
        num_infected[0] = 1

    else:
        raise ValueError('This option not implemented yet sorry!') #first column is susceptible, second infected, third resistant

    graph_attributes = np.array(graph_attributes,order='C')
    return c_sri_mc(adjacency_matrix, graph_attributes,age,transmission_probability,recovery_probability,occupation_probability,num_its)
    # return susceptible, infected, recovered

cdef int c_sri_mc(double[:, ::1] adj_mat, double[:,::1] graph_attributes, long[:, ::1] age, double transmission_probability, double recovery_probability, double occupation_probability, int num_its):
    

    cdef double[:,::1] num_susceptible = np.zeros((num_its+1,1))
    cdef double[:,::1] num_infected = np.zeros((num_its + 1,1))
    cdef double[:,::1] num_recovered = np.zeros((num_its+1,1))
    cdef int n, i, j
    cdef long num_possible_infections
    cdef long[:,::1] infections = np.zeros((len(adj_mat),1),dtype=np.int_)
    cdef double infection_probability, recovery_threshold, random_event

    for n in range(num_its):
        infections = np.zeros((len(adj_mat),1)) #number of infection events each person experiences
        for i in range(len(graph_attributes)):
            for j in range(len(graph_attributes)): #iterating over every edge in graph

                if i > j: #only counting the lower triangle of the symmetric matrix

                    if adj_mat[i,j] != 0: #only connected people

                        if graph_attributes[i,0] == 1 and graph_attributes[j,1] == 1: 
                            infections[i,0] += 1
                            #only counting events b/w an infected and susceptible person
                        elif graph_attributes[i,1] == 1 and graph_attributes[j,0] == 1:
                            infections[j,0] += 1

        susceptible = graph_attributes[:,0].nonzero()[0]    

        infected = graph_attributes[:,1].nonzero()[0]
        for person in susceptible: #for every susceptible person 
            num_possible_infections = infections[person,0]
            if num_possible_infections > 0: #if they had at least one opportunity to be infected
                infection_probability = transmission_probability * occupation_probability #their overall infection probability
                for i in range(num_possible_infections): 
                    random_event = np.random.random_sample() 
                    if infection_probability > random_event: #anything below infection probability considered an infection 
                        graph_attributes[person,0] = 0 
                        graph_attributes[person,1] = 1
                        break 


        for person in infected: #for every infected person
            recovery_threshold = np.random.random_sample()
            if recovery_probability > recovery_threshold: #anything below recovery probability considered a recovery 
                graph_attributes[person,1] = 0
                graph_attributes[person,2] = 1

        num_susceptible[n+1,0], num_infected[n+1,0], num_recovered[n+1,0] = np.sum(graph_attributes,axis=0)


    return num_susceptible[:,0], num_infected[:,0], num_recovered[:,0]
    







