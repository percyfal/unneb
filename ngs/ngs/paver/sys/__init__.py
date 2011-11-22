"""
__init__.py for sys

System related tasks
"""
import os
import glob
from paver.easy import *
from ngs.paver import run_cmd

@task
@cmdopts([('indir=', 'i', 'indir'), ('outdir=', 'o', 'outdir'),
          ('glob=', 'g', 'glob for relink'), ('rename=', 'r', 'comma-separated patterns for renaming')])
def relink(options):
    """Relink a bunch of files.

    Options (set in sys.relink section by default).

    indir
      input directory. Default: os.path.curdir

    outdir
      output directory. Default: os.path.curdir

    glob
      file glob. List of files to relink

    rename
      comma-separated string of format \"from,to\". After linking, attempts to rename symlinks
    """
    options.order("relink")
    glob_str = os.path.join(path(os.path.abspath(options.get("indir", os.path.abspath(os.path.curdir))))) / options.get("glob", "")
    files = glob.glob(glob_str)
    for f in files:
        tgt = path(os.path.join(os.path.abspath(options.get("outdir", os.path.abspath(os.path.curdir))), os.path.basename(f)))
        if options.get("rename", False):
            rfrom, rto = options.get("rename").split(",")
            tgt = path(tgt.replace(rfrom, rto))
        if tgt.exists():
            print >> sys.stderr, "target file %s exists: not symlinking" % tgt
            continue
        if options.dry_run:
            print "symlinking %s -> %s" % (tgt, f)
        else:
            os.symlink(f, tgt)

@task
@cmdopts([('glob=', 'g', 'glob for pbzip2'), ('decompress','d','decompress'), ('opts=', 'o', 'options')])
def pbzip2(options, info):
    """Run pbzip2 on a bunch of files.

    Options (set in sys.pbzip2 section by default).

    basedir
       directory to work in. Default: os.path.curdir

    pattern
       file glob to look for under basedir. Default: None

    opts
       command line options to pass to pbzip2. Default: -v

    decompress
       decompress file. Default: False
    """
    options.order('pbzip2')
    basedir = options.get('basedir', path(os.path.curdir))
    opts = options.get('opts', "-v")
    decompress = options.get('decompress', False)
    pattern = options.get('glob', None)
    if decompress:
        opts = opts + "d"
    if not pattern is None:
        files = basedir.walkfiles(pattern)
        cl = [" ".join(['pbzip2', opts, pattern])]
        if files:
            run_cmd(cl, files.next(), None, options.run, "Running pbzip2")

@task
@cmdopts([('archive=', 'a', 'archive for tar'), ('glob=', 'g', 'glob for tar'), ('opts=', 'o', 'options')])
def tar(options, info):
    """Run tar on a bunch of files.

    Options - set in sys.tar section

    archive
       archive file to (un)tar
    
    pattern
       file glob for files to include in archive
    """
    options.order('tar')
    opts = options.get('opts', "")
    pattern = options.get('glob', None)
    archive = options.get('archive', None)
    if not archive is None:
        if pattern is None:
            cl = [" ".join(['tar', opts, archive])]
        else:
            cl = [" ".join(['tar', opts, archive, pattern])]
        try:
            run_cmd(cl, None, None, options.run, "Running tar")
        except:
            pass

@task
@consume_args
def copy(args):
    """Copy files from src to dest."""
    options.order('copy')
    opts = options.get('opts', "-i")
    src, dest = args
    if not src is None and not dest is None:
        sh(" ".join(["cp", opts, src, dest]))

