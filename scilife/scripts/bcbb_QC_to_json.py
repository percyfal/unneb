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
import couchdb
import hashlib
from optparse import OptionParser

import glob
import json
import fnmatch
#from numpy import recarray
import numpy as np

from bcbio.pipeline.config_loader import load_config
from bcbio.broad.metrics import *
from bcbio.log import logger, setup_logging
from bcbio.pipeline.qcsummary import FastQCParser

class MetricsParser():
    """Basic class for parsing metrics"""
    def __init__(self):
        pass
        
    def extract_metrics(self, metrics_file):
        extension_maps = dict(
            filter_metrics=(self._parse_filter_metrics, "FILTER"),
            bc_metrics=(self._parse_bc_metrics, "BARCODE")
            )
        ## Modelled after broad.metrics: here only one file is allowed
        all_metrics = dict()
        for fname in metrics_file:
            fname = metrics_file
            ext = os.path.splitext(fname)[-1][1:]
            try:
                parse_fn, prefix = extension_maps[ext]
            except KeyError:
                parse_fn = None
            if parse_fn:
                with open(fname) as in_handle:
                    for key, val in parse_fn(in_handle).iteritems():
                        if not key.startswith(prefix):
                            key = "%s_%s" % (prefix, key)
                        all_metrics[key] = al
        return all_metrics
            
    def _parse_bc_metrics(self, in_handle):
        data = {}
        for key, val in in_handle.readline().split("\t"):
            data[key] = val
        return data
            
    def _parse_filter_metrics(self, in_handle):
        data = {}
        data["reads_processed"] = 

class ExtendedPicardMetricsParser(PicardMetricsParser):
    """Extend basic functionality and parse all picard metrics"""

    def __init__(self):
        PicardMetricsParser.__init__(self)

    def _get_command(self, in_handle):
        analysis = None
        while 1:
            line = in_handle.readline()
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
        res = dict(command=command, FIRST_OF_PAIR = d, SECOND_OF_PAIR = d, PAIR = d)
        while 1:
            info = in_handle.readline().rstrip("\n").split("\t")
            category = info[0]
            if len(info) <= 1:
                break
            vals = self._read_vals_of_interest(header, header, info)
            res[category] = vals
        return res

    def _parse_dup_metrics(self, in_handle):
        command = self._get_command(in_handle)
        header = self._read_off_header(in_handle)
        info = in_handle.readline().rstrip("\n").split("\t")
        vals = self._read_vals_of_interest(header, header, info)
        histvals = self._read_histogram(in_handle)
        return dict(command=command, metrics = vals, hist = histvals)

    def _parse_insert_metrics(self, in_handle):
        command = self._get_command(in_handle)
        header = self._read_off_header(in_handle)
        info = in_handle.readline().rstrip("\n").split("\t")
        vals = self._read_vals_of_interest(header, header, info)
        histvals = self._read_histogram(in_handle)
        return dict(command=command, metrics = vals, hist = histvals)

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
        self._data = {}
        self._element = None

    def parse(self, fp):
        self._parse_RunInfo(fp)
        return self._data

    def _start_element(self, name, attrs):
        self._element=name
        if name == "Run":
            self._data["Id"] = attrs["Id"]
            self._data["Number"] = attrs["Number"]
        elif name == "FlowcellLayout":
            self._data["FlowcellLayout"] = attrs
        elif name == "Read":
            self._data["Reads"].append(attrs)
            
    def _end_element(self, name):
        self._element=None

    def _char_data(self, data):
        want_elements = ["Flowcell", "Instrument", "Date"]
        if self._element in want_elements:
            self._data[self._element] = data
        if self._element == "Reads":
            self._data["Reads"] = []

    def _parse_RunInfo(self, fp):
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self._start_element
        p.EndElementHandler = self._end_element
        p.CharacterDataHandler = self._char_data
        p.ParseFile(fp)
    

