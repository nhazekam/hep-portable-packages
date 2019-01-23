load "common.plt"
set output ARG1

set title "Size of Cache Contents"
set ylabel "GB"

plot ARG2 using "alpha":(column("size")/1e9) with lines title 'Total Data', \
     ARG2 using "alpha":(column("usize")/1e9) with lines title 'Unique Data'
