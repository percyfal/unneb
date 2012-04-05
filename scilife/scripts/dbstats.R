#
# File: dbstats.R'
# Created: Tue Mar  6 09:40:43 2012
# $Id: $
#
# Copyright (C) 2012 by Per Unneberg
#
# Author: Per Unneberg
#
# Description:
#

# Functions for reading metrics files
read.dup_metrics <- function(infile, pct.mult=TRUE, pct.char=list("PERCENT"), ...) {
    lines <- readLines(infile)
    res <- list()
    res$metrics <- rbind(read.table(textConnection(lines[7:8]), header=TRUE, fill=TRUE, sep="\t", ...))
    res$metrics[res$metrics=="?"] <- NA
    if (pct.mult) {
        i <- unique(do.call("c", lapply(pct.char, function(x) {which(grepl(x, colnames(res$metrics)))})))
        res$metrics[,i] <- res$metrics[,i] * 100
    }
    res
}

read.align_metrics <- function(infile, pct.mult=TRUE, pct.char=list("PCT", "STRAND_BALANCE", "PF_HQ_ERROR_RATE"), ...) {
    lines <- readLines(infile)
    res <- list()
    res$metrics <- rbind(read.table(textConnection(lines[7:10]), header=TRUE, fill=TRUE, sep="\t", ...))
    res$metrics[res$metrics=="?"] <- NA
    res$metrics <- cbind(CATEGORY=res$metrics[,1], as.data.frame(lapply(res$metrics[,-1], function(x){if (mode(x) != "numeric") x <- as.numeric(x); x})))
    res$metrics$CATEGORY <- factor(res$metrics$CATEGORY, levels=c("FIRST_OF_PAIR", "SECOND_OF_PAIR", "PAIR"))
    if (pct.mult) {
        i <- unique(do.call("c", lapply(pct.char, function(x) {which(grepl(x, colnames(res$metrics)))})))
        res$metrics[,i] <- res$metrics[,i] * 100
    }
    res
}

read.insert_metrics <- function(infile, ...) {
    lines <- readLines(infile)
    res <- list()
    res$metrics <- rbind(read.table(textConnection(lines[7:8]), header=TRUE, fill=TRUE, sep="\t", ...))
    res$histogram <- rbind(read.table(textConnection(lines[11:length(lines)]), header=TRUE, fill=TRUE, sep="\t", ...))
    res
}
read.gc_metrics <- function(infile, ...) {
    lines <- readLines(infile)
    res <- list()
    nlines <- length(lines)
    res$metrics <- rbind(read.table(textConnection(lines[7:nlines]), header=TRUE, fill=TRUE, sep="\t", ...))
    res
}

read.eval_metrics <- function(infile, ...) {
    res <- fromJSON(infile)
    res
}

read.hs_metrics <- function(infile, pct.mult=TRUE, pct.char=list("PCT", "ON_BAIT_VS_SELECTED"), ...) {
    lines <- readLines(infile)
    res <- list()
    res$metrics <- rbind(read.table(textConnection(lines[7:8]), header=TRUE, fill=TRUE, sep="\t", ...))
    res$metrics[res$metrics=="?"] <- NA
    if (pct.mult) {
        i <- unique(do.call("c", lapply(pct.char, function(x) {which(grepl(x, colnames(res$metrics)))})))
        res$metrics[,i] <- res$metrics[,i] * 100
    }
    res
}

read.metrics <- function(filename, type=c("align_metrics", "dup_metrics", "eval_metrics", "gc_metrics", "hs_metrics", "insert_metrics"),...) {
    if (is.na(type)) {
        return(NA)
    }
    type <- as.character(type)
    type <- match.arg(type)
    con <- file(filename, "r")
    y <- switch(type,
                align_metrics = read.align_metrics(con),
                dup_metrics = read.dup_metrics(con),
                eval_metrics = read.eval_metrics(con),
                gc_metrics = read.gc_metrics(con),
                hs_metrics = read.hs_metrics(con),
                insert_metrics = read.insert_metrics(con))
    close(con)
    return(y)
}


# Load libraries
library(RJSONIO)
library(lattice)

# Read qc metadata file
qcfile <- ".QCmetrics.json"
con <- file(qcfile, "r")
qcdata <- fromJSON(con, nullValue=NA)
close(con)

