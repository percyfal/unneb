#! /usr/bin/perl -w
#
# File: gitaxonomy.pl
# Created: Mon Oct 17 15:37:31 2011
# $Id: $
#
# Copyright (C) 2011 by Per Unneberg
#
# Author: Per Unneberg
#
# Description:
# 

use lib '/bubo/home/h1/perun/local/lib/perl5/';
use SciLifeLab_SeqClass;
# use TaxonomyNCBI;
use strict;

my $usage = "Usage: $0 gilist

<gilist>    File with GIs, one per row";

if ($#ARGV != 0) {
  die $usage;
}
my $gifile = shift @ARGV;
open(IN, $gifile) || die "Can't open $gifile: $!\n";
my @gi = <IN>;
chomp @gi;
close(IN);
my ($prefix) = $gifile =~ /^([0-9a-zA-Z]+)\..+/;

# my $db=TaxonomyNCBI->new();
my $dir = "/bubo/proj/a2010001/projects/B_Nicklasson_11_02/nobackup/";
# $db->setDirDownload($dir);
# $db->readTaxonomyNCBI();
my $db = SciLifeLab_SeqClass->readBINfile("/bubo/proj/a2010001/projects/B_Nicklasson_11_02/nobackup/my_Taxonomy_20110914");
$db->reduceGIlist(@gi);
my $resfile = $prefix.".taxa.txt";
#$db->saveBINfile($resfile);
$db->saveTXTfile($resfile);

# $db->saveBINfile("gilist.txt");
foreach my $gi ( @gi ) {
        my $t = $db->getGI_TaxonID($gi);
        my $n = $db->getTaxon_toString($t);
        my $p = $db->getTaxon_Parent($t);
        my $c = $db->getTaxon_ID4UpperRank($t,"class");
	my $desc = $db->getGI_Desc($gi);
        print "gi= $gi \ttaxon= $t \tname= $n \tparent= $p \tclass= $c\tdesc= $desc\n";
}
