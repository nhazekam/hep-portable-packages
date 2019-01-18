load "common.plt"
set output ARG1

set title "Median Images in Cache"

plot ARG2 using "alpha":"images" with lines title 'Tree', \
     ARG3 using "alpha":"images" with lines title 'Random'
