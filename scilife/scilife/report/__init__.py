import re
import csv 
from texttable import *
import asciitable

class ProgramData():
    """Container class for program data output"""
    program = ""
    #version = ""
    #entries = []

    def __init__(self):
        self.data = dict()
    
    def as_rst(self, table, pad_char=" ", width=4):
        """Convert asciitable to rst table"""
        s = ".. table::"
        data = self.data[table].draw()
        s = s + [ pad_char * width + data[x] for x in data ]
        return s

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

    def read_table(self, infile, comment_char="#", delimiter="\t", header=True, na_char="NA"):
        table = Texttable()
        first = True
        with open(infile) as fp:
            rows = csv.reader(fp, delimiter=delimiter)
            for row in rows:
                if first:
                    ncol = len(row)
                    cwidth = [0 for x in range(ncol)]
                if header and first:
                    table.header(row)
                else:
                    if len(row) < ncol:
                        row = row + [na_char for x in range(0,ncol-len(row))]
                    table.add_row(row)
                first=False
                for i in range(len(row)):
                    if len(row[i]) > cwidth[i]:
                        cwidth[i] = len(row[i]) + 1

        table.set_cols_width(cwidth)
        table.set_cols_align(["l"] + ["r" for x in range(1,ncol)])
        fp.close()
        return table
