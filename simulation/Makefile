.PHONY: all
all: \
	sft.lst.txt \
	sft.buildinfo.json \
	sft.du.txt \
	sft.deps.json \
	sft.recent.json \
        sft.dist.dat \
        sft.sim.json \
        sft.tree.dat \
        sft.blind.dat \
        byteswritten.plt.pdf \
        images.plt.pdf \
        pkgs.plt.pdf \
        size.plt.pdf \
        upkgs.plt.pdf \
        usize.plt.pdf \
        inserts.plt.pdf \
        converge.plt.pdf \
        nanner.plt.pdf \
        deletes.plt.pdf \
        merges.plt.pdf \
        hits.plt.pdf \
        pool.plt.pdf \
        activeimgs.plt.pdf \
        workers.plt.pdf \
        tx.plt.pdf \
        txcost.plt.pdf \
        requests.plt.pdf \
        imagesizes.plt.pdf \
        efficiency.plt.pdf \
        overhead.plt.pdf \
        ops-tree.plt.pdf \
        sft.dist.pdf \
	sft.dot

sft.lst.txt:
	find /cvmfs/sft.cern.ch/lcg/releases/ -type f -name '.buildinfo_*.txt' > $@ || true

%.buildinfo.json: %.lst.txt
	./read_buildinfo.py < $< > $@

%.recent.json: %.buildinfo.json
	./recent.py < $< > $@

%.deps.json: %.buildinfo.json %.du.txt
	./deps.py $^ > $@

%.sim.json: %.deps.json
	./sim.py < $< > $@

%.du.txt: %.lst.txt
	cat $< | sed 's/[^/]*$$//' | xargs du -bs > $@ || true

%.dist.dat: %.deps.json
	./picks.py < $< > $@

%.tree.dat: %.sim.json
	./dat.py tree < $< > $@

%.blind.dat: %.sim.json
	./dat.py blind < $< > $@

%.dot: %.deps.json %.recent.json
	./graph.py $^ > $@

%.plt.pdf: %.plt sft.tree.dat sft.blind.dat common.plt
	gnuplot -c $< $@ sft.tree.dat sft.blind.dat

%.dist.pdf: dist.plt %.dist.dat
	gnuplot -c $^ $@

.PHONY: clean
clean:
	rm -rf *.pdf

.PHONY: nuke
nuke: clean
	rm -rf *.txt *.json *.dot *.dat
