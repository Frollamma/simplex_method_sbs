# Introduction
This project aims to get a working implementation of the Simplex Method capable of showing intermediate steps. In particular, we focus on the Full Tableau Simplex Method, for now. The output formats will be plain text (redirected to stdout or a file) and $\LaTeX$ (as a PDF and `.tex` file).

# Installation
To run it type
```
python main.py
```

# Mindset
This project focuses on providing **exact** results and showing them in a human-readable format with all steps included. For these reasons, I use `sympy`, a python package for symbolic calculations.

# Roadmap
- [x] Add support for Linear Programming Problem in standard form
- [ ] Handle degenerate cases
- [ ] Add CLI
- [ ] Add input of full problem
- [ ] Add support for Linear Programming Problem in non standard form (and conversion to standard form)
- [ ] Add $\LaTeX$ output
- [ ] Add Integer Linear Programming Problem support
- [ ] Add different simplex methods: The Revised Simplex Method, etc.
- [ ] Support file input and multiple files input

# Contributing
Any contribution is much appreciated!