# Make gigantic data frame of json object
i <- do.call("c", lapply(qcdata, function(x){length(x$FILES)>0}))
qc.df <- as.data.frame(do.call("rbind", lapply(names(qcdata[i]), function(x) { cbind(project=x, do.call("rbind", lapply(qcdata[[x]]$FILES, function(y) { y})))})))
# NOTE: there seems to be a bug in fromJSON when reading nested
# structures. Even though I pass nullValue=NA, nulls are translated to
# TRUE?!? This is remedied here:
qc.df[qc.df==TRUE] <- NA
bclevels <- c(levels(qc.df$bc)[sort(as.integer(levels(qc.df$bc)), index.return=TRUE)$ix], levels(qc.df$bc)[is.na(as.integer(levels(qc.df$bc)))])
qc.df$bc <- factor(qc.df$bc, levels=bclevels)
qc.df$lane <- factor(qc.df$lane, levels=as.character(sort(as.integer(levels(qc.df$lane)))))

# Read all metrics files into memory
metrics <- apply(qc.df, 1, function(x){read.metrics(x["target"], x["mtype"])})

##############################
## Look at duplication metrics
##############################
i.dup <- qc.df$mtype=="dup_metrics"
i.dup[is.na(i.dup)] <- FALSE
dup <- cbind(qc.df[i.dup,], do.call("rbind", do.call("c", metrics[i.dup])))

# Some nice plots
stripplot(PERCENT_DUPLICATION ~ project, data=dup,  scales=(list(x=list(rot=45))), par.settings=simpleTheme(pch=19),  ylim=c(0,100), xlab="Project", ylab="Percent duplication")
bwplot(PERCENT_DUPLICATION ~ project, data=dup, scales=(list(x=list(rot=45))), par.settings=simpleTheme(pch=19),  ylim=c(0,100), xlab="Project", ylab="Percent duplication")
bwplot(PERCENT_DUPLICATION ~ lane, data=dup, scales=(list(x=list(rot=45))), par.settings=simpleTheme(pch=19),  ylim=c(0,100), xlab="Lane", ylab="Percent duplication")

##############################
## Look at alignment metrics
##############################
i.aln <- qc.df$mtype=="align_metrics"
i.aln[is.na(i.aln)] <- FALSE
aln <- cbind(qc.df[i.aln,], do.call("rbind", do.call("c", metrics[i.aln])))

# Some nice plots
stripplot(TOTAL_READS/1e6 + PF_READS_ALIGNED/1e6  ~ project:sample, data=aln[aln$CATEGORY=="PAIR",], auto.key=list(text=c("Reads", "Aligned")), scales=list(x=list(rot=45),relation="free"), ylab="Reads (millions)", xlab="project:sample", par.settings=simpleTheme(col=c("black","red"), pch=21))
stripplot(PCT_PF_READS_ALIGNED ~ project:sample, data=aln[aln$CATEGORY=="PAIR",], scales=list(x=list(rot=45)), xlab="project:sample", par.settings=simpleTheme(pch=19))
stripplot(PCT_PF_READS_ALIGNED ~ project, data=aln[aln$CATEGORY=="PAIR",], scales=list(x=list(rot=45)), xlab="project", par.settings=simpleTheme(pch=19))

##############################
## Look at hs metrics
##############################
i.hs <- qc.df$mtype=="hs_metrics"
i.hs[is.na(i.hs)] <- FALSE
hs <- cbind(qc.df[i.hs,], do.call("rbind", do.call("c", metrics[i.hs])))

                                        # Some nice plots
stripplot(TOTAL_READS/1e6 + PF_READS_ALIGNED/1e6  ~ project:sample, data=aln[aln$CATEGORY=="PAIR",], auto.key=list(text=c("Reads", "Aligned")), scales=list(x=list(rot=45),relation="free"), ylab="Reads (millions)", xlab="project:sample", par.settings=simpleTheme(col=c("black","red"), pch=21))
stripplot(PCT_PF_READS_ALIGNED ~ project:sample, data=aln[aln$CATEGORY=="PAIR",], scales=list(x=list(rot=45)), xlab="project:sample", par.settings=simpleTheme(pch=19))
stripplot(PCT_PF_READS_ALIGNED ~ project, data=aln[aln$CATEGORY=="PAIR",], scales=list(x=list(rot=45)), xlab="project", par.settings=simpleTheme(pch=19))

##############################
### Save data
##############################
save(file="QCmetrics.rda")
