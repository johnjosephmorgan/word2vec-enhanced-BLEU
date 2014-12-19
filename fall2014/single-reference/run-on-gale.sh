#!/bin/bash -x


rm -Rf scores/wmt13.txt / 
rm -Rf logs/

mkdir -p scores logs

#get gale data
for pair in Arabic-English Chinese-English
do
for genre in NW WB
do
scripts/get-gale-ref-from-xml.pl  \
/home/john/GALE_MetricsMaTr08_10/data/GALEP2/$pair/${genre}/reference.xml  \
> data/eval-gale.08.2.$pair.$genre.ref
done
done

scripts/get-gale-ref-from-xml.pl  \
/home/john/GALE_MetricsMaTr08_10/data/GALEP25/Arabic-English/BN/reference.xml \
> data/eval-gale.08.25.Arabic-English.BN.ref

for genre in BC BN
do
scripts/get-gale-ref-from-xml.pl  \
/home/john/GALE_MetricsMaTr08_10/data/GALEP25/Chinese-English/$genre/reference.xml \
> data/eval-gale.08.25.Chinese-English.$genre.ref
done

for system in s01 s02 
do
scripts/paste-files.pl \
data/eval-gale.08.25.Arabic-English.BN.$system \
data/eval-gale.08.25.Arabic-English.BN.ref \
> data/eval_gale.08.25.Arabic-English.BN.${system}.txt
done

for genre in BC BN
do 
for system in s01 s02 s03
do
scripts/paste-files.pl \
data/eval-gale.08.25.Chinese-English.${genre}.$system \
data/eval-gale.08.25.Chinese-English.${genre}.ref \
> data/eval_gale.08.25.Chinese-English.${genre}.${system}.txt
done
done

for corpus in gale.08.25.Arabic-English.BN.s01 gale.08.25.Arabic-English.BN.s02 gale.08.25.Chinese-English.BC.s01 gale.08.25.Chinese-English.BC.s02 gale.08.25.Chinese-English.BC.s03 gale.08.25.Chinese-English.BN.s01 gale.08.25.Chinese-English.BN.s02 gale.08.25.Chinese-English.BN.s03 wmt13 artificial anomolous
do
python \
bleu/bleu.py  \
-C data/eval_$corpus.txt \
> scores/bleu-run-$corpus.txt
done


for corpus in gale.08.25.Arabic-English.BN.s01 gale.08.25.Arabic-English.BN.s02 gale.08.25.Chinese-English.BC.s01 gale.08.25.Chinese-English.BC.s02 gale.08.25.Chinese-English.BC.s03 gale.08.25.Chinese-English.BN.s01 gale.08.25.Chinese-English.BN.s02 gale.08.25.Chinese-English.BN.s03 wmt13 artificial anomolous
do
for metric in xleu sleu vleu
do
python \
$metric/$metric.py \
-C data/eval_$corpus.txt \
-V ./GoogleNews-vectors-negative300.bin.gz \
> scores/${metric}-run-${corpus}.txt
done
done

rm -Rf results/* 
rmdir results
mkdir -p results

for corpus in gale.08.25.Arabic-English.BN.s01 gale.08.25.Arabic-English.BN.s02 gale.08.25.Chinese-English.BC.s01 gale.08.25.Chinese-English.BC.s02 gale.08.25.Chinese-English.BC.s03 gale.08.25.Chinese-English.BN.s01 gale.08.25.Chinese-English.BN.s02 gale.08.25.Chinese-English.BN.s03 wmt13 artificial anomolous
do
echo "method	relevant	total	precision	score" > results/${corpus}.txt
for method in xleu bleu sleu vleu
do
cat scores/${method}-run-${corpus}.txt \
>> results/${corpus}.txt
done
done

scripts/multi-bleu.perl \
data/eval_corpus_ref.txt \
< data/eval_corpus_sys.txt \
> scores/multibleu-run-wmt13.txt

rm xleu_candidate_reference_similarity.log


for metric in xleu vleu sleu
do
echo "candidate	reference	similarity" > ${metric}_candidate_reference_similarity.log
cat ./${metric}_count_syns.log \
| grep root \
| perl -e \
"while (<>) {s/INFO:root://;s/[']//g;s/\[//g;s/\]//g;s/\(//g;s/\)//g;s/,//g;print;}" \
| sort -u \
>> ${metric}_candidate_reference_similarity.log
done
mv [bsvx]leu_candidate_reference_similarity.log logs/
