"""
Scilife config

Functions for loading and interacting with bcbb, galaxy and other stuff
"""
import os
import contextlib
import yaml

CONFIG_HOME = os.path.join(os.environ["HOME"], "config")
BCBB_CONFIG = os.path.join(CONFIG_HOME, "post_process.yaml")

def get_bcbb_config(config_file=BCBB_CONFIG):
    with open(config_file) as bc:
        bcbb_config = yaml.load(bc)
    return bcbb_config

# Use os.getenv("TOOL_DATA")
TOOL_DATA = "/bubo/nobackup/uppnex/reference/biodata/galaxy/tool-data/"
#TOOL_DATA = "/datad/biodata/galaxy/tool-data/"
_tool_data = dict(bwa = os.path.join(TOOL_DATA, "bwa_index.loc"),
                  bowtie = os.path.join(TOOL_DATA, "bowtie_indices.loc"),
                  samtools = os.path.join(TOOL_DATA, "sam_fa_indices.loc"))
                  
def get_genome_ref(genome_build):
    """Get genome reference"""
    cur_ref = None
    with open(_tool_data["samtools"]) as fp:
        for line in fp:
            if line.strip() and not line.startswith("#"):
                parts = line.strip().split()
                if parts[0] == "index":
                    parts = parts[1:]
                if parts[0] == genome_build:
                    cur_ref = parts[-1]
                    break
    if cur_ref is None:
        raise IndexError("Genome %s not found in %s" % (genome_build,
                                                        ref_file))
    return cur_ref
   
