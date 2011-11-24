"""
samtools programs
"""
import os
from paver.easy import *
from ngs.paver import run_cmd

##############################
## samtools default options
##############################
options.samtools_default = Bunch(
    program = "samtools",
    opts = "",
    view = dict(
        opts = "-bS",
        ext_out = None,
        ),
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

##############################
## Tasks
##############################
@task
@cmdopts([()])
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
