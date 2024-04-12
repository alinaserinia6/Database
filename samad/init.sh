#!/bin/bash

python3 main.py -h
python3 main.py deleteDB
python3 main.py register -n 0926985114 -i 40131053 -m CE -b 1403/09/30 -f Ali -l Naserinia -c 0
python3 main.py register -n 0926985111 -i 40131054 -m CE -b 1403/09/30 -f Ali -l Naserinia -c 0
python3 main.py credit -i 40131053 -m 10000
python3 main.py add -n baghali -d 1403-01-08 -p 10000 -i 100
python3 main.py add -n polo -d 1403-02-23 -p 5000 -i 1
python3 main.py reserve -s 40131054 -f 2
python3 main.py reserve -s 40131053 -f 1
python3 main.py credit -i 40131054 -m -10
python3 main.py credit -i 40131054 -m 5000
python3 main.py reserve -s 40131054 -f 2
python3 main.py showDB
python3 main.py delete 1
python3 main.py delete 2
python3 main.py change -s 1 -d null
python3 main.py showDB
python3 main.py change -d 1
python3 main.py showDB
python3 main.py remove 0926985114
python3 main.py remove 0926985111