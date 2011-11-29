import csv
import itertools
import asciitable.core as core
from asciitable.fixedwidth import FixedWidthHeader, FixedWidth

try:
    izip = itertools.izip
except AttributeError:
    izip = zip


class FixedWidthRstSplitter(core.BaseSplitter):
    """Split line based on fixed start and end positions for each ``col`` in
    ``self.cols``.

    This class requires that the Header class will have defined ``col.start``
    and ``col.end`` for each column.  The reference to the ``header.cols`` gets
    put in the splitter object by the base Reader.read() function just in time
    for splitting data lines by a ``data`` object. 

    Note that the ``start`` and ``end`` positions are defined in the pythonic
    style so line[start:end] is the desired substring for a column.  This splitter
    class does not have a hook for ``process_lines`` since that is generally not
    useful for fixed-width input.
    """
    delimiter_pad = ''
    row_delimiter_char = ''
    bookend = False
    row_char = ''
        
    def __call__(self, lines):
        for line in lines:
            vals = [line[x.start:x.end] for x in self.cols]
            if self.process_val:
                yield [self.process_val(x) for x in vals]
            else:
                yield vals

    def join(self, vals, widths, row_separator=False, row_char="-"):
        pad = self.delimiter_pad or ''
        delimiter = self.delimiter or ''
        if row_separator:
            delimiter = self.row_delimiter_char or delimiter
            pad = self.row_char or row_char
        
        padded_delim = pad + delimiter + pad
        if self.bookend:
            bookend_left = delimiter + pad
            bookend_right = pad + delimiter
        else:
            bookend_left = ''
            bookend_right = ''
        vals = [' ' * (width - len(val)) + val for val, width in zip(vals, widths)]
        return bookend_left + padded_delim.join(vals) + bookend_right



class FixedWidthRstData(core.BaseData):
    """Base table data reader.

    :param start_line: None, int, or a function of ``lines`` that returns None or int
    :param end_line: None, int, or a function of ``lines`` that returns None or int
    :param comment: Regular expression for comment lines
    :param splitter_class: Splitter class for splitting data lines into columns
    """

    splitter_class = FixedWidthRstSplitter
    row_position_char = "-"
    
    def write(self, lines):
        formatters = []
        for col in self.cols:
            formatter = self.formats.get(col.name, self.default_formatter)
            if not hasattr(formatter, '__call__'):
                formatter = core._format_func(formatter)
            col.formatter = formatter
            
        vals_list = []
        # Col iterator does the formatting defined above so each val is a string
        # and vals is a tuple of strings for all columns of each row
        for vals in izip(*self.cols):
            vals_list.append(vals)
            
        for i, col in enumerate(self.cols):
            col.width = max([len(vals[i]) for vals in vals_list])
            if self.header.start_line is not None:
                col.width = max(col.width, len(col.name))

        widths = [col.width for col in self.cols]

        # Start 
        if self.header.position_line is not None:
            char = self.row_position_char
            if len(char) != 1:
                raise ValueError('Position_char="%s" must be a single character' % char)
            vals = [char * col.width for col in self.cols]
            lines.append(self.splitter.join(vals, widths, True, char))

        if self.header.start_line is not None:
            lines.append(self.splitter.join([col.name for col in self.cols], widths))

        # Second header line
        if self.header.position_line is not None:
            char = self.header.position_char
            if len(char) != 1:
                raise ValueError('Position_char="%s" must be a single character' % char)
            vals = [char * col.width for col in self.cols]
            lines.append(self.splitter.join(vals, widths, True, char))

        for vals in vals_list:
            lines.append(self.splitter.join(vals, widths))
            # Add row separator
            if self.header.position_line is not None:
                char = self.row_position_char
                if len(char) != 1:
                    raise ValueError('Position_char="%s" must be a single character' % char)
                sepvals = [char * col.width for col in self.cols]
                lines.append(self.splitter.join(sepvals, widths, True, char))
        return lines


class FixedWidthRst(FixedWidth):
    """Write rst table"""
    def __init__(self, position_line=1, row_position_char='-', row_delimiter_char='+', position_char='=', delimiter_pad=' ', bookend=True):
         FixedWidth.__init__(self, delimiter_pad=delimiter_pad, bookend=bookend)
         # Reset self data
         self.data = FixedWidthRstData()
         self.data.header = self.header
         self.data.row_position_char = row_position_char
         self.header.data=self.data
         
         self.data.splitter.delimiter = '|'
         self.data.splitter.delimiter_pad = delimiter_pad
         self.data.splitter.row_delimiter_char = row_delimiter_char
         self.data.splitter.bookend = bookend
         
         self.header.position_line = position_line
         self.header.position_char = position_char
         self.data.start_line = position_line + 1
         self.header.splitter.delimiter = ''
         self.data.splitter.delimiter = '-'
        

