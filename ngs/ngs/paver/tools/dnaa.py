"""
dnaa toolkit
"""

import os
from paver.easy import *
from ngs.paver import run_cmd

##############################
## dnaa default options
##############################
options.dnaa_default = Bunch(

    )

##########
## Auto
##########
@task
@cmdopts
def auto():
    pass

##############################
## Tasks
##############################
