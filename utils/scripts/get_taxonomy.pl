#! /usr/bin/perl -w
#
# File: get_taxonomy.pl
# Created: Mon Dec  5 15:16:35 2011
# $Id: $
#
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
# Description:
# Download NCBI taxonomy

use strict;
use lib '/bubo/home/h1/perun/local/lib/perl5/';
use SciLifeLab_SeqClass;
my $db=SciLifeLab_SeqClass->new();
$db->setDirDownload("./");
$db->readTaxonomyNCBI();
$db->saveBINfile("ncbitaxonomy.bin");
