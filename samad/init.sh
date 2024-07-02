#!/bin/bash

TODAY=$(date '+%Y-%m-%d')
NOW=$(date '+%Y-%m-%d %H:%M:%S')

python3 main.py -h
python3 main.py deleteDB
python3 main.py register -n 0926985114 -i 40131053 -m CE -b 1403/09/30 -f Ali -l Naserinia -c 0
python3 main.py register -n 0926985111 -i 40131054 -m CE -b 1403/09/30 -f Saeed -l Pezeshkian -c 0
python3 main.py register -n 0926985112 -i 40131052 -m CS -b 1403/09/12 -f Masood -l Jalili -c 0
python3 main.py register -n 0926985112 -i 40131050 -m CS -b 1403/09/12 -f Masood -l Jalili -c 0  # duplicate id
python3 main.py credit -i 40131053 -m 10000
python3 main.py add -n baghali -d $TODAY -p 10000 -i 500
python3 main.py add -n polo -d $TODAY -p 5000 -i 600
python3 main.py add -n mahi -d $TODAY -p 5000 -i 700
python3 main.py add -n kashk -d 2023-07-03 -p 5000 -i 800
python3 main.py add -n ash -d 2023-07-10 -p 5000 -i 400  # less than 500
python3 main.py reserve -s 40131054 -f 2
python3 main.py reserve -s 40131053 -f 1
python3 main.py credit -i 40131054 -m -10
python3 main.py credit -i 40131054 -m 20000
python3 main.py reserve -s 40131054 -f 2
python3 main.py reserve -s 40131054 -f 1
python3 main.py reserve -s 40131054 -f 4
python3 main.py change -s 4 -d NULL
python3 main.py showDB
python3 main.py showToday
python3 main.py showStuToday
python3 main.py showLast10Transactions
python3 main.py showRemainFood
python3 main.py assetTurnover
python3 main.py studentFood
python3 main.py studentTransaction
python3 main.py change -s 1 -d NULL
python3 main.py change -s NULL -d 1 -t "$NOW"
python3 main.py change -s NULL -d 4 -t "$NOW"
NOW=$(date '+%Y-%m-%d %H:%M:%S')
python3 main.py change -s 3
python3 main.py change -d 3 -t "$NOW"
python3 main.py change -d 4 -t "$NOW"
python3 main.py showDB