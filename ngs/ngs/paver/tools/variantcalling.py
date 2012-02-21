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
    crispr_home = os.path.abspath("./"),
    )
options.mutect_default = Bunch(
    mutect_home = os.path.abspath("./"),
    opts = "",
    javamem = "-Xmx2g",
    validation_strictness = "SILENT",
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
        cl = [" ".join([path(options.get("annovar_home"))/ "convert2annovar.pl", opts, "--format %s %s | sed -e \"s/^[ \t]*//g\" > %s" % (fformat, query, outfile)])]
        run_cmd(cl, query, None, options.get("run"), msg="Running convert2annovar.pl")


##############################
## muTect
##############################        
@task
@cmdopts([("INPUT=", "I", "input normal sample"), ("INPUT2=", "T", "input tumour sample"), ("OUTPUT=", "O", "output file name"),
          ("COVERAGE_FILE=", "C", "coverage output file name")])
def muTect_paired():
    """Run muTect for paired normal/tumour sample."""
    options.order("muTect_paired")
    default = options.mutect_default
    normal = options.get("INPUT", None)
    tumour = options.get("INPUT2", None)
    dbsnp  = options.get("dbsnp", "")
    cosmic  = options.get("cosmic", "")
    if not normal is None and not tumour is None:
        OUTPUT = options.get("OUTPUT", "mutect_paired.call_stats.txt")
        coverage = options.get("COVERAGE_FILE", "mutect_paired.coverage.wig")
        VALIDATION_STRICTNESS = options.get("VALIDATION_STRICTNESS", default.get("VALIDATION_STRICTNESS"))
        ref = options.get("reference", options.index_loc["sam_fa"][options.ref][2])
        opts = options.get("opts", "")
        opts += " --reference_sequence %s --input_file:normal %s --input_file:tumor %s" % (ref, normal, tumour)
        if dbsnp:
            opts += " -B:dbsnp,VCF %s" % dbsnp
        if cosmic:
            opts += " -B:cosmic,VCF %s" % cosmic
        cl = [" ".join(["java -jar", options.get("javamem", default.get("javamem")),  path(options.get("mutect_home", default.get("mutect_home"))) / "muTect.jar", "--analysis_type MuTect", "--out %s" % OUTPUT, "--coverage_file %s" % coverage, "--log_to_file muTect_paired.log", opts])]
        run_cmd(cl, normal, OUTPUT, options.get("run"), msg="Running muTect_paired")


##############################
## CRISP
##############################
@task
@cmdopts([("INPUT=", "I", "input crisp results file")])
def crisp_to_vcf():
    """Convert crisp to vcf"""
    options.order("crisp_to_vcf")
    default = options.variantcalling_default
    infile = options.get("INPUT", None)
    if not infile is None:
        outfile = infile + ".vcf"
        opts = options.get("opts", "")
        cl = [" ".join(["%s" % path(options.get("crispr_home"))/ "crisp_to_vcf.py", infile, ">", outfile])]
        run_cmd(cl, infile, outfile, options.get("run"), msg="Running crisp_to_vcf")

        