class QCLane(dict):
    """Lane level class for holding qc data"""
    def __init__(self, flowcell, lane ):
        self.lane = lane
        self.bc_metrics = {}
        self.filter_metrics = {}

class QCSample(dict):
    """Sample-level class for holding qc metrics data"""

    _metrics = ["picard_metrics","fastqc","fastq_scr"]

    def __init__(self, flowcell, date, lane, barcode_name, barcode_id, sample_prj, sequence=None, barcode_type=None, genomes_filter_out=None):
        self["sample"] = {}
        self["sample"]["flowcell"] = flowcell
        self["sample"]["date"] = date
        self["sample"]["lane"] = lane
        self["sample"]["barcode_name"] = barcode_name
        self["sample"]["barcode_id"] = barcode_id
        self["sample"]["sample_prj"] = sample_prj
        self["sample"]["sequence"] = sequence
        self["sample"]["barcode_type"] = barcode_type
        self["sample"]["genomes_filter_out"] = genomes_filter_out
        self["metrics"] = {}
        self.picard_files = []
        for m in self._metrics:
            self["metrics"][m] = {}

    def get_name(self, nophix=False):
        if nophix:
            s = "%s_%s_%s_nophix_%s" % (self["sample"]["lane"], self["sample"]["date"], self["sample"]["flowcell"], self["sample"]["barcode_id"])
        else:
            s = "%s_%s_%s_%s"  % (self["sample"]["lane"], self["sample"]["date"], self["sample"]["flowcell"], self["sample"]["barcode_id"])
        return s

class FlowcellQCMetrics(dict):
    """Flowcell level class for holding qc data"""
    _metrics = ["RunInfo", "run_info_yaml"]

    def __init__(self, flowcell_dir, archive_dir):
        self.flowcell_dir = flowcell_dir
        self.archive_dir = archive_dir
        self["_id"] = None
        self["name"] = None
        self["entity_type"] = "FlowcellQCMetrics"
        self["entity_version"] = "0.1"
        self["sample"] = dict()
        self["lane"] = dict()
        self["metrics"] = dict()
        for m in self._metrics:
            self["metrics"][m] = None

    # def __repr__(self):
    #     return "<%s object, version %s>" % (self["type"], self["version"])
        
    def parseRunInfo(self, fn="RunInfo.xml"):
        fp = open(os.path.join(self.archive_dir, fn))
        parser = RunInfoParser()
        data = parser.parse(fp)
        fp.close()
        self["metrics"]["RunInfo"] = data
        self["_id"] = self.get_db_id()
        self["name"] = self.get_id()

    def parse_run_info_yaml(self, fn="run_info.yaml"):
        fp = open(os.path.join(self.archive_dir, fn))
        runinfo = yaml.load(fp)
        fp.close()
        for info in runinfo:
            if not self["lane"].has_key(info["lane"]):
                lane = QCLane(None, info["lane"])
                self["lane"][info["lane"]] = lane
            for mp in info["multiplex"]:
                sample = QCSample(self.get_flowcell(), self.get_date(), info["lane"], mp["name"], mp["barcode_id"], mp["sample_prj"], mp["sequence"], mp["barcode_type"], mp["genomes_filter_out"])
                bc_index = "%s_%s" % (info["lane"], mp["barcode_id"])
                self["sample"][bc_index] = sample
        self["metrics"]["run_info_yaml"] = runinfo

    def get_flowcell(self):
        return self.get("metrics").get("RunInfo").get("Flowcell")
    def get_date(self):
        return self.get("metrics").get("RunInfo").get("Date")
    def get_id(self):
        return self.get("metrics").get("RunInfo").get("Id")
    def get_db_id(self):
        return hashlib.md5(self.get_id()).hexdigest()
    def get_run_id(self, run_prefix=0):
        vals = self["metrics"]["RunInfo"]["Id"].split("_")
        return "%s_%s" % (vals[0], vals[3])

    def to_json(self):
        samples = [self["sample"][s] for s in self["sample"]]
        return json.dumps({'metrics':self["metrics"], 'samples':samples})

    def read_picard_metrics(self):
        picard_parser = ExtendedPicardMetricsParser()
        files = self._get_metrics(self.flowcell_dir)
        # Group files to samples
        for fn in files:
            fn_tgt = os.path.basename(fn).replace("_nophix_", "_")
            re_str = r'(\d+)_(\d+)_([A-Z0-9a-z]+XX)_?([a-zA-Z0-9]+)?-'
            m = re.search(re_str, fn_tgt)
            (lane, date, flowcell, bc) = m.groups()
            bc_index = "%s_%s" % (lane, bc)
            if self["sample"].has_key(bc_index):
                print >> sys.stderr, "reading metrics %s for sample %s" % (fn, bc_index)
            else:
                print >> sys.stderr, "WARNING: no sample %s for metrics %s" % (bc_index, fn)
            self["sample"][bc_index].picard_files.append(fn)
        for s in self["sample"]:
            metrics = picard_parser.extract_metrics(self["sample"][s].picard_files)
            self["sample"][s]["metrics"]["picard_metrics"] = metrics

    def _get_metrics(self, indir, re_str='.*.(align|hs|insert|dup)_metrics'):
        matches = []
        for root, dirnames, filenames in os.walk(indir):
            for fn in filenames:
                if re.match(re_str, fn):
                    matches.append(os.path.join(root, fn))
        return matches

    def read_fastqc_metrics(self):
        for s in self["sample"]:
            d = glob.glob(os.path.join(self.flowcell_dir, "fastqc", "%s_%s_*_%s*" % (self["sample"][s]["sample"]["lane"], self.get_run_id(), self["sample"][s]["sample"]["barcode_id"])))
            fastqc_dir=d[0]
            fqparser = ExtendedFastQCParser(fastqc_dir)
            stats = fqparser.get_fastqc_summary()
            self["sample"][s]["metrics"]["fastqc"] = {'stats':stats}

        
