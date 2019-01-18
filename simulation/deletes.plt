load "common.plt"
set output ARG1

set title "Delete Count"

plot ARG2 using "alpha":"deletes" with lines title 'Tree', \
     ARG3 using "alpha":"deletes" with lines title 'Random'
