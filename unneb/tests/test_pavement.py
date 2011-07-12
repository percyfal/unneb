"""
Test paver functions
"""

import os
import sys
import unittest


class PavementTest(unittest.TestCase):
    """Test pavement file"""
    
    def setUp(self):
        self.pavement = os.path.join(os.path.dirname(__file__), "config", "pavement.py")

