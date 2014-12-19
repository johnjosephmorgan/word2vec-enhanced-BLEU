#!/bin/bash -x

mkdir -p scores logs

rm xleu_count_syns.log

#generate some very simple sentences
python scripts/my_eval.py \
> data/gen.txt

#split the list of simple sentences
#1 sublist will serve as candidates and 1 as references
scripts/gen2corpus.pl \
data/gen.txt

shuf ./cands.txt > data/cands.txt
shuf ./refs.txt > data/refs.txt

#paste the candidates and references into 1 file
# we will use the cdec format for an evaluation corpus
# CANDIDATESENTENCE ||| REFERENCES 
scripts/paste-files.pl \
data/cands.txt \
data/refs.txt \
> data/eval_artificial.txt

mkdir -p results

python \
svxleu/svxleu.py \
-C data/eval_artificial.txt \
-V ./GoogleNews-vectors-negative300.bin.gz \
-t 0.85 \
> scores/svxleu-artificial.txt

python \
bleu/bleu.py \
-C data/eval_artificial.txt \
> scores/bleu-artificial.txt


scripts/multi-bleu.perl \
data/refs.txt \
< data/cands.txt \
> scores/multibleu-artificial.txt

rm svxleu_candidate_reference_similarity.log

echo "candidate	reference	similarity" > svxleu_candidate_reference_similarity.log
cat ./xleu_count_syns.log \
| grep root \
| perl -e \
"while (<>) {s/INFO:root://;s/[']//g;s/\[//g;s/\]//g;s/\(//g;s/\)//g;s/,//g;print;}" \
| sort -u \
>> svxleu_candidate_reference_similarity.log


mv svxleu_candidate_reference_similarity.log logs/
