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

class testSOLiDProjects(unittest.TestCase):
    def setUp(self):
        testdir = os.path.join(os.getcwd(), "test", "solid")
        if os.path.exists(testdir):
            shutil.rmtree(testdir)
        #self.wtse = WT_SingleRead("Test", "Test", "ref", testdir, "csfasta", "filterref", "exons_gtf", "junction_ref", None)
        tfkw = {'runname':'test',
                'samplename':'testsample',
                'reference':'reference',
                'basedir':testdir,
                'targetfile':'target',
                'annotation_gtf_file':'annotation'
                }
        self.tf = TargetedFrag(**tfkw)

    # def testWT_SingleRead(self):
    #     print self.wtse.global_ini()
    #     print self.wtse.wt_single_read_ini()

    # def testTargetedFrag(self):
    #     print self.tf.global_ini()
    #     print self.tf.saet_ini()
    #     print self.tf.small_indel_frag_ini()
    #     print self.tf.enrichment_ini()
    #     print self.tf.targeted_frag_workflow_ini()

    def testTargetedFragPrimer(self):
        print self.tf.primersets['F3']
        self.tf.init_project()
