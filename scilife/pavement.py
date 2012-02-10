from paver.easy import *
from paver.setuputils import setup, find_packages
import paver.doctools 

setup(
    name="scilife-ngs",
    version="0.1.1",
    description = "", 
    author="Per Unneberg",
    url="https://github.com/percyfal/unneb",
    packages=find_packages(),
    author_email="per.unneberg@scilifelab.se",
    install_requires = [
        "PyYAML >= 3.09",
        "unneb-ngs",
        "asciitable",
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

