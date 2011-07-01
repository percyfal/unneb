import os
import sys
import glob
from string import Template
__version__ = '0.2'

TEMPLATEDIR= os.path.join(os.path.dirname(__file__), "solid_templates")

# Templates
ini_templates = {
    'global_ini' : r"""
##  global parameters
run.name = %s
sample.name = %s

base.dir=../../
output.dir = ${base.dir}/output
temp.dir = ${base.dir}/temp
intermediate.dir = ${base.dir}/intermediate
log.dir = ${base.dir}/log
reads.result.dir = ${base.dir}/reads
reference=%s
scratch.dir=/scratch/solid

# override it locally in the pipeline ini file when needed
primer.set = %s

pipeline.cleanup.middle.files = 1
pipeline.cleanup.temp.files=1
job.cleanup.temp.files = 1
""",
    'mapping_ini' : r"""##  global settings for the pipeline run
import %s
read.length = %i

##  mapping pipeline
# mandatory parameters
# --------------------
mapping.run = 1
mapping.tagfiles.dir = %s
#mapping.tagfiles=
mapping.output.dir = %s

# optional parameters
# -------------------
# Parameter specifies the subfolder where repetitive .ma and .csfasta files were written
#mapping.repetitive.dir=
#mapping.number.of.nodes=3
#read.length=25
#mismatch.level=6
# Parameter defines the maximum number of best hits found in mapping.  [100]
matching.max.hits=10
#mask.positions=
#mapping.schema.file=
#matching.use.iub.reference=0
#mapping.run.classic=0
# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for unmapped reads.
#mapping.scheme.unmapped=
#mapping.scheme.unmapped.25=25.2.0
#mapping.scheme.repetitive.25=
#mapping.scheme.unmapped.35=30.3.0
#mapping.scheme.repetitive.35=
# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for unmapped reads of length greater or equal to 50.
#mapping.scheme.unmapped.50=25.2.0,25.2.15
# Parameter specifies an estimate of the sequencing error rate.
# Default value when not specified is 0.2
#mapping.qual.error.rate=

# Cleaning files 0/1 - files have to be removed when rerunning for some reason
#pipeline.cleanup.middle.files = 1
#job.cleanup.temp.files = 1

# Parameter scpecifies the threshold to decide whether a read is mapped uniquely in the reference.
#clear.zone=5

# Parameter specifies a negative score for mismatch which is used in local alignment mode.  
# When this is set to a non-negative number, the local mode is turned off and the output format of hits remains the same as that in V3.
# Default value when not specified is -2.0
#mapping.mismatch.penalty=

# Parameter specifies the full path and file name of the mapping stats file generated by the plugin
# Default value when not specified is ${output.dir}/s_mapping/mapping-stats.txt
mapping.stats.output.file=%s/mapping-stats.txt
""",
    'saet_ini' : r"""

""",
    'matobam_ini' : r"""############################
##
## matobam ini template
##
##############################
import %s
# Parameter specifies whether to run maToBam plugin. [1 - run, 0 - do not run]
ma.to.bam.run = 1
ma.to.bam.output.dir = ${output.dir}/bam
ma.to.bam.temp.dir = ${output.dir}/temp
ma.to.bam.qual.file = %s
ma.to.bam.match.file = %s
ma.to.bam.reference = %s
ma.to.bam.distribute.number.of.workers = 11
ma.to.bam.output.filter=primary
ma.to.bam.correct.to=reference
ma.to.bam.clear.zone=5
ma.to.bam.mismatch.penalty=-2.0
ma.to.bam.iubs.to=missing
ma.to.bam.library.type=fragment
ma.to.bam.library.name=%s
#ma.to.bam.slide.name=
#ma.to.bam.description=
ma.to.bam.sequencing.center=SciLife
ma.to.bam.tints=agy
ma.to.bam.base.qv.max=40
#ma.to.bam.temporary.dir=
""",

    'dibayes_ini' : r"""
## This is a configuration file for diBayes.
import %s
## ********************************************
## mapping parameters
## ********************************************
mapping.output.dir=${output.dir}/${primer.set}_mapping
## ********************************************
## positionErrors parameters
## ********************************************
position.errors.output.dir=${output.dir}/positionErrors/
## ********************************************
## diBayes parameters
## ********************************************
# mandatory parameters
# --------------------
# Parameter to specify whether to run Mutation Pipeline.
# [Options: 1 - Run, 0 - Don't run].
dibayes.run=1
# Parameter specifies the full path to location of directory
# where to write diBayes output files.
dibayes.output.dir=${output.dir}/diBayes/DB_OUT
# Parameter specifies the full path to location of directory in
# which to place temporary working files
dibayes.working.dir = ${temp.dir}/dibayes
# Parameter specifies the full path to the log directory
dibayes.log.dir = ${log.dir}/dibayes
# Parameter specifies the name of subdirectory in the output
# folder and the Name of the experimentprefix of the output files
dibayes.output.prefix = test_SNP
# Parameter specifies the reference sequence fasta file with full path
reference=%s
# Parameters specifies colon-separated list of the input sets in the format:
# file-full-path:mate-pair-flag:f3-position-err-file:[r3-position-err-file]
input.file.info=%s
# Maximal read length (e.g. 50). Note: this program allows
# combining reads from sources with different read lengths.
maximal.read.length = %s
# The parameter the criteria to report SNPs. [Options:highest|high|medium|low]
# Default value is 'medium' when not mentioned.
call.stringency = high
# optional parameters
# Changes on the algorithm fine tuning parameters will overridethe values that are preset by call.stringency setting.
# -------------------
# Polymorphism rate: Expected frequency of heterozygotes in the population: for example, 0.001 in humans
poly.rate = 0.001
# Parameter specifies to detect 2 Adjacent SNP's. [Options: 0 - do not detect, 1 - detect].
#detect.2.adjacent.snps=0
# Parameter specifies whether to write fasta file or not. [Options: 0 - Don't write fasta file, 1 - Write fasta file].
# Default value when not specified is 1.
write.fasta = 1
# Parameter specifies whether to write consensus_calls.txt. [Options: 0 - Don't write, 1 - Write].
# Default value when not specified is 1.
write.consensus = 1
# Parameter specifies whether to compress consensus_calls.txt by zipping it. [Options: 0 - Don't ZIP, 1 - ZIP].
compress.consensus = 0
# Parameter specifies whether to clean up the temporary files. [Options: 0 - Don.t clean, 1- Clean].
# Default value when not specified is 1.
#cleanup.tmp.files =1
# Parameter specifies not to call SNPs when the coverage of position is too high comparing to the median of the coverage distribution of all positions.
# NOTE: enable this filter for whole genome re-sequencing application; disable (default) it for transcriptome or target re-sequencing.
het.skip.high.coverage=0
# Parameter specifies the minimum mapping/pairing quality value.
# Default value when not specified is 0
#reads.min.mapping.qv=8
# Parameter specifies the required minimum for color quality value of non-reference allele to call a heterozygous SNP.
#het.min.nonref.color.qv=7
# Parameter specifies the required minimum for color quality value of non-reference allele to call a homozygous SNP.
#hom.min.nonref.color.qv=7
# Parameter species the requirement that the novel allele be on both strands :
# Parameter specifies the requirement that the novel allele is present on both strands and
# statistically similarly represented on both strand for both heterozygous and homozygous positionsSNPs.
# [Options: 0 - don't require, 1 - require]
#snp.both.strands = 0
# Parameter specifies the minimum required coverage to call a heterozygous SNP.
# [Allowed Values: Integer, 1-n]
#het.min.coverage = 3
# Parameter specifies Mthe minimum number of unique start position required to call a heterozgyote.
# [Allowed values: Integer, 1-n]
#het.min.start.pos = 3
# Parameter specifies the proportion of the reads containing either of the two candidate alleles.
# Filters positions with high raw error rate.
# [Allowed values: Float, 0-1]
#het.min.ratio.validreads=0.65
# The less common allele must be at least this proportion of the reads of the two heterozygote alleles.heterozygote.
# [Allowed values: Float, 0-1]
#het.min.allele.ratio=0.15
# Parameter specifies the Require at minimumleast 2 number of reads of an apparently valid tricolor calls to pass through filter to call 2 adjacent basesSNPs. i
# [Allowed Values: Integer]
#het.min.counts.tricolor=2
# Parameter specifies the required minimum coverage to call a homozygous SNP.
#hom.min.coverage=3
# Parameter specifies the Mminimum number of unique start position required to call a homozgyote.
# [Allowed values: Integer, 1-n]
#hom.min.start.pos=3
# Parameter specifies the required minimum coverage of candidate allele to consider this genome position for a Hhomozygous call.
#hom.min.allele.count=3
# Parameter specifies whether or not to filter the reads with indels.[Options: 0 - don't filter, 1 - filter].
# Default value when not specified is 1
#reads.no.indel=1
# Parameter specifies whether or not the reads to be are uniquely mapped. [Options: 0 - don't require, 1 - require].
# Default value when not specified is 0
#reads.only.unique=0
# Parameter specifies the threshold of mismatch/alignment length ratio.
# The reads whose mismatch/alignment length ratio is HIGHER than this specified threshold will be filtered.
# [Allowed values: Float, 0 - 1, 1 - don't filer]
#reads.max.mismatch.alignlength.ratio=1.0
# Parameter specifies rtTthe threshold of alignment-length / read-length ratio.
# The reads whose alignment-length/read-length ratio is are LESS than this specified threshold will be filtered.
# [Allowed values: Float, 0 - 1, 0 - don't filer]
#reads.min.mismatch.alignlength.ratio=0.0
# Parameter specifies whether to include the reads that only have one tag mapped (their mate tags are either unmapped or missing.)
# [Options: 0 - don't include, 1 - include]
#reads.include.no.mate=0

# Annotation pipeline
annotation.human.hg18=0
#annotation.gtf.file
#annotation.dbsnp.file.snpchrpos=
#annotation.dbsnp.file.snpcontigloc=
#annotation.dbsnp.file.snpcontiglocusid=

""",

    'positionError_ini' : r"""##  global parameters
import %s

##      position errors pipeline
position.errors.run = 1

# Location of BAM file from pairing plugin
# pairing.bam.dir=${output.dir}/pairing/

# Name of the BAM file for which position errors are to be calculated. If this key is missing a wild card search will be used. 
# If there is more than one .gff3 file in the input directory a position errors file will be generated for each one. (Optional)
# position.errors.input.bam.file = ${output.dir}/pairing/${primer.set.1}-${primer.set.2}-Paired.bam

# Position error output directory
position.errors.output.dir=${output.dir}/positionErrors

# Position error output file name
# position.errors.file=
"""
    }

