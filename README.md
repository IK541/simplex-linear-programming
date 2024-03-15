# Simplex algorithm for linear programming problems

The projext contains an implementation of simplex algorithm for solving linear programming problems. It produces a .tex file containing a series of tables showing consequitive steps of the algorithm. A html support is planned in a future.

## How to use

The program accepts one argument: a name of a text file with linear programming problem, and prints the result to the standard output

The text file should consist of 1 line with objective function consisting of a string ```min``` or ```max``` for minimizing or maximizing the objective function then a space separated list of coefficients of the decision variables in the objective function. Following lines should contain constaints in a form of space separated list of coefficients of each decision variable followed by ```>``` for $\geq$ or ```<``` for $\leq$, followed by the constant.

For example for a linear programming problem:

$$
\begin{gather*}
    \max{\left(x_1 - x_2\right)} \\
    x_1 - x_2 + 100 x_3 \leq 50 \\
    x_1 - x_2 + 40 x_3 \leq 10 \\
    x_3 \leq 1
\end{gather*}
$$

The input file should look like:

```
max 1 -1 0
1 -1 100 < 50
1 -1 40 < 10
0 0 1 < 1
```

The program can be run using:

```
py simplex.py input_file.txt > output_file.tex
```

Note that ```py``` is a python interpreter, which may have a different name on your system.

The .tex file is ready for compilation using programs like pdflatex:

```
pdflatex output_file.tex
```