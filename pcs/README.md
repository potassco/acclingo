## PCS files
The pcs (parameter configuration space) files in this folder denote what parameters acclingo will try to optimize. They also denote what values each option can take.

#### Parameter files for clasp
In the all_params.pcs file all solver parameters along with their possible values are given. If a parameter has a interval of possible values then this is represented in the pcs file aswell.  The interval can be integer based, e.g. the integer interval [1,64] means that any number between 1 and 64 is a valid value for the parameter. The interval can also be composed of reals, e.g. the interval [1.0,2.0]. This means that this file has an infite number of combinations in the configuration space.

The all_params_disc.pcs file has the same parameters as the all_params.pcs file. However, any parameter where there was an interval has its possible values reduced to only a couple of options. For example, instead of the interval [1,64] we now have the possible options {1,2,10,30,50,64}

The limited_params.pcs file cuts down parameters of the all_params_disc.pcs file and only keeps the ones that pertain to *optimization*.
