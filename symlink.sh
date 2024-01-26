#!/bin/sh

max=2765
for i in `seq 1000 $max`
do
    echo "$i"
    ln -s /Volumes/HARIDHAANAM/bitcoin/blocks/blk0$i.dat /Users/sreenath/Documents/bitcoin/blocks/blk0$i.dat
done