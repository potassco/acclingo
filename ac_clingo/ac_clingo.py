import inspect
import logging
import importlib.util

#from smac.facade.smac_facade import SMAC
#TODO: fix this hack by using the original SMAC facade after it was updated
from ac_clingo.facade.smac_facade import SMAC
from smac.scenario.scenario import Scenario

from ac_clingo.io.cmd_reader import CMDReader
from ac_clingo.tae.clasp_tae import ClaspTAE
from ac_clingo.intensification.intensification import Intensifier

__maintainer__='Marius Lindauer'
__license__ = "BSD"

class ACClingo(object):
    
    def __init__(self):
        '''
            Constructor
        ''' 
        
    def main(self):
        '''
            main method
        '''
        
        reader = CMDReader()
        args_, scen_opts = reader.read_cmd()
        
        # change log level
        logging.basicConfig(level=args_.verbose_level)
        root_logger = logging.getLogger()
        root_logger.setLevel(args_.verbose_level)
        
        scen = Scenario(scen_opts)
        
        if args_.tae_class:
            spec = importlib.util.spec_from_file_location("tae",args_.tae_class)
            tae_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tae_module)
            tae_class = inspect.getmembers(tae_module, inspect.isclass)[0][1]
            ctae = tae_class(ta_bin=args_.binary, runsolver_bin=args_.runsolver, 
                            memlimit=args_.memlimit,
                            run_obj=args_.run_obj,
                            par_factor=10)
        else:
            ctae = ClaspTAE(ta_bin=args_.binary, runsolver_bin=args_.runsolver, 
                            memlimit=args_.memlimit,
                            run_obj=args_.run_obj,
                            par_factor=10)
        
        # use individualized compare methode
        intensifier = Intensifier(tae_runner=None, stats=None, 
                                  traj_logger=None, rng=None,
                                  instances=None)
        
        smac = SMAC(scenario=scen, rng=args_.seed, tae_runner=ctae, intensifier=intensifier)
        conf = smac.optimize()
