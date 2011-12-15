## picard_sort_rmdup.mako
## remove duplicates with picard
## input: infiles, picard_home, n_procs

<%
i=1
bams = []
bamsorts = []
bamdups = []
for bam in infiles:
   bams.append("bam%s=%s" % (i,bam))
   bamsorts.append("bamsort%s=${bam%s%%.bam}-sort.bam" % (i, i))
   bamdups.append("bamdup%s=${bam%s%%.bam}-dup.bam" % (i, i))
   i=i+1
%>

$stdout=picard_sort_rmdup.stdout
$stderr=picard_sort_rmdup.stderr

## Set the bams
% for elem in bams:
${elem}
% endfor

## Set the bamsorts
% for elem in bamsorts:
${elem}
% endfor

## Set the bamdups
% for elem in bamdups:
${elem}
% endfor

## run sort - must be coordinate sorted
% for i in range(1,len(bams)+1):
# java -jar ${picard_home}/SortSam.jar INPUT=$bam${i} OUTPUT=$bamsort${i} SORT_ORDER=coordinate VALIDATION_STRINGENCY=SILENT
% endfor
# cat jobqueue | parallel -j 1 > $stderr 2> $stderr
wait

## run rmdup
touch jobqueue
% for i in range(1,len(bams)+1):
echo java -jar ${picard_home}/MarkDuplicates.jar INPUT=$bam${i} OUTPUT=$bamdup${i} METRICS_FILE=$bamdup${i}{%.bam}.metrics REMOVE_DUPLICATES=true VALIDATION_STRINGENCY=SILENT >> jobqueue
% endfor
cat jobqueue | parallel -j ${n_procs} >> $stdout 2>> $stderr

