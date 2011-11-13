# File: __init__.py
# Created: Mon Oct 24 17:01:30 2011
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
"""
Paver project tasks
"""
from paver.easy import *

def threads():
    return options.threads

def _uptodate(infile, outfile):
    pass

## Workflow
## 1. qc reads
## 2. map reads
## 3. realign reads
## 4. mark duplicates
## 5. recalibrate reads
## 6. genotyping
## 7. evaluation of genotyping

## Idea: 
## - keep track of current prefix and file type with pointers in options
## - perform command and update pointers
## - do atomic operations

##################################################
## Initialisation of options
##################################################
## Tuple with <unique_build_id>   <dbkey>   <display_name>   <file_path>
index_loc = dict(
    bowtie = dict(
        phix = tuple(["phix","phix","/bubo/nobackup/uppnex/reference/biodata/genomes/phiX174/phix/bowtie/phix"]),
        dasNov2 = tuple(["dasNov2","dasNov2","/bubo/sw/apps/bioinfo/bowtie/0.12.6/kalkyl/indexes/e_coli"]),
        hg19  = tuple(["hg19","hg19","/bubo/nobackup/uppnex/reference/biodata/genomes/Hsapiens/hg19/bowtie/hg19"]),
        unknown = tuple(["unknown","unknown","/bubo/nobackup/uppnex/reference/biodata/genomes/Hsapiens/hg19/bowtie/hg19"]),
        mm9 = tuple(["mm9","mm9","/bubo/nobackup/uppnex/reference/biodata/genomes/Mmusculus/mm9/bowtie/mm9"]),
        ),
    bwa = dict(
        hg19 = tuple(["hg19","hg19","/bubo/nobackup/uppnex/reference/biodata/genomes/Hsapiens/hg19/bwa/hg19.fa"]),
        mm9  = tuple(["mm9","mm9","/bubo/nobackup/uppnex/reference/biodata/genomes/Mmusculus/mm9/bwa/mm9.fa"]),
        ),
    sam_fa = dict(
        phix = tuple(["index","phix", "/bubo/nobackup/uppnex/reference/biodata/genomes/phiX174/phix/seq/phix.fa"]),
        mm9 = tuple(["index","mm9","/bubo/proj/a2010002/projects/data/genomes/Mmusculus/mm9/seq/mm9.fa"]),
        hg19 = tuple(["index","hg19","/bubo/proj/a2010002/projects/data/genomes/Hsapiens/hg19/seq/hg19.fa"]),
        unknown = tuple(["index","unknown","/bubo/nobackup/uppnex/reference/biodata/genomes/Hsapiens/hg19/seq/hg19.fa"]),
        ),
    )
db = dict(
    dbsnp = dict(
        dbsnp132 = tuple(["dbsnp132", ""]),
        ),
    seqcap = dict(
        sureselect_50mb = tuple(["sureselect_50mb", "/bubo/proj/a2010002/projects/data"]),
        ),
    )

def mysh2(command, capture = False, ignore_error=False, cwd=None):
    sh(command, capture=False, ignore_error=False, cwd=None)
    
def mysh(command):
    print command

def setup_options():
## Global-like options
## Standard setup - change in module files
    options(
        aligner = None,
        prefix = None,
        cl = [],
        force = False,
        threads = 8,
        db = db,
        ref = "hg19",
        paired_end=True,
        read1_suffix = "_1",
        read2_suffix = "_2",
        read_suffix = "",
        ext_fq = ".fastq",
        index_loc = index_loc,
        exec_fn = dict(fn = sh),
        run = True,
        )


## Setup the options
setup_options()

##################################################
## Basic tasks for getting configuration
##################################################
#@cmdopts(['w', 'which', ''])
@task
def list_ref(which="all"):
    """List currently defined references"""
    if which == "all":
        print options.index_loc

@task 
def list_db():
    """List variation databases"""
    print options.db

##############################
## Functions for execution
##############################
def run_cmd(cl):
    """Run a command and empty"""
    if options.run:
        options.exec_fn["fn"]("\n".join(cl))
        cl = []
    return cl