# Utility functions, not for export
def _make_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def _write_template(fo, template):
    """Write the template"""
    if not os.path.exists(fo):
        fp = open(fo, "w")
        fp.write(template)
        fp.close()
    
class PrimerSet():
    """Holds information about a primer set"""
    def __init__(self, primer, readlength, project):
        # Primer is one of F3, R3, F5-P2, F5-BC
        self.primer = primer
        self.read_length = readlength
        self.workdir = os.path.join(project.workdir,  primer + "_mapping")
        self.outputdir = os.path.join(project.outputdir, primer + "_mapping")
        self.reads = os.path.join(project.reads,  primer)
        self.project = project
        self._makedirs()

    def _makedirs(self):
        _make_dir(self.workdir)
        _make_dir(self.outputdir)
        _make_dir(self.reads)

    def mapping_ini_template(self, write=True):
        """mapping.ini template"""
        template = ini_templates['mapping_ini'] % ("../globals/" + self.project.global_ini, self.read_length, self.reads, self.outputdir, self.outputdir)
        if write:
            _write_template(os.path.join(self.workdir, "mapping.ini"), template)
        return template

    def matobam_ini_template(self, write=True):
        """matobam.ini template"""
        if len(glob.glob(os.path.join(self.reads, "*.qual"))) > 0:
            qualfile = glob.glob(os.path.join(self.reads, "*.qual"))[0]
        else:
            sys.stderr.write("\nWARNING: No quality file found\n")
            qualfile = ""
        matchfile = os.path.join(self.outputdir, self.project.sample + "_" + self.primer + ".csfasta.ma")
        template = ini_templates['matobam_ini'] % ("../globals/" + self.project.global_ini, qualfile, matchfile, self.project.reference, self.project.sample)
        if write:
            _write_template(os.path.join(self.workdir, "matobam.ini"), template)
        return template

    def saet_ini_template(self, write=True):
        """saet.ini template"""
        template = ini_templates['saet_ini'] % ()
        if write:
            _write_template(os.path.join(self.workdir, "saet.ini"), template)
        return template
    
    def bam_file(self):
        """get bam file name for this primer set"""
        return os.path.join(self.project.outputdir, "bam", self.project.sample + "_" + self.primer + ".csfasta.ma" + ".bam")

    def __str__(self):
        s = "\n".join(["\t".join(["Primer:",  self.primer]),
                       "\t".join(["Workdir:",  self.workdir]),
                       "\t".join(["Outputdir:",  self.outputdir]), 
                       "\t".join(["Reads:",  self.reads]),
                       "\t".join(["Basedir:",  self.project.basedir])])
        return s

