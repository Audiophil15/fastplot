# Fastplot

A simple script which goal is to allow fast plotting of simple functions using [Numpy] and [Matplotlib].

### Needed modules
Numpy and Matplotlib, to install these modules :
```sh
pip3 install numpy
pip3 install matplotlib
```

### Usage
Given a function defined in `function.py`:
```sh
python fastplot.py function
```

The function to plot must be defined in a separate file, along with the possible settings of the plot.
Possible settings are :
- the range of evaluation `[m, M]` by setting `m` **and** `M` (default `m, M = 0, 100`)
- the number `n` of evenly spaced values to get, can be defined using m and M (default `n=2*(M-m)`) 
- The `label` to be shown in the legend (default `label = ""`)

Example of "function" file :
```python
"""f-simple.py"""

from numpy import e

# Defining the range of evaluation
m, M = -15, 15

label = "f(x) = x^3 - 15x^2 + 0.21x + e"

def f(x) :
	return x**3 - 15*x*x + 0.21*x + e
```

### Notes
Line style could be added as a setting. Currently lazy but I could add it soon, it's the same idea.

Had the idea of the script to use together vimtex and Inkscape, Matplotlib is a way faster and better plotting tool than Inkscape, but it was tiring to rewrite constantly the same lines of code.

Hope it could help someone in any way.

[Numpy]:https://numpy.org/
[Matplotlib]:https://matplotlib.org/
