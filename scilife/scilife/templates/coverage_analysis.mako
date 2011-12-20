<%!
import scilife.report.gatk as gatk
import scilife.report.table as table
import asciitable
%>

<%
doc = gatk.DepthOfCoverage()
doc.read_depthofcoverage("depthofcoverage_out", indir=config['results'])
%>

${asciitable.write(doc.data["sample_summary"], Writer=table.FixedWidthRst, position_char='=', position_line=2, bookend=True, delimiter="|")}

