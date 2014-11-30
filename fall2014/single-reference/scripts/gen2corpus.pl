#!/usr/bin/perl -w
#gen2corpus.pl - make a evaluation corpus out of a list of generated sentences
use strict;
use warnings;
use Carp;

BEGIN {
    @ARGV == 1 or croak "gen2corpus.pl GENLISTFILE";
}


my @gens = <>;

my $half = $#gens / 2;
open my $C, '+>', "cands.txt" or croak "could not open file cands.txt for writing $!";
for my $i (0..$half) {
    print $C "$gens[$i]";
}
close $C;

open my $R, '+>', "refs.txt" or croak "could not open file refs.txt for writing $!";
for my $ i(($half + 1..$#gens)) {
    print $R "$gens[$i]";
    }
		      close $R;
