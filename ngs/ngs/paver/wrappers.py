"""
Wrappers for ngs analysis

NOTE: these are just wrappers that simply generate text strings for common ngs tasks
"""

VERSION = "0.1.0"

def make_bwa_cs_input(prefix):
    """Make bwa color space input"""
    cmd = " ".join(['solid2fastq.pl', prefix + "_", prefix])
    return cmd
        

def bwa(prefix, opts, ref):
    """Run bwa aligner"""
    infile  = prefix + ".fastq.gz"
    outfile = prefix + ".bwa.sai"
    cmd = " ".join(['bwa aln', opts, ref, infile, ">", outfile])
    return cmd
