#!/bin/sh

max=4
for i in `seq 1 $max`
do
    #echo "$i"
    python /Users/sreenath/Documents/bitcoin_code/ntgbtminer/ntgbtminer.py sreenath 1DpMnorqAqtuEuZhD3tNujL83QhD9qEvG4 0 > /Users/sreenath/Documents/bitcoin_code/logs/out_0_$i.log 2>&1 &
    sleep 1
    python /Users/sreenath/Documents/bitcoin_code/ntgbtminer/ntgbtminer.py sreenath 1DpMnorqAqtuEuZhD3tNujL83QhD9qEvG4 1000000000 > /Users/sreenath/Documents/bitcoin_code/logs/out_1000000000_$i.log 2>&1 &
    #sleep 1
    python /Users/sreenath/Documents/bitcoin_code/ntgbtminer/ntgbtminer.py sreenath 1DpMnorqAqtuEuZhD3tNujL83QhD9qEvG4 2000000000 > /Users/sreenath/Documents/bitcoin_code/logs/out_2000000000_$i.log 2>&1 &
    #sleep 1
    python /Users/sreenath/Documents/bitcoin_code/ntgbtminer/ntgbtminer.py sreenath 1DpMnorqAqtuEuZhD3tNujL83QhD9qEvG4 3000000000 > /Users/sreenath/Documents/bitcoin_code/logs/out_3000000000_$i.log 2>&1 &
done