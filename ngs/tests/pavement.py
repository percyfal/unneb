import sys
import os
from paver.easy import *
from ngs.paver import *
from ngs.paver.tools.bwa import *
#from paverpipe.samtools import *
#from ngs.paver.pipelines.pipelines import exome_pipeline
import yaml

## Project options
options(
    prefix = "test",
    samples = ["test", "newtest"],
    ref = "mm9",
    )

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

