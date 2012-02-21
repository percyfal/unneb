"""
Illumina related code.
"""
import os
import glob
import re
from paver.easy import *
from ngs.paver import run_cmd

def organize_illumina_input(ext="_fastq.txt", bc_str="*_barcode"):
    """Simple grouping of illumina read files.

    Returns: tuple (prefix, fastq1, fastq2)

    NOTE: currently assumes paired end reads.
    """
    bcdirs = glob.glob(os.path.join(options.dirs.data, "*", bc_str))
    fastafiles = []
    for d in bcdirs:
        fastafiles = fastafiles + glob.glob(os.path.join(d, "*" + ext))
    samplenames = set([re.sub("_[1-2]" + ext, "", x) for x in fastafiles])
    samples = []
    for sn in samplenames:
        f1 = sn + "_1" + ext
        f2 = sn + "_2" + ext
        if os.path.exists(f1) and os.path.exists(f2):
            samples.append((os.path.basename(sn), f1, f2))
        else:
            print "WARNING: %s or %s missing!" % (f1, f2)
    return samples

## TODO: this information should be calculated from sample_project_run_info.yaml file
def organize_bcbio_input(ext="-sort.bam"):
    """Organize samples from bcbio results
    
    Returns: tuple (sample_id, lane, date, flowcell_id)
    """
    restr = re.compile("([0-9_A-Z]+)_([0-9]{6})_([A-Z0-9]+)%s" % ext)
    glob_str = "*%s" % ext
    infiles = glob.glob(os.path.join(options.dirs.intermediate, glob_str))
    samples = []
    for inf in infiles:
        m = re.search(restr, inf)
        (_, sample_id) = m.group(1).split("_")
        samples.append((sample_id, m.group(1), m.group(2),m.group(3) ))
    return samples
    
def bcbio_file(stup, ext):
    """Make """
    
