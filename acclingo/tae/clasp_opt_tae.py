import sys
import os
import random
import re
from subprocess import Popen, PIPE
from math import log2

from acclingo.tae.clasp_tae import ClaspTAE

from smac.tae import StatusType
from smac.stats.stats import Stats
from smac.utils.constants import MAXINT

__author__ = "Marius Lindauer"
__license__ = "3-clause BSD"

float_regex = '[+-]?\d+(?:\.\d+)?(?:[eE][+-]\d+)?'

class ClaspOptTAE(ClaspTAE):

    
    def __init__(self, *args, **kwargs
                 ):

        super().__init__(*args, **kwargs)

    def handle_misc_args(self, misc):

        if self.run_obj != "quality":
            raise Exception("Run objective {} not supported. This TAE only supports 'quality'".format(self.run_obj))
        

        self.best_known=dict();
        if "best_known" in misc:
            with open(misc["best_known"]) as f:
                for line in f.readlines():
                   self.best_known[line.split(',')[0].strip()]=int(line.split(',')[1].strip())

        self.cost_func = self.scale_time_by_cost

        if "cost_function" in misc:
            if misc["cost_function"] == "diverse":
                self.cost_func = self.scale_time_by_cost
            elif misc["cost_function"] == "deep":
                self.cost_func = self.sum_time_and_weight

    def scale_time_by_cost(self, runtime, quality, cutoff):

        if quality == None or runtime == None:
            cost = cutoff * self.par_factor
        else:
            best = self.best_known[os.path.splitext(os.path.basename(instance))[0]]
            diff = float(rs_output["ta_quality"]) - float(best)
            prct = float(best)/100.0 if best!=0 else 1.0
            cost = min(float(cutoff * self.par_factor),ta_runtime*(1+(diff/prct))

        return cost

    def sum_time_and_weight(self, runtime, quality, cutoff):

        if quality == None or runtime == None:
            cost = self.par_factor
        else:
            
            best = self.best_known[os.path.splitext(os.path.basename(instance))[0]]
            if best == 0: 
                best = 1

        if quality == 0:
            quality == 0.1

        solution_quality = 1 - log2(float(best)/float(quality))

        runtime_quality = float(runtime)/float(cutoff)

        cost = min(self.par_factor, runtime_quality + solution_quality)

        return cost

    def calculate_cost(self, rs_output, solver_output, cutoff):

        if rs_output["ta_runtime"] is not None:
            ta_runtime = rs_output["ta_runtime"]
        elif solver_output["clingo_runtime"] is not None:
            ta_runtime = solver_output["clingo_runtime"]
        else:
            ta_runtime = None

        cost = self.cost_func(ta_runtime, solver_output["ta_quality"], cutoff)
        
        return cost
