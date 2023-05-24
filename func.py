import numpy as np

m, M = 1, 2.5
label="sqrt(2x+ln(x))"
title="Sample test"
xlabel = "x"
ylabel = "f(x)"
n=100000

def f(x):
	return np.sqrt(2*x+np.log(x))