from epidemic_network_modelling import age
cdef double cfib(int n):
	cdef int i
	cdef double a=0.0,b=1.0
	for i in range(n):
		a, b = a+b, a
	return a

def fib(x):
	return cfib(x)

def cythonage(array,trans_prob,recov_prob):
	return age(array,trans_prob,recov_prob)
