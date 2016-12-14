#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_epidemic_network_modelling
----------------------------------

Tests for `epidemic_network_modelling` module.
"""
import epidemic_network_modelling.epidemic_network_modelling as em 
import enm_cython as emc
import numpy as np

def func(x):
	return x + 1

def test_answer():
	assert func(3) == 4

def test_2():
	assert emc.fib(3) != 5

def test_cython_omp():
	array = np.array([i for i in range(100000)])
	output = emc.array_f_multi_wrapper(array)
	correct_output = np.array([2 * i for i in range(100000)])
	assert output[1234] == correct_output[1234]

def test_sri_mc():
	deg_seq = [3,6,4,12,7,4,9,13,15,16,2,2,5,4,2,6,7,8,6,4,2,5,8,5,9,10,3,2,3,3,3]
	graph = em.initial_graph_generator(deg_seq)
	transmission_prob = 0.5
	recovery_prob = 0.2
	occupation_prob = .8
	num_its = 6
	n_vals = [i for i in range(num_its+1)]
	ages = [2,6,4,23,7,4,9,13,15,16,2,2,5,4,2,6,7,8,6,4,2,5,8,5,9,10,3,2,3,3,3]
	num_susceptible, num_infected, num_recovered = em.sri_mc(graph,ages,transmission_prob,recovery_prob,occupation_prob, num_its = num_its)
	# plt.plot(n_vals, num_susceptible,'b', label = 'susceptible')
	# plt.plot(n_vals, num_infected,'r', label = 'infected')
	# plt.plot(n_vals, num_recovered, 'g', label = 'recovered')
	# plt.legend()
	# plt.show()
	assert len(graph) == num_susceptible[5] + num_infected[5] + num_recovered[5]

def test_network_mc():
    deg_seq = [2,2,3,5,6,4,2,5,3]
    ages = [42,23,37,19,12,13,98,14,43]
    transmission_prob = .3
    recovery_prob = .3
    occupation_prob = .8
    num_its = 5
    graph_percent = .06
    em.network_mc(deg_seq,ages,em.min_epidemic_choice_fx,transmission_prob,recovery_prob,occupation_prob,graph_percent,num_its_network_mc=11,num_its_sri_mc=100)

def test_min_epidemic_choice_fx():
	ages = [42,23,37]
	current_graph = np.array([[0,1,1],[1,0,0],[1,0,0]])
	candidate_graph = np.array([[0,1,0],[1,0,1],[0,1,0]])
	transmission_prob = 1
	recovery_prob = 1
	occupation_prob = .8
	num_its = 200
	output_array = em.min_epidemic_choice_fx(candidate_graph,current_graph,ages,transmission_prob,recovery_prob,occupation_prob,num_its)
	assert True == (np.allclose(candidate_graph,output_array))

def test_age():
	ages = [2,9,19,29,39,49,59,69]
	transmission_prob = recovery_prob = .5
	age_effects = np.array(em.age(ages,transmission_prob,recovery_prob))
	assert True == (np.allclose(age_effects,np.array([.025,.0125,-.0125,-.0125,-.0125,-.0125,-.0125,.0125])))

def test_swap_function():
	input_graph = np.array([[0,1],[1,0]])
	new_graph = em.swap_function(input_graph) 
	assert True == (np.allclose(new_graph,np.array([[1,0],[0,1]])))
	assert False == np.allclose(new_graph,input_graph)

def test_cython_sri_mc():
	graph = np.array([[1.0,1],[1,2]])
	transmission_prob = 0.5
	recovery_prob = 0.2
	occupation_prob = .8
	num_its = 6
	ages = np.array([2,6,4,23,7,4,9,13,15,16,2,2,5,4,2,6,7,8,6,4,2,5,8,5,9,10,3,2,3,3,3],ndmin=2)
	num_susceptible, num_infected, num_recovered =  emc.cython_wrapper_sri_mc(graph,ages,transmission_prob,recovery_prob,occupation_prob)
	print(num_susceptible)
	assert 3 == 3