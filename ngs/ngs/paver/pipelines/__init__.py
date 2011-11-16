import os
from paver.easy import *
from ngs.paver import run_cmd

@task
def project_exome_pipeline_cl(options):
    """Construct cl for project_exome_pipeline"""
    options.sbatch.kw.update(jobname = "pep_cl_%s" % os.path.basename(options.sbatch.kw.workdir))
    cl = [" ".join(['project_exome_pipeline.py', options.project_config, 
          options.sbatch.kw.workdir, os.path.join(options.dirs.data, options.item, "project_run_info.yaml")])]
    run_cmd(cl)
