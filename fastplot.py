#!/bin/python3

import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from sys import argv
from Equation import Expression
import re


"""
Script meant to allow fast plotting of (1) simple functions, possibly with some constant parameters in addition of the variable, or (2) data files, made of one or two columns of numbers.

If (1) :
It needs an associated file to import, in which the mathematical function to plot and all other constants are defined.
The main mathematical function must be named f (defined as something like 'def f(x)').
Constant parameters need to be defined and assigned in the same file.

Range of evaluation is set by default to [0, 100]. It can be change by defining integers m and M
Number of evaluations on the choosen interval is set by default to 2*(M-m). Can also be changed by defining an integer n.

If (2) :
It needs a file with the values to be plotted given either as one column which will be plotted against arbitrary absciss axis, or as two columns, the values of the second column plotted against the ones of the first.

In both cases a label, title, and axis labels can be set. When defined in a Python file the values must be enclosed in quotes (") to be parsed, in a data file quotes don't change anything.
All those fields are empty by default.
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

"""Parse tools"""

def parseOptions(argv) :
	global mode
	global plotmode
	global filepath
	global order
	global filtering
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
					order = int(arg.split("r")[1].strip()[0])
				except :
					order = 1

		else :
			filepath = arg

	if plotmode == "" :
		plotmode = "p"

	return mode, plotmode, order, filepath

def findinfile(fieldname, file) :
	value = ""
	file.seek(0)
	for l in file.readlines() :
		if fieldname in l :
			try :
				founds = list(map(str.strip, l.split("=")))
				if fieldname in founds :
					value = l[l.find("=")+1:].strip().replace('"','')
			except :
				pass
	file.seek(0)
	return value


"""Equation parser functions"""

# Tests if the user entered something like "2x+5" which isn't parsed. Nothing stops him to write "xy" instead of "x*y" though.
def hasImpliedMultiplication(expression) :
	found = re.search("[0-9]+[a-zA-Z]+", expression)
	return found

def impliedMultiplicationError(foundExpr) :
	print("\n\tError : Multiplication should be explicit : \"%s\" instead of \"%s\"\n"%( re.search("[0-9]+", foundExpr.group()).group()+"*"+re.search("[a-zA-Z]+", foundExpr.group()).group(), foundExpr.group()))

def stringToFunc(string) :
	found = hasImpliedMultiplication(string)
	if found :
		impliedMultiplicationError(found)
		raise ValueError("The string has implied multiplication")
	else :
		return Expression(string, ["x"])



usage = "Usage : python fastplot.py mode -(plotmode) -[options] (file|expression)\nModes available :\n\t-e  : Enter an equation that will be parsed\n\t-ff : Give a file containing a python-defined function\n\t-df : Give a file containing data on one or two columns that will be plotted or scattered\nModes for the plot (can be combined) :\n\t-s : Points will be scattered\n\t-p : Points will form a continuous curve\n\t-r<order> : A fitting curve is plotted over the plotted curve/data, of the given order (max 9)\n"


if __name__ == "__main__" :

	if len(argv) < 3 :

		# Not enough arguments on the command line

		print(usage)
		exit(1)

	# Defining the defaults for the needed variables

	mode = ""
	plotmode = ""
	filepath = ""

	m, M = 0, 100
	n = 2*(M-m)
	order = 0

	title = ""
	label = ""
	xlabel = ""
	ylabel = ""

	parseOptions(argv)

	if mode == "" :
		print("You need to choose a mode !")
		exit(21)
	if filepath == "" :
		print("You need to give a file path !")
		exit(22)

	if mode == "e" :

		f = stringToFunc(filepath)
		pass

	if mode != "e" :

		file = open(filepath, "r")
		title = findinfile("title", file)
		label = findinfile("label", file)
		xlabel = findinfile("xlabel", file)
		ylabel = findinfile("ylabel", file)
		file.close()

	if mode == "ff" :

		try :
			# If the extension is left, it will be removed
			if filepath[-3:] == ".py" :
				filepath = filepath[:-3]
			function = __import__(filepath, globals(), locals(), [], 0)

			f = function.f
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

		except Exception as e :
			print("Error : ", e)
			print("Error during the import of the file containing the function to plot.")
			exit(2)

	if mode in ["e", "ff"] :

		x = np.linspace(m, M, n)
		y = f(x)

	if mode == "df" :

		file = open(filepath, "r")
		data = []

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
		file.close()

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
