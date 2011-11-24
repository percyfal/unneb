"""
teqc

Target Enrichment Analysis tasks
"""
import os
from paver.easy import *
from ngs.paver import run_cmd

##############################
## Tasks
##############################
@task
@cmdopts([("abam=", "a", "bam input file"), ("target=", "t", "target bed file"),
          ("ucscgenome=", "u", "UCSC genome"), ("flank=", "f", "flanking sequence - a comma-separated list")])
def teqc():
    """Run teqc_enrichment.py script. 

    Uses pybedtools to do the magic.
    """
    options.order("teqc", add_rest=True)
    bamfile = options.get("abam", None)
    targetfile = options.get("target", None)
    ucscgenome = options.get("ucscgenome", None)
    flank = options.get("flank", None)
    opts = ""
    if not ucscgenome is None:
        opts += "--build=%s" % ucscgenome
    if not flank is None:
        opts += "--flank=%s" % flank
    if bamfile is None or targetfile is None:
        print >> sys.stderr, "missing arguments"
    cl = [" ".join(["teqc_enrichment.py", bamfile, targetfile, opts])]
    run_cmd(cl, bamfile, None, options.run, None)