class SolidProject():
    """Generate templates for SOLiD projects"""
    def __init__(self, runname, sample, reference, basedir="./"):
        self.runname = runname
        self.sample = sample
        self.reference = reference
        self.basedir = basedir
        self.global_ini = "globals.ini"
        self.workdir = os.path.join(basedir, "workdir")
        self.outputdir = os.path.join(basedir, "output")
        self.reads = os.path.join(basedir, "reads")
        self.logdir = os.path.join(basedir, "log")
        self.tempdir = os.path.join(basedir, "temp")
        self.intermediatedir = os.path.join(basedir, "intermediate")
        self.globaldir = os.path.join(basedir, "workdir", "globals")
        self.dibayesdir = os.path.join(basedir, "workdir", "dibayes")
        self.positionerrordir = os.path.join(basedir, "workdir", "positionErrors")
        self.dibayesoutputdir = os.path.join(basedir, "output", "dibayes")
        self.positionerroroutputdir = os.path.join(basedir, "output", "positionErrors")
        self.primersets = {}

        _make_dir(self.logdir)
        _make_dir(self.tempdir)
        _make_dir(self.intermediatedir)

    def add_primer_set(self, primer, readlength=50):
        self.primersets[primer] = PrimerSet(primer, readlength, self)
        self.primersets[primer].mapping_ini_template()
        self.primersets[primer].matobam_ini_template()
            
    def max_read_length(self):
        rl = 0
        for k in self.primersets.keys():
            if self.primersets[k].read_length > rl:
                rl = self.primersets[k].read_length
        return rl
    
    def bamfiles(self):
        bf = []
        for k in self.primersets.keys():
            bf.append(self.primersets[k].bam_file())
        return bf

    def mapping_plan(self):
        """Make a mapping plan file"""
        pass

    def global_ini_template(self, write=True):
        """global.ini template"""
        _make_dir(self.globaldir)
        template = ini_templates['global_ini'] % (self.runname, self.sample,  self.reference, ",".join(self.primersets.keys()))
        if write:
            _write_template(os.path.join(self.globaldir, "globals.ini"), template)
        return template

    def dibayes_ini_template(self, run_type = 0, write=True):
        """dibayes.ini template"""
        _make_dir(self.dibayesdir)
        _make_dir(self.dibayesoutputdir)
        self.positionerror_ini_template()
        template = ini_templates['dibayes_ini'] % ("../globals/" + self.global_ini, self.reference, self.outputdir + ":" + str(run_type) + ":" + self.positionerroroutputdir,  self.max_read_length())
        if write:
            _write_template(os.path.join(self.dibayesdir, "dibayes.ini"), template)
        return template

    def positionerror_ini_template(self, write=True):
        """positionError.ini template"""
        _make_dir(self.positionerrordir)
        _make_dir(self.positionerroroutputdir)
        template = ini_templates['positionError_ini'] % ("../globals/" + self.global_ini)
        if write:
            _write_template(os.path.join(self.positionerrordir, "positionerror.ini"), template)
        return template
        

