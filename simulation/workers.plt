load "common.plt"
set output ARG1

set title "Workers per Job"

plot ARG2 using "alpha":"workers" with lines title 'Tree', \
     ARG3 using "alpha":"workers" with lines title 'Random'
