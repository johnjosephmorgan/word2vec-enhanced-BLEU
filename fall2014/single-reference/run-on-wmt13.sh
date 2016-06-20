#!/bin/bash -x


rm -Rf scores/wmt13.txt 
rm -Rf logs/

mkdir -p scores logs

python \
bleu/bleu.py  \
-C data/eval_wmt13.txt \
> scores/bleu-run-wmt13.txt


python \
svxleu/svxleu.py \
-C data/eval_wmt13.txt \
-V ./GoogleNews-vectors-negative300.bin.gz \
-t 0.80 \
> scores/wmt13.txt


mkdir -p results

echo "method	relevant	total	precision	score" > results/wmt13.txt
cat scores/wmt13.txt \
>> results/wmt13.txt

scripts/multi-bleu.perl \
data/eval_corpus_ref.txt \
< data/eval_corpus_sys.txt \
> scores/multibleu-run-wmt13.txt

rm xleu_candidate_reference_similarity.log

echo "candidate	reference	similarity" > candidate_reference_similarity.log
cat ./xleu_count_syns.log \
| grep root \
| perl -e \
"while (<>) {s/INFO:root://;s/[']//g;s/\[//g;s/\]//g;s/\(//g;s/\)//g;s/,//g;print;}" \
| sort -u \
>> svxleu_candidate_reference_similarity.log

mv svxleu_candidate_reference_similarity.log logs/
