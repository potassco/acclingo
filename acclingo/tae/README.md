# TAEs
A TAE is a special class that runs the target algorithm and reports the results of the runs back to the SMAC optimizer. We have 3 available TAEs at the moment. ```clasp_tae.py``` implements the basic TAE. It works for regular clingo and supports optimizing for **runtime**. The ```clasp_opt_tae.py``` file contains a TAE that is used to optimize for **quality**. This means that, in order to use this TAE effectively, the encoding/instance must have an optimization(e.g. minimize) statement. Finally, the asprin TAE, found in the ```asprin_tae.py``` file, is intended to be used with [asprin](https://github.com/potassco/asprin). This TAE is used to optimize for **runtime** and the run is considered successful only when it finds the optimum value. Below we cover how the cost of a single run is calculated for the three TAEs.

# Clingo and Asprin TAE cost function

The cost function for both of these TAEs is very simple. It takes either the runtime if the run was successful or the runtime multiplied by the par factor otherwise.
```
cost = runtime
```

# Optimization TAE

The optimization TAE is used when we want to find configurations for optimization problems. There are two types of cost calculations. First, the "diverse" formula scales the time taken to find the solution by how the quality found compares to the best known value, percentage wise. For example, if the best known quality is 100 and the configuration managed to find a solution with quality 110 then the runtime is scaled up by 1+10. If the solution quality is 50 then the runtime is scaled by 1+(-50).
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

You can decide which formula to use by providing the key "cost_function" and a value of either "diverse" or "deep" to the ```--tae-args``` option. The default function is "diverse".

```
--tae-args "{\"cost_function\": \"diverse\"}"
```

# Building your own TAE

To build your own TAE we can use the ```template_tae.py``` file as a starting point. Simply copy it and start working on the new file.

If your TAE has any arguments you should handle them inside the *handle_misc_args* function. The extra argument come mostly from the ```--tae-args``` option. Most importantly, in this function it is defined what type of run objective the TAE supports (either runtime or quality). An example of a misc argument to handle comes from the optimization TAE, which handles whether the "deep" or "diverse" cost function will be used based on the value in the misc dictionary.

Then, define how the cost for a given run is calculated using the *calculate_cost* function. The function receives the parsed output of the runsolver file aswell as the parsed output of the solver. It also receives the cutoff time of the run as a parameter. The return value should be the cost of the run as a float value.

Finally, if your system has an output format that is different from clingo, or if you need to parse some data that is not already parsed by default you can use the functions *parse_extra_solver_data* and *parse_extra_runsolver_data*. Those function receive the full text of the output of the solver and runsolver respectively. Their return value should be a dictionary. It is important to note that the values parsed here will then be passed on to the cost function so that it can make use of them if necessary.