class SOLiDProject(object):
    """Template class for SOLiD projects"""
    _key_map = {'runname':'run.name', 'samplename':'sample.name', 'basedir' : 'base.dir', 'reference':'reference.file'}
    def __init__(self, runname, samplename, reference, basedir):
        self.workflow = self.__class__.__name__
        self.global_ini_file = os.path.join(basedir, "workdir", "globals", "global.ini")
        self.config = {'runname' :runname,
                       'samplename' : samplename,
                       'reference' : reference,
                       'basedir' : basedir
                       }
        self.basedirs = {'work': os.path.join(basedir, "workdir"),
                         'output' : os.path.join(basedir, "output"),
                         'reads' : os.path.join(basedir, "reads"),
                         'log' : os.path.join(basedir, "log"),
                         'temp' : os.path.join(basedir, "temp"),
                         'intermediate' : os.path.join(basedir, "intermediate")
                         }
        self.workdirs = {'dibayes' : os.path.join(basedir, "workdir", "dibayes"),
                         'positionErrors' : os.path.join(basedir, "workdir", "positionErrors")
                         }
        self.outdirs = {'dibayes' : os.path.join(basedir, "output", "dibayes"),
                        'positionErrors' : os.path.join(basedir, "output", "positionErrors")
                        }
        self.template_path = os.path.join(TEMPLATEDIR, self.workflow)
        self.d = {}

    def _set_d(self):
        d = {}
        for k in self.config.keys():
            d[k] = " = ".join([self._key_map[k], str(self.config[k])])
            if self.config[k] == None:
                d[k] = "# " + d[k]
        d['global_ini'] = self.global_ini_file
        return d

    def global_ini(self):
        print "In function"
        inifile = os.path.join(self.template_path, 'global.ini')
        with open(inifile) as in_handle:
            tmpl = Template(in_handle.read())
        return tmpl.safe_substitute(self.d)

