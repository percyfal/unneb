#! /usr/bin/python
#
# File: test_pavement.py
# Created: Tue Jun 21 12:56:01 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
# Description:
# Test suite for pavement 

import os
import sys
import os.path
import unittest

# Add the library path
exe_path=os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path, "..")))

# Add the paver modules
from ngs.paver.slurm import *
from ngs.paver.wrappers import *

class TestDrmtask(unittest.TestCase):
    def setUp(self):
        @drmtask
        def drma():
            print "Set up drm"
        self.drm = drma

    def test(self):
        print self.drm

class TestDrmtaskWithoutInit(unittest.TestCase):
    def setUp(self):
        self.drm = None
        self.drm2 = None
        @drmtask
        def drma():
            print "drma"
        self.drm = drma
        @drmtask
        def drma2():
            print "drma"
        self.drm2 = drma

    def testName(self):
        print self.drm
        print self.drm2

class TestDrmtaskWithCommand(unittest.TestCase):
    def setUp(self):
        self.drm = None
        @drmtask
        def bwa(self):
            prefix = "../test_data/test/test.single.bwa"
            cmd = sam_to_bam(prefix)
            bwa.add_job(cmd)
            bwa.run_job()
            return bwa
        self.drm = bwa

    def testBwa(self):
        print "Bwa test" + str(self.drm.cmd)

if __name__ == '__main__':
    unittest.main()

