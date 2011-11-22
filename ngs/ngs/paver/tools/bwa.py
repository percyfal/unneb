"""
bwa program
"""
import os

from paver.easy import *
from ngs.paver import run_cmd

"""
Bwa program suite options
"""

@task
def auto():
    bwa = dict(
        program = "bwa",
        opts = "",
        cl = [],
        map_reads = map_reads,
        aln = dict(
            opts = "-k 1 -n 3 -t " + str(options.threads),
            ext_out = ".sai",
            ),
        samse = dict(
            opts = "",
            ext_out = ".sam",
            ),
        sampe = dict(
            opts = "",
            ext_out = ".sam",
            ),
        )
## Setup options to use bwa
    options.aligner = bwa

## Tasks
@task
def align(options):
    """Run bwa aln bwa.opts options.ref infile > outfile"""
    msg = "Running paver.ngs.tools.bwa.align"
    prefix, ext = os.path.splitext(options.prefix)
    if not ext:
        ext = options.ext_fq
    infile = prefix + ext
    outfile = prefix + bwa["aln"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "aln", bwa["aln"]["opts"], options.index_loc["bwa"][options.ref][2], infile, ">", outfile]))
    bwa["cl"] = run_cmd(bwa["cl"], infile, outfile, options.run, msg)

@task
def sampe(options):
    """Run bwa sampe. Takes as input a fastq file or a prefix."""
    msg = "Running paver.ngs.tools.bwa.sampe"
    prefix, ext = os.path.splitext(options.prefix)
    if not ext:
        ext = options.ext_fq
    fastq1  = prefix + options.read1_suffix + ext
    fastq2  = prefix + options.read2_suffix + ext
    saifile1 = prefix + options.read1_suffix + bwa["aln"]["ext_out"]
    saifile2 = prefix + options.read2_suffix + bwa["aln"]["ext_out"]
    out = options.prefix + bwa["sampe"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "sampe", bwa["sampe"]["opts"], options.index_loc["bwa"][options.ref][2], saifile1, saifile2, fastq1, fastq2, ">", out]))
    bwa["cl"] = run_cmd(bwa["cl"], saifile1, out)

@task
def samse():
    """Run bwa samse"""
    prefix, ext = os.path.splitext(options.prefix)
    if not ext:
        ext = options.ext_fq
    saifile = prefix + options.read_suffix + bwa["aln"]["ext_out"]
    fastq = prefix + options.read_suffix + options.ext_fq
    out = options.prefix + bwa["samse"]["ext_out"]
    bwa["cl"].append(" ".join([bwa["program"], "samse", bwa["samse"]["opts"], options.index_loc["bwa"][options.ref][2], saifile, fastq, ">", out]))
    bwa["cl"] = run_cmd(bwa["cl"], saifile, out)

@task
def map_reads():
    """Collects bwa functions for mapping. Runs aligner and samse/sampe"""
    options.run = False
    if options.paired_end:
        environment.call_task("ngs.paver.tools.bwa.align")
        environment.call_task("ngs.paver.tools.bwa.align")
        environment.call_task("ngs.paver.tools.bwa.sampe")
    options.run = True
    bwa["cl"] = run_cmd(bwa["cl"])


##################################################
## Tasks to look at bwa
##################################################
@task
def bwa_config():
    """List bwa configuration"""
    print options.aligner


## solid2fastq.pl
@task
@cmdopts([("indir=", "i", "input directory"), ("outdir=", "o", "output directory"),
          ("glob=", "g", "file glob"), ("csfasta=", "c", "csfasta file"),
          ("qual=", "q", "quality file"), ("prefix=", "p", "prefix")])
def solid2fastq():
    """Run solid2fastq.pl.

    Options (defined in options.bwa):

    indir
      input directory. Default: os.path.curdir

    outdir
      output directory. Default: os.path.curdir

    glob
      file glob

    csfasta
      csfasta file

    qual
      quality file

    prefix
      file prefix. Will look for prefix.csfasta and prefix_QV.qual
    """
    options.order("solid2fastq")
    prefix = options.get("prefix", None)
    outprefix = prefix
    indir = path(os.path.abspath(options.get("indir", os.path.curdir)))
    outdir = path(os.path.abspath(options.get("outdir", os.path.curdir)))
    csfasta = indir / options.get("csfasta", prefix + ".csfasta")
    qual = indir / options.get("qual", prefix + "_QV.qual")
    opts = options.get("opts")
    if csfasta.exists():
        cl = " ".join(["solid2fastq.pl", prefix, outprefix])
