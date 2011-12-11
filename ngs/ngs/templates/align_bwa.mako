## align_bwa.mako
## input: fastq1 fastq2 bwa_ref

out1=`basename ${fastq1}`
sai1=<%text>${out1%.txt}.sai</%text>
## Run bwa aligner
bwa aln ${bwa_opts} ${bwa_ref} ${fastq1} -f $sai1

% if not fastq2 is None:
out2=`basename ${fastq2}`
sai2=<%text>${out2%.txt}.sai</%text>
## Run bwa aligner
bwa aln ${bwa_opts} ${bwa_ref} ${fastq2} -f $sai2
% endif

sam=<%text>${out1%_1_fastq.txt}.sam</%text>
% if not fastq2 is None:
## Convert with sampe
bwa sampe ${bwa_ref} $sai1 $sai2 ${fastq1} ${fastq2} -f $sam
% else:
## Convert with samse
bwa samse ${bwa_ref} $sai1 ${fastq1} -f $sam
% endif
