#!/usr/bin/bash
x=1

while [ $x -le 645123 ] # 4 358, 5 2012, #15 1407316, 14 4714356, 13 3473737, 12 2257929, 11 1290245, 10 645123, 9 280489, 8 105184, 7 33659, 6 9062, 5 2014, 4 360, 3 50, 2 5
    # 16 102438, 17 5657228, 18 1513448, 19 3473737, 20 2257929, 21 1290245, 22 645123
do
    rm -rf "data/ones_22_$x.json"
    echo "rm -rf data/ones_22 _ $x.json"
    echo "Welcome $n $x times"
    x=$(( $x + 1 ))
done