#!/bin/bash

set -e

python main.py -f data/ftims.html --plain
python main.py -f data/weeia.html --plain

python main.py -f output/ftims.txt --arff
python main.py -f output/weeia.txt --arff
