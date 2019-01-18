load "common.plt"
set output ARG1

set title "Merge Count"

plot ARG2 using "alpha":"merges" with lines title 'Tree', \
     ARG3 using "alpha":"merges" with lines title 'Random'
