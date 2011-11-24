import sys
import os
from paver.easy import *
from paver.doctools import *
from ngs.paver import *
from ngs.paver.sys import *
from ngs.paver.tools.gatk import *
from ngs.paver.tools.picard import *
from ngs.paver.tools.bwa import *
from ngs.paver.tools.bedtools import *
import yaml

testdir = path(os.path.dirname(os.path.abspath(__file__)))
sampledir = testdir / os.pardir / "data" / "fastq"

options(
    #prefix = "test",
    aligner = "bwa",
    samples = ["test", "newtest"],
    infile = [sampledir / "test_1.fastq", sampledir / "test_2.fastq"],
    ref = "hg19",
    GATK = Bunch(
        gatk_home = "/bubo/sw/apps/bioinfo/GATK/1.2.12/",
        INPUT= "aoei",
        ),
    )
options.picard = Bunch(picard_home = "/bubo/sw/apps/bioinfo/picard/1.41/")
options.FastqToSam = Bunch(
    FASTQ = options.infile[0],
    FASTQ2 = options.infile[1],
    OUTPUT = "tabor",
    )
options.MergeBamAlignment = Bunch(
    UNMAPPED_BAM = "test_1.bam",
    )

## Set log dir to log
options.log = Bunch(dir = path("log"))
options.pbzip2 = Bunch(opts = "-dv")
options.tar = Bunch(opts = "-xvf")
options.sbatch = Bunch(
    kw = dict(
        project_id = 'a2010003',
        time = "50:00:00",
        constraint = '',
        jobname = '',
        workdir = os.path.curdir,
        partition = 'node',
        cores = '1',
        mail_type = 'ALL',
        mail_user = 'per.unneberg@scilifelab.se',
        header = '',
        footer = '',
        command_str = '',
        )
    )

options.fastq1 = options.infile[0]
options.fastq2 = options.infile[1]

@task
def align_samples():
    """Align samples"""
    for s in options.samples:
        options.prefix = s
        options.aligner["map_reads"]()

@task
def config_to_yaml():
    """Print config in yaml format. TODO: Fix options_to_yaml converter"""
    print options

@task
def task1():
    """Test task 1"""
    print options.ref


@task 
def task2():
    """Print dependency"""
    options.ref="hg19"
    task1()
    print dir(environment)

@task
def task3(options):
    """Test options as parameter"""
    ref = options.get('ref')
    print ref

kw = dict(ref="hg19")

@task
def task4(options):
    """Test kw as options"""
    mytest = options.get('test', "default")
    print mytest

@task
def task5():
    """Pass options to task 4"""
    task4(test="noo")

@task
def run_gatk():
    """Run gatk"""
    options.GATK.INPUT="oeu"
    options.sbatch.kw["outfile"] = "tabort.sh"
    environment.call_task("ngs.paver.tools.gatk.GATK")

@task
def run_fts():
    """Run fastqtosam"""
    options.sbatch.kw["outfile"] = "testit.sh"
    options.FastqToSam = Bunch(FASTQ = options.infile[0],
                               FASTQ2 = options.infile[1],
                               OUTPUT = "test.bam",
                               opts = "RUN_DATE=ooeuoe"
                               )
    options.run=False
    environment.call_task("ngs.paver.tools.picard.FastqToSam")
    options.MergeBamAlignment = Bunch(
        UNMAPPED_BAM = prefix(options.infile[0]) + "_fastq.bam",
        )
    options.run=True
    environment.call_task("ngs.paver.tools.picard.MergeBamAlignment")


@task
@cmdopts([("prefix=", "p", "file prefix"), ("ext_in=", "e", "file extension (suffix)"),
          ("ext_out=", "o", "outfile extension (suffix)")])
def new_align():
    """Run bwa aln bwa.opts options.ref infile > outfile"""
    options.order("align", "bwa_default")
    msg = "Running paver.ngs.tools.bwa.align"
    print options.new_align.get("prefix")
    
    print options.get("prefix")
    #prefix, ext = os.path.splitext(options.get("prefix"))
    #print prefix
    # if not ext:
    #     ext = options.get("ext", options.ext_fq)
    # infile = prefix + ext
    # outfile = prefix + options.get("ext_out", options.get("aln")["ext_out"])
    # cl = [" ".join([options.get("program"), "aln", options.get("aln")["opts"], options.index_loc["bwa"][options.ref][2], infile, ">", outfile])]
    # run_cmd(cl, infile, outfile, options.run, msg)
