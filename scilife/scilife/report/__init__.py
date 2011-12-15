import re
import asciitable

class ProgramData():
    """Container class for program data output"""
    program = ""
    #version = ""
    #entries = []

    def __init__(self):
        self.data = dict()
    
    def as_rst(self, table):
        """Convert asciitable to rst table"""
        s = ".. table::"

    def _pad_table(self, table, char=" ", width=4):
        """Pad all lines in a table."""
        if not self.data.exists(table):
            raise "no such %s key in self" % table
        else:
            return [ char * width + self.data[x] for x in self.data[table] ]

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
