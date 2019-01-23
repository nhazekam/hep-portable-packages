load "common.plt"
set output ARG1

set title "Median Image Size"
set ylabel "GB"

plot ARG2 using "alpha":(column("imagesizes")/1e9) with lines title 'Tree', \
     ARG3 using "alpha":(column("imagesizes")/1e9) with lines title 'Random', \
     ARG4 using "alpha":(column("imagesizes")/1e9) with lines title 'Distribution'
