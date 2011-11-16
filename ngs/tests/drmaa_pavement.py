#! /usr/bin/python
#
# File: pavement.py
# Created: Mon Jun 20 11:41:04 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
# Description:
# Test pavement for ngs suite

from paver.easy import *
from paver.path import *

import os
import sys

# Add the library path
sys.path.insert(0,".")
# Add the development path
sys.path.insert(0, "/bubo/home/h1/perun/projects/dev/unneb.git/ngs")
# Load the ngs classes
from ngs.paver.slurm import *
from ngs.paver.wrappers import *

#init("a2010003")

# Add the top path
top = os.getcwd()

## Test the drmtask
@drmtask
def test1():
    print "test 1"
    print test1.drmaa_session()

@drmtask
def test2():
    print "test 2"
    print test1.drmaa_session()
    print test2.drmaa_session()

@sbatch
def test3():
    print "test 3"
    test3.sample = options.sample
    print "test3.sample: " + str(test3.sample)

@drmtask
def test4():
    print "test 4"
    prefix = "../test_data/test/test.single.bwa"
    cmd = sam_to_bam(prefix)
    print test4
    print cmd
    print "Forced? " + str(cmd.force)
    print str(cmd.run_task())
    test4.add_job(cmd)
    test4.add_job([cmd, cmd])

    print "%s" % (test4.run_job())
