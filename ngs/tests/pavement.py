import sys
import os
from paver.easy import *
from paver.doctools import *
from ngs.paver import *
from ngs.paver.sys import *
#from ngs.paver.tools.bwa import *
#from ngs.paver.tools.picard import *
## import ngs.paver.log
## import  ngs.paver.cluster.sbatch
#from paverpipe.samtools import *
#from ngs.paver.pipelines.pipelines import exome_pipeline
import yaml

## Project options
options(
    prefix = "test",
    samples = ["test", "newtest"],
    infile = ["test_1.fastq", "test_2.fastq"],
    ref = "mm9",
    )
## Set log dir to log
options.log = Bunch(dir = path("log"))
options.pbzip2 = Bunch(opts = "-dv")
options.tar = Bunch(opts = "-xvf")

def setup_fastq_files():
    options.fastq1 = options.infile[0]
    options.fastq2 = options.infile[1]

# Ugly hack to test
setup_fastq_files()

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
