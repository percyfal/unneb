"""
Test report classes
"""
import os
import time
import subprocess
import unittest
import matplotlib.pyplot as plt
import scilife.report.gatk as gatk

class ReportTest(unittest.TestCase):
    """Test reporting functionality"""

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.prefix = "depthofcoverage_out_A"
        self.doc = gatk.DepthOfCoverage()

    def test_1_plot_depthofcoverage(self):
        """plot depth of coverage"""
        self.doc.read_depthofcoverage(self.prefix, self.data_dir)        
        self.doc.plot_depthofcoverage(outfile="test.png")
        self.doc.plot_depthofcoverage(xlim=(10,20), outfile="test.png")

    def test_2_read_depthofcoverage(self):
        doc = gatk.DepthOfCoverage()
        t1 =  time.clock()
        doc.read_depthofcoverage(self.prefix, self.data_dir)
        t2 = time.clock()
        print "Elapsed time read_depthofcoverage: %s" % str(t2-t1)

    def test_3_read_depthofcoverage(self):
        doc = gatk.DepthOfCoverage()
        t1 = time.clock()
        doc.read_data(self.prefix, self.data_dir)
        t2 = time.clock()
        print "Elapsed time read_data: %s" % str(t2-t1)
