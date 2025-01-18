#!/bin/bash

clickAndWait() {
    xdotool mousemove --sync $1 $2
    xdotool click 1
    sleep $3
}

for i in $(seq 1 $1)
do
    clickAndWait 1330 904 1 #auto roll
    clickAndWait 967 790 1 #change loss option
    clickAndWait 1109 511 1 #change to number of rolls
    for i in $(seq 1 10)
    do
        clickAndWait 1376 512 0.4 #change number of rolls
    done
    clickAndWait 1165 906 4150 #start and wait
done