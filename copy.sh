#!/bin/sh

max=2780
for i in `seq 1292 $max`
do
    echo "$i"
    cp /Volumes/HARIDHAANAM/bitcoin/blocks/blk0$i.dat ~/Documents/bitcoin/blocks/blk0$i.dat
done


#ln -s /Volumes/HARIDHAANAM/bitcoin/blk00001.dat /Users/sreenath/Documents/bitcoin/blocks/blk00001.dat