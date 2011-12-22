"""
variant calling programs
"""
import os

from paver.easy import *
from ngs.paver import run_cmd

##############################
## default options
##############################
options.variantcalling_default = Bunch(
    
    )


##############################
## Tasks
##############################
@task
@cmdopts([()])

