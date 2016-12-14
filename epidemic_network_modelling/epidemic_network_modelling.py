import numpy as np
import scipy.stats as ss 
import networkx as nx

def initial_graph_generator(degree_sequence):
    '''This function uses networkx's implemented random graph generator to generate a pseudograph 
    from the given degree distribution. Pseudograph may contain self-edges and loops. As n gets large these can be ignored.

    Input: degree_sequency (list of integers).'''
    return nx.to_numpy_matrix(nx.configuration_model(degree_sequence))

def sri_mc (adjacency_matrix, age,transmission_probability,recovery_probability,occupation_probability, init_distrib = 0,num_its = 100):
    '''This function evolves the given network (represented by its adjacency matrix) over time. At each time step a
    certain subsection of the infected population randomly recovers/dies and a certain subsection of the susceptible 
    population is infected. 

    Example
    -------

    adj_mat = [[0,1,1],[1,0,1],[1,1,0]]
    init_distrib = [1,0,0]
    age = [12,34,72]
    transmission_p= .3
    recovery_p = .5
    occupation_p = .7
    num_susceptible, num_infected, num_recovered = sri_mc(adj_mat, age, transmission_p,recovery_p,occupation_p, init_distrib = init_distrib)
    print(num_susceptible[94], num_infected[94], num_recovered[94])
    >>>>  1  1  1

    Inputs
    ------

    adjacency_matrix : symmetric numpy array of integers (the adjacency matrix for the network) 
    ages : array of integers of same length as adjacency matrix (the ages of each person)
    transmission_probability : float from 0 to 1 (probability an infected person connected to a susceptible person infects her)
    recovery_probability : float from 0 to 1 (probability an infected person recovers/dies)
    occupation_probability : float from 0 to 1 (probability two connected people actually saw each other. Tunable parameter)
    init_distrib : [optional] array of integers of same length as adjacency matrix (the initial infection distribution)
        --- Each array address corresponds to the same person as the ages value and the adjacency_matrix row of same address
        --- Each array value should be a 0 if the person is not infected and a 1 if the person is infected
        --- If no initial distribution is passed in, the first person is assumed to be patient 0 and the analysis procedes
    num_its : [optional] integer > 0 (number of iterations to evolve the model over. Each iteration can be considered a day) 

    Outputs
    -------
    Note- First value in each array is the initial distribution. Thus the total number of values in each array
          is the specified number of iterations plus one (defaults to 101)
    num_susceptible : array of integers (the number of remaining susceptible people at each time step)
    num_infected : array of integers (the number of remaining infected people at each time step)
    num_recovered : array of integers (the number of recovered/dead people at each time step)'''

    if init_distrib == 0:
        num_people = len(adjacency_matrix)
        graph_attributes = np.transpose(np.vstack((np.vstack((np.ones(num_people),np.zeros(num_people))), np.zeros(num_people)))) 
    
        #first column is susceptible, second infected, third resistant. Each row is a person
        num_susceptible = [0 for i in range(num_its+1)] #first value in array is the initial distribution
        num_infected = [0 for i in range(num_its+1)]
        num_recovered = [0 for i in range(num_its+1)]
        graph_attributes[0,0] = 0
        graph_attributes[0,1] = 1 
        num_susceptible[0] = num_people - 1
        num_infected[0] = 1

    else:
        return ValueError('This option not implemented yet. Sorry!') #first column is susceptible, second infected, third resistant



    for n in range(num_its):
        infections = np.zeros((len(adjacency_matrix),1)) #number of infection events each person experiences

        for i in range(len(graph_attributes)):
            for j in range(len(graph_attributes)): #iterating over every edge in graph

                if i > j: #only counting the lower triangle of the symmetric matrix

                    if adjacency_matrix[i,j] != 0: #only connected people

                        if graph_attributes[i,0] == 1 and graph_attributes[j,1] == 1: 
                            infections[i] += 1
                            pass
                            #only counting events b/w an infected and susceptible person
                        elif graph_attributes[i,1] == 1 and graph_attributes[j,0] == 1:
                            infections[j] += 1
                            pass

        susceptible = graph_attributes[:,0].nonzero()[0]    

        infected = graph_attributes[:,1].nonzero()[0]
        for person in susceptible: #for every susceptible person
            num_possible_infections = int(infections[person])
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

        num_susceptible[n+1], num_infected[n+1], num_recovered[n+1] = np.sum(graph_attributes,axis=0)


    return num_susceptible, num_infected, num_recovered


