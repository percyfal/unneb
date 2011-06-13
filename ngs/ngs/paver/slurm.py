"""
Classes and function that work with slurm
"""
import sys
import os
from paver.tasks import Task, task
from paver.easy import sh, path, options, environment

VERSION = "0.1.0"

class SbatchError(Exception):
    """Exception for Sbatch"""
    pass

# Add sample option to paver command line
# TODO: make optional for user?
options(
    sample = None,
    )

# Wrapper for initialising project
# Ugly fix for checking if sample name present
# Since I am using the paver options it has to start with sample=
def initialise_project(project_name, sample_dir=path(".")):
    """Initialise project name for use with sbatch objects"""
    Sbatch.sbatch_opts['A'] = project_name
    is_help = True in set([x == "-h" for x in sys.argv])
    if not is_help:
        try:
            sample = str(sys.argv[[x.startswith("sample=") for x in sys.argv].index(True)].split("=")[1])
        except:
            raise SbatchError("No sample defined")
        Sbatch.sbatch_opts['D'] = path(sample_dir) / sample
    Sbatch.is_initialised = True
    
class Sbatch(Task):
    __doc__ = "Sbatch class, subclass of paver Task"
    is_initialised = False
    _sbatch_kw = ['A', 'C', 't', 'p', 'n', 'e', 'o', 'D', 'J']
    _sbatch_vals = [None, 'fat', '50:00:00', 'node', 8, None, None, None, None]
    sbatch_opts = dict((x,y) for x,y in zip(_sbatch_kw, _sbatch_vals))

    def __init__(self, func):
        Task.__init__(self, func)
        self.sbatch_command = "sbatch"
        self.sbatch_opts['J'] = self.__name__
        self.sbatch_opts['e'] = self.__name__ + ".stderr"
        self.sbatch_opts['o'] = self.__name__ + ".stdout"
        self.modules = ['bioinfo-tools']

    def __str__(self):
        output = ["Set options", "-" * 30]
        for k in self._sbatch_kw:
            output.append("  " + " : ".join([str(k), str(self.sbatch_opts[k])]))
        return "\n".join(output)

    # TODO: fix formatting
    def run_sbatch(self, command, command_line=False, **kw):
        if not self.is_initialised:
            raise SbatchError("Sbatch project name not set: please set default project name using the \"initialise_project\" function")
        keys = sorted(kw.keys())
        for k in keys:
            self.sbatch_opts[k] = kw[k]

        # Run sbatch from command line
        # Has to be single core job
        if command_line:
            sbatch_command = self.sbatch_command
            self.sbatch_opts['n'] = 1
            self.sbatch_opts['p'] = None
            self.sbatch_opts['C'] = None
            
            for kw in self._sbatch_kw:
                if self.sbatch_opts[kw] != None:
                    sbatch_command += " ".join([" -" + str(kw), str(self.sbatch_opts[kw]) ] )
            cmd = " ".join([sbatch_command, command])
            sh(cmd)
        # Run sbatch script
        else:
            sbatch_file = "#!/bin/bash -l\n"
            sbatch_file += "#Project: " + self.sbatch_opts['A'] + "\n"
            for kw in self._sbatch_kw:
                if self.sbatch_opts[kw] != None:
                    sbatch_file += " ".join(["#SBATCH", "-" + str(kw), str(self.sbatch_opts[kw])]) + "\n"

            # Add verbosity
            sbatch_file += "\n".join(["# Run info","echo \"Running on: $(hostname)\""])

            # Add modules
            sbatch_file += "\n\n# Load modules\n"
            sbatch_file += "\n".join(["module load " + x for x in self.modules])
            sbatch_file += "\n\n# Passed commands\n" + command + "\n\n"
            shfile = self.sbatch_opts['D'] / self.sbatch_opts['J'] + ".sh"
            fp = open(shfile, 'w')
            fp.write(sbatch_file)
            fp.close()
            cmd = " ".join([self.sbatch_command, shfile])
            sh(cmd)

def sbatch(func):
    """Creates an sbatch task of function"""
    if isinstance(func, Sbatch):
        return func
    sbatch = Sbatch(func)
    return sbatch
