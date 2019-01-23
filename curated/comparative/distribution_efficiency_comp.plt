load "common.plt"
set output ARG4

set title "Cache versus Container Efficiency"
set ylabel "Percent"
set yrange [:103]
set xrange [0.4:]

set key center left

plot ARG1 using "alpha":(column("usize")/column("size")*100) with lines title 'Distribution Cache Efficiency', \
     ARG1 using "alpha":(column("efficiency")*100) with lines title 'Distribution Container Efficiency', \
     ARG2 using "alpha":(column("usize")/column("size")*100) with lines title 'Dependency Tree Cache Efficiency', \
     ARG2 using "alpha":(column("efficiency")*100) with lines title 'Dependency Tree Container Efficiency', \
     ARG3 using "alpha":(column("usize")/column("size")*100) with lines title 'Random Cache Efficiency', \
     ARG3 using "alpha":(column("efficiency")*100) with lines title 'Random Container Efficiency'
