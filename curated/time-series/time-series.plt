set terminal pdf monochrome size 11in,8.5in font "Helvetica,30"
set output ARG2

set title "Summary of a Single Simulation"
set xlabel "Requests"
set ylabel "Count"
set y2label "TB"
set ytics nomirror
set y2tics nomirror
set xrange [:250]
set key top left

plot ARG1 using "step":"hits" with line axes x1y1 title "Hits", \
     '' using "step":"inserts" with line axes x1y1 title "Inserts", \
     '' using "step":"deletes" with line axes x1y1 title "Deletes", \
     '' using "step":"merges" with line axes x1y1 title "Merges", \
     '' using "step":(column("size")/1e12) with line axes x1y2 title "Cached Data", \
     '' using "step":(column("byteswritten")/1e12) with line axes x1y2 title "Bytes Written"
