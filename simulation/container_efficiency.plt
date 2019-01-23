load "common.plt"
set output ARG1

set title "Cumulative Bytes Written"
set ylabel "GB"

plot ARG2 using "alpha":(column("byteswritten")/1e9) with lines title 'Actual Bytes Written', \
     ARG2 using "alpha":(column("reqwritten")/1e9) with lines title 'Requested Bytes Written', \
