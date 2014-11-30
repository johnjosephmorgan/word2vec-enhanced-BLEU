#!/bin/bash -x
./paste-files.pl \
/home/john/school/computational_semanntics/project/data/wmt13/wmt13-data/plain/system-outputs/newstest2013/de-en/newstest2013.de-en.umd.2922 \
/home/john/school/computational_semanntics/project/data/wmt13/wmt13-data/plain/references/newstest2013-ref.en \
> eval_corpus.txt
