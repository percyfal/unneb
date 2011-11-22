"""
Paver project tasks
"""
import os
from paver.easy import *

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

##############################
## Index locations
## Read from galaxy config
##############################
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

## Global-like options
## Standard setup - change in module files
## This has to be run when module is loaded, not for a particular task
@task
def auto():
    """Initializes options."""
    options(
        aligner = None,
        prefix = None,
        cl = [],
        force = False,
        threads = 8,
        db = db,
        ref = "hg19",
        paired_end=True,
        fastq1 = None,
        fastq2 = None,
        read1_suffix = "_1",
        read2_suffix = "_2",
        ext_fq = ".fastq",
        index_loc = index_loc,
        exec_fn = dict(fn = sh),
        run = True,
        )
    options.read_suffix = lambda: options.paired_end and options.read1_suffix or ""
## Run the init function
auto()



##################################################
## Basic tasks for getting configuration
##################################################
@task
def list_ref():
    """List currently defined references"""
    print options.index_loc

@task 
def list_db():
    """List variation databases"""
    print options.db

##############################
## Functions for execution
##############################
def _check_options():
    options.wrapper = options.get("wrapper", "sh")
    if options.wrapper == "sbatch":
        import ngs.paver.parallel.sbatch
    if not options.get("log", None) is None:
        from ngs.paver.log import set_handler    
        set_handler(options)

@task
def process_cl():
    """Task to process current options.cl"""
    cl = options.cl
    options.cl = []
    run_cmd(cl, None, None, options.get("run"), msg="Running process_cl to cleanup cl")
    
def run_cmd(cl, infile=None, outfile=None, run=True, msg=None):
    """Run a command and empty"""
    _check_options()
    options.cl += cl
    if not options.force:
        if path(infile).exists() and path(outfile).exists():
            if path(infile).mtime < path(outfile).mtime:
                run = False
                print "-----> Task is up to date"
    if not path(infile).exists() and not infile is None:
        run = False
        print "-----> No such infile " + str(infile)
    if run:
        options.exec_fn["fn"]("\n".join(options.cl))
        if options.has_key("log"):
            options.log.logger.info(str(msg))
        options.cl = []

## Simple getters
def current_prefix(ext=""):
    """Return current prefix + possible extension"""
    if not options.prefix is None:
        return options.prefix + ext
    else:
        return None

def prefix(obj):
    """Strip read suffices and file name extension"""
    ret = path(obj).stripext()
    ret = ret.rstrip(options.read_suffix).rstrip(options.read1_suffix).rstrip(options.read2_suffix)
    return os.path.basename(ret)

