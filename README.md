# acclingo

> Automatic algorithm configuration for `clingo`

# Licence

This program is free software: you can redistribute it and/or modify it under the terms of the 3-clause BSD license (please see the LICENSE file).

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

You should have received a copy of the 3-clause BSD license along with this program (see LICENSE file). If not, see https://opensource.org/licenses/BSD-3-Clause.

# Overview

`acclingo` relies on `SMAC3` to automatically optimize parameter configurations of `clingo` and `clingo`-based systems given a set of instances and a performance measure.

# Installation

`acclingo` only requires `SMAC3` to be installed, sources and documentation can be found here: https://github.com/automl/SMAC3. 

# Usage

No further installation is necessary and the main script can be executed via following commandline:
```
python3 scripts/acclingo.py --instance_dir <directory> <optional options>
```
The directory with the instances is the only required parameter, all other options are optional, see `--help` for more information.
Per default, `acclingo` retrieves a parameter configuration optimizing runtime for solving grounded instances from the parameter space described [here](pcs/params.pcs) using instances that may be gzipped from `<directory>` .
We provide a static binaries for Linux 64 of `clingo 5.1.0` and `runsolver 3.3.4` [here](binaries/).

# Advanced Example
```
python scripts/acclingo --instance_dir <directory> --fn_suffix ".gz" --binary <solver> --run_obj quality --tae_args "{\"best_known\": \"<csv file>\"}" --tae_class acclingo/tae/clasp_opt_tae.py --cutoff <timeout for one run> --ac_budget <timout for algorithm configuration>
```



