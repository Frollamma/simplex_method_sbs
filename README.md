# Introduction
This project aims to get a working implementation of the Simplex Method capable of showing intermediate steps. In particular, we focus on the Full Tableau Simplex Method, for now. The output formats will be plain text (redirected to stdout or a file) and $\LaTeX$ (as a PDF and `.tex` file).

# Mindset
Style decisions:
- I didn't put the argument `tol` in many functions in `util.py`, because I think it affects code readability for a feature that will be never really used. At least efficiency and numerical problems are not the main concern of this project.

# Roadmap
- [ ] Add support for Linear Programming Problem in standard form
- [ ] Add input of full problem
- [ ] Add support for Linear Programming Problem in non standard form (and conversion to standard form)
- [ ] Add $\LaTeX$ output
- [ ] Add Integer Linear Programming Problem support
- [ ] Add The Revised Simplex Method and others...

# Contributing
Any contribution is much appreciated!