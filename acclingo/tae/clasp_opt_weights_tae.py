import sys
import os
import random
import re
from subprocess import Popen, PIPE

from smac.tae.execute_ta_run import StatusType, ExecuteTARun
from smac.stats.stats import Stats
from smac.runhistory.runhistory import RunHistory
from smac.utils.constants import MAXINT

from tempfile import NamedTemporaryFile

__author__ = "Marius Lindauer"
__license__ = "3-clause BSD"

float_regex = '[+-]?\d+(?:\.\d+)?(?:[eE][+-]\d+)?'

class ClaspOptTAE(ExecuteTARun):

    
    def __init__(self, ta_bin:str, runsolver_bin:str,
                 ta=None, 
                 memlimit:int=2048,
                 stats:Stats=None, runhistory:RunHistory=None, 
                 run_obj:str="runtime",
                 par_factor=10,
                 cost_for_crash: float=float(MAXINT),
                 abort_on_first_run_crash: bool=True,
                 misc=dict()
                 ):
        """
            executes a target algorithm run with a given configuration
            on a given instance and some resource limitations
            Uses the original SMAC/PILS format (SMAC < v2.10)
    
            Attributes
            ----------
            ta_bin: str
                clasp binary
            runsolver_bin: str
                runsolver binary
            memlimit: int
                memory limit in GB
            stats: Stats
                run statistics object from SMAC
            runhistory: RunHistory
                runhistory object from SMAC
            run_obj: str
                run objective (runtime or quality)
            par_factor: int
                penalized average runtime factor

            misc: Can contain the following key:value pairs
                    "solution": float
                    "time"    : float
                    "penalty" : float
                    "normalized": bool
        """
        super().__init__(ta=ta,
                         stats=stats, runhistory=runhistory, 
                         run_obj=run_obj,
                         par_factor=par_factor,
                         cost_for_crash=cost_for_crash,
                         abort_on_first_run_crash=abort_on_first_run_crash)

        self.ta_bin = ta_bin
        self.runsolver_bin = runsolver_bin
        self.memlimit = memlimit
        self.par_factor = par_factor
        self.best_known=dict();
        self.solution_weight = 0.5
        self.time_weight = 0.5
        self.unsolved_penalty = 1
        self.normalized = False

        if "best_known" in misc:
            with open(misc["best_known"]) as f:
                for line in f.readlines():
                   self.best_known[line.split(',')[0].strip()]=int(line.split(',')[1].strip())

        if "solution" in misc:
            self.solution_weight = float(misc["solution"])

        if "time" in misc:
            self.time_weight = float(misc["time"])
        
        if "penalty" in misc:
            self.unsolved_penalty = float(misc["penalty"])

        if "normalized" in misc:
            self.normalized = misc["normalized"]

        self.encoding = ""

        self.mode = "clasp"

        if "encoding" in misc:
            self.encoding = misc["encoding"]

        if "mode" in misc:
            self.mode = misc["mode"]
        
    def run(self, config, instance,
            cutoff,
            seed=12345,
            budget=None,
            instance_specific="0"
            ):
        """
            runs target algorithm <self.ta> with configuration <config> on
            instance <instance> with instance specifics <specifics>
            for at most <cutoff> seconds and random seed <seed>

            Parameters
            ----------
                config : dictionary (or similar)
                    dictionary param -> value
                instance : string
                    problem instance
                cutoff : double
                    runtime cutoff
                seed : int
                    random seed
                instance_specific: str
                    instance specific information (e.g., domain file or solution)
            Returns
            -------
                status: enum of StatusType (int)
                    {SUCCESS, TIMEOUT, CRASHED, ABORT}
                cost: float
                    cost/regret/quality/runtime (float) (None, if not returned by TA)
                runtime: float
                    runtime (None if not returned by TA)
                additional_info: dict
                    all further additional run information
        """

        
        if not instance.endswith(".gz"):
            cmd = "{bin} {encoding} {instance} --seed {seed} ".format(bin=self.ta_bin, encoding=self.encoding, instance=instance, seed=seed)       
        else:
            cmd = "bash -c 'zcat {instance} | {bin} {encoding} --seed {seed} ".format(instance=instance, bin=self.ta_bin, encoding=self.encoding, seed=seed )       
        
        params = []
        for name in config:
            value = config[name]
            if value is None:
                continue
            params.append(name)
            params.append(value)
        thread_to_params, thread_to_solver, params_to_tags = self.parse_parameters(params)
        
        thread_count = int(max(thread_to_params.keys()))
        config_file = "config_file.tmp"
        with open(config_file, "w") as cfile:
            for t, p_list in thread_to_params.items():
                if t == 0: # global params
                    for p in p_list:
                            cmd += " " + p
                else:
                    new_p_list = []
                    thread_config = "auto"
                    for p in p_list:
                        if "--configuration" in p:
                            thread_config = p.split("=")[1]
                        else:
                            new_p_list.append(p)

                    cfile.write("{}({}): {}\n".format(t, thread_config, " ".join(new_p_list)))
        
        cmd += " --mode={}".format(self.mode)
        cmd += " --configuration={}".format(config_file)
        cmd += " --quiet=2 --stats"
        cmd += " --parallel-mode={}".format(thread_count)
        
        if instance.endswith(".gz"):
           cmd += "'"
         
        # runsolver
        random_id = random.randint(0,2**20)
        tmp_dir = "."
        watcher_file = NamedTemporaryFile(suffix=".log", prefix="watcher-%d-" %(random_id), dir=tmp_dir, delete=False)
        watcher_file.close()
        watcher_file = watcher_file.name
        solver_file = NamedTemporaryFile(suffix=".log", prefix="solver-%d-" %(random_id), dir=tmp_dir, delete=False)
        solver_file.close()
        solver_file = solver_file.name
        
        cmd = "setsid %s -C %d -M %d -w %s -o %s %s" %(self.runsolver_bin, cutoff, self.memlimit, watcher_file, solver_file, cmd) 

        self.logger.debug("Calling: %s" % (cmd))
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout_, stderr_ = p.communicate()

        self.logger.debug("Stdout: %s" % (stdout_))
        self.logger.debug("Stderr: %s" % (stderr_))
        
        ta_status_rs, ta_runtime, ta_exit_code = self.read_runsolver_output(watcher_file)

        ta_status, ta_quality, clingo_runtime = self.parse_output(fn=solver_file, exit_code=ta_exit_code)
                
        if ta_runtime is None:
            ta_runtime = clingo_runtime
        
        if not ta_status:
            ta_status = ta_status_rs

        if ta_status in [StatusType.CRASHED, StatusType.ABORT]:
            self.logger.warn(
                "Target algorithm crashed. Last 5 lines of stdout and stderr")
            self.logger.warn("\n".join(stdout_.split("\n")[-5:]))
            self.logger.warn("\n".join(stderr_.split("\n")[-5:]))
        else:
            os.remove(watcher_file)
            os.remove(solver_file)

        if ta_quality == None or ta_runtime == None:
            cost = self.par_factor * self.unsolved_penalty
        else:
            
            best = self.best_known[os.path.splitext(os.path.basename(instance))[0]]
            if best == 0: 
                best = 1
            
            #normalized or not, it only affects how the solution quality is calculated
            if not self.normalized:
                # not normalized
                solution_quality = float(ta_quality)/float(best)
            else:
                # normalized
                solution_quality = 1 - (float(best)/float(ta_quality)) if ta_quality != 0 else 0

            runtime_quality = float(ta_runtime)/float(cutoff)
  
            cost = min(float(self.par_factor * self.unsolved_penalty), self.time_weight * runtime_quality + self.solution_weight * solution_quality)
            
        return ta_status, cost, ta_runtime, {}
    
    def parse_parameters(self, params,prefix="--",separator="="):
        ''' parse parameters; syntax: -@[Thread]:{[component]:|S|F}*[param] [value]#
            globals parameters at thread-id 0
            Args:
                parameter : parameter list
                prefix: of build parameters, e.g. "--" (can be overwritten by parameter file)
                separator: of build parameters, e.g. "=" for --t=8 or " " for --t 8
            Returns:
                thread_to_params:    thread-id to list of parameters (0 -> global parameters)
                thread_to_solver:    thread-id to solver binary
                params_to_tags:      parameter name to smac like tags 
        '''     
        params_to_tags = {}
        thread_to_params = {}
        thread_to_solver = {}
        parallel_thread_list = []
        threadIndex = 0
        while params:
            localParam = {}
            local_prefix = prefix
            local_separator = separator
            value = ""
            option = ""
            backupparams = []
            while(params != []):
                head = params.pop(0)
                value = str(params.pop(0)).replace("'","")
                if not "solver" in head: 
                    value = value.replace("__",",")
                value_is_int = False
                try:
                    value = int(value)
                    value = str(value)
                    value_is_int = True
                except ValueError:
                    value_is_int = False
                if not value_is_int:
                    try:
                        value = round(float(value),4) # some solvers have problems with E notation, e.g. 6,37E8
                        value = str(value)
                    except ValueError:
                        pass
                if (head.startswith("@"+str(threadIndex))):
                    option = head[3:]
                    optionSplits = option.split(":")
                    parameterName = optionSplits.pop() # last item in list = parameterName
                    if (parameterName == "solver"): # special filter for solver binary path
                        thread_to_solver[threadIndex] = value
                        continue
                    if (parameterName == "prefix"):
                        local_prefix = value
                        continue
                    if (parameterName == "separator"):
                        if value == "W": # parameter with only whitespaces is not allowed by SMAC
                            value = " "
                        local_separator = value
                        continue
                    if len(optionSplits) > 0:  # composed multi parameter
                        skip = False
                        flag = False
                        component = -1
                        if (params_to_tags.get(parameterName) == None):
                            params_to_tags[parameterName] = set()
                        for opt in optionSplits:
                            if (opt == "F"): # Flag
                                flag = True
                                continue
                            if (opt == "S"): # skip
                                skip = True
                                continue
                            try:
                                component = int(opt)
                            except ValueError:
                                params_to_tags[parameterName].add(opt)
                        if (skip == True):
                            continue
                        if (flag == True and value == "no"):
                            continue # won't be passed to solver
                        if (flag == True and value == "yes"):
                            value = ""
                        if (component != -1):
                            if (localParam.get(parameterName) == None):
                                localParam[parameterName] = {}
                            localParam[parameterName][component] = value
                        else:
                            localParam[parameterName] = value
                        tags = params_to_tags[parameterName]
                        if "ITERATIVE" in tags:
                            parallel_thread_list.append(threadIndex)
                    else:
                        localParam[option] = value
                else:
                    backupparams.append(head) # keep unhandled
                    backupparams.append(value)
            params = backupparams
            if not (len(localParam) == 0 and threadIndex > 0):
                thread_to_params[threadIndex] = self.__dic_to_flat_list(localParam, local_prefix, local_separator)
            threadIndex += 1
        #print(thread_to_params)
        self.__join_multi_threading_solver(thread_to_params, thread_to_solver, params_to_tags, parallel_thread_list)
        return thread_to_params, thread_to_solver, params_to_tags
    
    def __join_multi_threading_solver(self, thread_to_params, thread_to_solver, params_to_tags, parallel_thread_list):
        '''
            join all multi threading solvers and increase their thread argument
            Args:
                thread_to_params:    thread-id to list of parameters (0 -> global parameters)
                thread_to_solver:    thread-id to solver binary
                params_to_tags:      parameter name to smac like tags
                parallel_thread_list: list of threadindexes of parallel solvers 
        '''
        handled_solvers = []
        for parallel_thread in parallel_thread_list:
            try:    
                solver = thread_to_solver[parallel_thread]
            except KeyError:
                continue
            params = thread_to_params[parallel_thread]
            dup_dict = dict(map(lambda t, x: (t,x==solver), thread_to_solver.items()))
            dups = 0
            index = 1
            # remove all duplicates
            for thread, dup in dup_dict.items():
                if dup == True:
                    dups += 1
                    thread_to_solver.pop(thread)
                    thread_to_params.pop(thread)
                    index += 1
                    
            # modify configuration, resp. threading parameter
            for par_index in range(0, len(params), 2): # pair (parameter_name, value)
                parameter_name = params[par_index]
                value = params[par_index+1]
                tags_minus = params_to_tags.get(parameter_name[1:]) # parameter has already prefix attached :-(
                tags_minus_minus = params_to_tags.get("--"+parameter_name[2:])
                if (tags_minus and "ITERATIVE" in tags_minus) or (tags_minus_minus and "ITERATIVE" in tags_minus_minus): 
                    #TODO: if a parameter name is used more than once (can happen by using several solver),
                    #      the parameter tag mapping is not unique -> not proper handled right now
                    value = dups # assumption: number of threads is an integer
                    params[par_index+1] = str(value)
            handled_solvers.append(solver)
            thread_to_solver[parallel_thread] = solver
            thread_to_params[parallel_thread] = params
        
    def __sorted_dict_values(self, adict):
        keys = list(adict.keys())
        keys.sort()
        return map(adict.get, keys)
    
    def __dic_to_flat_list(self, adict, prefix, separator):
        '''
            convert dictionary to flat parameter list
            Args:
                adict: dictionary : head -> value
                prefix: prefix of parameter head, e.g. "--"
        '''
        allP = []
        for k,v in adict.items():
            if (type(v) is dict):
                vsort = self.__sorted_dict_values(v)
                sortedvalues = ",".join(vsort)
                if separator == " ":
                    allP.append(prefix+k)
                    allP.append(sortedvalues)
                else:
                    allP.append(prefix+k+separator+sortedvalues )
            else:
                if (type(v) is list):
                    allP.extend(v)
                else:
                    if (v == ""):   # flag handling
                        allP.append(prefix+k)
                    else:
                        if separator == " ":
                            allP.append(prefix+k)
                            allP.append(v)
                        else:
                            allP.append(prefix+k+separator+v)
                            
        return allP
    
    def parse_output(self, fn, exit_code):
        '''
        Parse a results file to extract the run's status (SUCCESS/CRASHED/etc) and other optional results.
    
        Args:
            fn: a name to the file containing clasp stdout.
            exit_code : exit code of target algorithm
        Returns:
            ta_status, ta_quality 
        '''
        self.logger.debug("reading solver results from %s" % (fn))
        with open(fn) as fp:
            data = str(fp.read())
        
        ta_status = None
        ta_quality = None
        
        match=None
        
        for match in re.finditer(r"Optimization: ([0-9]+)", data):
            pass
        
        if match:
            ta_quality = int(match.group(1))
        
        if re.search('UNSATISFIABLE', data):
            ta_status = StatusType.SUCCESS
        elif re.search('SATISFIABLE', data):
            ta_status = StatusType.SUCCESS
        elif re.search('OPTIMUM FOUND', data):
            ta_status = StatusType.SUCCESS
        elif re.search('s UNKNOWN', data):
            ta_status = StatusType.TIMEOUT
        elif re.search('INDETERMINATE', data):
            ta_status = StatusType.TIMEOUT
        
        clingo_runtime = re.search(r"Time[ ]*:[ ]*(\d+\.\d+)s", data).group(1)
        
        return ta_status, ta_quality, float(clingo_runtime) 

    def read_runsolver_output(self, watcher_fn: str):
        '''
            reads self._watcher_file, 
            extracts runtime
            and returns if memout or timeout found
            
            Arguments
            ---------
            watcher_fn: str
                watcher output file of runsolver
            
            Returns
            -------
            ta_status, ta_runtime, ta_exit_code
            
        ''' 
        
        ta_status = StatusType.CRASHED       
        ta_runtime = None
        ta_exit_code = None
        
        self.logger.debug("Reading runsolver output from %s" % (watcher_fn))
        with open(watcher_fn) as fp:
            data = str(fp.read())

        if (re.search('runsolver_max_cpu_time_exceeded', data) or re.search('Maximum CPU time exceeded', data)):
            ta_status = StatusType.TIMEOUT

        if (re.search('runsolver_max_memory_limit_exceeded', data) or re.search('Maximum VSize exceeded', data)):
            ta_status = StatusType.TIMEOUT
            ta_misc = "memory limit was exceeded"
           
        cpu_pattern1 = re.compile('^runsolver_cputime: (%s)' % (float_regex), re.MULTILINE)
        cpu_match1 = re.search(cpu_pattern1, data)
            
        cpu_pattern2 = re.compile('^CPU time \\(s\\): (%s)' % (float_regex), re.MULTILINE)
        cpu_match2 = re.search(cpu_pattern2, data)

        if (cpu_match1):
            ta_runtime = float(cpu_match1.group(1))
        if (cpu_match2):
            ta_runtime = float(cpu_match2.group(1))

        exitcode_pattern = re.compile('Child status: ([0-9]+)')
        exitcode_match = re.search(exitcode_pattern, data)

        if (exitcode_match):
            ta_exit_code = int(exitcode_match.group(1))
            
        return ta_status, ta_runtime, ta_exit_code
