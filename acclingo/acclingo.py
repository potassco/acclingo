import inspect
import logging
import importlib.util

from smac.facade.smac_ac_facade import SMAC4AC
from smac.intensification.intensification import Intensifier
from smac.scenario.scenario import Scenario

from acclingo.io.cmd_reader import CMDReader
from acclingo.tae.clasp_tae import ClaspTAE

from acclingo import extract_configs

import re


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

        tae_args = {"ta_bin": args_.binary, "runsolver_bin": args_.runsolver, 
                "memlimit": args_.memlimit,
                "run_obj": args_.run_obj,
                "par_factor": 10,
                "misc": args_.tae_args}
        
        if args_.tae_class:
            spec = importlib.util.spec_from_file_location("tae",args_.tae_class)
            tae_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tae_module)
            tae_class = inspect.getmembers(tae_module, inspect.isclass)[0][1]

        else:
            tae_class = ClaspTAE
            
        smac = SMAC4AC(scenario=scen, rng=args_.seed, tae_runner=tae_class, tae_runner_kwargs=tae_args)

        conf = smac.optimize()

        print("\n")
        config = extract_configs.parse_options_from_folder(smac.output_dir, add_defaults=False, thread_separator=" || ", hydra=False)

        matches = re.findall(r"\|\|", config)

        if len(matches) == 2:
            print("Best configuration as a clingo readable command line (folder ; command line):\n")
            print(config.replace("||", ""))

        elif len(matches) > 2:
            print("Best configuration with || as thread separator (folder ; preprocess options || options for thread 1 || thread 2 || ... :\n")
            print(config)