load "common.plt"
set output ARG1

set title "Unique Data in Cache"
set ylabel "GB"

plot ARG2 using "alpha":(column("usize")/1e9) with lines title 'Tree', \
     ARG3 using "alpha":(column("usize")/1e9) with lines title 'Random', \
     ARG4 using "alpha":(column("usize")/1e9) with lines title 'Distribution'
