#!/usr/bin/env python
# File: pipelines.py
# Created: Thu Nov  3 23:15:19 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
from paver.easy import *
from paver.tasks import *
from ngs.paver.tools.gatk import *
from ngs.paver.tools.samtools import *

"""
Make pipelines
"""

@task
def exome_pipeline():
    print "running exome_pipeline"
    for sample in options.samples:
        print "Collecting info for sample " + sample
        options.prefix = sample
        options.aligner["map_reads"]()
        options.gatk["realign"]()
    sh("\n".join(options.aligner["cl"]))
    sh("\n".join(options.gatk["cl"]))
