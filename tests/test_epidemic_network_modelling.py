#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_epidemic_network_modelling
----------------------------------

Tests for `epidemic_network_modelling` module.
"""


import sys
import unittest
import matplotlib.pyplot as plt

from epidemic_network_modelling import epidemic_network_modelling as em



class TestEpidemic_network_modelling(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sri_mc(self):
    	deg_seq = [3,6,4,12,7,4,9,13,15,16,2,2,5,4,2,6,7,8,6,4,2,5,8,5,9,10,3,2,3,3,3]
    	graph = em.initial_graph_generator(deg_seq)
    	transmission_prob = 0.5
    	recovery_prob = 0.2
    	occupation_prob = .8
    	num_its = 50
    	n_vals = [i for i in range(num_its+1)]
    	ages = [2,6,4,23,7,4,9,13,15,16,2,2,5,4,2,6,7,8,6,4,2,5,8,5,9,10,3,2,3,3,3]
    	num_susceptible, num_infected, num_recovered = em.sri_mc(graph,ages,transmission_prob,recovery_prob,occupation_prob, num_its = num_its)
    	plt.plot(n_vals, num_susceptible,'b', label = 'susceptible')
    	plt.plot(n_vals, num_infected,'r', label = 'infected')
    	plt.plot(n_vals, num_recovered, 'g', label = 'recovered')
    	plt.legend()
    	plt.show()
    	self.assertEqual(len(graph),num_susceptible[5] + num_infected[5] + num_recovered[5])





        
tests = unittest.TestLoader().loadTestsFromTestCase(TestEpidemic_network_modelling)
unittest.TextTestRunner().run(tests)
        


if __name__ == '__main__':
    sys.exit(unittest.main())