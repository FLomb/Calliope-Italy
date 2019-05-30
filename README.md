# Calliope-Italy
Calliope-based 20-node representation of the Italian energy system, including both power sector and residential heat (currently DHW only).

## Requirements
Calliope version 0.6.3

## Versions
Both versions are based on a 3-step logic:
- Iteration 0: free min_cost optimisation
- Iteration 1: min_co2, within a 5% neighbourhood of the total_cost_0
- Iteration (2:n): min weighted sum of scores.cap per loc::tech, within a 10% neighbourhood of the cost (ideally, different locs for VRES, though slightly more expensive)

Versions 0.1 and 0.2 differentiate in terms of the "Iteration (2:n)" logic, i.e. the maximally-different-location logic.
- v.0.1 uses a scoring method which assings a weight based on the "share" of installed capacity for each loc::tech combination.
Quite a bad idea indeed. Increasing a loc::tech cap means increasing overall capacity and decreasing the share in other loc::techs. Weird and hardly controllable behaviour. Gets stuck into the same NOS after a couple of iterations.

- v.0.2 uses an "integer" scoring method, which assings a +1 score to loc::techs which are increasing installed capacity compared to Iteration 1. Much better idea. However, still gets stuck after a couple of iterations, as expected, as it currently fails to check if the capacity installed in a given loc::tech in a j-th iteration is "new" compared to *all* previous iterations. Quite easy to fix, currently on it.
[Work in progress]
