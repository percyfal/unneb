from paver.easy import *
from paver.setuputils import setup
import paver.doctools 

setup(
    name="unneb-ngs",
    version="0.1",
    description = "", 
    author="Per Unneberg",
    url="https://github.com/percyfal/unneb",
    packages=['test'],
    author_email="per.unneberg@scilifelab.se",
    install_requires = [
        "PyYAML >= 3.09",
        ],
    test_suite = 'nose.collector',
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

