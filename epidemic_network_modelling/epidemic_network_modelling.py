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
		graph_attributes = init_distrib #first column is susceptible, second infected, third resistant



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

	print(graph_attributes)

	return num_susceptible, num_infected, num_recovered








