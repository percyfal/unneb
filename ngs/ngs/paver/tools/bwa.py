#!/usr/bin/env python
# File: bwa.py
# Created: Thu Nov  3 22:05:07 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
import os

from paver.easy import *
from ngs.paver import run_cmd

"""
Bwa program suite options
"""
## Tasks
@task
def align():
    """Run bwa aln bwa.opts options.ref infile > outfile"""
    prefix, ext = os.path.splitext(options.prefix)
    if not ext:
        ext = options.ext_fq
    infile = prefix + ext
    outfile = prefix + bwa["aln"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "aln", bwa["aln"]["opts"], options.index_loc["bwa"][options.ref][2], infile, ">", outfile]))
    bwa["cl"] = run_cmd(bwa["cl"], infile, outfile, options.run)

@task
def sampe():
    """Run bwa sampe. Takes as input a fastq file or a prefix."""
    prefix, ext = os.path.splitext(options.prefix)
    if not ext:
        ext = options.ext_fq
    fastq1  = prefix + options.read1_suffix + ext
    fastq2  = prefix + options.read2_suffix + ext
    saifile1 = prefix + options.read1_suffix + ".sai"
    saifile2 = prefix + options.read2_suffix + ".sai"
    out = options.prefix + bwa["sampe"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "sampe", bwa["sampe"]["opts"], options.index_loc["bwa"][options.ref][2], saifile1, saifile2, fastq1, fastq2, ">", out]))
    bwa["cl"] = run_cmd(bwa["cl"], saifile1, out)

@task
def samse():
    """Run bwa samse"""
    prefix, ext = os.path.splitext(options.prefix)
    if not ext:
        ext = options.ext_fq
    saifile = prefix + options.read_suffix + ".sai"
    fastq = prefix + options.read_suffix + options.ext_fq
    out = options.prefix + bwa["samse"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "samse", bwa["samse"]["opts"], options.index_loc["bwa"][options.ref][2], saifile, fastq, ">", out]))
    bwa["cl"] = run_cmd(bwa["cl"], saifile, out)

@task
def map_reads():
    """Collects bwa functions for mapping. Runs aligner and samse/sampe"""
    options.run = False
    if options.paired_end:
        environment.call_task("ngs.paver.tools.bwa.align")
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
