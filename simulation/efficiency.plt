load "common.plt"
set output ARG1

set title "Compute/Network Efficiency/Speedup/Slowdown (??)"
set ylabel "Percent"
set yrange [:103]

plot ARG2 using "alpha":(column("efficiency")*100) with lines title 'Tree', \
     ARG3 using "alpha":(column("efficiency")*100) with lines title 'Random'
