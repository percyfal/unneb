#!/usr/bin/env python
"""Collect QC metrics from /proj/a2010002/projects

Usage:
  collect_QC_metrics.py [--dry_run --verbose]

Simple script for collecting QC metrics and syncing
files /proj/a2010002/projects/data/QC. Currently file
globs are hardcoded, which means the following files
will be targeted:

  - *.align_metrics
  - *.hs_metrics
  - *.insert_metrics
  - *.dup_metrics
  - *.PicardDup_metrics

Timing: it takes approximately 10 minutes to scan the directories.
Therefore, I keep a simple database consisting of a list of
the files. 
"""

import os
import sys
import re
from optparse import OptionParser

import json
import glob
import shutil
import fnmatch
import pickle

QC_DIR="/proj/a2010002/projects/data/QC"
PROJECT_DIR="/proj/a2010002/projects"

# Uninteresting directories - edit at will
FILTER=['mpileup_test', 'agilent_kinome', 'delivery_reports', 'patriks',
        'test', 'a_lindblom_11_01.old','data', 'single_lane_deliveries',
        'Sample_1168', 'fastq_screen', 'software',  '101122_SN139_0199_B80HM7ABXX',
        'pelins_barcode', 'truecrypt']

# Database of transferred files
DBFILE=".QCmetricsdb"
JSONDBFILE=".QCmetrics.json"

# Dictionary of extension types
mtypes = dict(align_metrics = "align_metrics",
              dup_metrics = "dup_metrics",
              insert_metrics = "insert_metrics",
              eval_metrics = "eval_metrics",
              gc_metrics = "gc_metrics",
              hs_metrics = "hs_metrics"
              )

def main():
    # Make a dictionary of project names
    glob_str = os.path.join(PROJECT_DIR, "*")
    dirlist = [x for x in glob.glob(glob_str)]
    projects = [os.path.basename(x) for x in filter(_filter_fun, dirlist)]

    # Read database file if it exists
    qc = dict()
    if os.path.exists(os.path.join(QC_DIR, DBFILE)):
        fp = open(os.path.join(QC_DIR, DBFILE), "r")
        qc = pickle.load(fp)
        fp.close()

    # for p in projects:
    #     files = qc[p]["FILES"]
    #     newfiles = []
    #     for x in files:
    #         newfiles.append( _classify_file(x[0]))
    #     qc[p]["FILES"] = newfiles

    # fp = open(os.path.join(QC_DIR, DBFILE), "w")
    # pickle.dump(qc, fp)
    # fp.close()
    #print qc

    # Loop projects for metrics files of interest
    metrics = dict()
    for p in projects:
        indir = os.path.join(PROJECT_DIR, p)
        metrics[p] = dict()
        metrics[p]["PRJ_MODIFICATION_TIME"] = os.path.getmtime(indir)
        if qc.has_key(p) and not options.init_db:
            if qc[p]["PRJ_MODIFICATION_TIME"] > metrics[p]["PRJ_MODIFICATION_TIME"] or options.force:
                print >> sys.stderr, "Project %s modified since last run; doing file metrics collection" % p
                if options.verbose:
                    print "Scanning project %s" % p
                    files = _get_metrics(indir)
                    metrics[p]["FILES"] = [_classify_file(x,p) for x in files]
                    qc[p].update(metrics[p])
            else:
                print >> sys.stderr, "Project %s not modified: not doing anything" % p
        else:
            print >> sys.stderr, "Project %s not previously in database: adding" % (p)
            files = _get_metrics(indir)
            if options.verbose:
                print >> sys.stderr, "Added metrics files %s" % (",".join(files))
            metrics[p]["FILES"] = [_classify_file(x, p) for x in files]
            qc[p] = metrics[p]

    # Save database file
    fp = open(os.path.join(QC_DIR, DBFILE), "w")
    pickle.dump(qc, fp)
    fp.close()
    fp = open(os.path.join(QC_DIR, JSONDBFILE), "w")
    json.dump(qc, fp)
    fp.close()

    # Traverse all projects, adding the metrics files to the file tree looking like:
    # QC/project/flowcellid/*.metrics
    # flowcellid is either a real flowcell or a virtual run as defined by bcbb

    # The virtual runs effectively means that there is no way of
    # knowing which file belongs to which without having the
    # corresponding yaml files.
    if options.init_db:
        metrics = qc
    for p in metrics.keys():
        _safe_make_dir(os.path.join(QC_DIR, p))
        try:
            qcfiles = metrics[p]["FILES"]
            for d in qcfiles:
                _copy_file(d['file'], p, d['date'], d['flowcellid'])
        except:
            pass

        
