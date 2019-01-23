.PHONY: all
all: distribution_efficiency_comp.pdf distribution_efficiency.pdf operation_count.pdf cache_efficiency.pdf container_efficiency.pdf

.PHONY: clean
clean:
	rm -f *.dat *.pdf

comparative-%.dat: comparative.json dat.py
	./dat.py $* < $< > $@

distribution_efficiency_comp.pdf: distribution_efficiency_comp.plt comparative-dist.dat comparative-tree.dat comparative-blind.dat
	gnuplot -c $^ $@

%.pdf: %.plt comparative-dist.dat
	gnuplot -c $^ $@
