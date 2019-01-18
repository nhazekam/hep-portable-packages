load "common.plt"
set output ARG1

set title "Unique Packages in Cache"

plot ARG2 using "alpha":"upkgs" with lines title 'Tree', \
     ARG3 using "alpha":"upkgs" with lines title 'Random'
