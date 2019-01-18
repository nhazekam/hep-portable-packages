load "common.plt"
set output ARG1

set title "Concurrent Applications in Cache"

plot ARG2 using "alpha":"requests" with lines title 'Tree', \
     ARG3 using "alpha":"requests" with lines title 'Random'
