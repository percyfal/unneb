## samtools_mpileup.mako
## run samtools mpileup
## input: infiles

<%
i=1
bams = []
for bam in infiles:
   bams.append("bam%s=%s" % (i,bam))
   i=i+1
%>

## Set the bams
% for elem in bams:
${elem}
% endfor

## run rmdup
% for i in range(1,len(bams)+1):
samtools mpileup ${opts} -f ${ref} $bam${i} &
% endfor

