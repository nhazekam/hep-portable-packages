load "common.plt"
set output ARG1

set title "Total Package Count"

plot ARG2 using "alpha":"pkgs" with lines title 'tree', \
     ARG3 using "alpha":"pkgs" with lines title 'random'
