load "common.plt"
set output ARG1

set title "Images in Worker Caches"

plot ARG2 using "alpha":"activeimgs" with lines title 'Tree', \
     ARG3 using "alpha":"activeimgs" with lines title 'Random'
