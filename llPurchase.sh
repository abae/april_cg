#!/bin/bash

clickAndWait() {
    xdotool mousemove --sync $1 $2
    xdotool click 1
    sleep $3
}

clickAndWait 726 202 4 #buy button
clickAndWait 1137 946 5 #$20 pack

# clickAndWait 1315 565 5 #payment method
clickAndWait 1315 962 5 #payment method bank
# clickAndWait 1315 1029 5 #payment method bank

#--citi dc
# xdotool type "260" #card code

#--citi checking
# xdotool type "888" #card code

#--sofi checking
# xdotool type "288" #card code

#--chase amazon
# xdotool type "882" #card code

#--amex gold
#xdotool type "3657" #card code

#--discover it
#xdotool type "786" #card code

sleep 2
# clickAndWait 1237 902 13 #purchase button
clickAndWait 1237 865 28 #purchase button bank
# clickAndWait 1237 784 13 #purchase button bank
# clickAndWait 972 523 2 #close payment
clickAndWait 972 608 2 #close payment bank
clickAndWait 988 739 5 #close purchase
echo "Purchased pack $i/$1"
# python3 starSpellCheckMinute.py

# wait about a minute
sleep 9

clickAndWait 993 739 5 #close purchase

clickAndWait 200 200 1
clickAndWait 205 200 1
clickAndWait 200 200 1
