#!/bin/bash

rm --recursive VYSLEDOK
cp TEST/test.warc /home/martin/Reasearch/git/clueWeb 
gzip test.warc
./app.py --file=test.warc.gz --output=VYSLEDOK
