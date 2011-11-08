import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
from paver.easy import *
from ngs.paver import *
#from paverpipe.bwa import *
#from paverpipe.samtools import *
from ngs.paver.pipelines.pipelines import exome_pipeline
import yaml

## Project options
options(
    prefix = None,
    samples = ["sample1", "sample2"],
    aligner = bwa,
    )

@task
def config_to_yaml():
    """Print config in yaml format. TODO: Fix options_to_yaml converter"""
    print options
