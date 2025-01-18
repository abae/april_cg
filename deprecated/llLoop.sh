#!/bin/bash

clickAndWait() {
    xdotool mousemove --sync $1 $2
    xdotool click 1
    sleep $3
}

for i in $(seq 1 $1)
do
    sh ./llPurchase.sh 1 5 0

    clickAndWait 571 450 7
    clickAndWait 780 715 1
    clickAndWait 780 715 1
    clickAndWait 780 715 1
    clickAndWait 1692 986 5

    python3 ./llAutoBj.py 35

    clickAndWait 292 199 5
done
