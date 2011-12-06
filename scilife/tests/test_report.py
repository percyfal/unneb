"""
Test report classes
"""
import os
import subprocess
import unittest
import matplotlib.pyplot as plt
import scilife.report.gatk as gatk

class ReportTest(unittest.TestCase):
    """Test reporting functionality"""

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")

    def test_1_read_depthofcoverage(self):
        """Read and write depthofcoverage output"""
        doc = gatk.DepthOfCoverage()
        doc.read_depthofcoverage("depthofcoverage_out", self.data_dir)
        #print doc.data['sample_cumulative_coverage_counts']
        #print doc.data['sample_cumulative_coverage_counts'].dtype


    def test_2_plot_depthofcoverage(self):
        """plot depth of coverage"""
        doc = gatk.DepthOfCoverage()
        doc.read_depthofcoverage("depthofcoverage_out", self.data_dir)
        doc.plot_depthofcoverage()
        plt.savefig("test.png")
        plt.clf()
        doc.plot_depthofcoverage(xlim=(10,20))
        plt.savefig("test2.png")
        plt.clf()