class ExtendedFastQCParser(FastQCParser):
    def __init__(self, base_dir):
        FastQCParser.__init__(self, base_dir)

    def get_fastqc_summary(self):
        metric_labels = ["Per base sequence quality", "Basic Statistics", "Per sequence quality scores",
                         "Per base sequence content", "Per base GC content", "Per sequence GC content",
                         "Per base N content", "Sequence Length Distribution", "Sequence Duplication Levels",
                         "Overrepresented sequences", "Kmer Content"]
        metrics = {x : self._to_dict(self._fastqc_data_section(x)) for x in metric_labels}
        return metrics

    def _to_dict(self, section):
        if len(section) == 0:
            return {}
        header = [x.strip("#") for x in section[0].rstrip("\t").split("\t")]
        d = []
        for l in section[1:]:
            d.append(l.split("\t"))
        data = np.array(d)
        df = {header[i]:data[:,i].tolist() for i in range(0,len(header))}
        return df

        
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
    qc_obj = FlowcellQCMetrics(fc_dir, fc_dir)
    qc_obj.parseRunInfo()
    qc_obj.parse_run_info_yaml()
    qc_obj.read_picard_metrics()
    qc_obj.read_fastqc_metrics()
    couch = couchdb.Server("http://maggie.scilifelab.se:5984")
    try:
        db = couch['qc']
        obj = db.get(qc_obj.get_db_id())
    except:
        options.dry_run=True

    if obj is None:
        if options.dry_run:
            print "DRY_RUN: saving qc data for %s" % qc_obj.get_id()
            print qc_obj
        else:
            db.save(qc_obj)
    else:
        if options.dry_run:
            print "DRY_RUN: updating %s" % qc_obj.get_id()
        else:
            qc_obj["_rev"] = obj.get("_rev")
            db.save(qc_obj)
    

    
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
    
