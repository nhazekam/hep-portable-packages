.PHONY: all
all: cdf.pdf

.PHONY: clean
clean:
	rm -f *.pdf

%.dat: %.csv
	./clean.py < $< > $@

cdf.pdf: cdf.plt atlas.dat cms.dat sft.dat lhcb.dat
	gnuplot -c $^ $@
