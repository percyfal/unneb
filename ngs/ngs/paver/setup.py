#!/usr/bin/env python
# File: setup.py
# Created: Fri Nov  4 13:54:51 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#

from paver.easy import *
from paverpipe.samtools import *

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
