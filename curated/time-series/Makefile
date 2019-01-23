.PHONY: all
all: time-series.pdf

.PHONY: clean
clean:
	rm -f *.dat *.pdf

time-series.dat: time-series.json ser.py
	./ser.py dist 0.75 0 < $< > $@

time-series.pdf: time-series.plt time-series.dat
	gnuplot -c  $^ $@
