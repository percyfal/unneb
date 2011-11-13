#!/usr/bin/env python
# File: bwa.py
# Created: Thu Nov  3 22:05:07 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
from paver.easy import *
from ngs.paver import run_cmd

"""
Bwa program suite options
"""
## Functions
@task
def align():
    """Run bwa aln bwa.opts options.ref options.prefix.fqext > options.prefix.ext_out"""
    if options.prefix is None:
        return
    infile = options.prefix + options.read_suffix + options.ext_fq
    out = options.prefix + options.read_suffix + bwa["aln"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "aln", bwa["aln"]["opts"], options.index_loc["bwa"][options.ref][2], infile, ">", out]))
    bwa["cl"] = run_cmd(bwa["cl"])

@task
def sampe():
    """Run bwa sampe"""
    if options.prefix is None:
        return
    infile1 = options.prefix + options.read1_suffix + ".sai"
    infile2 = options.prefix + options.read2_suffix + ".sai"
    fqfile1 = options.prefix + options.read1_suffix + options.ext_fq
    fqfile2 = options.prefix + options.read2_suffix + options.ext_fq
    out = options.prefix + bwa["sampe"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "sampe", bwa["sampe"]["opts"], options.index_loc["bwa"][options.ref][2], infile1, infile2, fqfile1, fqfile2, ">", out]))
    bwa["cl"] = run_cmd(bwa["cl"])

@task
def samse():
    """Run bwa samse"""
    if options.prefix is None:
        return
    infile = options.prefix + options.read_suffix + ".sai"
    fqfile = options.prefix + options.read_suffix + options.ext_fq
    out = options.prefix + bwa["samse"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "samse", bwa["samse"]["opts"], options.index_loc["bwa"][options.ref][2], infile, fqfile, ">", out]))
    bwa["cl"] = run_cmd(bwa["cl"])

@task
def map_reads():
    """Collects bwa functions for mapping. Runs aligner and samse/sampe"""
    options.run = False
    if options.paired_end:
        options.read_suffix = options.read1_suffix
        environment.call_task("ngs.paver.tools.bwa.align")
        options.read_suffix = options.read2_suffix
        environment.call_task("ngs.paver.tools.bwa.align")
        environment.call_task("ngs.paver.tools.bwa.sampe")
    options.run = True
    bwa["cl"] = run_cmd(bwa["cl"])

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
        ),
    samse = dict(
        opts = "",
        ext_out = ".sam",
        ),
    sampe = dict(
        opts = "",
        ext_out = ".sam",
        ),
    )

## Setup options to use bwa
options.aligner = bwa

##################################################
## Tasks to look at bwa
##################################################
@task
def bwa_config():
    """List bwa configuration"""
    print options.aligner