class WT_SingleRead(SOLiDProject):

    def __init__(self, runname, samplename, reference, basedir, csfastafile, qualfile, filterref, exons_gtf, junction_ref, read_length=50):
        SOLiDProject.__init__(self, runname, samplename, reference, basedir)
        _key_map = self._key_map.update({'read_length':'read.length', 'csfastafile':'mapping.tagfiles', 'qualfile':'qual.file',
                                         'filter_reference':'filter.reference.file', 'exons_gtf':'exons.gtf.file', 'junction_reference':'junction.reference.file'})
        self.config.update({
                'read_length':read_length,
                'csfastafile':csfastafile,
                'qualfile':qualfile, 
                'filter_reference':filterref,
                'exons_gtf':exons_gtf,
                'junction_reference':junction_ref
                })
        self.d = self._set_d()

    def wt_single_read_ini(self):
        inifile = os.path.join(self.template_path, 'wt.single.read.workflow.ini')
        with open(inifile) as in_handle:
            tmpl = Template(in_handle.read())
        return tmpl.safe_substitute(self.d)


class TargetedFrag(SOLiDProject):
    def foo(self):
        pass

class TargetedPE(SOLiDProject):
    def foo(self):
        pass

class ReseqFrag(SOLiDProject):
    def foo(self):
        pass



