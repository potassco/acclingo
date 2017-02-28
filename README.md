# ac_clingo

> Automatic algorithm configuration for `clingo`

# Licence

This program is free software: you can redistribute it and/or modify it under the terms of the 3-clause BSD license (please see the LICENSE file).

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

You should have received a copy of the 3-clause BSD license along with this program (see LICENSE file). If not, see https://opensource.org/licenses/BSD-3-Clause.

# Overview

`ac_clingo` relies on `SMAC3` to automatically optimize parameter configurations of `clingo` and `clingo`-based systems given a set of instances and a performance measure.

# Installation

`ac_clingo` only requires `SMAC3` to be installed, sources and documentation can be found here: https://github.com/automl/SMAC3. 

# Usage

No further installation is necessary and the main script can be executed via following commandline:
```
python3 scripts/ac_clingo.py --instance_dir <directory> <optional options>
```
The directory with the instances is the only required parameter, all other options are optional.
Per default, `ac_clingo` optimizes a parameter configuration for solving only from the parameter space described [here](pcs/params.pcs) using grounded instances from `<directory>` that may be gzipped.
We provide a static binary for `clingo 5.1.0` and `runsolver 3.3.4` [here](binaries/).
