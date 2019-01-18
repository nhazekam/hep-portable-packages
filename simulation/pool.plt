load "common.plt"
set output ARG1

set title "Number of Jobs in Pool"

plot ARG2 using "alpha":"pool" with lines title 'Tree', \
     ARG3 using "alpha":"pool" with lines title 'Random'
