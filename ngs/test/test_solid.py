#! /usr/bin/python
#
# File: test_solid.py
# Created: Wed Jun 29 17:01:31 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
# Description: 
# Test suite for solid templates

import os
import sys
import unittest
import shutil

# Add the library path
exe_path=os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0,os.path.abspath(os.path.join(exe_path, "..")))
# Add the paver modules
from ngs.solid import *

class testPrimerSet(unittest.TestCase):
    def setUp(self):
        testdir = os.path.join(os.getcwd(), "test", "solid")
        if os.path.exists(testdir):
            shutil.rmtree(testdir)
        self.sp = SolidProject("Test", "Test", "Ref", basedir=testdir)
        self.ps = PrimerSet("F3", 50, self.sp)

    def testAddPrimerSet(self):
        self.sp.add_primer_set("F3")
        self.sp.global_ini_template()
        self.sp.dibayes_ini_template()

class testSolidProjects(unittest.TestCase):
    def setUp(self):
        testdir = os.path.join(os.getcwd(), "test", "solid")
        if os.path.exists(testdir):
            shutil.rmtree(testdir)
        #self.sp = SOLiDProject("Test", "Test", "ref", basedir=testdir)
        self.wtse = WT_SingleRead("Test", "Test", "ref", testdir, "csfasta", "filterref", "exons_gtf", "junction_ref", None)

    def testTemplates(self):
        #print "First looking at " + str(self.sp)
        print "Now looking at " + str(self.wtse)
        print  self.wtse.global_ini()
        print self.wtse.wt_single_read_ini()
