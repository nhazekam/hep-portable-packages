load "common.plt"
set output ARG2

set title "Cumulative Bytes Written"
set ylabel "GB"
set xrange [0.4:]

plot ARG1 using "alpha":(column("byteswritten")/1e9) with lines title 'Actual Bytes Written', \
     ARG1 using "alpha":(column("reqwritten")/1e9) with lines title 'Requested Bytes Written', \
