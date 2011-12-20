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
# @task
# def auto():
#     """Initializes options."""
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

##############################
## auto task
##############################
# @task
# def auto():
#     """auto task: check namespaces"""
#     print options
#     print "running auto"

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

@task
@cmdopts([("section=", "s", "select section to print")])
def print_options():
    """List options"""
    import pprint
    pp = pprint.PrettyPrinter(indent = 4)
    section = options.get("section", None)
    if section is None:
        pp.pprint(options)
    else:
        if options.has_key(section):
            sec = options.get(section)
            pp.pprint(sec)
        else:
            pass

##############################
## Functions for execution
##############################
def _check_options():
    options.wrapper = options.get("wrapper", "sh")
    if options.wrapper == "sbatch":
        import ngs.paver.parallel.sbatch
    if options.wrapper == "drmaa":
        import ngs.paver.parallel.DRMAA
    # sh should check options.cl - if longer than 1, don't run
    if options.wrapper == "sh":
        options.cl = "\n".join(options.cl)
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
    options.cl += cl
    _check_options()
    if not options.force:
        if path(infile).exists() and path(outfile).exists():
            if path(infile).mtime < path(outfile).mtime:
                run = False
                print "-----> Task is up to date"
    if not path(infile).exists() and not infile is None:
        run = False
        print "-----> No such infile " + str(infile)
    if run:
        options.exec_fn["fn"](options.cl)
        if options.has_key("log"):
            options.log.logger.info(str(msg))
        options.cl = []

##############################
## xargs task
## Wrap a task through xargs
##############################
@task
@cmdopts([("glob=", "g", "glob of files to process"), ("task=", "t", "task to run"), ("proc=", "p", "number of processes to use")])
def task_to_xargs():
    options.order("task_to_xargs")
    task = options.get("task", None)
    # Collect tasks
    options.run = False
    if not task is None:
        glob_str = options.get("glob")
        infiles = glob.glob(glob_str)
        for f in infiles:
            
            call.task(task)
        print options.cl
        


##############################
## Simple getters
##############################        
def current_prefix(ext=""):
    """Return current prefix + possible extension"""
    if not options.prefix is None:
        return options.prefix + ext
    else:
        return None

def get_prefix(obj):
    """Strip read suffices and file name extension"""
    prefix, ext = os.path.splitext(obj)
    import re
    prefix = re.sub("%s|%s|%s" % (options.read_suffix, options.read1_suffix, options.read2_suffix), "", prefix)
    return os.path.basename(prefix), ext

