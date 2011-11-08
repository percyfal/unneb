#!/usr/bin/env python
# File: samtools.py
# Created: Thu Nov  3 23:08:23 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#

"""
samtools programs
"""
from paver.easy import *

samtools = dict(
    program = "samtools",
    opts = "",
    view = dict(
        opts = "-bS",
        ext_out = None,
        ),
    )

## Functions
@task
def sam2bam():
    if options.prefix is None:
        return
    samfile = options.prefix + ".sam"
    out = options.prefix + samtools["sam2bam"]["ext_out"]
    samtools["cl"].append(" ".join([samtools["program"], "view", 
                                   samtools["sam2bam"]["opts"], samfile, ">", out]))
    sh(samtools["cl"])

@needs("sam2bam")
@task
def samsort():
    if options.prefix is None:
        return
    bamfile = options.prefix + ".bam"
    out = options.prefix + samtools["samsort"]["ext_out"]
    samtools["cl"].append(" ".join([samtools["program"], "sort", 
                                   bamfile, out]))
    sh(samtools["cl"])
    
samtools = dict(
    program = "samtools",
    opts = "",
    cl = [],
    sam2bam = dict(
        opts = "-b",
        ext_out = ".bam",
        cl = sam2bam,
        ),
    samsort = dict(
        opts = "",
        ext_out = ".sort.bam",
        cl = samsort,
        ),
    )
