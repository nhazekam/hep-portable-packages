load "common.plt"
set output ARG2

set title "Container versus Cache Efficiency"
set ylabel "Percent Efficiency"
set yrange [:103]
set xrange [0.4:]

set label "Lower Cache\nEfficiency Limit" at 0.45,50
set arrow from 0.65,0 to 0.65,103 nohead
set arrow from 0.5,40 to 0.6,40

set arrow from 0.95,0 to 0.95,103 nohead
set label "Upper Compute\nTime Limit" at 0.82,50
set arrow from 0.92,40 to 0.82,40

plot ARG1 using "alpha":(column("usize")/column("size")*100) with lines title 'Cache', \
     ARG1 using "alpha":(column("efficiency")*100) with lines title 'Container'
