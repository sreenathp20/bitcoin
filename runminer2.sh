#!/bin/sh

max=10
for i in `seq 1 $max`
do
    . /Users/sreenath/Documents/bitcoin_code2/venv/bin/activate
    python /Users/sreenath/Documents/bitcoin_code2/bitcoin/ntgbtminer/ntgbtminer.py sreenath 1DpMnorqAqtuEuZhD3tNujL83QhD9qEvG4 0 > /Users/sreenath/Documents/bitcoin_code2/logs/out_0_$i.log 2>&1 &
done