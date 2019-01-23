load "common.plt"
set output ARG1

set title "Tree Efficiency"
set ylabel "Percent"
set yrange [:103]

plot ARG2 using "alpha":(column("usize")/column("size")*100) with lines title 'Cache Efficiency', \
     ARG2 using "alpha":(column("efficiency")*100) with lines title 'Container Efficiency'
