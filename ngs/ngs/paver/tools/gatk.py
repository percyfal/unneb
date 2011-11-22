"""
GATK - wrapper for GenomeAnalysisTK.jar
"""
import os

from paver.easy import *
from ngs.paver import run_cmd

## Setup options
@task
def auto():
    """Initialize GATK options"""
    options(
        gatk_config = Bunch(
            gatk_home = os.path.abspath("./"),
            opts = "",
            javamem = "-Xmx6g",
            )
        )


@needs("ngs.paver.tools.gatk.auto")
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
    options.order("GATK", "gatk_config")
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
def IndelRealigner():
    """Run the indel realigner"""
    config = gatk["IndelRealigner"]
    infile = [options.prefix + config["ext_in"][0],
              options.prefix + config["ext_in"][1]]
    outfile = options.prefix + config["ext_out"]
    gatk["cl"].append(" ".join([gatk["program"], "-T IndelRealigner", 
                                #[" ".join([config["opt_in"][i], infile[i]]) for i in range(0, len(infile))],
                                "-R", options.reference, 
                                "-o", outfile, config["opts"]]))
def realign():
    """Realign reads"""
    environment.call_task("paverpipe.gatk.IndelRealigner")
    return gatk["cl"]

## Some tasks
# gatk["realign"] = realign

# options(
#     GATK = gatk
#     )
