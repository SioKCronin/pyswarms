# -*- coding: utf-8 -*-

"""
Hyperparameter grid search.

Compares the relative performance of hyperparameter value combinations in
optimizing a specified objective function.

For each hyperparameter, user can provide either a single value or a list
of possible values. The cartesian products of these hyperparameters are taken
to produce a grid of all possible combinations. These combinations are then
tested to produce a list of objective function scores. The search method
default returns the minimum objective function score and hyperparameters that
yield the minimum score, yet maximum score can also be evaluated.

Parameters
----------
* c1 : float
    cognitive parameter
* c2 : float
    social parameter
* w : float
    inertia parameter
* k : int
    number of neighbors to be considered. Must be a
    positive integer less than `n_particles`
* p: int {1,2}
    the Minkowski p-norm to use. 1 is the
    sum-of-absolute values (or L1 distance) while 2 is
    the Euclidean (or L2) distance.

>>> options = {'c1': [1, 2, 3],
               'c2': [1, 2, 3],
               'w' : [2, 3, 5],
               'k' : [5, 10, 15],
               'p' : 1}
>>> g = GridSearch(LocalBestPSO, n_particles=40, dimensions=20,
                   options=options, objective_func=sphere_func, iters=10)
>>> best_score, best_options = g.search()
>>> best_score
0.498641604188
>>> best_options['c1']
1
>>> best_options['c2']
1
"""

import operator as op
import itertools
import numpy as np
from pyswarms.utils.search.base_search import SearchBase

class GridSearch(SearchBase):
    """Exhaustive search of optimal performance on selected objective function
    over all combinations of specified hyperparameter values."""

    def __init__(self, optimizer, n_particles, dimensions, options,
                 objective_func, iters,bounds=None, velocity_clamp=None):
        """Initializes the paramsearch."""

        # Assign attributes
        super().__init__(optimizer, n_particles, dimensions, options,
                objective_func, iters, bounds=bounds,
                velocity_clamp=velocity_clamp)

    def generate_grid(self):
        """Generates the grid of all hyperparameter value combinations."""

        #Extract keys and values from options dictionary
        params = self.options.keys()
        items = [x if type(x) == list \
                 else [x] for x in list(zip(*self.options.items()))[1]]

        #Create list of cartesian products of hyperparameter values from options
        list_of_products = list(itertools.product(*items))

        #Return list of dicts for all hyperparameter value combinations
        return [dict(zip(*[params, list(x)])) for x in list_of_products]

