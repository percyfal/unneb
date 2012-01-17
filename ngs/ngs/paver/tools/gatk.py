"""
GATK - wrapper for GenomeAnalysisTK.jar
"""
import os
import glob
from paver.easy import *
from ngs.paver import run_cmd

##############################
## GATK default options
##############################
options(
    gatk_default = Bunch(
        gatk_home = os.path.abspath("./"),
        opts = "",
        javamem = "-Xmx6g",
        ),
    )
    

##############################
## gatk default wrapper
##############################
@task
@cmdopts([('program=', 'p', 'gatk program'), ('opts=', 'o', 'gatk program options'), ('gatk_home=', 'g', 'gatk home'), ('INPUT=', 'I', 'input')])
def GATK():
    """Run GATK program.

    Options:

    INPUT
      Most (all?) gatk programs require an infile

    OUTPUT
      Output file name

    program
      GATK program to run (-T option)

    opts
      command line options to pass to GATK and the program type.

    gatk_home
      location of gatk
    """
    options.order("GATK", "gatk_default")
    INPUT = options.get("INPUT", "")
    OUTPUT = options.get("OUTPUT", "")
    program = options.get("program", "")
    javamem = options.get("javamem")
    opts = options.get("opts", "")
    gatk_home = options.get("gatk_home")
    cl = [" ".join(["java -jar", javamem, path(gatk_home) / "GenomeAnalysisTK.jar", "-T", program, "INPUT=" + str(INPUT), "OUTPUT=" + str(OUTPUT), str(opts)])]
    if INPUT:
        run_cmd(cl, None, None, options.run, "Running gatk program %s" % program)

@task
@cmdopts([("INPUT_LIST=", "I", "input list"), ("OUTPUT=", "o", "output file name base"),
          ("bam=", "b", "bam glob"), ("REF=", "R", "reference genome"), ("TARGET=", "L", "target sequence")])
def DepthOfCoverage():
    """Run DepthOfCoverage.
        
    Options:

    INPUT_LIST
      List of input files
      
    OUTPUT
      Output file name base

    bam
      glob of bam files

    opts
      command line options to pass
    """
    options.order("DepthOfCoverage", "gatk_default")
    output = options.get("OUTPUT", "depthofcoverage")
    bamfiles = glob.glob(options.get("bam", ""))
    if len(bamfiles) > 0:
        with open("bamfiles.list", "w") as out_handle:
            for bf in bamfiles:
                out_handle.write(os.path.abspath(bf) + "\n")
    input_list = options.get("INPUT_LIST", "bamfiles.list")
    javamem = options.get("javamem")
    opts = options.get("opts", "")
    gatk_home = options.get("gatk_home")
    cl = [" ".join(["java -jar", javamem, path(gatk_home) / "GenomeAnalysisTK.jar", "-T", "DepthOfCoverage", "-I", str(input_list), "-o", str(output), "-R", options.get("REF"), "-L", options.get("TARGET"), str(opts)])]
    if os.path.exists(input_list):
        run_cmd(cl, None, None, options.run, "Running DepthOfCoverage")
    
