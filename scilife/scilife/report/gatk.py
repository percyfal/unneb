import os
import re
import asciitable
from asciitable.fixedwidth import *
from scilife.report import ProgramData
from scilife.report.table import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.recfunctions import append_fields


class DepthOfCoverage(ProgramData):
    """Container class for DepthOfCoverage object"""
    program = "DepthOfCoverage"
    ext_keys = ["sample_cumulative_coverage_counts", 
                "sample_cumulative_coverage_proportions",
                "sample_interval_statistics",
                "sample_statistics",
                "sample_interval_summary",
                "sample_summary"]
    ext = dict(sample_cumulative_coverage_counts = "sample_cumulative_coverage_counts", 
               sample_cumulative_coverage_proportions = "sample_cumulative_coverage_proportions",
               sample_interval_statistics = "sample_interval_statistics",
               sample_statistics = "sample_statistics",
               sample_interval_summary = "sample_interval_summary",
               sample_summary = "sample_summary")

    def __init__(self):
        ProgramData.__init__(self)

    def read_depthofcoverage(self, prefix, indir="."):
        """read depthofcoverage tables"""
        ## Read sample summary - skip last line since lacks columns
        infile = os.path.abspath(os.path.join(indir, prefix + "." + self.ext["sample_summary"]))
        with open(infile) as fp:
            self.data["sample_summary"] = asciitable.read(infile, delimiter="\t", guess=False, data_end=-1)
            
        ## Read rest of tables
        for k in self.ext_keys[0:(len(self.ext_keys) - 1)]:
            infile = os.path.abspath(os.path.join(indir, prefix + "." + self.ext[k]))
            tab = asciitable.read(self._sniff_table(infile), delimiter="\t", guess=False)
            self.data[k] = tab

    def read_data(self, prefix, indir="."):
        ## Read sample summary - skip last line since lacks columns
        infile = os.path.abspath(os.path.join(indir, prefix + "." + self.ext["sample_summary"]))  
        self.data["sample_summary"] = self.read_table(infile)
        for k in self.ext_keys[0:(len(self.ext_keys) - 1)]:
            infile = os.path.abspath(os.path.join(indir, prefix + "." + self.ext[k]))
            self.data[k] = self.read_table(infile)

    def plot_depthofcoverage(self, which="sample_cumulative_coverage_counts", xlim=(None, None), ylim=(None, None), relative=True, outfile=None):
        """plot depth of coverage"""
        data = self.data[which]
        n = len(data)
        if ylim is (None, None):
            ylim = (0, n)
        for i in range(0,n):
            y = np.array(data[i].tolist()[1:]).astype("float")
            nc = y.size
            if xlim == (None, None):
                xlim = (0, nc)
            y = y[xlim[0]:xlim[1]]
            x = range(xlim[0], xlim[1], 1)
            if relative:
                y = y/y[0]
            plt.plot(x, y)
        if not outfile is None:
            plt.savefig(outfile)
        plt.clf()

