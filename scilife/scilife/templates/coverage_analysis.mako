<%!
import scilife.report.gatk as gatk
import scilife.report.table as table
%>

<%
doc = gatk.DepthOfCoverage()
doc.read_depthofcoverage(depthofcoverage["prefix"], indir=config['results'])
#doc.read_data(depthofcoverage["prefix"], indir=config['results'])
%>

${asciitable.write(doc.data["sample_summary"], Writer=table.FixedWidthRst, position_char='=', position_line=2, bookend=True, delimiter="|")}
