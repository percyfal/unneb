"""
picard program suite options and tasks
"""
import os
from paver.easy import *
from ngs.paver import run_cmd, current_prefix, prefix
from bcbio.utils import curdir_tmpdir

## Picard options
@task
def auto():
    if not options.has_key("picard_config"):
        options.picard_config = Bunch()
    options.picard_config.update(
            picard_home  = os.path.abspath("./"),
            opts = "",
            javamem = "-Xmx6g",
            INPUT = "",
            OUTPUT = "",
            )

@needs("ngs.paver.tools.picard.auto")
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
    options.order("picard", "picard_config")
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
     

@needs("ngs.paver.tools.picard.auto")
@task
@cmdopts([("FASTQ=", "f", "input fastq file"), ("FASTQ2", "g", "second input fastq"),
          ("OUTPUT=", "O", "output file"), ("SAMPLE_NAME=", "s", "sample name"),
          ("QUALITY_FORMAT=", "Q", "quality format")])
def FastqToSam():
    """Write unaligned bam file"""
    options.order("FastqToSam", "picard_config")
    f1 = options.get("FASTQ", current_prefix(options.read_suffix + options.ext_fq))
    f2 = options.get("FASTQ2",read2())
    qv = options.get("QUALITY_FORMAT", "Standard")
    output = options.get("OUTPUT", None)
    sample_name = options.get("SAMPLE_NAME", prefix(f1))
    opts = options.get("opts", "")
    if not output is None and not sample_name is None:
        opts += " FASTQ=%s FASTQ2=%s QUALITY_FORMAT=%s SAMPLE_NAME=%s OUTPUT=%s" % (f1, f2, qv, sample_name, output)
        cl = [" ".join(["java -jar", options.get("javamem"), path(options.get("picard_home")) / "FastqToSam.jar", opts])]
        run_cmd(cl, f1, output, options.get("run"), msg="Running FastqToSam")
    else:
        print >> sys.stderr, "required argument missing"

@needs("ngs.paver.tools.picard.auto")
@task
@cmdopts([("UNMAPPED_BAM=", "u", "unmapped bam file"),("OUTPUT=", "O", "output file"),
          ("REFERENCE_SEQUENCE=", "R", "reference sequence")])
def MergeBamAlignment():
    """Run MergeBamAlignment"""
    options.order("MergeBamAlignment",  "picard_config")
    unmapped_bam = options.get("UNMAPPED_BAM", options.prefix)
    output = options.get("OUTPUT", prefix(unmapped_bam) + ".bam")
    ref = options.get("REFERENCE_SEQUENCE", options.index_loc.get(options.aligner).get(options.ref)[2])
    opts = options.get("opts", "")
    if not unmapped_bam is None:
        opts += " OUTPUT=%s UNMAPPED_BAM=%s REFERENCE_SEQUENCE=%s" % (output, unmapped_bam, ref)
        cl = [" ".join(["java -jar", options.get("javamem"), path(options.get("picard_home")) / "MergeBamAlignment.jar", opts])]
        run_cmd(cl, unmapped_bam, output, options.get("run"), msg="Running MergeBamAlignment")
    else:
        print >> sys.stderr, "required argument unmapped_bam missing"

@task
def SortSam():
    pass

@task
def MergeSamFiles():
    pass

