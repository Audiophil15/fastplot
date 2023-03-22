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

def parseOptions(argv) :
	mode = ""
	plotmode = ""
	filepath = ""
	order = 0
	for arg in argv[1:] :
		if arg[0] == "-" :
			if (a := arg[1:]) in ["e", "df", "ff"] :
				mode = a
			if "s" in a :
				plotmode += "s"
			if "p" in a :
				plotmode += "p"
			if "r" in a :
				try :
					order = int(arg.split("r")[1][0])
				except :
					order = 1

		else :
			filepath = arg

	if plotmode == "" :
		plotmode = "p"

	return mode, plotmode, order, filepath

def findinfile(fieldname, file) :
	value = ""
	for l in file.readlines() :
		if fieldname in l :
			try :
				founds = list(map(str.strip, l.split("=")))
				if fieldname in founds :
					value = founds[-1].strip()
			except :
				pass
	file.seek(0)
	return value


usage = "Usage : python fastplot.py mode [plotmode] (file|expression)\nNo .py extension should be left after the function file (but the script will remove it if your forget to).\nModes available :\n\t-e  : Enter an equation that will be parsed\n\t-ff : Give a file containing a python-defined function\n\t-df : Give a file containing data on two columns that will be plotted or scattered\nModes for the plot (can be combined) :\n\t-s : Points will be scattered\n\t-p : Points will form a continuous curve\n"


if __name__ == "__main__" :

	if len(argv) < 3 :

		# Not enough arguments on the command line

		print(usage)
		exit(1)

	else :

		mode, plotmode, order, filepath = parseOptions(argv)
		if mode == "" :
			print("You need to choose a mode !")
			exit(21)
		if filepath == "" :
			print("You need to give a file path !")
			exit(22)

		# Defining the defaults for the needed variables

		m, M = 0, 100
		n = 2*(M-m)
		title = ""
		label = ""
		xlabel = ""
		ylabel = ""


		if mode == "e" :
			pass

		if mode == "ff" :

			try :
				# If the extension is left, it will be removed
				if filepath[-3:] == ".py" :
					filepath = filepath[:-3]
				function = __import__(filepath, globals(), locals(), [], 0)

				try :
					m, M = function.m, function.M
				except :
					print("No custom window range found")
					pass
				try :
					n = function.n
				except :
					print("No custom sample number found")
					pass
				try :
					title = function.title
				except :
					print("No custom title found")
					pass
				try :
					label = function.label
				except :
					print("No custom label found")
					pass
				try :
					xlabel = function.xlabel
				except :
					print("No custom label found for x")
					pass
				try :
					ylabel = function.ylabel
				except :
					print("No custom label found for y")
					pass

			except :
				print("Error during the import of the file containing the function to plot.")
				exit(2)

			x = np.linspace(m, M, n)
			y = function.f(x)

		if mode == "df" :
			file = open(filepath, "r")
			data = []

			title = findinfile("title", file)
			label = findinfile("label", file)
			xlabel = findinfile("xlabel", file)
			ylabel = findinfile("ylabel", file)
			for l in file.readlines() :
				try :
					if (d := list(map(float, l.split()))) != [] :
						data.append(d)
				except :
					pass

			data = list(zip(*data))
			if len(data) == 1 :
				y = data[0]
				x = list(range(len(y)))
			elif len(data) == 2 :
				x, y = data

		if "s" in plotmode :
			plt.scatter(x, y, label=label)
		if "p" in plotmode :
			plt.plot(x, y, label=label)
		if order :
			reg = np.polynomial.polynomial.Polynomial.fit(x, y, order)
			plt.plot(x, reg(np.array(x)), label=reg.convert())
			plt.legend()
		if (label!="") :
			plt.legend()
		plt.title(title)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.show()
