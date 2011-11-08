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
