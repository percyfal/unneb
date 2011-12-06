import re
import asciitable

class ProgramData():
    """Container class for program data output"""
    program =""

    def __init__(self):
        self.data = dict()
        self.version = ""

    def to_rst_table(self):
        """Convert asciitable to rst table"""
        s = ".. table::"


    def _sniff_table(self,filename):
        """Read all lines in a table. If header starts with a space, add a description"""
        re_space = re.compile("^\s+\S+")
        fp = open(filename)
        lines = fp.readlines()
        fp.close()
        i = 0
        for l in lines:
            match = re_space.match(l)
            if match:
                lines[i] = "rowname" + lines[i]
                continue
            i = i + 1
        return lines
