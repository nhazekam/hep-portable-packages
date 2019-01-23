load "common.plt"
set output ARG1

set title ARG2
set yrange [0:]
set xrange [0.4:]

plot ARG3 using "alpha":(column(ARG2)) with lines title ARG3, \
     ARG4 using "alpha":(column(ARG2)) with lines title ARG4, \
     ARG5 using "alpha":(column(ARG2)) with lines title ARG5, \
     ARG6 using "alpha":(column(ARG2)) with lines title ARG6
