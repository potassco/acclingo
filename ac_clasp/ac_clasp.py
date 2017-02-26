import logging

from smac.facade.smac_facade import SMAC
from smac.scenario.scenario import Scenario

from ac_clasp.io.cmd_reader import CMDReader

__maintainer__='Marius Lindauer'
__license__ = "BSD"

class ACClasp(object):
    
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
        
        smac = SMAC(scenario=scen, rng=args_.seed)
        conf = smac.optimize()
