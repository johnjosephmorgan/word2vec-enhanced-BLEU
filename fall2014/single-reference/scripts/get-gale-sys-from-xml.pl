#!/usr/bin/perl -w
#get-gale-sys-from-xml.pl - get the gale system output data
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
