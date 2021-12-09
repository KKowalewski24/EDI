#!/bin/bash

python main.py -n 4 8 16 32 -i 10000 -lr 0.01 -pn 10000 -pw 8 -ti data/01.bmp data/08.bmp
python main.py -n 4 8 16 32 -i 10000 -lr 0.01 -pn 10000 -pw 8 -ti data/02.bmp data/07.bmp
python main.py -n 4 8 16 32 -i 10000 -lr 0.01 -pn 10000 -pw 8 -ti data/03.bmp data/06.bmp
python main.py -n 4 8 16 32 -i 10000 -lr 0.01 -pn 10000 -pw 8 -ti data/04.bmp data/05.bmp
