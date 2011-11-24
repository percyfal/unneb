#!/usr/bin/env python
"""
Calculate target enrichment using pybedtools

Usage:
    teqc_enrichment.py [options] -abam <bamfile> -b <bedfile>
"""

import os
import sys
import pybedtools
from time import gmtime, strftime
from optparse import *
from pybedtools import genome_registry

def main(bamfile, bedfile):
    abam = pybedtools.BedTool(bamfile)
    bed = pybedtools.BedTool(bedfile)
    on_target = abam.intersect(bed).count()
    mapped = abam.count()
    print "Mapped reads:\t%s" % mapped
    print "On target:\t%s" % on_target
    target_size = 0
    for feature in iter(bed):
        target_size += feature.end - feature.start
    print "Target size:\t%s" % target_size
    try:
        chroms = getattr(genome_registry, options.build)
        genome_size = sum([x[1] for i in chroms.values()])
    except:
        pass
    print "Genome size:\t%s" % genome_size
        
    outfile = os.path.abspath(os.path.splitext(bamfile)[0] + ".enrichment_metrics")
    target_fraction = float(target_size) / float(genome_size)
    on_target_fraction = float(on_target) / float(mapped)
    fp = open(outfile, "w")
    fp.write("# Run date: %s\n" % strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
    fp.write("# Command: %s\n" % " ".join(sys.argv))
    fp.write("MAPPED\tON_TARGET\tTARGET_SIZE\tGENOME_SIZE\tENRICHMENT\n")
    fp.write("%s\t%s\t%s\t%s\t%.5f\n" % (mapped, on_target, target_size, genome_size, on_target_fraction/target_fraction))
    fp.close()
    
if __name__ == "__main__":
    usage = """teqc_enrichment.py [options] bamfile bedfile"""
    parser = OptionParser(usage=usage)
    parser.add_option("-b", "--build", dest="build", default="hg19")
    parser.add_option("-f", "--flank", dest="flank", default=None)
    (options, args) = parser.parse_args()
    if len(args) < 2:
        print __doc__
        sys.exit()
    kwargs = dict()
    main(*args, **kwargs)
