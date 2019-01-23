set terminal pdf monochrome
set output OUT
set datafile separator ","
set boxwidth 0.9 relative
set style data histograms
set style histogram cluster
set style fill solid 1.0 border lt -1
set logscale y
set key off
set xrange [-1:]
set xlabel "log2 file size (B)"
set ylabel "Count"
set arrow from 20, graph 0 to 20, graph 1 nohead
plot SRC using 2
#plot SRC using 2:xticlabels(1)
