"""
tools
"""
import os

from paver.easy import *
from ngs.paver import run_cmd

@task
@cmdopts([("INPUT=", "I", "input read file"), ("TMPDIR=", "T", "temp dir"),
          ("REFGENEFILE=", "R", "reference gene file")])
def ngsrich_evaluate():
    """Run NGSrich."""
    options.order("ngsrich_evaluate")
    readfile = options.get("INPUT", None)
    refgenefile = options.get("REFGENEFILE", "refGene.txt")
    if readfile is None:
        return
    prefix, ext = os.path.splitext(readfile)
    tmpdir = options.get("TMPDIR", os.path.join("/scratch/tmp/%s" % os.path.basename(prefix)))
    enrichdir = os.path.join(os.path.dirname(prefix), "enrichment/" + os.path.basename(prefix))
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    if not os.path.exists(enrichdir):
        os.makedirs(enrichdir)
    cl = [" ".join(["java NGSrich", "evaluate -r %s" % readfile,  "-u %s -t %s -o %s" % (refgenefile, options.teqc.target, enrichdir),
                    "-T %s" % tmpdir] )]
    run_cmd(cl, readfile, None, options.run, "Running NGSrich on %s" % readfile)
    sh("rm -rf %s" % tmpdir)


