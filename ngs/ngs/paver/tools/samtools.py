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
    view = Bunch(
        opts = "-bS",
        ext_out = None,
        ),
    sam2bam = Bunch(
        opts = "-bSh",
        ext_out = ".bam",
        ),
    bam2bam = Bunch(
        opts = "-bh",
        ext_out = ".bam",
        ),
    samsort = Bunch(
        opts = "",
        ext_out = ".sort.bam",
        ),
    mpileup = Bunch(
        opts = "-us",
        ext_out = "",
        )
    )

##############################
## Tasks
##############################
@task
@cmdopts([("INPUT=", "I", "input sam file")])
def sam2bam():
    """Run samtools view."""
    options.order("sam2bam")
    default = options.samtools_default
    samfile = options.get("INPUT", options.get("prefix", None))
    if samfile is None:
        return
    opts = options.get("opts", default.sam2bam.get("opts"))
    outfile = samfile.replace(".sam", ".bam")
    cl = [" ".join(["samtools view", opts, samfile, ">", outfile])]
    run_cmd(cl, samfile, outfile, options.run, "Running %s" % cl)

@task
@cmdopts([("INPUT=", "I", "input bam file")])
def bam2bam():
    """Run samtools view on bam file."""
    options.order("bam2bam")
    default = options.samtools_default
    bamfile = options.get("INPUT", options.get("prefix", None))
    if bamfile is None:
        return
    opts = options.get("opts", default.bam2bam.get("opts"))
    ext_out = options.get("ext_out", "test")
    outfile = bamfile.replace(".bam", ext_out)
    cl = [" ".join(["samtools view", opts, bamfile, ">", outfile])]
    run_cmd(cl, bamfile, outfile, options.run, "Running %s" % cl)

@task
@cmdopts([("INPUT=", "I", "input sam file")])
def compress_sam():
    """Replace sam file content with text string.

    If bam file exists, replace sam file content with a text string pointing to bam file.

    NOTE: use at own risk! Does not check whether bam file is correct.
    """
    options.order("compress_sam")
    samfile = options.get("INPUT", options.get("prefix", None))
    if samfile is None:
        return
    bamfile = samfile.replace(".sam", ".bam")
    if os.path.exists(bamfile):
        if not options.dry_run:
            out_handle = open(samfile, "w")
            out_handle.write("%s converted to %s\n" % (samfile, bamfile))
            out_handle.close()
        else:
            print "%s converted to %s" % (samfile, bamfile)

@task
@cmdopts([("INPUT=", "I", "input sam file")])
def samsort():
    """Run samtools sort."""
    options.order("samsort")
    default = options.samtools_default
    infile = options.get("INPUT", options.get("prefix", None))
    if infile is None:
        return
    prefix, ext = os.path.splitext(infile)
    opts = options.get("opts", default.samsort.get("opts"))
    outfile = infile.replace(ext, "-sort")
    cl = [" ".join(["samtools sort", opts, infile, prefix + "-sort"])]
    run_cmd(cl, infile, None, options.run, "Running %s" % cl)

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
    options.order("mpileup")
    INPUT = os.path.abspath(options.get("INPUT", None))
    ref = options.get("reference", options.index_loc["sam_fa"][options.ref][2])
    opts = options.get("opts", "")
    if not INPUT is None:
        outfile = options.get("outfile", os.path.abspath(os.path.splitext(INPUT)[0] + ".mpileup"))
        cl = [" ".join(["samtools mpileup", str(opts), "-f", ref, INPUT, ">", outfile])]
        run_cmd(cl, INPUT, outfile, options.run, "running samtools mpileup")
