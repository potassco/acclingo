# Asprin TAE

This TAE is very similar to the basic clasp TAE. The only differences are that it only counts a solution as a succesful solution if the optimum was found and that it needs an asprin "binary" or a way to call asprin. The penalty for no solution or no optimal solution is the maximum available time multiplied by some penalty value . This penalty value can be given as a parameter:

⋅⋅* Parameter to penalize no optimal solution = "penalty": float

example:
```
--tae_args "{\"penalty\": 3}"
```

# Optimization Weights (clasp_opt_weights_tae.py) TAE

The optimization weights TAE is a variant of "clasp\_opt\_tae" where the cost of not finding the optimal solution is calculated based on the time it takes to find some solution (or no solution) and the solution quality.

## Solution quality
There are two ways to calculate the cost of the solution: normalized cost and not normalized cost. For both calculations we assume that a higher value is always worse.

Normalized cost uses the following formula:
```
    solution_quality = 1 - (best_known_solution / found_solution_quality)
```
this formula will be between 0 and 1 for all values *worse* than the best solution. A solution is worse than another if its value is higher(E.g 10 is worse than 5). If the solution found is better, the value will become negative.

Not normalized quality cost uses the following formula:
```
    solution_quality = (found_solution_quality / best_known_solution)
```
This formula basically gives a ratio of the quality of the found solution to the best known solution. So, a value higher than 1 means that the found solution is worse and a value below 1 means that the found solution is better.

## Runtime quality
The Above formulas are used to gage the solution quality. To calculate the actual cost we also want to take a look at the time quality. The following formula is used regardless of the which quality formula is used:
```
    runtime_quality = (found_solution_runtime / cutoff)
```
Where cutoff is the maximum runtime. The value ranges from 0 to 1 with a higher value being worse as it took longer to find the solution.

## Solution Cost calulation

If a solution was not found for the current instance, the following formula is used
```
    cost = par_factor * unsolved_penalty
```
Par factor is usually set to 10 and unsolved penalty is a predefined value that modifies par factor.

The actual cost is then calculated with the following formula:
```
    cost = time_weight * runtime_quality + solution_weight * solution_quality
```
We take both runtime and solution quality and add them based on some predefined weights. If the cost is *higher* than the cost for no solution, then the cost for no solution is taken instead.

## TAE Parameters:

⋅⋅* Parameter for solution quality weight = "solution": float
⋅⋅* Parameter for runtime quality weight  = "time"    : float
⋅⋅* Parameter for no solution penalty     = "penalty" : float
⋅⋅* Parameter to choose quality formula   = "normalized": bool

⋅⋅* Path to csv file containing list of best solutions = "best_known": str

example:

```
--tae_args "{\"best_known\": \"bestbound/bestboundfile.csv\", \"solution\": 0.6, \"time\": 0.4, \"penalty\": 5, \"normalized\": 1}"
```




