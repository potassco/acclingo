# TAEs
A TAE is a special class that is supposed to run the algorithm and report the results of the run back to SMAC. We have 3 available TAEs at the moment. clasp_tae.py implements the basic TAE. It works for regular clingo and supports optimizing for **runtime**. The clasp_opt_tae.py file contains a TAE that is used to optimize for **quality**. This means that, in order to use this TAE effectively, the encoding/instance must have an optimization(e.g. minimize) statement. Finally, the asprin TAE is intended to be used with asprin(add link). This TAE is used to optimize for **runtime** and the run is considered successful only when the run found the optimum value.

# Clingo and Asprin TAE cost function

The cost function for both of these TAEs is very simple. It takes either the runtime if the run was successful or the runtime multiplied by the par factor otherwise.

# Optimization TAE

The optimization TAE is used when we want to find configurations for optimization problems. There are 2 types of cost calculations. First, the "diverse" formula scales the time taken to find the solution by how the quality found compares to the best known value percentage wise. E.g. if the best quality yet has been 100 and the configuration managed to find a solution with quality 110 then the runtime is scaled up by 1+10. if the solution quality is 50 then the runtime is scaled by 1+(-50).
```
cost = runtime * (1 + percentage*100)
```


The second formula, called "deep", is calculated by dividing the best found value by the solution quality, taking the log2 of the result and then subtracting it to 1:
```
quality_cost = 1 - log2(best/quality))
```

Then, we also calculate the ratio of the runtime to the cutoff:
```
runtime_cost = runtime/cutoff
```

To get the actual cost, we sum up those 2 values. If there was no solution found then we take the par factor as the cost.
```
cost = runtime_cost + quality_cost
```

# Building your own TAE

To build your own TAE, first you need to create a file and copy the imports from the clasp_opt_tae.py file. Then, define your class and make it inherit ClaspTAE. The init function should look as follows:
```
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
```

Then, if your TAE has any arguments you should handle them inside the *handle_misc_args* function. The extra argument come mostly from the ```--tae-args``` option. Most importantly, in this function it is defined what type of run objective the TAE supports (either runtime or quality). For example, the function in the clasp_opt_tae.py handles whether the TAE will use the "deep" or "diverse" cost function based on the value given.
```
def handle_misc_args(self, misc):
    handle the args
    return nothing
```

Then, define how the cost for a given run is calculated using the *calculate_cost* function. The function receives the parsed output of the runsolver file aswell as the parsed output of the solver. It also receives the cutoff time of the run as a parameter. The return value should be the cost of the run as a float value.
```
def calculate_cost(self, runsolver_output, solver_output, cutoff):

    return cost
```

Finally, if your system has an output format that is different from clingo, or if you need to parse some data that is not already parsed by default you can use the functions *parse_extra_solver_data* and *parse_extra_runsolver_data*. Those function receive the full text of the output of the solver and runsolver respectively. Their return value should be a dictionary.
```
def parse_extra_solver_data(self, data):

    return a_dictionary
```