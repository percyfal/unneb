"""
bedtools wrappers
"""
import os
import glob
from paver.easy import *
from ngs.paver import run_cmd

options.bedtools_default = Bunch(
    bedtools_home = os.path.abspath("./"),
    opts = "",
)

##############################
## Tasks
##############################
@task
@cmdopts([("abam=", "m", "bam file"), ("b=", "b", "bed file b"),
          ("a=", "a", "bed file a"),
          ("d", "d", "Report depth"), ("output=", "o", "output file")])
def coverageBed():
    """coverageBed wrapper"""
    options.order("coverageBed", "bedtools_default")
    a = options.get("a", None)
    b = options.get("b", None)
    abam = options.get("abam", None)
    d = options.get("d", False)
    output = options.get("output", "/dev/stdout")
    aopt = "-a"
    if not abam is None:
        aopt = "-abam"
        a = abam
    opts = options.get("opts", "")
    if d:
        opts += "-d"
    if not a is None:
        cl = [" ".join(["coverageBed", opts, aopt, a, "-b", b, ">", output])]
        run_cmd(cl, a, output, options.run, None)

@task
@cmdopts([("bams=", "a", "glob of bam files"), ("bed=", "b", "bed file")])
def multiBamCov():
    """multiBamCov wrapper"""
    options.order("multiBamCov", "bedtools_default")
    bams = options.get("bams", None)
    bamfiles = glob.glob(bams)
    bed = options.get("bed", None)
    if bamfiles is None or bed is None:
        return
    outfile = options.get("outfile", os.path.splitext(bamfiles[0])[0] + "-multiBamCov.txt")
    opts = options.get("opts", "")
    cl = [" ".join([path(options.get("bedtools_home"))/ "multiBamCov", "-bams", os.path.abspath(os.path.join(options.get("workdir", "./"), bams)), "-bed", bed, opts])]
    run_cmd(cl, bamfiles[0], outfile, options.get("run"), None)
    
