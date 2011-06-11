from paver.easy import *
from paver.setuputils import setup, find_packages

setup(
    name="unneb-ngs",
    packages=find_packages(),
    version="0.1",
    url="https://github.com/percyfal/unneb",
    author="Per Unneberg",
    author_email="per.unneberg@scilifelab.se",
    install_requires = [
        "PyYAML >= 3.09",
        ]
    )

@task
@needs(['html', "distutils.command.sdist"])
def sdist():
    """Generate docs and source distribution."""
    pass
