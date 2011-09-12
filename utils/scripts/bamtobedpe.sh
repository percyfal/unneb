#! /bin/bash
#
# File: bamtobedpe.sh
# Created: Mon Sep 12 09:15:03 2011
# $Id: $
#
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
# Description:
# 

usage()
{
    cat <<EOF
Usage: bamtobedpe.sh bamfile

Convert bamfile to bed removing PE-tags if necessary (/1 /2 in Illumina)
EOF
}

if [[ $# -ne 1 ]]; then 
    usage
    exit 1
fi

BAMFILE=$1
BEDFILE=$1.bed
echo Running "bamToBed -i $BAMFILE | sed -e \"s/\/[1-2]//\" > $BEDFILE"
bamToBed -i $BAMFILE | sed -e "s/\/[1-2]//" > $BEDFILE
rename .bam.bed -bam.bed $BEDFILE
