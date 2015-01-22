#!/bin/bash -x

rm ./xleu_count_syns.log 
mkdir -p scores logs

for corpus in wmt13
do
python \
bleu/bleu.py  \
-C data/eval_$corpus.txt \
> scores/bleu-run-$corpus.txt
done

for threshold in 00 70 80 90 95
do
python \
svxleu/svxleu.py \
-C data/eval_wmt13.txt \
-V ./GoogleNews-vectors-negative300.bin.gz \
-t 0.${threshold} \
> scores/wmt13-${threshold}.txt

rm logs/svxleu_candidate_reference_similarity_${threshold}.log

echo "candidate	reference	similarity" > logs/svxleu_candidate_reference_similarity_${threshold}.log
cat ./xleu_count_syns.log \
| grep root \
| perl -e \
"while (<>) {s/INFO:root://;s/[']//g;s/\[//g;s/\]//g;s/\(//g;s/\)//g;s/,//g;print;}" \
| sort -u \
>> logs/svxleu_candidate_reference_similarity_${threshold}.log

rm ./xleu_count_syns.log 
done

mkdir -p results

for threshold in 00 70 80 90 95
do
rm results/wmt13-${threshold}.txt
echo "method	relevant	total	precision	score" > results/wmt13-${threshold}.txt
cat scores/wmt13-${threshold}.txt \
>> results/wmt13-${threshold}.txt
done

scripts/multi-bleu.perl \
data/eval_corpus_ref.txt \
< data/eval_corpus_sys.txt \
> scores/multibleu-run-wmt13.txt

rm xleu_candidate_reference_similarity.log
