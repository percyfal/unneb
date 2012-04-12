#!/usr/bin/env python
# File: bcbb_QC_to_json.py
# Created: Thu Apr  5 11:34:59 2012
# Copyright (C) 2012 by Per Unneberg
#
# Author: Per Unneberg
#
"""
Collect and convert bcbb output metrics to json

Usage:
  bcbb_QC_to_json.py config flowcellid [--dry_run --verbose]

"""

import os
import sys
import re
from optparse import OptionParser

import glob
import json
import fnmatch

from bcbio.pipeline.config_loader import load_config
from bcbio.broad.metrics import *
from bcbio.log import logger, setup_logging
from bcbio.pipeline.qcsummary import FastQCParser

class ExtendedPicardMetricsParser(PicardMetricsParser):
    """Extend basic functionality and parse all metrics"""

    def __init__(self):
        PicardMetricsParser.__init__(self)

    def _read_vals_of_interest(self, want, header, info):
        want_indexes = [header.index(w) for w in header]
        vals = dict()
        for i in want_indexes:
            vals[header[i]] = info[i]
        return vals

    def _parse_align_metrics(self, in_handle):
        header = self._read_off_header(in_handle)
        d = dict([[x, []] for x in header])
        res = dict(FIRST_OF_PAIR = d, SECOND_OF_PAIR = d, PAIR = d)
        while 1:
            info = in_handle.readline().rstrip("\n").split("\t")
            category = info[0]
            if len(info) <= 1:
                break
            vals = self._read_vals_of_interest(header, header, info)
            res[category] = vals
        return res

    def _parse_dup_metrics(self, in_handle):
        header = self._read_off_header(in_handle)
        info = in_handle.readline().rstrip("\n").split("\t")
        vals = self._read_vals_of_interest(header, header, info)
        histvals = self._read_histogram(in_handle)
        return dict(metrics = vals, hist = histvals)

    def _parse_insert_metrics(self, in_handle):
        header = self._read_off_header(in_handle)
        info = in_handle.readline().rstrip("\n").split("\t")
        vals = self._read_vals_of_interest(header, header, info)
        histvals = self._read_histogram(in_handle)
        return dict(metrics = vals, hist = histvals)

    def _read_histogram(self, in_handle):
        labels = self._read_to_histogram(in_handle)
        vals = dict([[x, []] for x in labels])
        while 1:
            line = in_handle.readline()
            info = line.rstrip("\n").split("\t")
            if len(info) < len(labels):
                break
            for i in range(0, len(labels)):
                vals[labels[i]].append(info[i])
        return vals

    def _read_to_histogram(self, in_handle):
        while 1:
            line = in_handle.readline()
            if line.startswith("## HISTOGRAM"):
                break
        return in_handle.readline().rstrip("\n").split("\t")

class QCSample():
    """Class for holding qc metrics data"""

    labels = ["name","filename","flowcell","date",
              "lane","bc","bc_name"]
    metrics = ["align_metrics",
              "dup_metrics","hs_metrics","insert_metrics",
              "eval_metrics","fastqc","fastq_scr"]

    def init__(self, name, filename, flowcell, date, lane, bc, bc_name):
        self.sample = {}
        self.sample["name"] = name
        self.sample["filename"] = filename
        self.sample["flowcell"] = flowcell
        self.sample["date"] = date
        self.sample["lane"] = lane
        self.sample["bc"] = bc
        self.sample["bc_name"] = bc_name
        self.metrics = {}
        for m in metrics:
            self.metrics[m] = {}
    
    def to_json(self):
        pass
    
def main(config_file, fc_dir, run_info_yaml=None):
    config = load_config(config_file)
    if config.get("qcdb", None) is None:
        sys.exit()
    else:
        qcdb_config = config.get("qcdb", {})
    analysis = config.get("analysis", {})
    setup_logging(config)
    qcdb_store_dir = qcdb_config.get("qcdb_store_dir", None)
    run_main(fc_dir, qcdb_store_dir)

def run_main(fc_dir, qcdb_store_dir):
    metrics_files = _get_metrics(fc_dir)
    picard_parser = ExtendedPicardMetricsParser()
 
    for mf in metrics_files:
        fn = os.path.basename(mf)
        #(lane, date, flowcell, bc) = fn.split("_")
        re_str = r'(\d+)_(\d+)_([A-Z0-9a-z]+XX)_?([a-zA-Z0-9]+)?-'
        m = re.search(re_str, fn)
        (lane, date, flowcell, bc) = m.groups()
        sample = "_".join([lane, str(bc)])
        #print "%s %s %s %s %s" % (sample, lane, date, flowcell, bc)
        #print mf
        metrics = picard_parser.extract_metrics([mf])
        #print json.dump(metrics, sys.stdout)
        
    fastqc_dir = "/Users/peru/Org/ScilifeCore/delivery_data/projects/SOLiD_JPA/fastqc/GMS_D1_F3.single_fastqc"
    fastqc_file = "/Users/peru/Org/ScilifeCore/delivery_data/projects/SOLiD_JPA/fastqc/GMS_D1_F3.single_fastqc/fastqc_data.txt"
    fqparser = FastQCParser(fastqc_dir)
    graphs = fqparser.get_fastqc_graphs()
    stats, overrep = fqparser.get_fastqc_summary()
    print stats
    print overrep
    print graphs
#def _read_metrics(infile):
    

def _get_metrics(indir):
    matches = []
    for root, dirnames, filenames in os.walk(indir):
        for filename in fnmatch.filter(filenames, '*metrics'):
            matches.append(os.path.join(root, filename))
    return matches

                                 

if __name__ == "__main__":
    usage = """
bcbb_QC_to_json.py config flowcellid
"""
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      default=False)
    parser.add_option("-n", "--dry_run", dest="dry_run", action="store_true",
                      default=False)

    (options, args) = parser.parse_args()
    if len(args) != 2:
        print __doc__
        sys.exit()

    kwargs = dict(
        )
    main(*args, **kwargs)
    
