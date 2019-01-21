load "common.plt"
set output ARG1

set title "Operation Counts (Tree)"

plot ARG2 using "alpha":"inserts" with lines title 'Inserts', \
     ARG2 using "alpha":"deletes" with lines title 'Deletes', \
     ARG2 using "alpha":"merges" with lines title 'Merges', \
     ARG2 using "alpha":"hits" with lines title 'Hits'
