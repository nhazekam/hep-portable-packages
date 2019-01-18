load "common.plt"
set output ARG1

set title "Total Bytes Written"
set ylabel "TB"

plot ARG2 using "alpha":(column("byteswritten")/1e12) with lines title 'Tree', \
     ARG3 using "alpha":(column("byteswritten")/1e12) with lines title 'Random'
