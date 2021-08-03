import sys
import os
import random
import re
from subprocess import Popen, PIPE

from smac.tae.execute_ta_run import StatusType, ExecuteTARun
from smac.stats.stats import Stats
from smac.utils.constants import MAXINT

from tempfile import NamedTemporaryFile

__author__ = "Marius Lindauer"
__license__ = "3-clause BSD"

float_regex = '[+-]?\d+(?:\.\d+)?(?:[eE][+-]\d+)?'

class AsprinTAE(ExecuteTARun):

    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def handle_misc_args(self, misc):
        """
        If your TAE has some misc args it has to handle to that here!
        Also, it has to handle the self.run_obj argument.
        E.g., it may only support runtime or quality
        """
        pass      

    def calculate_cost(self, rs_output, solver_output, cutoff):

        if self.run_obj == "runtime":
            # get runtime if optimum was found, else apply penalty
            if solver_output["ta_status"] == StatusType.SUCCESS:
                cost = ta_runtime
            else:
                cost = cutoff * self.par_factor
        else:
            cost = ta_quality
            
        return cost
    
    def parse_extra_solver_data(self, data):
        '''
        Parse a results file to extract the run's status (SUCCESS/CRASHED/etc) and other optional results.
    
        Args:
            fn: a name to the file containing asprin stdout.
            exit_code : exit code of target algorithm
        Returns:
            ta_status, ta_quality 
        '''

        ta_status = None

        if re.search('UNSATISFIABLE', data):
            ta_status = StatusType.TIMEOUT
        elif re.search('SATISFIABLE', data):
            ta_status = StatusType.TIMEOUT
        elif re.search('OPTIMUM FOUND', data):
            ta_status = StatusType.SUCCESS
        elif re.search('s UNKNOWN', data):
            ta_status = StatusType.TIMEOUT
        elif re.search('INDETERMINATE', data):
            ta_status = StatusType.TIMEOUT
            
        return {"ta_status": ta_status}
