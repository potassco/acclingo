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
        """
        Use this function to handle any misc args. The misc argument of the function
        represets a dictionary that is given in the command line by the --tae-args option.

        This function should handle the self.run_obj. That is, if the correct run objective was given.
        """

        if self.run_obj != "quality":
            raise Exception("Run objective {} not supported. This TAE only supports 'quality'".format(self.run_obj))
       
    def calculate_cost(self, rs_output, solver_output, cutoff):
        pass

    def parse_extra_solver_data(self, data):
        """
        Use this function to parse extra data from the output of the solver
        It is also possible to overwrite the data from the regular parse_output function

        this has to return a dictionary
        """
        return {}

    def parse_extra_runsolver_data(self, data):
        """
        Use this function to parse extra data from the output of the runsolver
        It is also possible to overwrite the data from the regular parse_output function

        this has to return a dictionary
        """
        return {}