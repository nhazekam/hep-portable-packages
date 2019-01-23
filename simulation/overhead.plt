load "common.plt"
set output ARG1

set title "Median Request Overhead"
set ylabel "GB"

plot ARG2 using "alpha":(column("overhead")/1e9) with lines title 'Tree', \
     ARG3 using "alpha":(column("overhead")/1e9) with lines title 'Random', \
     ARG4 using "alpha":(column("overhead")/1e9) with lines title 'Distribution'
