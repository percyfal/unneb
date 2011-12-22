"""
Illumina related code.
"""
import os
import glob
import re
from paver.easy import *
from ngs.paver import run_cmd

def organize_illumina_input(ext="_fastq.txt"):
    """Simple grouping of illumina read files.

    Returns: tuple (prefix, fastq1, fastq2)

    NOTE: currently assumes paired end reads.
    """
    bcdirs = glob.glob(os.path.join(options.dirs.data, "*", "*_barcode"))
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
