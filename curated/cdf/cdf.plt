set terminal pdf monochrome
set output ARG5

set logscale x
#set logscale y
set key top left
set title "Cumulative File Sizes"
set xlabel "File Size"
set ylabel "Count (millions)"
set xtics ("1 KB" 1e3, "1 MB" 1e6, "1 GB" 1e9)

plot ARG1 using 1:2 with lines title "ATLAS", \
     ARG2 using 1:2 with lines title "CMS", \
     ARG3 using 1:2 with lines title "SFT", \
     ARG4 using 1:2 with lines title "LHCB"
