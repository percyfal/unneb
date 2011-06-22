"""
Wrappers for ngs analysis

NOTE: these are just wrappers that simply generate text strings for common ngs tasks
"""

from paver.easy import path

VERSION = "0.1.0"


class Command:
    """Class that does simple up-to-date checking based on file modification dates"""
    def __init__(self, cmd, source, target, comment_char="#", force=False):
        self.cmd = cmd
        self.comment_char = comment_char
        self._force = force
        self.source = path(source)
        self.target = path(target)
        
    def run_task(self):
        if not self.target.exists() or self.target.getmtime() < self.source.getmtime():
            return True
        else:
            return False
        
    def fget(self):
        return self._force
    def fset(self, arg):
        self._force = bool(arg)
    force = property(fget, fset)

    @property
    def comment(self):
        if self.run_task() or self._force:
            return ""
        else:
            return self.comment_char
        
    def __str__(self):
        return self.comment + self.cmd

    def command(self):
        return self.comment + self.cmd

# class Command():
#     """Command class that includes code for checking if task is up-to-date"""
#     def __init__(self, cmd_string, source, target):
#         self.source = path(source)
#         self.target = path(target)
#         self.command = cmd_string
#         self.comment_char = "# "

#     def __str__(self):
#         return self.cmd()

#     def is_up_to_date(self):
#         if self.target.getmtime() < self.source.getmtime():
#             return False
#         else:
#             return True

#     def cmd(self):
#         if not self.is_up_to_date():
#             self.command = self.comment_char + self.command
#         return self

def make_bwa_cs_input(prefix, suffix=".csfasta.gz"):
    """Make bwa color space input"""
    cmd = Command(" ".join(['solid2fastq.pl', prefix + "_", prefix]), 
                  prefix + "_F3" + suffix,
                  prefix + ".single.fastq.gz"
                  )
    return cmd

def bwa(prefix, opts, ref):
    """Run bwa aligner"""
    infile  = prefix + ".fastq.gz"
    outfile = prefix + ".bwa.sai"
    cmd = Command(" ".join(['bwa aln', opts, ref, infile, ">", outfile]), infile, outfile)
    return cmd

def sam_to_bam(prefix, opts="-bS"):
    """Run samtools to convert from sam to bam"""
    infile = prefix + ".sam"
    outfile = prefix + ".bam"
    cmd = Command(" ".join(['samtools view', opts, infile, ">", outfile]), infile, outfile)
    return cmd
