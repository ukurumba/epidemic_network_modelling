#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_epidemic_network_modelling
----------------------------------

Tests for `epidemic_network_modelling` module.
"""

import epidemic_network_modelling.epidemic_network_modelling as em 
from epidemic_network_modelling import fib
import numpy as np

def func(x):
	return x + 1

def test_answer():
	assert func(3) == 4

def test_2():
	assert fib.fib(3) != 5


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

# def test_network_mc(self):
#     deg_seq = [1,2,3]
#     graph = em.initial_graph_generator(deg_seq)
#     ages = [42,23,37]
#     transmission_prob = .3
#     recovery_prob = .3
#     occupation_prob = .8
#     num_its = 5

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