#!/usr/bin/perl -w
#get-gale-ref-from-xml.pl - get the gale reference data
use strict;
use warnings;
use Carp;

LINE: while ( my $line = <> ) {
    chomp $line;
    next LINE unless ( $line =~ /^<seg\s/ );
    $line =~ s/^<seg id=\"\d+?\">//;
    $line =~ s/<\/seg>//;
    print "$line\n";
}
