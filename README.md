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
python scripts/acclingo --instance_dir <directory> <optional options>
```
The directory with the instances is the only required parameter, all other options are optional, see `--help` for more information.
Per default, `acclingo` retrieves a parameter configuration optimizing runtime for solving grounded instances from the parameter space described [here](pcs/params.pcs) using instances that may be gzipped from `<directory>` .
We provide static binaries for Linux 64 of `clingo 5.1.0` and `runsolver 3.3.4` [here](binaries/).
 
# Advanced Example

We provide the following example enabling algorithm configuration for instances with optimization statements.
Instead of runtime, we optimize a cost function taking into account runtime and quality of solution relative to a best known bound.

```
python scripts/acclingo --instance_dir <directory> --fn_suffix ".gz" --binary <solver>
--run_obj quality --cutoff <timeout> --ac_budget <timeout>
--tae_class acclingo/tae/clasp_opt_tae.py --tae_args "{\"best_known\": \"<csv file>\"}"  
```

- `--fn_suffix ".gz"`: Only instances with extension .gz are considered in the instance directory
- `--binary <solver>`: Provide a custom binary of the solver that gets called from the target algorithm execution class (TAE)
- `--run_obj quality`: Instead of runtime optimize a cost function
- `--cutoff <timeout>`: Timeout for individual algorithm runs
- `--ac_budget <timeout>`: Timeout for acclingo
- `--tae_class acclingo/tae/clasp_opt_tae.py`: TAE that expects `<solver>` to be a `clingo` binary and grounded instances to include `#minimize` statements. If no solution was found or the resulting cost is bigger then the ParN score, the ParN score is returned as costs. Per default 10*cutoff. Otherwise the cost is runtime times percental difference of achieved quality to best known bound.
- `--tae_args "{\"best_known\": \"<csv file>\"}"`: String in json format that passes auxiliary arguments to the TAE. The TAE expects the csv file to have instance names without extension in the first column and integers representing the best known bound in the second.

# Additional Options

The --tae_args can also be used to change the mode of clingo. By default it is set to "clasp". If the instances require an additional file(encoding) to run, you can also provide it with the --tae_args option using "encoding":
```
--tae_args "{\"mode\": \"clingo\", \"encoding\": \"path/to/encoding.lp\"}"
```
