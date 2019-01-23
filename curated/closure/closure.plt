set terminal pdf monochrome size 11in,8.5in font "Helvetica,30"
set output ARG2

set title "Dependencies of Package Selections"
set ytics nomirror
set y2tics nomirror
set key top left
set xlabel "Packages Requested"
set ylabel "Packages Included"
set y2label "GB"

plot ARG1 using "picks":"choicecount" with lines axes x1y1 title "Request Count", \
     "" using "picks":(column("choicesize")/1e9) with lines axes x1y2 title "Request Size", \
     "" using "picks":"closurecount" with lines axes x1y1 title "Resolved Count", \
     "" using "picks":(column("closuresize")/1e9) with lines axes x1y2 title "Resolved Size"
