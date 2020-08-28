# Overview

Library based on matplotlib to draw the pyrochlore lattice and configurations of the Spin Ice model.

It can, and probably should, be executed as a script

`python -m pyrodraw`

and follow the instructions which appear on the screen.

# Installation

`$ pip install pyrodraw`

# Basic usage

Depending on the parameters suplied:
* No arguments: draws only the pyrochlore lattices and adds details such as names to the axes.
* '+ z': draws the spin ice +z configuration.
* 'ms': draws the saturation configuration with the field at [111], with positives simple monopoles in all Up Tetrahedra.
* 'md': draws the configuration with positive double monopoles in all Up Tetrahedra.
* Name of a file along with a column number: the data is obtained from it to draw the configuration.

# Possible general improvements
The following are things I didn't know how to do it properly by the time I built the library, and for the purpose of the project it didn't worth changing them when I published it.
* The documentation is not properly done (doesn't follow a docstring convention), and it's in spanish.
* It probably should use argparse for managing the arguments.

# TODO
* Add a circle path as a bottom lid for the arrows.
* Be possible to annotate the field direction when using the field arrow.
