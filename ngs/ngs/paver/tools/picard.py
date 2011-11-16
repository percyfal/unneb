#!/usr/bin/env python
# File: picard.py
# Created: Sun Nov 13 20:59:26 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#

"""
picard program suite options and tasks
"""
import os

from paver.easy import *
from ngs.paver import run_cmd
from bcbio.utils import curdir_tmpdir

def picard_run(program):
    cl = " ".join(["java -jar", os.path.join(picard["path"], program + ".jar")])
    for k,v in picard[program]["opts"].items():
        if v != "":
            cl += " %s=%s" % (k,v)
    return cl

## Tasks
@task
def FastqToSam():
    """Run java -jar FastqToSam. One or two input files."""
    outfile = "%s.bam" % (os.path.basename(options.fastq1)[0])
    picard["FastqToSam"]["opts"]["FASTQ"]= options.fastq1
    picard["FastqToSam"]["opts"]["OUTPUT"]= outfile
    picard["FastqToSam"]["opts"]["SAMPLE_NAME"]= os.path.splitext(options.fastq1)[0]
    if not options.fastq2 is None:
        picard["FastqToSam"]["opts"]["FASTQ2"]= options.fastq2
    picard["cl"].append(picard_run("FastqToSam"))
    picard["cl"] = run_cmd(picard["cl"], options.fastq1, outfile)
                                                           

@task
def MergeBamAlignment():
    pass

@task
def SortSam():
    pass

@task
def MergeSamFiles():
    pass

## Picard options
picard = dict(
    path = "/bubo/sw/apps/bioinfo/picard/1.41",
    cl = [],
    FastqToSam = dict(
        opts = dict(QUALITY_FORMAT="Illumina",
                    READ_GROUP_NAME="",
                    SAMPLE_NAME = "",
                    PLATFORM_UNIT = "",
                    PLATFORM = "",
                    TMP_DIR = "tmp",
                    )
        )
    )
## Setup options to use picard
options.picard = picard
