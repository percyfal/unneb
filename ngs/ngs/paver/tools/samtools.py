"""
samtools programs
"""
import os
from paver.easy import *
from ngs.paver import run_cmd

##############################
## samtools default options
##############################
options.samtools_default = Bunch(
    program = "samtools",
    opts = "",
    view = dict(
        opts = "-bS",
        ext_out = None,
        ),
    sam2bam = dict(
        opts = "-b",
        ext_out = ".bam",
        #cl = sam2bam,
        ),
    samsort = dict(
        opts = "",
        ext_out = ".sort.bam",
        #cl = samsort,
        ),
    mpileup = dict(
        opts = "-us",
        ext_out = "",
        )
    )

##############################
## Tasks
##############################
@task
@cmdopts([()])
def sam2bam():
    if options.prefix is None:
        return
    samfile = options.prefix + ".sam"
    out = options.prefix + samtools["sam2bam"]["ext_out"]
    samtools["cl"].append(" ".join([samtools["program"], "view", 
                                   samtools["sam2bam"]["opts"], samfile, ">", out]))
    sh(samtools["cl"])

@needs("sam2bam")
@task
def samsort():
    if options.prefix is None:
        return
    bamfile = options.prefix + ".bam"
    out = options.prefix + samtools["samsort"]["ext_out"]
    samtools["cl"].append(" ".join([samtools["program"], "sort", 
                                   bamfile, out]))
    sh(samtools["cl"])

@task
@cmdopts([("INPUT=", "I", "input file"), ("outfile=", "o", "outfile"),
          ("reference=", "r", "reference file")])
def mpileup():
    """Run samtools mpileup.
    
    Options:

    INPUT
      Input file
    outfile 
      output file
    reference
      reference sequence
    """
    options.order(options.get("samtools_default")["mpileup"], "samtools_default", add_rest=True)
    INPUT = os.path.abspath(options.get("INPUT", None))
    ref = options.get("reference", options.index_loc["sam_fa"][options.ref][2])
    opts = options.get("opts", "")
    if not INPUT is None:
        outfile = options.get("outfile", os.path.abspath(os.path.splitext(INPUT)[0] + ".mpileup"))
        cl = [" ".join([options.get("program"), "mpileup", str(opts), "-f", ref, INPUT, ">", outfile])]
        run_cmd(cl, INPUT, outfile, options.run, "running samtools mpileup")