class oldSolidProject():
    """Generate templates for SOLiD projects"""
    def __init__(self, runname, sample, reference, root="./", global_ini="globals.ini", paired_end=False):
        self.runname = runname
        self.sample = sample
        self.reference = reference
        self.root = root

        # Calculate the directories
        workdir = os.path.join(root, "workdir")
        globalsdir = os.path.join(workdir, "globals")
        self.reads1_dir = os.path.join(root, "reads1")
        self.reads2_dir = os.path.join(root, "reads2")
        self.work_dir = workdir
        self.mappingF3_dir = os.path.join(workdir, "mapping_F3")
        self.mappingR3_dir = os.path.join(workdir, "mapping_R3")
        self.pairing_dir = os.path.join(workdir, "pairing")
        self.positionErrors_dir = os.path.join(workdir, "positionErrors")
        self.matobam_dir = os.path.join(workdir, "matobam")
        self.globals_dir = globalsdir

        self.global_ini = os.path.join(globalsdir, global_ini)
        self.global_ini_rel = os.path.join("..", "globals", global_ini)
        print self.global_ini_rel
        self.paired_end = bool(paired_end)

    def _make_dir(self, outdir):
        if not os.path.exists(outdir):
            os.makedirs(outdir)
            
    def make_solid_dir_structure(self):
        """Generate typical solid analysis directory structure"""
        self._make_dir(self.reads1_dir)
        self._make_dir(self.work_dir)
        self._make_dir(self.globals_dir)
        self._make_dir(self.mappingF3_dir)
        self._make_dir(self.positionErrors_dir)
        self._make_dir(self.matobam_dir)
        if self.paired_end:
            self._make_dir(self.reads2_dir)
            self._make_dir(self.mappingR3_dir)
            self._make_dir(self.pairing_dir)

            
    def init_solid_project(self):
        """Initialize solid project"""
        self.make_solid_dir_structure()
        global_ini = self.global_ini_template()
        mapping_ini = self.mapping_ini_template()
        positionErrors_ini = self.positionErrors_ini_template()
        pairing_ini = self.pairing_ini_template()
        matobam_ini = self.matobam_ini_template()

    def _write_template(self, fo, template):
        """Write the template"""
        if not os.path.exists(fo):
            fp = open(fo, "w")
            fp.write(template)
            fp.close()
        

    def matobam_ini_template(self, write=True):
        self.matobam_ini = os.path.join(self.matobam_dir, "matobam.ini")
        """matobam.ini template"""
        template = ""
        if write:
            self._write_template(self.matobam_ini, template)
        return template

    def global_ini_template(self, write=True):
        """global.ini template"""
        template = r"""############################
############################
##
##  global parameters
##
run.name = %s
sample.name = %s

base.dir=../../
output.dir = ${base.dir}/outputs
temp.dir = ${base.dir}/temp
intermediate.dir = ${base.dir}/intermediate
log.dir = ${base.dir}/log
reads.result.dir.1 = ${base.dir}/reads1
reads.result.dir.2 = ${base.dir}/reads2
reference=%s
scratch.dir=/scratch/solid

# override it locally in the pipeline ini file when needed
primer.set = F3

pipeline.cleanup.middle.files = 1
job.cleanup.temp.files = 1
""" % (self.runname, self.sample, self.reference)
        if write:
            self._write_template(self.global_ini, template)

        return template

    def positionErrors_ini_template(self, write=True):
        """positionErrors.ini template"""
        self.positionErrors_ini = os.path.join(self.positionErrors_dir, "positionErrors.ini")

        template = ""# r"""""" % (self.global_ini)
        if write:
            self._write_template(self.positionErrors_ini, template)
        return template

    def pairing_ini_template(self, write=True):
        """pairing.ini template"""
        self.pairing_ini = os.path.join(self.pairing_dir, "pairing.ini")
        template = r"""#           To include some common variables.
import ../globals/global.ini
#Reference genome file name.

## *************************************************************
##   pairing
## ************************************************************

# mandatory parameters
# --------------------
# Parameter specifies whether to run or not pairing pipeline. [1: to run, 0:to not run]
pairing.run = 1
# Mapping output directories 
mate.pairs.tagfile.dirs = ${base.dir}/outputs/mappingF3,${base.dir}/outputs/mappingR3

mates.file.dir = ${output.dir}/pairing

# optional parameters
# -------------------

# Selects a set of parameters for indel search: 1: Deletions to 11, insertions to 3, Small indels. 2: Deletions to 14, insertions to 4, 
# Small indels. 3: Insertions from 4 to 14 4: Insertions from 15 to 20. 5: Longer deletions from 12 to 500. 
# Any of the values 1-5 may be entered, separated by comments
#indel.preset.parameters = 1,3,4,5

# Max Base QV. - The maximum value for a base quality value
#max.base.qv = 40

# Minimum Insert - Minimum insert size defining a good mate. If this is not set the code will attempt to measure the best value
#insert.start = 

# Maximum Insert - Maximum insert size defining a good mate. If this is not set the code will attempt to measure the best value
#insert.end = 

# Rescue Level - "Usually 2 * the mismatch level
#mate.pairs.rescue.level = 4

# Pairing statistics file name 
#mates.stats.report.name = pairingStats.stats

# Max Hits for Indel Search
#indel.max.hits = 10

# Maximum Hits
#matching.max.hits = 100

# Mapping Mismatch Penalty
#mapping.mismatch.penalty = -2.0


# Rescue Anchor Length
#pairing.anchor.length

# Minimum Non-mapped Length for Indels
#indel.min.non-matched.length = 10

# Rescue Level for Indels - Default for 50mers,3 for 35mers, and 2 for 25mers.
#indel.max.mismatches = 5

# Use template Rescue File For Indels
#use.template.rescue.file = true

# Max mismatches in indel search for tag 1
#pairing.indel.max.mismatch.tag1 = 5

# Max mismatches in indel search for tag 2
#pairing.indel.max.mismatch.tag2 = 5

# Pair Uniqueness Threshold
#pair.uniqueness.threshold = 10.0

# Maximum estimated insert size
#max.insert.estimate = 20000

# Minimum estimated insert size
#min.insert.estimate = 0

# Primer set - Use this only when both directories specified by mate.pairs.tagfile.dirs are the same. Then the files must have these strings 
# immediately before the .csfasta, if present, or the .ma extension.
# primer.set = F3,R3

# Mark PCR and optical duplicates
#pairing.mark.duplicates = true

# Color quality file path 1 - Color quality file path for first tag. Use instead of reads directories.
#pairing.color.qual.file.path.1 = 

# Color quality file path 2 - If either file path is explicitly set, both must be.
#pairing.color.qual.file.path.2 = 

# Annotations: How to correct color calls - 
#Specifies how to correct the color calls.
# 'missing' - Replaces all inconsistent read-colors with '.'. These will translate to 'x' in the base space representation, attribute 'b'.
# 'reference' - Replaces all read-colors annotated inconsistent (i.e., 'a' or 'b') with the corresponding reference color.
# 'singles' - Replaces all 'single' inconsistent colors (i.e., those annotated 'a' or 'b' and not adjacent to another 'b') with the corresponding 
#       reference color. Replaces all other inconsistent colors with '.'.
# 'consistent' - For each block of contiguous inconsistent colors, replace all single insistent colors 
#       (i.e., those annotated 'a' or 'b' and not adjacent to another 'b') with the corresponding reference color. Replace all other inconsistent 
# colors with '.'.
# 'qvThreshold' - A scheme combining the four above choices, based on the specified qvThreshold. (--correctTo: default is missing)
#pairing.to.bam.correct.color.calls = reference

# Single-tint annotation - Represents any number of single-tint annotations.
# 'a' - Isolated single-color mismatches (grAy).
# 'g' - Color position that is consistent with an isolated one-base variant (e.g., SNP).
# 'y' - Color position that is consistent with an isolated two-base variant.
#    (default is agy if not specified.)
#pairing.to.bam.single.tint = agy

# User Library prefix - Prefix for LB attribute of BAM file. Accepts any characters except tab and hyphen
#pairing.library.name =












##################################
##################################
##
##  temp files and folders keep
##  # don't keep temp files and folders for clean run ...   make it =1, if you want them to be deleted.
#pipeline.cleanup.middle.files = 0
#job.cleanup.temp.files = 0
"""
        if write and self.paired_end:
            self._write_template(self.pairing_ini, template)
        return template
