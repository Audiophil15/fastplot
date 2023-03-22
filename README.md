# Fastplot

A simple script which goal is to allow fast plotting of simple functions using [Numpy] and [Matplotlib].

### Needed modules
[Numpy] and [Matplotlib], to install these modules :

- Linux :
Package managers can usually get Python3 packages (something like `python3-matplotlib`, `python3-numpy`)

- Windows :
Follow the respective links to Numpy and Matplotlib

or...

- pip :
```sh
pip3 install numpy
pip3 install matplotlib
```

### Usage

```sh
py fastplot.py MODE [PLOT MODES] FILE
```

Modes are (exclusive) :
- `-df` : Data file mode, requires a file containing the data to plot.
- `-ff` : Function file mode, requires a file containing the Python function to plot.

Plot modes, available for both previous modes, are (non exclusive) :
- `-s` : Scatter the data.
- `-p` : Plot the data with a line.
- `-r[order]` : Plot a regression curve, of order 1 if no order si given.

The mode and plot mode must be set separately but plotm modes can be combined, for example `-df -sr3p` works but `-dfs` doesn't.

#### Given a function defined in `function.py`:
```sh
python fastplot.py function
```

The function to plot must be defined in a separate file, along with the possible settings of the plot.
Possible settings are :
- the range of evaluation `[m, M]` by setting `m` **and** `M` (default `m, M = 0, 100`)
- the number `n` of evenly spaced values to get, can be defined using m and M only if they are defined in the same file (default `n=2*(M-m)`)

#### Given data saved in `data`:
```sh
python fastplot.py data
```

The data to plot must be defined in a separate file, along with the possible settings of the plot. The dataset must be presented in two columns. Only one column will plot the data against an integer list of the same size (as would do `plt.plot(y)`).

Some options can be set for both function and data modes (and must be set in the respective files) :
- The `title` of the plot (default `title = ""`)
- The `label` to be shown in the legend (default `label = ""`)
- The `xlabel` to be shown under the absciss (default `xlabel = ""`)
- The `ylabel` to be shown next to the ordinates (default `ylabel = ""`)

### Examples

Example of "function" file :
```python
""" f-simple.py """

from numpy import e

# Defining the range of evaluation
m, M = -15, 15

label = "f(x) = x^3 - 15x^2 + 0.21x + e"

def f(x) :
	return x**3 - 15*x*x + 0.21*x + e
```

Example of "data" file :
```
title = "Cool data"

0.0		0
0.5		-0.25
1.0		1
1.5		-2.25
2.0		4
2.5		-6.25
3.0		9
3.5		-12.25
```

### Notes
Line style could be added as a setting. Currently lazy but I could add it soon, it's the same idea.

Had the idea of the script to use together vimtex and Inkscape, Matplotlib is a way faster and better plotting tool than Inkscape, but it was tiring to rewrite constantly the same lines of code.

Hope it could help someone in any way.

[Numpy]:https://numpy.org/
[Matplotlib]:https://matplotlib.org/
