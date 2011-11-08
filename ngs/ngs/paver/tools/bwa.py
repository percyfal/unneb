#!/usr/bin/env python
# File: bwa.py
# Created: Thu Nov  3 22:05:07 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#

from paver.easy import *
from paverpipe.setup import *

## Need to run this in every file?!?
setup_options()

"""
Bwa program suite options
"""
## Functions
@task
def bwa_aln():
    if options.prefix is None:
        return
    infile = options.prefix + ".fq"
    out = options.prefix + bwa["aln"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "aln", bwa["aln"]["opts"], options.db["reference"], infile, ">", out]))

@task
def sampe():
    if options.prefix is None:
        return
    infile1 = options.prefix + options.read1_suffix + ".sai"
    infile2 = options.prefix + options.read2_suffix + ".sai"
    fqfile1 = options.prefix + options.read1_suffix + ".fq"
    fqfile2 = options.prefix + options.read2_suffix + ".fq"
    out = options.prefix + bwa["sampe"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "sampe", bwa["sampe"]["opts"], options.db["reference"], infile1, infile2, fqfile1, fqfile2, ">", out]))

@task
def map_reads():
    """Collects bwa functions for mapping"""
    environment.call_task("paverpipe.bwa.bwa_aln")
    if options.paired_end:
        environment.call_task("paverpipe.bwa.sampe")
    return bwa["cl"]

## For some reason need to set this as a dictionary
## The Bunch class removes function definitions?!?

bwa = dict(
    program = "bwa",
    opts = "",
    cl = [],
    map_reads = map_reads,
    aln = dict(
        opts = "-k 1 -n 3 -t " + str(options.threads),
        ext_out = ".sai",
        cl = bwa_aln,
        ),
    samse = dict(
        opts = "",
        ext_out = ".sam",
        ),
    sampe = dict(
        opts = "",
        ext_out = ".sam",
        cl = sampe,
        ),
    )

## Setup options to use bwa
## options.aligner = bwa
