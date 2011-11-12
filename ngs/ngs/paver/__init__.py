# File: __init__.py
# Created: Mon Oct 24 17:01:30 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
"""
Paver project tasks
"""
from paver.easy import *
from ngs.paver.tools.bwa import bwa

def threads():
    return options.threads

def _uptodate(infile, outfile):
    pass

## How to check dependencies?
def sbatch(command, label=None, capture=False, ignore_error=False, cwd=None):
    """Runs a command, but launch it through sbatch script submission"""
    if label is None:
        sbatch_file = "tmp.sh"
    else:
        sbatch_file = path(label + ".sh")
        fp = open(sbatch_file)
    ## Print file to stdout
    if tasks.environment.dry_run:
        pass
    sh("sbatch " + sbatch_file, capture, ignore_error, cwd)

## Set a function pointer to sh or sbatch or drmaa or whatever...
options(config = dict(sh = sh))

## Workflow
## 1. qc reads
## 2. map reads
## 3. realign reads
## 4. mark duplicates
## 5. recalibrate reads
## 6. genotyping
## 7. evaluation of genotyping

## Idea: 
## - keep track of current prefix and file type with pointers in options
## - perform command and update pointers
## - do atomic operations

## Setup options to use bwa
## options.aligner = bwa


from paver.easy import *
from ngs.paver.tools.samtools import *

"""
Put description here
"""

## Setup databases
## Read from galaxy if available
db = dict(
    reference = "reference.fa",
    dbsnp = None,
    )

def setup_options():
## Global-like options
## Standard setup - change in module files
    options(
        aligner = None,
        prefix = None,
        cl = [],
        force = False,
        threads = 8,
        db = db,
        paired_end=True,
        read1_suffix = "_1",
        read2_suffix = "_2",
        )
