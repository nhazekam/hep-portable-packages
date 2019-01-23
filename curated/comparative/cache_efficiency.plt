load "common.plt"
set output ARG2

set title "Cache Contents Duplication"
set ylabel "GB"
set xrange [0.4:]

plot ARG1 using "alpha":(column("usize")/1e9) with lines title 'Unique Data in Cache', \
     ARG1 using "alpha":(column("size")/1e9) with lines title 'Total Data in Cache', \
