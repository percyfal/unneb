"""
Sample pavement file
"""

import os
import sys

from paver.easy import *
from unneb.paver.misc import *

options(
    rsync = Bunch(
        program = "rsync",
        user = "perun",
        host = "biologin.uppmax.uu.se",
        dest = "tabort",
        src = "tabort"
        )
    )
