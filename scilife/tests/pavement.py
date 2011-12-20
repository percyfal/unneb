import sys
import os
from paver.easy import *
from mako.template import Template
from mako.lookup import TemplateLookup
from scilife.templates import TEMPLATE_DIR
import scilife.utils

options(
    # fcid = "/bubo/proj/a2010002/nobackup/illumina/110929_SN1018_0028_BB024JACXX",
    # run_info = "/bubo/proj/a2010002/archive/110929_SN1018_0028_BB024JACXX/run_info.yaml",
    # project_info = "/bubo/home/h1/perun/config/post_process.yaml",
    fcid = "/datad/projects/a2010002/projects/e_hellstrom_11_01/flowcells/111017_AD072NACXX",
    run_info ="/datad/projects/a2010002/projects/e_hellstrom_11_01/flowcells/111017_AD072NACXX/project_run_info.yaml",
    project_info = "/home/peru/config/post_process.yaml",
    intermediate = "/datad/projects/a2010002/projects/e_hellstrom_11_01/intermediate/nobackup/111017_AD072NACXX_paver",
    )


mylookup = TemplateLookup(directories=[TEMPLATE_DIR])

kw = dict(
    config=dict(
        results = "/datad/projects/a2010002/projects/e_hellstrom_11_01/intermediate/nobackup/111017_AD072NACXX_paver"),
    )

@task
def make_mako_report():
    """Make a simple mako report.

    Generates output for several mako files."""
    coverage_tmpl = mylookup.get_template("coverage_analysis.mako")
    coverage_tmpl.render(**kw)
    
