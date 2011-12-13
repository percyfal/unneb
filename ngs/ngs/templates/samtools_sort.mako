## samtools_sort.mako
## convert to bam and sort
## input: infiles

<%
i=1
sams = []
bams = []
for sam in infiles:
    sams.append("sam%s=%s" % (i, sam))
    bams.append("bam%s=${sam%s%%.sam}.bam" % (i, i))
    i = i + 1
%>
## Set the sam files
% for elem in sams:
${elem}
% endfor

## Set the bam files
% for elem in bams:
${elem}
% endfor

## run 
% for i in range(1,len(bams)+1):
samtools view -bSh $sam${i} > $bam${i} &
% endfor
wait

## Remove sam files but keep file name for sanity check
% for i in range(1,len(bams)+1):
echo "$sam${i} converted to $bam${i}" > $sam${i}
% endfor
wait

<%
i=1
bamsort_prefix = []
for b in bams:
    bamsort_prefix.append("bamsort_prefix%s=${bam%s%%.bam}-sort" % (i,i))
    i = i + 1
%>
## Set the bamsort_prefix files
% for elem in bamsort_prefix:
${elem}
% endfor

## run 
% for i in range(1,len(bamsort_prefix)+1):
samtools sort $bam${i} $bamsort_prefix${i} &
% endfor
wait
