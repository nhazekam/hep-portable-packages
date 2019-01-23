load "common.plt"
set output ARG2

set title "Operation Counts"
set xrange[0.4:]

plot ARG1 using "alpha":"inserts" with lines title 'Inserts', \
     ARG1 using "alpha":"deletes" with lines title 'Deletes', \
     ARG1 using "alpha":"merges" with lines title 'Merges', \
     ARG1 using "alpha":"hits" with lines title 'Hits'
