set terminal pdf monochrome size 11in,8.5in font "Helvetica,30"
set output ARG2

set title "Dependencies of a Set of Packages"
set y2tics

set xlabel "Selection size (packages)"
set y2label "GB"

plot ARG1 using 1:2 with lines axes x1y1 title "Packages", \
     ARG1 using 1:($3/1e9) with lines axes x1y2 title "Data"
