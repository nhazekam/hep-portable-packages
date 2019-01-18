load "common.plt"
set output ARG1

set title "Transfer Efficiency vs. Concurrent Apps"

set y2tics
set ylabel "Percent"

plot ARG2 using "alpha":(column("efficiency")*100) with lines axes x1y1 title 'Efficiency', \
     ARG2 using "alpha":"requests" with lines axes x1y2 title 'Concurrent Apps'
