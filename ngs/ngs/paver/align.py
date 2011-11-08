#!/usr/bin/env python
# File: align.py
# Created: Thu Nov  3 22:06:30 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#

"""
Alignment related tasks
"""

@task
def align_reads():
    """Align reads to reference"""
    in_ext = "."
    infile = options.prefix
    options.cl.append([options.aligner.program, options.aligner.opts, options.aligner.args, options.aligner.out])
    options.prefix += ".sai"

@task
@needs("align_reads")
def align_reads_filt():
    options.cl.append([options.aligner.program, options.aligner.opts, options.aligner.args, options.aligner.out])
    print options.cl
    print "\n".join([" ".join(x) for x in options.cl])
    
