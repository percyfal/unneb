"""
Classes and functions for pipelines
"""
import sys
import os
from mako.template import Template

VERSION = "0.1.0"

def make_sbatch(mail, jobname, project, application, mailtype="ALL", report="all_samples_summary.pdf", data_dir="./", config="analysis.yaml", analysis_dir="./", nodes=1, partition="node", time="150:00:00"):
    #if application not in set(['exome_pipeline.py']):
    #    Exception("Application " + application + " unknown")
    tmpl = Template(sbatch_template)
    return tmpl.render(t_mail=mail, t_jobname=jobname, t_project=project, t_application=application, t_nodes=nodes, t_mailtype=mailtype, t_report=report, t_data_dir=data_dir, t_config=config, t_analysis_dir=analysis_dir, t_partition=partition, t_time=time)

sbatch_template=r"""
#!/bin/bash
ANALYSIS_DIR=\"${t_analysis_dir}\"
DATA_DIR=\"${t_data_dir}\"
CONFIG=\"${t_config}\"
MAILTO=\"${t_mail}\"
REPORT=\"${t_report}\"

# The pipeline does not rely on this variable.
# This is just to prevent system's /tmp filling up
# if some program *does* rely on it.
TMPDIR=/scratch/$SLURM_JOB_ID

#SBATCH -p ${t_partition}
#SBATCH -N ${t_nodes}
#SBATCH -t ${t_time}
#SBATCH -J ${t_jobname}
#SBATCH -A ${t_project}
#SBATCH --mail-user=${t_mail}
#SBATCH --mail-type=${t_mailtype}
#SBATCH -o ${t_jobname}.out
#SBATCH -e ${t_jobname}.err

## Letting group members rw the runs
## WARNING: \"uppmax\" group is maybe too lax
umask 007

${t_application} $CONFIG $ANALYSIS_DIR $DATA_DIR
"""
