load "common.plt"
set output ARG1

set title "Tree Efficiency"
set ylabel "Percent"
set yrange [:103]
set xrange [0.4:]

plot ARG2 using "alpha":(column("cache_efficiency")*100) with lines title 'Cache Efficiency', \
     ARG2 using "alpha":(column("container_efficiency")*100) with lines title 'Container Efficiency', \
     ARG2 using "alpha":(column("hitrate")*100) with lines title 'Container Hitrate'
