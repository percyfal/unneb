#!/usr/bin/env python
# File: gatk.py
# Created: Thu Nov  3 22:05:48 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#

from paver.easy import *
from ngs.paver.setup import setup_options

setup_options()
"""
GATK 
"""

@task
def IndelRealigner():
    config = gatk["IndelRealigner"]
    infile = [options.prefix + config["ext_in"][0],
              options.prefix + config["ext_in"][1]]
    outfile = options.prefix + config["ext_out"]
    gatk["cl"].append(" ".join([gatk["program"], "-T IndelRealigner", 
                                #[" ".join([config["opt_in"][i], infile[i]]) for i in range(0, len(infile))],
                                "-R", options.reference, 
                                "-o", outfile, config["opts"]]))

gatk = dict(
    home = "$GATK_HOME",
    program = "java -jar $GATK_HOME/GenomeAnalysisTK.jar",
    opts = "",
    cl = [],
    RealignerTargetCreator = dict(
        opts = "-l INFO",
        ext_out = "",
        ), 
    IndelRealigner = dict(
        opts = "",
        opt_in = ["-I", "-targetIntervals"],
        ext_in = [".bam", ".intervals"],
        ext_out = "",
        cl = IndelRealigner,
        ),
)

def realign():
    """Realign reads"""
    environment.call_task("paverpipe.gatk.IndelRealigner")
    return gatk["cl"]

## Some tasks
gatk["realign"] = realign

options(
    gatk = gatk
    )
