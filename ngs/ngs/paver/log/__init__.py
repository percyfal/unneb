import os
from paver.easy import *
import logbook
log = logbook.Logger("ngspaver")

def set_handler(options):
    options.log.dir = options.log.get("dir", path(os.path.curdir) / "log")
    path(options.log.dir).makedirs()
    options.log.logger = log
    options.log.handler = logbook.FileHandler(path(options.log.dir) / "%s.log" % log.name)
    options.log.handler.push_application()

# This is run when importing module?
if not isinstance(options.log, Bunch):
    options.log = Bunch(logger = log,
                        handler = None)
    options.log.dir = path(os.path.curdir) / "log"



