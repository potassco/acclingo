import sys
import time
import copy
import logging
import typing
from collections import Counter
from collections import OrderedDict

import numpy as np

from smac.smbo.objective import sum_cost
from smac.stats.stats import Stats
from smac.utils.constants import MAXINT, MAX_CUTOFF
from smac.configspace import Configuration
from smac.runhistory.runhistory import RunHistory
from smac.tae.execute_ta_run import StatusType
from smac.intensification.intensification import Intensifier

__author__ = "Marius Lindauer"

class Intensifier(Intensifier):

    '''
        takes challenger and incumbents and performs intensify
    '''

    def __init__(self, tae_runner, stats, traj_logger, rng, instances,
                 instance_specifics=None, cutoff=MAX_CUTOFF, deterministic=False,
                 run_obj_time=True, run_limit=MAXINT, minR=1, maxR=2000):
        '''
        Constructor

        Parameters
        ----------
        tae_runner : tae.executre_ta_run_*.ExecuteTARun* Object
            target algorithm run executor
        stats: Stats()
            stats object            
        traj_logger: TrajLogger()
            TrajLogger object to log all new incumbents
        rng : np.random.RandomState
        instances : list
            list of all instance ids
        instance_specifics : dict
            mapping from instance name to instance specific string
        cutoff : int
            runtime cutoff of TA runs
        deterministic: bool
            whether the TA is deterministic or not
        run_obj_time: bool
            whether the run objective is runtime or not (if true, apply adaptive capping)
        run_limit : int
            Maximum number of target algorithm runs per call to intensify.
        maxR : int
            Maximum number of runs per config (summed over all calls to
            intensifiy).
        minR : int
            Minimum number of run per config (summed over all calls to
            intensify).
        '''
        super().__init__(tae_runner=tae_runner, 
                         stats=stats, 
                         traj_logger=traj_logger, 
                         rng=rng, 
                         instances=instances,
                         instance_specifics=instance_specifics, 
                         cutoff=cutoff, 
                         deterministic=deterministic,
                         run_obj_time=run_obj_time, 
                         run_limit=run_limit, 
                         minR=minR, 
                         maxR=maxR)

    def _compare_configs(self, incumbent: Configuration, 
                         challenger: Configuration, 
                         run_history: RunHistory,
                         aggregate_func: typing.Callable):
        '''
            compare two configuration wrt the runhistory 
            and return the one which performs better (or None if the decision is not safe)

            Decision strategy to return x as being better than y:
                1. x has at least as many runs as y
                2. x performs better than y on the intersection of runs on x and y

            Implicit assumption: 
                challenger was evaluated on the same instance-seed pairs as incumbent

            Parameters
            ----------
            incumbent: Configuration
                current incumbent
            challenger: Configuration
                challenger configuration
            run_history: RunHistory
                stores all runs we ran so far
            aggregate_func: typing.Callable
                aggregate performance across instances

            Returns
            -------
            None or better of the two configurations x,y
        '''

        inc_runs = run_history.get_runs_for_config(incumbent)
        chall_runs = run_history.get_runs_for_config(challenger)
        to_compare_runs = set(inc_runs).intersection(chall_runs)

        # performance on challenger runs
        chal_perf = aggregate_func(
            challenger, run_history, to_compare_runs)
        inc_perf = aggregate_func(
            incumbent, run_history, to_compare_runs)

        # Line 15
        if chal_perf > inc_perf and len(chall_runs) >= self.minR:
            # Incumbent beats challenger
            self.logger.debug("Incumbent (%.4f) is better than challenger (%.4f) on %d runs." % (
                inc_perf, chal_perf, len(chall_runs)))
            return incumbent

        # Line 16
        if not set(inc_runs) - set(chall_runs):
            # Challenger is as good as incumbent
            # and has at least the same runs as inc
            # -> change incumbent

            n_samples = len(chall_runs)
            self.logger.info("Challenger (%.4f) is better than incumbent (%.4f) on %d runs." % (
                chal_perf, inc_perf, n_samples))
            self.logger.info(
                "Changing incumbent to challenger: %s" % (challenger))
            self.stats.inc_changed += 1
            self.traj_logger.add_entry(train_perf=chal_perf,
                                       incumbent_id=self.stats.inc_changed,
                                       incumbent=challenger)
            return challenger

        return None  # undecided
