import os
from mako.template import Template
from paver.easy import *


SBATCH_TEMPLATE = Template('''\
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
<%
if (constraint):
    constraint_str = "#SBATCH -C " + constraint
else:
    constraint_str = ""
%>
${constraint_str}
${header}
${command_str}
${footer}
''')

options.sbatch.template = SBATCH_TEMPLATE
    # kw = Bunch(
    #     project_id = '',
    #     time = "50:00:00",
    #     constraint = '',
    #     jobname = '',
    #     workdir = os.path.curdir,
    #     partition = 'node',
    #     cores = '8',
    #     mail_type = 'ALL',
    #     mail_user = '',
    #     header = '',
    #     footer = '',
    #     command_str = '',
    #     )


def sbatch(command):
    """Wraps an external command in a sbatch template script"""
    kw = options.sbatch.kw
    kw.command_str = command
    if options.dry_run:
        print >> sys.stderr, options.sbatch.template.render(**kw)
    else:
        outfile = options.sbatch.kw.get("outfile", None)
        if not outfile is None:
            fp = open(outfile, "w")
            fp.write(options.sbatch.template.render(**kw))
            fp.close()

## Set exec_fn to sbatch
options.exec_fn = dict(fn = sbatch)