def _copy_file(f, p, date, flowcellid):
    label = ""
    if not date is None and not flowcellid is None:
        label = "%s_%s" % (date, flowcellid)
    outdir = os.path.join(QC_DIR, p, label)
    _safe_make_dir(outdir)
    src = f
    tgt = os.path.join(outdir, os.path.basename(f))
    
    if options.dry_run:
        print >> sys.stderr, "Copying %s to %s" % (src, tgt)
    else:
        if not os.path.exists(tgt):
            if options.verbose:
                print >> sys.stderr, "Copying %s to %s" % (src, tgt)
            shutil.copyfile(src, tgt)
        else:
            print >> sys.stderr, "WARNING: %s already exists; not overwriting" % tgt
    

def _classify_file(f, p):
    (prefix, ext) = os.path.splitext(f)
    mtype = None
    method = "bcbb"
    lane = None
    bc = None
    sample = None
    date = None
    flowcellid = None
    flowcelltype = None
    try:
        mtype = mtypes[ext.lstrip(".")]
    except:
        pass

    if not ext:
        try:
            f.endswith("picardDup_metrics")
            mtype = "dup_metrics"
            method = "custom"
            sample = os.path.basename(f).rstrip("picardDup_metrics")
        except:
            print >> sys.sterr, "WARNING: unknown filetype %s" % f
    fcre = r'^(\d+)_(\d{6})_([0-9A-Z]+)_?(\d+)?'
    fcre_with_sample = r'^(\d+)_([0-9A-Za-z]+)_(\d{6})_([0-9A-Z]+)'
    m = re.match(fcre, os.path.basename(f))
    if m:
        lane = m.group(1).strip()
        date = m.group(2).strip()
        flowcellid = m.group(3).strip()
        bc  = m.group(4).strip() if m.group(4) else None
        sample = bc
    else:
        m = re.match(fcre_with_sample, os.path.basename(f))
        if m:
            lane = m.group(1).strip()
            sample = m.group(2).strip()
            date = m.group(3).strip()
            flowcellid = m.group(4).strip()
            bc = sample
        
    if flowcellid:
        if len(flowcellid) == 6:
            flowcelltype = "virtual"
        else:
            flowcelltype = "illumina"

    # Add target file info
    label = ""
    if not date is None and not flowcellid is None:
        label = "%s_%s" % (date, flowcellid)
    outdir = os.path.join(QC_DIR, p, label)
    tgt = os.path.join(outdir, os.path.basename(f))
    
    return dict(file=f, target=tgt, mtype=mtype, method=method, lane=lane, flowcellid=flowcellid, flowcelltype=flowcelltype, date=date, bc=bc, sample=sample)

def _safe_make_dir(d):
    if os.path.exists(d):
        return
    print >> sys.stderr, "Making directory %s" % d
    if options.dry_run:
        return
    os.mkdir(d)

def _get_metrics(indir):
    matches = []
    for root, dirnames, filenames in os.walk(indir):
        for filename in fnmatch.filter(filenames, '*metrics'):
            matches.append(os.path.join(root, filename))
    return matches

def _filter_fun(name):
    ret = True
    ret = os.path.isdir(name)
    if os.path.basename(name) in FILTER:
        ret = False
    return ret

if __name__ == "__main__":
    usage = """
      collect_QC_metrics.py [--dry_run --verbose]
      """
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--init-db", dest="init_db", action="store_true",
                      default=False)
    parser.add_option("-f", "--force", dest="force", action="store_true",
                      default=False)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      default=False)
    parser.add_option("-n", "--dry_run", dest="dry_run", action="store_true",
                      default=False)
    (options, args) = parser.parse_args()
    if len(args) != 0:
        print __doc__
        sys.exit()
    
    kwargs = dict(
        )
    main(*args, **kwargs)
