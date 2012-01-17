"""
variant calling programs
"""
import os

from paver.easy import *
from ngs.paver import run_cmd

##############################
## default options
##############################
options.variantcalling_default = Bunch(
    annovar_home = os.path.abspath("./"),
    )


##############################
## Tasks
##############################
@task
@cmdopts([("INPUT=", "I", "input query file"), ("OUTPUT=", "O", "output file prefix"),
          ("DB=", "D", "database location")])
def annovar_annotate_variation():
    """Run annovar annotate variation."""
    options.order("annovar_annotate_variation")
    query = options.get("INPUT", None)
    database = options.get("DB", path(options.get("annovar_home")) / "humandb")
    opts = options.get("opts", None)
    if not query is None:
        outfile = options.get("OUTPUT", query + "annotate_variation")
        cl = [" ".join([path(options.get("annovar_home"))/ "annotate_variation.pl", opts, "--outfile %s" % (outfile), query, database])]
        run_cmd(cl, query, None, options.get("run"), msg="Running annovar annotate variation")

@task
@cmdopts([("INPUT=", "I", "input query file"), ("OUTPUT=", "O", "output file prefix"),
          ("DB=", "D", "database location")])
def annovar_summarize_annovar():
    """Run annovar summarize annovar."""
    options.order("annovar_summarize_annovar")
    query = options.get("INPUT", None)
    database = options.get("DB", path(options.get("annovar_home")) / "humandb")
    opts = options.get("opts", "")
    if not query is None:
        outfile = options.get("OUTPUT", query + ".summarize_annovar")
        cl = [" ".join([path(options.get("annovar_home"))/ "summarize_annovar.pl", opts, "--outfile %s" % (outfile), query, database])]
        run_cmd(cl, query, None, options.get("run"), msg="Running summarize_annovar.pl")
        

@task
@cmdopts([("INPUT=", "I", "input variant file"), ("OUTPUT=", "O", "output file name"),
          ("FORMAT=", "F", "format")])
def annovar_convert_to_annovar():
    """Run annovar convert to annovar."""
    options.order("annovar_convert_to_annovar")
    query = options.get("INPUT", None)
    fformat = options.get("FORMAT", "vcf4")
    opts = options.get("opts", "")
    if not query is None:
        outfile = options.get("OUTPUT", query + ".avinput")
        cl = [" ".join([path(options.get("annovar_home"))/ "convert2annovar.pl", opts, "--format %s --outfile %s" % (fformat, outfile), query])]
        run_cmd(cl, query, None, options.get("run"), msg="Running convert2annovar.pl")
        
