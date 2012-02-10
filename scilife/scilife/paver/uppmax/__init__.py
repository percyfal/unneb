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
        options.automated_initial_analysis.yaml_config = "/bubo/home/h1/perun/config/peru_post_process.yaml"
        options.automated_initial_analysis.INPUT = os.path.join(options.dirs.data, os.path.basename(fc))
        options.automated_initial_analysis.run_info = os.path.join(options.dirs.data, os.path.basename(fc), "project_run_info.yaml")
        options.sbatch.jobname = "aia_" + fc[7:12]
        call_task("scilife.paver.uppmax.automated_initial_analysis")
