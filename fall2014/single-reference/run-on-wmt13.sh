#!/bin/bash -x


rm -Rf scores/wmt13.txt 
rm -Rf logs/

mkdir -p scores logs

for corpus in wmt13 anomolous
do
python \
bleu/bleu.py  \
-C data/eval_$corpus.txt \
> scores/bleu-run-$corpus.txt
done

for corpus in wmt13 anomolous
do
python \
svxleu/svxleu.py \
-C data/eval_$corpus.txt \
-V ./GoogleNews-vectors-negative300.bin.gz \
-t 0.80 \
> scores/${corpus}.txt
done

mkdir -p results

for corpus in wmt13 anomolous
do
echo "method	relevant	total	precision	score" > results/${corpus}.txt
cat scores/${corpus}.txt \
>> results/${corpus}.txt
done

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
