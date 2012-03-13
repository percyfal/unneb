"""
uppmax helper functions
"""
import os


from paver.easy import *
import ngs.paver
from ngs.paver import run_cmd

from scilife.templates import TEMPLATE_DIR, SBATCH_HEADER_TEMPLATE

options.automated_initial_analysis = Bunch()

@task
@cmdopts([("INPUT=", "I", "input flowcell to run pipeline on")])
def automated_initial_analysis():
    """Run automated_initial_analysis.

    INPUT: flowcell to run pipeline on"""

    options.order("automated_initial_analysis")
    INPUT = options.get("INPUT", None)
    if not INPUT is None:
        yaml_config = options.get("yaml_config", "post_process.yaml")
        run_info = options.get("run_info", "run_info.yaml")
        cl = [" ".join(["automated_initial_analysis.py", yaml_config, INPUT, run_info])]
        run_cmd(cl, INPUT, None, True, "running automated_initial_analysis")

@task
def multi_automated_initial_analysis():
    """Generate command for all flowcells."""
    for fc in options.illumina.flowcell_ids:
        options.automated_initial_analysis.INPUT = os.path.join(options.dirs.data, os.path.basename(fc))
        options.sbatch.jobname = "aia_" + "".join([x[0:2] for x in options.project_name.split("_")]) + fc[7:12]
        oldworkdir = options.sbatch.workdir
        options.sbatch.workdir = os.path.join(options.sbatch.workdir, fc[7:12])
        options.automated_initial_analysis.run_info = os.path.join(options.sbatch.workdir, os.path.basename(fc) + ".yaml")
        call_task("scilife.paver.uppmax.automated_initial_analysis")
        options.sbatch.workdir = oldworkdir
