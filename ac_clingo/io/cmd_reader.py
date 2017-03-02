import os
import logging
import glob
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, SUPPRESS


class CMDReader(object):

    """
        use argparse to parse command line options

        Attributes
        ----------
        logger : Logger oject
    """

    def __init__(self):
        """
        Constructor
        """
        self.logger = logging.getLogger("CMDReader")
        pass

    def read_cmd(self):
        """
            reads command line options

            Returns
            -------
                args_: parsed arguments; return of parse_args of ArgumentParser
        """

        parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
        req_opts = parser.add_argument_group("Required Options")
        req_opts.add_argument("--instance_dir", required=True,
                              help="directory with instances (not recursive")
   
        opt_opts = parser.add_argument_group("Optional Options")
        
        opt_opts.add_argument("--fn_suffix", default=".lp",
                              help="suffix of instance file names")
        opt_opts.add_argument("--cutoff", default=10, type=int,
                              help="running time cutoff [sec]")
        opt_opts.add_argument("--memlimit", default=2048, type=int,
                              help="memory limit")
        opt_opts.add_argument("--ac_budget", default=360,
                              help="configuration budget [sec]")
        opt_opts.add_argument("--run_obj", default="runtime",
                              choices=["runtime", "quality"],
                              help="run objective")

        opt_opts.add_argument("--binary", default="binaries/clingo",
                              help="target binary")
        opt_opts.add_argument("--pcs_file", default="pcs/params.pcs",
                              help="parameter configuration file")
        opt_opts.add_argument("--runsolver", default="binaries/runsolver",
                              help="runsolver binary")
        opt_opts.add_argument("--tae_class", default=None,
                              help="TAE class to individualize clingo calls -- has to inherit from smac.tae.execute_ta_run.ExecuteTARun")


        opt_opts.add_argument("--seed", default=12345, type=int,
                              help="random seed")
        opt_opts.add_argument("--verbose_level", default=logging.INFO,
                              choices=["INFO", "DEBUG"],
                              help="random seed")
        opt_opts.add_argument("--tae_args", default="{}",
                              help="Miscellaneous options for the TAE")
        

        args_, misc = parser.parse_known_args()
        self._check_args(args_)
        args_.tae_args=json.loads(args_.tae_args)

        # remove leading '-' in option names
        misc = dict((k.lstrip("-"), v.strip("'"))
                    for k, v in zip(misc[::2], misc[1::2]))

        misc["instances"] = self._find_files(dir_=args_.instance_dir, suffix_=args_.fn_suffix)
        misc["wallclock_limit"] = args_.ac_budget
        misc["cutoff_time"] = args_.cutoff
        misc["paramfile"] = args_.pcs_file
        misc["algo"] = ""
        misc["run_obj"] = args_.run_obj

        return args_, misc

    def _check_args(self, args_):
        """
            checks command line arguments
            (e.g., whether all given files exist)

            Parameters
            ----------
            args_: parsed arguments
                parsed command line arguments

            Raises
            ------
            ValueError
                in case of missing files or wrong configurations
        """

        pass
    
    def _find_files(self, dir_:str, suffix_:str):
        '''
            return list of files in dir_ with given suffix_ 
        '''
        insts = glob.glob(os.path.join(dir_, "*%s" %(suffix_)))
        self.logger.debug("#Instances: %d" %(len(insts)))
        return [[x] for x in insts]
        
