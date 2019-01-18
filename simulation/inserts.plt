load "common.plt"
set output ARG1

set title "Insert Count"

plot ARG2 using "alpha":"inserts" with lines title 'Tree', \
     ARG3 using "alpha":"inserts" with lines title 'Random'
