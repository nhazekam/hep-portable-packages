load "common.plt"
set output ARG1

set title "Transfers per Job"

plot ARG2 using "alpha":"tx" with lines title 'Tree', \
     ARG3 using "alpha":"tx" with lines title 'Random'
