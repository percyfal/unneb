"""
picard program suite options and tasks

Default options are set in picard_default.
"""
import os
from paver.easy import *
from ngs.paver import run_cmd, current_prefix, get_prefix
from bcbio.utils import curdir_tmpdir

##############################
## picard default options
##############################
options.picard_default = Bunch(
    picard_home  = os.path.abspath("./"),
    opts = "",
    javamem = "-Xmx6g",
    validation_stringency="SILENT",
    )

##############################
## Picard run function
##############################
def run(options, fun, infile, outfile):
    """Run picard."""
    opts = ""
    cl = [" ".join(["java -jar", options.get("javamem"), path(options.get("picard_home")) / fun, opts])]
    run_cmd(cl, f1, output, options.get("run"), msg="Running %s" + fun)
    


##############################
## picard basic wrapper
##############################
@task
@cmdopts([('program=', 'p', 'picard program'), ('opts=', 'o', 'picard program options'), ('picard_home=', 'h', 'picard home')])
def picard():
    """Run picard program.

    Options:
    program
      Picard program

    opts
      command line options to pass to Picard program.

    picard_home
      location of picard programs
    """
    options.order("picard", "picard_default")
    program = options.get("program", "")
    if not program.endswith(".jar"):
        program = program + ".jar"
    javamem = options.get("javamem")
    INPUT = options.get("INPUT", None)
    OUTPUT = options.get("OUTPUT", None)
    opts = options.get("opts", "")
    picard_home = options.get("picard_home")
    cl = [" ".join(["java -jar", javamem, path(picard_home) / program, opts])]
    run_cmd(cl, INPUT, OUTPUT, options.run, msg=None)


def read2():
    """Return read 2 if paired end"""
    retval = "none"
    if options.paired_end:
        retval = current_prefix(options.read2_suffix + options.ext_fq)
    return retval

@task
@cmdopts([("FASTQ=", "f", "input fastq file"), ("FASTQ2", "g", "second input fastq"),
          ("OUTPUT=", "O", "output file"), ("SAMPLE_NAME=", "s", "sample name"),
          ("QUALITY_FORMAT=", "Q", "quality format")])
def FastqToSam():
    """Write unaligned bam file"""
    options.order("FastqToSam", "picard_default")
    f1 = options.get("FASTQ", current_prefix(options.read_suffix + options.ext_fq))
    f2 = options.get("FASTQ2",read2())
    qv = options.get("QUALITY_FORMAT", "Standard")
    output = options.get("OUTPUT", None)
    sample_name = options.get("SAMPLE_NAME", get_prefix(f1)[0])
    opts = options.get("opts", "")
    if not output is None and not sample_name is None:
        opts += " FASTQ=%s FASTQ2=%s QUALITY_FORMAT=%s SAMPLE_NAME=%s OUTPUT=%s" % (f1, f2, qv, sample_name, output)
        cl = [" ".join(["java -jar", options.get("javamem"), path(options.get("picard_home")) / "FastqToSam.jar", opts])]
        run_cmd(cl, f1, output, options.get("run"), msg="Running FastqToSam")
    else:
        print >> sys.stderr, "required argument missing"

@task
@cmdopts([("UNMAPPED_BAM=", "u", "unmapped bam file"),("OUTPUT=", "O", "output file"),
          ("REFERENCE_SEQUENCE=", "R", "reference sequence")])
def MergeBamAlignment():
    """Run MergeBamAlignment"""
    options.order("MergeBamAlignment",  "picard_default")
    unmapped_bam = options.get("UNMAPPED_BAM", options.prefix)
    output = options.get("OUTPUT", get_prefix(unmapped_bam)[0] + ".bam")
    ref = options.get("REFERENCE_SEQUENCE", options.index_loc.get(options.aligner).get(options.ref)[2])
    opts = options.get("opts", "")
    if not unmapped_bam is None:
        opts += " OUTPUT=%s UNMAPPED_BAM=%s REFERENCE_SEQUENCE=%s" % (output, unmapped_bam, ref)
        cl = [" ".join(["java -jar", options.get("javamem"), path(options.get("picard_home")) / "MergeBamAlignment.jar", opts])]
        run_cmd(cl, unmapped_bam, output, options.get("run"), msg="Running MergeBamAlignment")
    else:
        print >> sys.stderr, "required argument unmapped_bam missing"


@task
@cmdopts([("INPUT=", "I", "input"), ("OUTPUT=", "O", "output"), ("METRICS=", "M", "metrics"),
          ("VALIDATION_STRINGENCY=", "V", "validation stringency")])
