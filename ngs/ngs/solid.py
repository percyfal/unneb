import os

__version__ = '0.1.0'

class SolidProject():
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

    def _write_template(self, fo, template):
        """Write the template"""
        if not os.path.exists(fo):
            fp = open(fo, "w")
            fp.write(template)
            fp.close()
        
    def mapping_ini_template(self, write=True):
        """mapping.ini template
        Default example taken from 
        """
        self.mappingF3_ini = os.path.join(self.mappingF3_dir, "mapping.ini")
        self.mappingR3_ini = os.path.join(self.mappingR3_dir, "mapping.ini")
        template=r"""
##################################
##################################
##
##  global settings for the pipeline run
##
import %s
read.length = 50

##################################
##################################
##
##  mapping pipeline
##


# mandatory parameters
# --------------------

# Parameter is used top specify to run the mappign pipe line
mapping.run = 1

# Parameter specifies the directory where the csfasta file to be used as input exists
# If multiple csfasta files exist in the input directory first file is chosen
# it is advaisdable nto sue this parameter but use mapping.tagfiles mentioned below if multiple csfasta files exist in same directory
mapping.tagfiles.dir = ${reads.result.dir.1}

# Parameter specifies the exact csfast file to be used for mapping
#mapping.tagfiles=

# Parameter specifies the output directory where the mapping pipeline output should be placed
mapping.output.dir = ${output.dir}/mappingF3

# optional parameters
# -------------------


# Parameter specifies the subfolder where repetitive .ma and .csfasta files were written
#mapping.repetitive.dir=

# Parameter specifies whether or not to run mapreads with multithread mode.
# The default value is 'true' when the parameter is not specified
#mapping.run.multithread=

# Parameter specifies number of processors per node to be used for mapping.
# The read file will be divided into this number of chunks and passed to mapreads.
# The default is 8 when not specified
#mapping.np.per.node=

# Parameter specifies number of nodes available.  
# The read file will be divided into this number of chunks before further divided into ${mapping.np.per.node} of chunks. 
# The default value is 3 when not specified
#mapping.number.of.nodes=

# Parameter specifies the minimum number of reads the *.csfasta file should have for read split to happen.
#mapping.min.reads=

# Parameter specifies the total memory available for mapreads in Giga Bytes.
# The default value can be set during installation by asking customers the lowest memory size available across nodes in cluster.
#mapping.memory.size=

# Parameter specifies the full path of reference file.
#reference=

# Parameter specifies the default value for read length if running classic mapping. 
# Default value when not specified is 25
#read.length=


# Parameter defines default value of number of mismatches allowed when running classic mapping.
# Default value when not specified is 6
#mismatch.level=

# Parameter defines the maximum number of best hits found in mapping. 
# Default value when not specified is 100
#matching.max.hits=

# Parameter specifies whether or not to write read sequences to the final .ma file. [1 - write, 0 - do not write]
# Default value when not specified is 1
#mapping.write.sequence=

# Parameter specifies how to penalize adjacent mismatches. 
# 1: Only count consistent adjacent mismatches as 1; 0: Count adjacent mismatches as 2
# Default when not specified is 0
#mapping.valid.adjacent=

# Parameter specifies an array of integers that indicates the positions in the read sequence that will be excluded in mapping.
# Parameter when not specified wil result in no masking
#mask.positions=

# Parameter specifies the schema file with full path used in mapping.
#mapping.schema.file=

# Parameter specifies whether or not to support reference sequences with IUB codes.matching.use.iub.reference
# Default when not specified is 0
#matching.use.iub.reference=

# Parameter specifies whether or not to run classic mapping. [1 - run , 0 - do not run]
# Default value when not specified is 0
#mapping.run.classic=

# Parameter specifies the length of read to use when running classic mapping.
# Deafault when not specified is taken from read.length parameter
#mapping.classic.anchor.length=

# Parameter specifies the number of mismatches allowed when running classic mapping.
# Deafault when not specified is taken from mismatch.level parameter
#mapping.classic.mismatch=

# Parameter specifies the lower limit of number of hits.  Used to determine the branch a matched read goes to during iterative mapping.
# Default value when not specified is 1
#mapping.hits.lower.limit=

# Parameter specifies the upper limit of number of hits.  Used to determine the branch a matched read goes to during iterative mapping. 
# Default value when not specified is 100
#mapping.hits.upper.limit=

# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for unmapped reads.
#mapping.scheme.unmapped=

# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for repetitive reads.

# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for unmapped reads of length between [25, 35].
# Default when not specified is 25.2.0
#mapping.scheme.unmapped.25=

# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for repetitive reads of length between [25, 35].
#mapping.scheme.repetitive.25=

# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for unmapped reads of length between [35, 50].
# Default value when not specified is 30.3.0
#mapping.scheme.unmapped.35=

# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for repetitive reads of length between [35, 50].
#mapping.scheme.repetitive.35=

# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for unmapped reads of length greater or equal to 50.
# default value when not specified is 25.2.0,25.2.15
#mapping.scheme.unmapped.50=

# Parameter specifies a list of anchorLength.mismatchAllowed.anchorStart separated by comma for repetitive reads of length greater or equal to 50.
#mapping.scheme.repetitive.50=

# Parameter specifies an estimate of the sequencing error rate.
# Default value when not specified is 0.2
#mapping.qual.error.rate=

# Parameter specifies an estimate of percentage of genome unique at length L with 1 mismatch.
# In human there are 10 percent of positions match to somewhere else at 50.1.
# Default value when not specified is 1.0
#mapping.qual.bvalue=

# Parameter specifies whether or not .ma file uses multi-contig format.
# Always 1, the multi-contig format contig_pos.mm in BioScope.
# Default value when not specified is 1
#mapping.qual.pvalue=

# Parameter specifies the minimum local score [0-100] of unique hit to filter out.
# Default value when not specified is 0
#mapping.qual.filter.cutoff=


##################################
##################################
##
##  temp files and folders keep 
##

# Parameter specifies whether or not to delete intermediate files generated in mapping pipeline. [1 - delete, 0 - not to delete]
# The default value when not specified is 1
#pipeline.cleanup.middle.files = 0

# Parameter specifies whether or not to delete intermediate files from split and gather. [1 - delete, 0 - not to delete]
# The default when not specified is 1
#job.cleanup.temp.files = 0


## ********************************************
## mapping stats  parameters
## ********************************************

# Parameter scpecifies the threshold to decide whether a read is mapped uniquely in the reference.
#clear.zone=5

# Parameter specifies a negative score for mismatch which is used in local alignment mode.  
# When this is set to a non-negative number, the local mode is turned off and the output format of hits remains the same as that in V3.
# Default value when not specified is -2.0
#mapping.mismatch.penalty=

# Parameter specifies the full path to the location where mapping pipeline result is located.
# Default value when not specified is ${output.dir}/s_mapping
#mapping.output.dir=${output.dir}/s_mapping

# Parameter specifies the full path and file name of the mapping stats file generated by the plugin
# Default value when not specified is ${output.dir}/s_mapping/mapping-stats.txt
#mapping.stats.output.file=${output.dir}/s_mapping/mapping-stats.txt
""" % (self.global_ini)
        if write:
            self._write_template(self.mappingF3_ini, template)
            if self.paired_end:
                self._write_template(self.mappingR3_ini, template)

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

        template = r"""####################################
####################################
##
##  global parameters
##
import %s
primer.set = ${primer.set.1},${primer.set.2}

##********************************************
##      position errors pipeline
##********************************************
# Parameter specifies whether to run or not position errors pipeline. [1: to run, 0:to not run]
position.errors.run = 1

# Location of BAM file from pairing plugin
pairing.bam.dir=${output.dir}/pairing/

# Name of the BAM file for which position errors are to be calculated. If this key is missing a wild card search will be used. 
# If there is more than one .gff3 file in the input directory a position errors file will be generated for each one. (Optional)
position.errors.input.bam.file = ${output.dir}/pairing/${primer.set.1}-${primer.set.2}-Paired.bam

# Position error output directory
position.errors.output.dir=${output.dir}/position-errors

# Position error output file name
position.errors.file=
""" % (self.global_ini)
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
