import os
import asciitable
from asciitable.fixedwidth import *
from scilife.report.table import *

def to_rst_table(tab):
    """Convert asciitable to rst table"""
    s = ".. table::"

class DepthOfCoverage():
    """Container class for DepthOfCoverage object"""
    def __init__(self):
        self.data = dict()

    def read_depthofcoverage(self, prefix, indir="."):
        """read depthofcoverage tables"""
        ext = ["sample_cumulative_coverage_counts","sample_cumulative_coverage_proportions",
               "sample_interval_statistics","sample_interval_summary","sample_statistics",
               "sample_summary"]
        ## Read sample summary - skip last line since lacks columns
        infile = os.path.abspath(os.path.join(indir, prefix + "." + ext[5]))
        with open(infile) as fp:
            self.data[ext[5]] = asciitable.read(infile, delimiter="\t", guess=False, data_end=-1)
            
            # for e in ext:
            #     infile = prefix + "." + e
            #     with open(infile) as fp:
            #         tab = asciitable.read(infile)
            #         data[e] = tab


def read_depthofcoverage(prefix, indir="."):
    """read depthofcoverage tables"""
    ext = ["sample_cumulative_coverage_counts","sample_cumulative_coverage_proportions",
           "sample_interval_statistics","sample_interval_summary","sample_statistics",
           "sample_summary"]
    data = dict()
    ## Read sample summary - skip last line since lacks columns
    infile = os.path.abspath(os.path.join(indir, prefix + "." + ext[5]))
    with open(infile) as fp:
        data[ext[5]] = asciitable.read(infile, delimiter="\t", guess=False, data_end=-1)
    
    # for e in ext:
    #     infile = prefix + "." + e
    #     with open(infile) as fp:
    #         tab = asciitable.read(infile)
    #         data[e] = tab
    return data

def plot_depthofcoverage(which="sample_cumulative_coverage_counts"):
    """plot depth of coverage"""
    
    
