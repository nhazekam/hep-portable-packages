load "common.plt"
set output ARG1

set title "Container Efficiency"
set ylabel "Percent"
set yrange [:103]

plot ARG2 using "alpha":(column("efficiency")*100) with lines title 'Tree', \
     ARG3 using "alpha":(column("efficiency")*100) with lines title 'Random', \
     ARG4 using "alpha":(column("efficiency")*100) with lines title 'Distribution'
