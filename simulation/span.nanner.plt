load "common.plt"
set output ARG1

set title "Tree Efficiency"
set ylabel "Percent"
set yrange [:103]
set xrange [0.4:]

plot ARG3 using "alpha":(column("cache_efficiency")*100) with lines ls 1 title "Cache ".ARG3, \
     ARG3 using "alpha":(column("container_efficiency")*100) with lines ls 1 title "Container ".ARG3, \
     ARG4 using "alpha":(column("cache_efficiency")*100) with lines ls 2 title "Cache ".ARG4, \
     ARG4 using "alpha":(column("container_efficiency")*100) with lines ls 2 title "Container ".ARG4, \
     ARG5 using "alpha":(column("cache_efficiency")*100) with lines ls 3 title "Cache ".ARG5, \
     ARG5 using "alpha":(column("container_efficiency")*100) with lines ls 3 title "Container ".ARG5, \
     ARG6 using "alpha":(column("cache_efficiency")*100) with lines ls 4 title "Cache ".ARG6, \
     ARG6 using "alpha":(column("container_efficiency")*100) with lines ls 4 title "Container ".ARG6
