.PHONY: all
all: closure.pdf

.PHONY: clean
clean:
	rm -f *.pdf

closure.dat: deps.json closure.py
	./closure.py < $< > $@

closure.pdf: closure.plt closure.dat
	gnuplot -c $^ $@