def MarkDuplicates():
    """Mark duplicates.
    
    """
    options.order("MarkDuplicates", "picard_default")
    infile = options.get("INPUT", None)
    prefix, ext = os.path.splitext(infile)
    outfile = options.get("OUTPUT", prefix + "-dup" + ext)
    metrics = options.get("METRICS", prefix + "-dup.metrics")
    validation_stringency = options.get("VALIDATION_STRINGENCY", "SILENT")
    opts = options.get("opts", "")
    if not infile is None:
        opts += " INPUT=%s OUTPUT=%s METRICS_FILE=%s VALIDATION_STRINGENCY=%s" % (infile, outfile, metrics, validation_stringency)
        cl = [" ".join(["java -jar", options.get("javamem"), path(options.get("picard_home")) / "MarkDuplicates.jar", opts ])]
        run_cmd(cl, infile, outfile, options.get("run"), msg="Running MarkDuplicates")
    else:
        print >> sys.stderr, "required argument missing"

@task
@cmdopts([("INPUT=", "I", "input"), ("OUTPUT=", "O", "output"),
          ("SORT_ORDER=", "S", "sort order"), ("VALIDATION_STRINGENCY=", "V", "validation stringency")])
def SortSam():
    """Sort sam/bam file"""
    options.order("SortSam", "picard_default")
    infile = options.get("INPUT", None)
    prefix, ext = os.path.splitext(infile)
    outfile = options.get("OUTPUT", prefix + "-sort" + ext)
    sort_order = options.get("SORT_ORDER", "coordinate")
    validation_stringency = options.get("VALIDATION_STRINGENCY", "SILENT")
    opts = options.get("opts", "")
    if not infile is None:
        opts += " INPUT=%s OUTPUT=%s SORT_ORDER=%s VALIDATION_STRINGENCY=%s" % (infile, outfile, sort_order, validation_stringency)
        cl = [" ".join(["java -jar", options.get("javamem"), path(options.get("picard_home")) / "SortSam.jar", opts ])]
        run_cmd(cl, infile, outfile, options.get("run"), msg="Running SortSam")
    else:
        print >> sys.stderr, "required argument missing"

@task
@cmdopts([("INPUT=", "I", "input"), ("VALIDATION_STRINGENCY=", "V", "validation stringency")])
def BuildBamIndex():
    """Build bam index"""
    options.order("BuildBamIndex", "picard_default")
    infile = os.path.abspath(options.get("INPUT", None))
    outfile = os.path.abspath(options.get("OUTPUT", infile.rstrip(".bam") + ".bai"))
    validation_stringency = options.get("VALIDATION_STRINGENCY", "SILENT")
    opts = options.get("opts", "")
    if not infile is None:
        opts += " INPUT=%s OUTPUT=%s VALIDATION_STRINGENCY=%s" % (infile, outfile, validation_stringency)
        cl = [" ".join(["java -jar", options.get("javamem"), path(options.get("picard_home")) / "BuildBamIndex.jar", opts ])]
        run_cmd(cl, infile, outfile, options.get("run"), msg="Running BuildBamIndex")
    else:
        print >> sys.stderr, "required argument missing"



@task
def MergeSamFiles():
    pass

@task
@cmdopts([("INPUT=", "I", "input"), ("OUTPUT=", "O", "output"),
          ("REFERENCE_SEQUENCE=", "R", "reference sequence")])
def CollectAlignmentSummaryMetrics():
    """Collect alignment summary metrics."""
    options.order("CollectAlignmentSummaryMetrics", "picard_default")
    infile = options.get("INPUT", None)
    prefix, ext = os.path.splitext(infile)
    outfile = options.get("OUTPUT", prefix + ".align_metrics")
    ref = options.get("REFERENCE_SEQUENCE", options.index_loc.get(options.aligner).get(options.ref)[2])
    opts = options.get("opts", "")
    if not infile is None:
        opts += " INPUT=%s OUTPUT=%s REFERENCE_SEQUENCE=%s" % (infile, outfile, ref)
        cl = [" ".join(["java -jar", options.get("javamem"), path(options.get("picard_home")) / "CollectAlignmentSummaryMetrics.jar", opts])]
        run_cmd(cl, infile, outfile, options.get("run"), msg="Running CollectAlignmentSummaryMetrics")
    else:
        print >> sys.stderr, "required argument infile missing"
    