def network_mc(degree_sequence, ages, choice_function, transmission_probability, recovery_probability,occupation_probability,graph_percent,num_its_network_mc = 10, num_its_sri_mc = 100):
    ''' This function iterates randomly over many possible networks in the graph, selecting the top networks using a 
    supplied choice function. Typically the choice function will involve evolving the given network over many different possible
    configurations using a swap function that maintains the input degree sequence. 

    Example
    -------
    

    Inputs
    ------
    degree sequence : array of integers (the degree sequence for every person in the network)
    ages : array of integers of same length as degree sequence (the ages of each person)
    choice function : function that takes inputs as follows: choice_fx(candidate_state,current_state,transmission_probability,recovery_probability,occupation_probability,num_its_sri_mc)
    transmission_probability : float from 0 to 1 (probability an infected person connected to a susceptible person infects her)
    recovery_probability : float from 0 to 1 (probability an infected person recovers/dies)
    occupation_probability : float from 0 to 1 (probability two connected people actually saw each other. Tunable parameter)
    init_distrib : [optional] array of integers of same length as adjacency matrix (the initial infection distribution)
        --- Each array address corresponds to the same person as the ages value and the adjacency_matrix row of same address
        --- Each array value should be a 0 if the person is not infected and a 1 if the person is infected
        --- If no initial distribution is passed in, the first person is assumed to be patient 0 and the analysis procedes


    Outputs
    -------
    likely_network : 2-D array of length n x n where n is the length of the input degree sequence (approximation of the most likely network)
    '''
    initial_graph = initial_graph_generator(degree_sequence)
    current_state = initial_graph
    print(current_state.shape)
    graphs = []
    counter = []


    for i in range(num_its_network_mc):
        #generating next graph
        candidate_state = swap_function(current_state)
        current_state = choice_function(candidate_state,current_state,ages, transmission_probability,recovery_probability,occupation_probability,num_its_sri_mc)

        #check if the graph is already in the list. if not, append it to the list
        identical_graph_found = False
        for graph in range(len(graphs)):

            if np.allclose(graphs[graph],current_state) == True: 
                counter[graph] += 1
                identical_graph_found = True

        if identical_graph_found == False:
            graphs.append(current_state)
            counter.append(1)

    #calculating number of graphs to return
    uniques = len(counter)
    returned = int(uniques * graph_percent)
    if returned == 0:
        returned = 1 

    #sorting by counter value and selecting the correct graphs
    #source for zipping: http://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
    graph_and_counter = zip(counter,graphs)
    likely_graphs = [graph for counter, graph in sorted(graph_and_counter,reverse = True, key = lambda count: count[0])]    
    return likely_graphs[:returned]

def min_epidemic_choice_fx(candidate_array,current_array,ages,transmission_probability,recovery_probability,occupation_probability,num_its_sri_mc,init_distrib=0):
    '''This is a built-in function that chooses the next graph for the Network MC using the Metropolis-Hastings algorithm for MCMC.
    Because the MCMC occurs via constrained swapping, q(i|j) = q(j|i) where q is the candidate-generating function and i and j
    are potential arrays. Thus, the transition probability is min(pi_j / pi_i, 1) where pi_j / pi_j is a function of choice. Here,
    we set pi_j / pi_i to equal num_susceptible_j / num_susceptible_i after all iterations.'''

    avg_num_susceptible_j = 0
    avg_num_susceptible_i = 0
    for i in range(100): #collecting average numbers of susceptible people after repeated evolution of network 
        num_susceptible_j,_,_ = sri_mc(candidate_array,ages,transmission_probability,recovery_probability,occupation_probability,num_its=num_its_sri_mc,init_distrib=init_distrib)
        num_susceptible_i,_,_ = sri_mc(current_array,ages,transmission_probability,recovery_probability,occupation_probability,num_its=num_its_sri_mc,init_distrib=init_distrib)
        avg_num_susceptible_j += num_susceptible_j[num_its_sri_mc]
        avg_num_susceptible_i += num_susceptible_i[num_its_sri_mc]
    alpha = min(float(avg_num_susceptible_j)/avg_num_susceptible_i,1)
    u = np.random.random_sample()
    if u <= alpha: 
        return candidate_array
    else:
        return current_array

def age(ages,transmission_probability,recovery_probability):
    '''This function returns the effects of age on probability of getting a disease. This is essentially a guess function 
    for the effects of age, but literature suggests those over 65 and children are more prone to disease.'''

    age_effects = []
    for i in range(len(ages)):
        if ages[i] > 64:
            age_effects.append(.05 * transmission_probability *recovery_probability)
        elif ages[i] <=64 and ages[i] > 13:
            age_effects.append(-.05 * transmission_probability * recovery_probability)
        elif ages[i] <=12 and ages[i] > 5: 
            age_effects.append(.05 * transmission_probability * recovery_probability)
        elif ages[i] <= 5:
            age_effects.append(.10 * transmission_probability * recovery_probability)

    return age_effects

def swap_function(graph):
    '''This function swaps two edges on a given graph.

    Input
    -----

    graph : numpy array (adjacency matrix of current graph)'''

    #making new object
    graph = np.array(graph.tolist())
    if np.count_nonzero(graph) == len(graph) * len(graph):
        raise ValueError('Fully connected network: impossible to utilize constrained swapping MC method')
    print(graph.shape)
    i_1 = np.random.randint(0,len(graph))
    j_1 = np.random.randint(0,len(graph))
    i_2 = np.random.randint(0,len(graph))
    j_2 = np.random.randint(0,len(graph))

    while graph[i_1,j_1] == 0 or graph[i_2,j_2] == 0 or graph[i_1,j_2] != 0 or graph[i_2,j_1] != 0:
        i_1 = np.random.randint(0,len(graph))
        j_1 = np.random.randint(0,len(graph))
        i_2 = np.random.randint(0,len(graph))
        j_2 = np.random.randint(0,len(graph))

    graph[i_1,j_1] = 0
    graph[i_2,j_2] = 0
    graph[i_1,j_2] = 1
    graph[i_2,j_1] = 1
    return graph













