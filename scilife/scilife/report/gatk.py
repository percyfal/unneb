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
    
    def __init__(self):
        ProgramData.__init__(self)

    def read_depthofcoverage(self, prefix, indir="."):
        """read depthofcoverage tables"""
        ext = ["sample_cumulative_coverage_counts","sample_cumulative_coverage_proportions",
               "sample_interval_statistics","sample_interval_summary","sample_statistics",
               "sample_summary"]
        ## Read sample summary - skip last line since lacks columns
        infile = os.path.abspath(os.path.join(indir, prefix + "." + ext[5]))
        with open(infile) as fp:
            self.data[ext[5]] = asciitable.read(infile, delimiter="\t", guess=False, data_end=-1)
            
        ## Read rest of tables
        for e in ext[0:4]:
            infile = os.path.abspath(os.path.join(indir, prefix + "." + e))
            with open(infile) as fp:
                tab = asciitable.read(self._sniff_table(infile), delimiter="\t", guess=False)
                self.data[e] = tab


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
        plt.show()


