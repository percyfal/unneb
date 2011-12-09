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

my $usage = "Usage: $0 gilist dbfile

<gilist>    File with GIs, one per row
<dbfile>    BIN taxonomy database file
";

if ($#ARGV != 1) {
  die $usage;
}
my $gifile = shift @ARGV;
my $dbbinfile = shift @ARGV;
open(IN, $gifile) || die "Can't open $gifile: $!\n";
my @gi = <IN>;
chomp @gi;
close(IN);
my ($prefix) = $gifile =~ /^([0-9a-zA-Z]+)\..+/;
my $db = SciLifeLab_SeqClass->readBINfile($dbbinfile);
$db->reduceGIlist(@gi);
# my $resfile = $prefix.".taxa.txt";
# $db->saveTXTfile($resfile);

print "gi\ttaxon\tparent\tclass\tkingdom_abbrev\tkingdom\tspecies_name\tdesc\n";
foreach my $gi ( @gi ) {
        my $t = $db->getGI_TaxonID($gi) || "NA";
        my $n = $db->getTaxon_toString($t) || "NA";
        my $p = $db->getTaxon_Parent($t) || "NA";
        my $c = $db->getTaxon_ID4UpperRank($t,"class") || "NA";
	my $desc = $db->getGI_Desc($gi) || "NA";
	my ($kingdom_abbrev, $kingdom, $species_name) = ($n) =~ /species\s+:\s+(\S+)\s+:\s+(\S+)\s+:\s+(.+)\s+:/;
	$kingdom_abbrev = $kingdom_abbrev || "NA";
	$gi = $gi || "NA";
	$species_name = $species_name || "NA";
	$kingdom = $kingdom || "NA";
        print "$gi\t$t\t$p\t$c\t$kingdom_abbrev\t$kingdom\t$species_name\t$desc\n";
}
