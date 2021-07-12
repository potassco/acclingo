from argparse import ArgumentParser 
import json
import pickle

INCUMBENT = "incumbent"

FLAG = "F"
SKIP = "S"
SPECIAL = -1

def read_traj_aclib(file_path):
    with open(file_path, "r") as f:
        for line in f: pass

    options_list = json.loads(line)[INCUMBENT]
    options_list = [opt.replace("\'", "") for opt in options_list]

    return options_list

def read_hydra_pkl(file_path):
    with open(file_path, "rb") as f:
        configs = pickle.load(f)

    options_lists = []
    for c in configs:
        options_lists.append(list_from_configspace(c))

    return options_lists

def list_from_configspace(config):

    config_list = []
    for c in config:
        c_val = config.get(c)
        config_str = c + "=" + str(c_val)
        config_list.append(config_str)

    return config_list

def get_options_traj(file_path, thread_separator=" ", program=None):
    
    options_list = read_traj_aclib(file_path)
    options = parse_options(options_list, thread_separator=thread_separator)
    
    if program is not None:
        test_options(options, program)

    return options

def get_options_hydra(file_path, thread_separator=" // ", program=None):

    options_lists = read_hydra_pkl(file_path)

    # read all options lists
    # grab first one as main
    # append all but the "general" options from the other ones
    # get first one using // separator
    # get rest by using that separator and doing split
    # append rest to first

    main_config = parse_options(options_lists[0], thread_separator=" // ")

    for config in options_lists[1:]:
        options = parse_options(config, thread_separator=" // ")
        options = options.split("//")

        main_config = main_config + " // ".join(options[1:])

    if program is not None:
        test_options(main_config, program)

    return main_config.replace(" // ", thread_separator)

def parse_options(options, thread_separator=" "):
    arguments = {}
    
    for opt in options:
        options, val = opt.split("=")
     
        # take first argument out(useless), store name and then take name out
        thread = options.split(":")[0].replace("@","")
        options = options.split(":")[1:]
        name = options[-1]
        options = options[:-1]

        if thread not in arguments:
            arguments[thread] = {}
        
        if len(options) > 0 and options[0] == SKIP:
            continue

        if name not in arguments[thread]:
            arguments[thread][name] = {}

        if len(options) > 0:
            # first argument is either a flag a skip a number or a "No"
            if options[0] == FLAG:
                # flags with value no will be skipped, yes leads to no arguments
                if val == "no":
                    arguments[thread][name][SPECIAL] = SKIP

            elif options[0].lower() == u"no":
                arguments[thread][name][1] = val
                arguments[thread][name][SPECIAL] = "no"
            else:
                # assign the value to the position given by the option
                arguments[thread][name][int(options[0])] = val            

        else:
            # if there are no options
            arguments[thread][name][1] = val
    
    arg_str = ""
    
    for thread in sorted(arguments.keys()):
        thread_args = arguments[thread]
        for name, args in thread_args.items():
            pre_arg_str=argstostring(name, args)
            #deal with special cases
            if "no-vsids-progress" in pre_arg_str:
                pre_arg_str = pre_arg_str.replace("--no-vsids-progress", "--vsids-progress=no")
            if "dom-heur" in pre_arg_str:
                # this is for asprin's python parameter since python params use a space to spread multi args instead of ,
                pre_arg_str = pre_arg_str.replace(",", " ")

            arg_str += pre_arg_str + " "

        # add separator between thread arguments    
        arg_str += thread_separator

    return arg_str.replace("  ", " ") # dont have 2 spaces in a row for no reason

def argstostring(name, args):

    # deal with special solver argument
    if name == "solver":
        return ""
    
    # dealing with special options in the options
    if SPECIAL in args:
        if args[SPECIAL] == SKIP:
            return ""
        if args[SPECIAL] == "no":
            if args[1] == u"no":
                return "--no-" + name
            else:
                # for eq=0 ?? 
                return "--" + name + "=" + ",".join([args[pos] for pos in sorted(args) if pos > 0])

    elif len(args) > 0:
        return "--" + name + "=" + ",".join([args[pos] for pos in sorted(args) if pos != SPECIAL])
    
    else:
        # flags
        return "--" + name
