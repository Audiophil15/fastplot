import numpy as np
import matplotlib.pyplot as plt
from sys import argv

"""
Script meant to allow fast plotting of simple functions, possibly with some constant parameters in addition of the variable
It needs an associated file to import, in which the mathematical function to plot and all other constants are defined.

The main mathematical function must be named f (defined as something like 'def f(x)').
Constant parameters need to be defined and assigned in the same file.

Range of evaluation is set by default to [0, 100]. It can be change by defining integers m and M
Number of evaluations on the choosen interval is set by default to 2*(M-m). Can also be changed by defining an integer n.
Legend label is empty by default, can be set declaring a 'label' string variable.
"""

"""
# Example of file :

from numpy import e

# Defining the range of evaluation
m, M = -15, 15

label = "f(x) = x^3 - 15x^2 + 0.21x + e"

def f(x) :
	return x**3 - 15*x*x + 0.21*x + e
"""

usage = "Usage : python fastplot.py <file>\nNo .py extension should be left after the function file (but the script will remove it if your forget to)."


if __name__ == "__main__" :

	if len(argv) < 2 :

		# Not enough arguments on the command line

		print(usage)
		exit(1)

	else :

		# Defining the defaults for the needed variables

		m, M = 0, 100
		n = 2*(M-m)
		label = ""

		try :
			# If the extension is left, it will be removed
			if argv[1][-3:] == ".py" :
				argv[1] = argv[1][:-3]
			function = __import__(argv[1], globals(), locals(), [], 0)

			try :
				m, M = function.m, function.M
			except :
				pass
			try :
				n = function.n
			except :
				pass
			try :
				label = function.label
			except :
				pass

		except :
			print("Error during the import of the file containing the function to plot.")
			exit(2)


		x = np.linspace(m, M, n)

		y=function.f(x)

		plt.plot(x, y, label=label)
		if (label!="") :
			plt.legend()
		plt.show()
