#!/bin/bash -x

rm -Rf scores/wmt13.txt scores/ sleu_count_syns.log xleu_count_syns.log sleu.log xleu.log
mkdir -p scores

python scripts/my_eval.py \
> data/gen.txt

cat data/gen.txt \
| sort -u \
> data/gen-sorted.txt

scripts/gen2corpus.pl \
data/gen-sorted.txt

mv ./cands.txt ./refs.txt data/

scripts/paste-files.pl \
data/cands.txt \
data/refs.txt \
> data/eval_artificial.txt

for corpus in artificial wmt13 anomolous
do
python \
bleu/bleu.py  \
-C data/eval_$corpus.txt \
> scores/bleu-run-$corpus.txt

python \
vleu/vleu.py \
-C data/eval_$corpus.txt \
-V ~/word2vec/vectors.bin \
> scores/vleu-run-$corpus.txt

python \
sleu/sleu.py \
-C data/eval_$corpus.txt \
-V ~/word2vec/vectors.bin \
> scores/sleu-run-$corpus.txt

python \
xleu/xleu.py \
-C data/eval_$corpus.txt \
-V ~/word2vec/vectors.bin \
> scores/xleu-run-$corpus.txt
done

rm -Rf results/* 
rmdir results
mkdir -p results

for corpus in wmt13 artificial anomolous
do
echo "method	relevant	total	precision	score" > results/${corpus}.txt
for method in bleu sleu vleu xleu
do
cat scores/${method}-run-${corpus}.txt \
>> results/${corpus}.txt
done
done

scripts/multi-bleu.perl \
data/eval_corpus_ref.txt \
< data/eval_corpus_sys.txt \
> scores/multibleu-run-wmt13.txt
