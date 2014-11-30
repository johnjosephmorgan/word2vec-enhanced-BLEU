#!/bin/bash -x

python \
./my_eval.py \
| sort -u \
> gen.txt

