#!/usr/bin/env python
# File: testPaverInit.py
# Created: Mon Oct 24 17:41:00 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#

"""
Tests for initialization of paver ngs tools
"""

import os
import sys
import subprocess
import unittest
import shutil
import contextlib
import glob
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
from paver.easy import *
from paverpipe import *

class ngsInitTest(unittest.TestCase):
    """Paver ngs init test"""
    def setUp(self):
        self.pavement = "pavement.py"
        print options
        options(
            prefix = "test"
            )
    def test_1_pipeline(self):
        """Test startup of pipeline"""
        print options
        
