"""
bwa program
"""
import os

from paver.easy import *
from ngs.paver import run_cmd

##############################
## bwa default options
##############################
options.bwa_default = Bunch(
    program = "bwa",
    opts = "",
    cl = [],
    #map_reads = map_reads,
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

##############################
## Tasks
##############################
@task
@cmdopts([("prefix=", "p", "file prefix"), ("ext_in=", "e", "file extension (suffix)"),
          ("ext_out=", "o", "outfile extension (suffix)")])
def align():
    """Run bwa aln bwa.opts options.ref infile > outfile"""
    options.order("align", "bwa_default", add_rest=True)
    msg = "Running paver.ngs.tools.bwa.align"
    prefix = options.align.get("prefix", options.get("prefix"))
    if prefix is None:
        return
    prefix, ext = os.path.splitext(prefix)
    if not ext:
        ext = options.align.get("ext_in", options.ext_fq)
    infile = prefix + ext
    outfile = prefix + options.get("ext_out", options.get("aln")["ext_out"])
    cl = [" ".join([options.get("program"), "aln", options.get("aln")["opts"], options.index_loc["bwa"][options.ref][2], infile, ">", outfile])]
    run_cmd(cl, infile, outfile, options.run, msg)

@task
@cmdopts([("prefix=","p", "file prefix"), ("ext_in=", "e", "file extension (suffix)"),
          ("ext_out=", "o", "outfile extension (suffix)") ])
def sampe(options):
    """Run bwa sampe. Takes as input a fastq file or a prefix."""
    msg = "Running paver.ngs.tools.bwa.sampe"
    options.order("sampe", "bwa_default")
    prefix = options.sampe.get("prefix", options.get("prefix"))
    if prefix is None:
        return
    prefix, ext = os.path.splitext(prefix)
    if not ext:
        ext = options.sampe.get("ext_in", options.ext_fq)
    fastq1  = prefix + options.get("read1_suffix") + ext
    fastq2  = prefix + options.get("read2_suffix") + ext
    saifile1 = prefix + options.get("read1_suffix") + options.get("aln")["ext_out"]
    saifile2 = prefix + options.get("read2_suffix") + options.get("aln")["ext_out"]
    out = prefix + options.get("sampe")["ext_out"]
    cl = " ".join([options.get("program"), "sampe", options.get("sampe")["opts"], options.index_loc["bwa"][options.ref][2], saifile1, saifile2, fastq1, fastq2, ">", out])
    run_cmd(cl, saifile1, out)

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
    options.align = Bunch()
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

