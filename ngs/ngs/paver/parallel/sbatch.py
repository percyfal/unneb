"""
sbatch wrapper
"""
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
options.sbatch_template = SBATCH_TEMPLATE
kw = Bunch(
    mail_type = "ALL",
    header = "",
    footer = "",
    constraint = "",
    partition = "node",
    jobname = "paver_sbatch",
)

# TODO: should check that kw has all parameters
def sbatch(command):
    """Wraps an external command in a sbatch template script"""
    command_list = "\n".join(command)
    options.order("sbatch")
    sbatchkw = options.get("sbatch", None)
    kw.update(sbatchkw)
    if kw is None:
        print >> sys.stderr, "sbatch keyword dictionary not defined: please set options for project_id, time etc"
        sys.exit()
    kw.command_str = command_list
    if options.get("bg", False):
        kw.command_str = kw.command_str.replace("\n", " &\n") + " &\nwait\n"
    if kw.jobname == "":
        kw.jobname = "paver_sbatch"
    kw.workdir = os.path.abspath(kw.workdir)
    if options.dry_run:
        print >> sys.stderr, options.sbatch_template.render(**kw)
    else:
        outfile = kw.get("outfile", kw.jobname + ".sh")
        if not outfile is None:
            fp = open(outfile, "w")
            fp.write(options.sbatch_template.render(**kw))
            fp.close()

## Set exec_fn to sbatch
options.exec_fn = dict(fn = sbatch)
