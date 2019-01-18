load "common.plt"
set output ARG1

set title "Worker Transfer per Job"
set ylabel "GB"

plot ARG2 using "alpha":(column("txcost")/1e9) with lines title 'Tree', \
     ARG3 using "alpha":(column("txcost")/1e9) with lines title 'Random'
