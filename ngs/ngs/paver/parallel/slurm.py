"""
Classes and function that work with slurm
"""
import sys
import os
import time
import drmaa
from paver.tasks import Task, task
from paver.easy import sh, path, options, environment

VERSION = "0.1.1"

class SbatchError(Exception):
    """Exception for Sbatch"""
    pass

class DrmaaError(Exception):
    """Exception for Drmaa"""
    pass


class Project:
    """Class that holds simple information about a project"""
    def __init__(self, project, email=None, sample=None, sample_dir=None):
        self.project_name = project
        self.email_address = email
        self.sample_name = sample
        self.sample_directory = sample_dir

    @property
    def sample(self):
        return "%s" % (self.sample_name)

    @property 
    def label(self):
        if self.sample_name is None:
            return ""
        else:
            return self.sample_name

    @property
    def prefix(self):
        return "%s" % (self.sample_name)

    @property
    def sample_dir(self):
        return "%s" % (self.sample_directory)
    
    @property 
    def sample_path(self):
        return "%s" % (path(self.sample_directory, self.label))

    @property
    def email(self):
        return self.email_address

    @property
    def project(self):
        return self.project_name

# def init(project, sample=None, sample_dir=path("."), email=None):
#     """Init function for slurm.py
#     Must be run by user to initialize drm"""
#     print "Initializing Drmtask instance variables..."
#     Drmtask.project = Project(project, email, sample, sample_dir)
#     Drmtask.is_initialized = True
#     Drmtask.drm = drmaa.Session()
#     Drmtask.drm.initialize()

sample= None
    
options(
    sample = None,
    )
    

# Wrapper for initialising project
# Ugly fix for checking if sample name present
# Since I am using the paver options it has to start with sample=
def initialise_project(project_name, sample_directory=path(".")):
    """Initialise project name"""
    Sbatch.project_name = project_name
    is_help = True in set([x == "-h" for x in sys.argv])
    if not is_help:
        try:
            sample = str(sys.argv[[x.startswith("sample=") for x in sys.argv].index(True)].split("=")[1])
        except:
            raise SbatchError("No sample defined")
        Sbatch.sample = sample
        Sbatch.sample_dir = path(sample_directory)
    Sbatch.is_initialised = True

##################################################
## drmtask
## task to be submitted to a distributed resource management system
##################################################
class Drmtask(Task):
    is_initialized = False
    project = None
    drm = None
    
    def __init__(self, func):
        Task.__init__(self, func)
        self.modules = ['bioinfo-tools']
        self.cmd = []
        # If this is first task initialize an class holder for the session
        if Drmtask.drm is None:
            Drmtask.drm = drmaa.Session()
            Drmtask.drm.initialize()
        self.jt = self.drm.createJobTemplate()

    def __del__(self):
        self.drm.deleteJobTemplate(self.jt)

    def add_job(self, cmd):
        self.cmd.append(cmd)

    def run_job(self, force=False):
        cmd_string = ""
        for cmd in self.cmd:
            if force:
                cmd.force = True
            cmd_string += str(cmd)
        self.jt.remoteCommand = cmd_string
        return self.jt.remoteCommand

    def drmaa_session(self):
        return self.drm

    def __str__(self):
        return "Project %s\nCommand \"%s\"" % (self.project, self.jt.remoteCommand)

def drmtask(func):
    """Initiates an drm task of function"""
    if isinstance(func, Drmtask):
        return func
    drmtask = Drmtask(func)
    return drmtask



class Sbatch(Task):
    __doc__ = "Sbatch class, subclass of paver Task"
    is_initialised = False
    sample = sample
    sample_dir = path(".")
    project_name = None
    _sbatch_kw = ['A', 'C', 't', 'p', 'n', 'e', 'o', 'D', 'J', 'mail_user', 'mail_type' ]
    _sbatch_vals = [None, None, '50:00:00', 'node', 8, None, None, None, None, None, None]

    def __init__(self, func):
        Task.__init__(self, func)
        self.sbatch_command = "sbatch"
        self.sbatch_opts = dict((x,y) for x,y in zip(self._sbatch_kw, self._sbatch_vals))
        self.sbatch_opts['A'] = self.project_name
        self.sbatch_opts['D'] = self.sample_dir / str(self.sample)
        self.sbatch_opts['J'] = self.__name__ + "." + str(self.sample)
        self.sbatch_opts['e'] = self.__name__ + ".stderr"
        self.sbatch_opts['o'] = self.__name__ + ".stdout"
        self.modules = ['bioinfo-tools']

    def __str__(self):
        output = ["Set options", "-" * 12]
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

        sbatch_file = "#!/bin/bash -l\n"
        sbatch_file += "#Project: " + self.sbatch_opts['A'] + "\n"
        for kw in self._sbatch_kw:
            if self.sbatch_opts[kw] != None:
                dash = '-'
                eq = ' '
                if len(kw) > 1:
                    dash = '--'
                    eq = '='
                if kw == 'mail_user':
                    if self.sbatch_opts['mail_type'] == None:
                        self.sbatch_opts['mail_type'] = "ALL"
                sbatch_file += " ".join(["#SBATCH", dash + str(kw.replace("_", "-")) + eq + str(self.sbatch_opts[kw])]) + "\n"
        # Add verbosity
        sbatch_file += "\n".join(["# Run info","echo \"Running on: $(hostname)\""])
        
        # Add modules
        sbatch_file += "\n\n# Load modules\n"
        sbatch_file += "\n".join(["module load " + x for x in self.modules])
        sbatch_file += "\n\n# Passed commands\n" + command + "\n\n"
        shfile = self.sbatch_opts['D'] / self.__name__ + ".sh"
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

