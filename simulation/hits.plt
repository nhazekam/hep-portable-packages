load "common.plt"
set output ARG1

set title "Hit Count"

plot ARG2 using "alpha":"hits" with lines title 'Tree', \
     ARG3 using "alpha":"hits" with lines title 'Random'
