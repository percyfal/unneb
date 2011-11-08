from paver.easy import *
from paver.setuputils import setup, find_packages
import paver.doctools 

setup(
    name="unneb-ngs",
    version="0.2",
    description = "", 
    author="Per Unneberg",
    url="https://github.com/percyfal/unneb",
    packages=find_packages(),
    author_email="per.unneberg@scilifelab.se",
    install_requires = [
        "PyYAML >= 3.09",
        "bcbio-nextgen >= 0.2",
        ],
    test_suite = 'nose.collector',
    scripts = ['scripts/project_paver_init.py']
)

@task
def html():
    """html task"""
    print "html"

@task
@needs(['html', "distutils.command.sdist"])
def sdist():
    """Generate docs and source distribution."""
    pass

