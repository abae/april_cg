#!/bin/sh
# play a game of blackjack after buying packs.

clickAndWait() {
    xdotool mousemove --sync $1 $2
    xdotool click 1
    sleep $3
}

clickAndWait 292 199 5 #home button
clickAndWait 278 314 1 #category button
clickAndWait 574 448 8 #game button

for i in $(seq 1 $1)
do
    clickAndWait 784 726 1 #+1 button
done

clickAndWait 1692 1006 10 #play button

python3 ./llAutoBj.py $((300/{$1})) $1
