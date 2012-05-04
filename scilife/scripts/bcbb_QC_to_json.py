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
import yaml
import xml.parsers.expat
from optparse import OptionParser

import glob
import json
import fnmatch

from bcbio.pipeline.config_loader import load_config
from bcbio.broad.metrics import *
from bcbio.log import logger, setup_logging
from bcbio.pipeline.qcsummary import FastQCParser

class MetricsParser():
    """Basic class for parsing metrics"""
    def __init__(self):
        pass

    def extract_metrics(self, metrics_file):
        pass

    def _parse_bc_metrics(self, in_handle):
        pass
    
    def _parse_filter_metrics(self, in_handle):
        pass

class ExtendedPicardMetricsParser(PicardMetricsParser):
    """Extend basic functionality and parse all picard metrics"""

    def __init__(self):
        PicardMetricsParser.__init__(self)

    def _get_command(self, in_handle):
        analysis = None
        while 1:
            line = in_handle.readline()
            print line
            if line.startswith("# net.sf.picard.analysis") or line.startswith("# net.sf.picard.sam"):
                break
        return line.rstrip("\n")

    def _read_off_header(self, in_handle):
        while 1:
            line = in_handle.readline()
            if line.startswith("## METRICS"):
                break
        return in_handle.readline().rstrip("\n").split("\t")


    def _read_vals_of_interest(self, want, header, info):
        want_indexes = [header.index(w) for w in header]
        vals = dict()
        for i in want_indexes:
            vals[header[i]] = info[i]
        return vals

    def _parse_align_metrics(self, in_handle):
        command = self._get_command(in_handle)
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

class RunInfoParser():
    """RunInfo parser"""
    def __init__(self):
        self.data = dict()
        self.element = None

    def parse(self, fp):
        self._parse_RunInfo(fp)

    def _start_element(self, name, attrs):
        self.element=name
        if name == "Run":
            self.data["Id"] = attrs["Id"]
            self.data["Number"] = attrs["Number"]
        elif name == "FlowcellLayout":
            self.data["FlowcellLayout"] = attrs
        elif name == "Read":
            self.data["Reads"].append(attrs)
            
    def _end_element(self, name):
        self.element=None

    def _char_data(self, data):
        want_elements = ["Flowcell", "Instrument", "Date"]
        if self.element in want_elements:
            self.data[self.element] = data
        if self.element == "Reads":
            self.data["Reads"] = []
            

    def _parse_RunInfo(self, fp):
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self._start_element
        p.EndElementHandler = self._end_element
        p.CharacterDataHandler = self._char_data
        p.ParseFile(fp)
    
    def to_json(self):
        return json.dumps(self.data)

class QCLane():
    """Lane level class for holding qc data"""
    def __init__(self, flowcell, lane ):
        pass

class QCSample():
    """Sample-level class for holding qc metrics data"""

    _metrics = ["align_metrics",
                "dup_metrics","hs_metrics","insert_metrics",
                "eval_metrics","fastqc","fastq_scr"]

    def __init__(self, flowcell, date, lane, barcode_name, barcode_id, sample_prj, sequence=None, barcode_type=None, genomes_filter_out=None):
        self.sample = {}
        self.sample["flowcell"] = flowcell
        self.sample["date"] = date
        self.sample["lane"] = lane
        self.sample["barcode_name"] = barcode_name
        self.sample["barcode_id"] = barcode_id
        self.sample["sample_prj"] = sample_prj
        self.sample["sequence"] = sequence
        self.sample["barcode_type"] = barcode_type
        self.sample["genomes_filter_out"] = genomes_filter_out
        self.metrics = {}
        for m in _metrics:
            self.metrics[m] = {}
    
    def to_json(self):
        return json.dumps({'sample':self.sample, 'metrics':self.metrics})

class QCFlowcell():
    """Flowcell level class for holding qc data"""
    _metrics = ["RunInfo", "run_info_yaml"]

    def __init__(self, flowcell_dir, archive_dir):
        self.flowcell_dir = flowcell_dir
        self.archive_dir = archive_dir
        self.samples = dict()
        self.lanes = dict()
        self.metrics = dict()
        for m in self._metrics:
            self.metrics[m] = None

    def parseRunInfo(self, fn="RunInfo.xml"):
        fp = open(os.path.join(self.archive_dir, fn))
        parser = RunInfoParser()
        parser.parse(fp)
        fp.close()
        self.metrics["RunInfo"] = parser.to_json()

    def parse_run_info_yaml(self, fn="run_info.yaml"):
        fp = open(os.path.join(self.archive_dir, fn))
        runinfo = yaml.load(fp)
        fp.close()
        for info in runinfo:
            if not self.lanes.has_key(info["lane"]):
                lane = QCLane(None, info["lane"])
        self.metrics["run_info_yaml"] = json.dumps(runinfo)
        
    def to_json(self):
        return self.metrics

    def read_picard_metrics(self):
        picard_parser = ExtendedPicardMetricsParser()
        files = self.get_metrics(self.flowcell_dir)
        for fn in files:
            re_str = r'(\d+)_(\d+)_([A-Z0-9a-z]+XX)_?([a-zA-Z0-9]+)?-'
            m = re.search(re_str, fn)
            (lane, date, flowcell, bc) = m.groups()
            sample = "_".join([lane, str(bc)])
            metrics = picard_parser.extract_metrics([mf])
            print metrics

    def _get_metrics(self, indir, re_str='.*.(align|hs|insert|dup)_metrics'):
        matches = []
        for root, dirnames, filenames in os.walk(indir):
            for fn in filenames:
                fn = os.path.basename(mf).replace("_nophix_", "_")
                if re.match('', fn):
                    matches.append(os.path.join(root, fn))
        return matches


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
    qc_obj = QCFlowcell(fc_dir, fc_dir)
    qc_obj.parseRunInfo()
    qc_obj.parse_run_info_yaml()
    print qc_obj.to_json()
    sys.exit()
#     for mf in metrics_files:
#         fn = os.path.basename(mf).replace("_nophix_", "_")
#         print fn
#         if fn.endswith("bc.metrics"):
#             re_str = r'(\d+)_(\d+)_([A-Z0-9a-z]+XX).*'
#             m = re.search(re_str, fn)
#             (lane, date, flowcell) = m.groups()
#             bc = None
#         elif fn.endswith("filter.metrics"):
#             pass
# #        else:
        
    fastqc_dir = "/Users/peru/Org/ScilifeCore/delivery_data/projects/SOLiD_JPA/fastqc/GMS_D1_F3.single_fastqc"
    fastqc_file = "/Users/peru/Org/ScilifeCore/delivery_data/projects/SOLiD_JPA/fastqc/GMS_D1_F3.single_fastqc/fastqc_data.txt"
    fqparser = FastQCParser(fastqc_dir)
    graphs = fqparser.get_fastqc_graphs()
    stats, overrep = fqparser.get_fastqc_summary()
    print stats
    print overrep
    print graphs

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
    
