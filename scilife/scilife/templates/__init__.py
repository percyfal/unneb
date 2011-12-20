"""
templates config
"""

import os
from mako.template import Template

TEMPLATE_DIR = os.path.abspath(os.path.dirname(__file__))

SBATCH_HEADER_TEMPLATE = Template('''\
#!/bin/bash -l
TMPDIR=/scratch/$SLURM_JOB_ID

#SBATCH -A ${project_id}
#SBATCH -t ${time}
#SBATCH -o ${jobname}.stdout
#SBATCH -e ${jobname}.stderr
#SBATCH -J ${jobname}
#SBATCH -D ${workdir}
#SBATCH -p ${partition}
#SBATCH -n ${cores}
#SBATCH --mail-type=${mail_type}
#SBATCH --mail-user=${mail_user}

${header}
''')

