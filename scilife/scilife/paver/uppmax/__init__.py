"""
uppmax helper functions
"""
import os


from paver.easy import *
import ngs.paver
from ngs.paver import run_cmd

from scilife.templates import TEMPLATE_DIR, SBATCH_HEADER_TEMPLATE


@task
@cmdopts([("INPUT=", "I", "input flowcell to run pipeline on")])
def project_analysis_pipeline():
    """Run project_analysis_pipeline

    INPUT: flowcell to run pipeline on"""

    options.order("project_analysis_pipeline")
    INPUT = options.get("INPUT", None)
    if not INPUT is None:
        yaml_config = options.get("yaml_config", "post_process.yaml")
        run_info = options.get("run_info", "run_info.yaml")
        cl = [" ".join(["project_analysis_pipeline.py", yaml_config, INPUT, run_info])]
        run_cmd(cl, INPUT, None, True, "running project_analysis_pipeline")
