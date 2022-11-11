# Math functoins should be imported from numpy rather than the math module because it allows to apply functions on vectors

from numpy import sin, pi

# param 1
k1 = 0.5
# param 2
k2 = pi

# Just changing the number of evaluations (m and M must be defined if used to define n)
m, M = 0, 100
n = 5*(M-m)

label = "f(x)"

def g(x, k1, k2) :
	return sin(k1*x)*k2

def f(x) :
	return g(x, k1, k2)

