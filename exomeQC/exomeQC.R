#
# File: exomeQC.R
# Created: Tue May 24 15:21:31 2011
#
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
# Description:
# Perform simple TEQC stats
#

## How to run:
## R CMD BATCH --vanilla '--args  config="config.yaml"' exomeQC.R logfile

usage <- "Usage: R CMD BATCH --vanilla '--args exomerc=\"config.yaml\"' exomeQC.R logfile"

## Read command line
args <- commandArgs(TRUE)
if (length(args) == 0)
    stop(usage)
for (i in 1:length(args)) {
    eval(parse(text=args[[i]]))
}
if (!exists("exomerc"))
    stop(usage)

## Load required packages
library(TEQC)
library(yaml)

##################################################
## Load config file
##################################################
exomerc <- yaml.load_file(exomerc)
##################################################
## Functions
##################################################
## obj - the object to be plotted
## fun - the function as a named list (list(fun=fun)), otherwise not possible to deparse function name
##     see http://stackoverflow.com/questions/1567718/r-getting-a-function-name-as-a-string
## sample - the sample name
##
plotwrapper <- function(obj, fun, sample=exomerc$label, extralab=NULL, outdir=exomerc$outdir, ...) {
    prefix <- gsub("\\.|\\_", "-", paste(sample, names(fun), sep="-"))
    if (!is.null(extralab))
        prefix <- paste(prefix, extralab, sep="-")
    outfile <- paste(file.path(outdir, prefix), ".png", sep="")
    png(file=outfile)
    fun[[1]](obj, ...)
    dev.off()
}

## Load targets
targets <- get.targets(exomerc$target)

## Fraction of genome that consists of target
ft <- fraction.target(targets, genome = exomerc$genome)
wt <- sum(width(targets))

## Read bed file, without read names
reads <- get.reads(exomerc$bedfile, zerobased=FALSE, chrcol=1, startcol=2, endcol=3, idcol=4)

## Do we have paired-end reads? In that case, run reads2pairs
if (exomerc$pairedend) {
    readpairs <- reads2pairs(reads)
    plotwrapper(readpairs$readpairs, list(insert.size.hist=insert.size.hist), main=paste("Insert sizes for", exomerc$label),  breaks=10)
}

## 1. Chromosome barplot
## Do sequenced reads fall in target regions?
if (exomerc$analyses$barplot) {
    print("plotting sequenced reads in target regions")
    plotwrapper(reads, list(chrom.barplot=chrom.barplot), targets=targets, main=paste("Reads on targets for", exomerc$label))
}

## 2. Capture specificity
## Fraction aligned reads that overlap with any target region
## Calculate fraction reads per target with varying offsets
if (exomerc$analyses$specificity) {
    print("calculating capture specificity")
    fr <- fraction.reads.target(reads, targets)
    fr.50 <- fraction.reads.target(reads, targets, 50)
    fr.100 <- fraction.reads.target(reads, targets, 100)
}

## 3. Enrichment
## (no. reads on target / no. aligned reads) / (target size / genome size)
if (exomerc$analyses$enrichment) {
    print("calculating enrichment")
    enrichment <- fr / ft
}


if (exomerc$analyses$coverage) {
    ## 4a. Coverage
    ##    get read coverage for each target region
    print("calculating coverage")
    Coverage <- coverage.target(reads, targets, perTarget=TRUE, perBase=TRUE)


    ## 4b. Number of reads per target
    ##     get the number of reads that fall within a target region
    print("calculating coverage as reads per target")
    Coverage.reads <- readsPerTarget(reads, Coverage$targetCoverages)

    ## 4c. k-wise coverage
    ##     make table of k-wise coverage
    print("calculating k-wise coverage")
    kval <- c(1,5,10,20,30,40,50,60)
    Coverage.k <- covered.k(Coverage$coverageTarget, k=kval)

    ## 4d. Visualize coverage
    print("visualizing coverage")
    threshold <- 8
    plotwrapper(Coverage$coverageTarget, list(coverage.hist=coverage.hist), covthreshold=threshold, main=paste("Coverage Distribution for", exomerc$label))

    ## 4e. Coverage uniformity
    print("visulizing uniformity")
    plotwrapper(Coverage, list(coverage.uniformity=coverage.uniformity), main=paste("Normalized coverage for", exomerc$label))

    ## 4f. Coverage and length bias
    print("visualising coverage and length bias")
    plotwrapper(Coverage.reads, list(coverage.targetlength.plot=coverage.targetlength.plot), main=paste("Number of reads per target for", exomerc$label), plotcolumn="nReads", pch=16, cex=1.5, extralab="nReads" )
    plotwrapper(Coverage.reads, list(coverage.targetlength.plot=coverage.targetlength.plot), main=paste("Average coverage per target for", exomerc$label), plotcolumn="avgCoverage", pch=16, cex=1.5, extralab="avgCoverage" )
}

## 5. Duplicates
##    How big a problem is PCR duplicates?
##    Mostly for paired end reads
if (exomerc$analyses$duplicates) {
    if (exomerc$pairedend) {
        plotwrapper(readpairs$readpairs, list(duplicates.barplot=duplicates.barplot), targets=targets, ylab="Fraction of read pairs")
    } else {
        plotwrapper(reads, list(duplicates.barplot=duplicates.barplot), targets=targets)
    }
}
##################################################
## Make text report
##################################################


##################################################
## Save data
##################################################
if (exomerc$saverda) {
    rdafile <- file.path(exomerc$outdir, paste("exomeQC-", exomerc$label, ".rda", sep=""))
    save.image(file=rdafile)
}