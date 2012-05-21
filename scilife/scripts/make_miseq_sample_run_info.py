#!/usr/bin/env python
# File: make_miseq_sample_run_info.py
# Created: Tue Mar 27 17:10:57 2012
# Copyright (C) 2012 by Per Unneberg
#
# Author: Per Unneberg
#

"""
Make sample run info file for miseq data.
"""

import sys
import os
from optparse import OptionParser

import csv
import codecs
import unicodedata
import yaml
import glob
import re

def main(flowcell_dir, csv_sample_sheet):
    multiplex_dir = os.path.join(flowcell_dir, "Data/Intensities/BaseCalls/Multiplex")
    fileObj = codecs.open( csv_sample_sheet, "r", "latin-1" )
    lane = 1
    samples = False
    mp = dict(details=list())
    for row in fileObj.readlines():
        if samples:
            s = dict()
            rdata = row.split(",")
            sample = rdata[0].split(" ")[0].encode("ascii")
            s['description'] = sample
            s['lane'] = str(lane)
            s['files'] = get_files(multiplex_dir,sample)
            s['analysis'] = 'Align_standard'
            s['genome_build'] = 'hg19'
            s['hybrid_target'] = '/proj/a2010002/projects/data/seqcap/agilent/targets/SureSelect_All_Exon_50mb_with_annotation_hg19_bed.interval_list'
            s['hybrid_bait'] = '/proj/a2010002/projects/data/seqcap/agilent/probes/SureSelect_All_Exon_50mb_with_annotation_hg19_bed.interval_list'
            lane = lane + 1
            mp["details"].append(s)
        if row.startswith("Sample_ID"):
            header = row.split(",")
            samples = True
    yaml.add_representer(unicode, lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:str', value))
    print yaml.dump(mp)


def get_files(multiplex_dir, sample):
    reads_glob = os.path.join(multiplex_dir, "s_G1_L001_R*_00_" + sample + "*.fastq.gz")
    reads = glob.glob(reads_glob)
    return reads

def _to_ascii(s):
    return unicodedata.normalize('NFKD', unicode(s)).encode('ascii', 'ignore')

    
if __name__ == "__main__":
    usage = """
    make_miseq_sample_run_info.py <flowcell_dir> <csv_sample_sheet>
    """
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    if len(args) < 2:
        print __doc__
        sys.exit()
    kwargs = dict()
    main(*args, **kwargs)
