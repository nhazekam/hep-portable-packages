.PHONY: all
all: \
	sft.lst.txt \
	sft.buildinfo.json \
	sft.du.txt \
	sft.deps.json \
	sft.usage.json \
	sft.recent.json \
        sft.dist.dat \
        sft.sim.json \
        sft.tree.dat \
        sft.lxplus.dat \
        sft.blind.dat \
        byteswritten.plt.pdf \
        images.plt.pdf \
        pkgs.plt.pdf \
        size.plt.pdf \
        upkgs.plt.pdf \
        usize.plt.pdf \
        inserts.plt.pdf \
        converge.plt.pdf \
        deletes.plt.pdf \
        merges.plt.pdf \
        hits.plt.pdf \
        imagesizes.plt.pdf \
        cont_eff.plt.pdf \
        cache_eff.plt.pdf \
        nanner.plt.pdf \
        nanner2.plt.pdf \
        nanner3.plt.pdf \
        overhead.plt.pdf \
        ops-tree.plt.pdf \
        peaksize.plt.pdf \
        sft.dist.pdf \
	sft.dot

sft.lst.txt:
	find /cvmfs/sft.cern.ch/lcg/releases/ -type f -name '.buildinfo_*.txt' > $@ || true

%.buildinfo.json: %.lst.txt
	./read_buildinfo.py < $< > $@

%.usage.txt: %.usage.tar.gz
	tar -xzf $<
	find $*.usage/ -type f  > $@ || true
	find $*.usage/ -type f | wc -l

%.usage.json: %.usage.txt
	./read_usage.py < $< > $@

%.recent.json: %.buildinfo.json
	./recent.py < $< > $@

%.deps.json: %.buildinfo.json %.du.txt
	./deps.py $^ > $@

%.sim.json: %.deps.json %.usage.json
	./sim.py < $< > $@

%.du.txt: %.lst.txt
	cat $< | sed 's/[^/]*$$//' | xargs du -bs > $@ || true

%.dist.dat: %.deps.json
	./picks.py < $< > $@

lxplus.%.dat: sim.%.json
	./dat.py dist < $< > $@

%.lxplus.dat: %.sim.json
	./dat.py dist < $< > $@

%.tree.dat: %.sim.json
	./dat.py tree < $< > $@

%.blind.dat: %.sim.json
	./dat.py blind < $< > $@

%.dot: %.deps.json %.recent.json
	./graph.py $^ > $@

nanner.%.plt.pdf: par_nanner.plt lxplus.%.dat common.plt
	gnuplot -c $< $@ lxplus.$*.dat

CACHE = 2
REQUEST = 500
USES = 5

CACHE_DAT = $(foreach cache, 0 1 2 5 10 ,lxplus.$(cache).$(REQUEST).$(USES).dat)
REQUEST_DAT = $(foreach req, 10 100 500 1000 ,lxplus.$(CACHE).$(req).$(USES).dat)
USES_DAT = $(foreach uses, 1 5 10 25 ,lxplus.$(CACHE).$(REQUEST).$(uses).dat)

nanner.cache.plt.pdf : span.nanner.plt ${CACHE_DAT} common.plt
	gnuplot -c  $< $@ nanner ${CACHE_DAT}

nanner.request.plt.pdf : span.nanner.plt ${REQUEST_DAT} common.plt
	gnuplot -c  $< $@ nanner ${REQUEST_DAT}

nanner.uses.plt.pdf : span.nanner.plt ${USES_DAT} common.plt
	gnuplot -c  $< $@ nanner ${USES_DAT}


%.cache.percent.plt.pdf : span.generic.percent.plt ${CACHE_DAT} common.plt
	gnuplot -c  $< $@ $* ${CACHE_DAT}

%.request.percent.plt.pdf : span.generic.percent.plt ${REQUEST_DAT} common.plt
	gnuplot -c  $< $@ $* ${REQUEST_DAT}

%.uses.percent.plt.pdf : span.generic.percent.plt ${USES_DAT} common.plt
	gnuplot -c  $< $@ $* ${USES_DAT}



%.cache.plt.pdf : span.generic.plt ${CACHE_DAT} common.plt
	gnuplot -c  $< $@ $* ${CACHE_DAT}

%.request.plt.pdf : span.generic.plt ${REQUEST_DAT} common.plt
	gnuplot -c  $< $@ $* ${REQUEST_DAT}

%.uses.plt.pdf : span.generic.plt ${USES_DAT} common.plt
	gnuplot -c  $< $@ $* ${USES_DAT}

%.dist.pdf: dist.plt %.dist.dat 
	gnuplot -c $^ $@

NANNERS = $(foreach cache, 0 1 2 5 10,$(foreach req, 10 100 500 1000 ,$(foreach uses, 1 5 10 , nanner.$(cache).$(req).$(uses).plt.pdf)))

SPAN_GRAPHS = $(foreach type, cache request uses,$(foreach field, imagesizes hitrate byteswritten overhead nanner , $(field).$(type).plt.pdf))

SPAN_PERCENT_GRAPHS = $(foreach type, cache request uses,$(foreach field, cache_efficiency container_efficiency , $(field).$(type).percent.plt.pdf))

.PHONY: graph_spectrum
graph_spectrum : ${SPAN_GRAPHS} ${SPAN_PERCENT_GRAPHS}

.PHONY: clean_spectrum
clean_spectrum :
	rm ${SPAN_GRAPHS} ${SPAN_PERCENT_GRAPHS}

.PHONY: reload
reload:
	git checkout -- sft.lst.txt
	git checkout -- sft.du.txt
	git checkout -- sft.buildinfo.json



.PHONY: clean
clean:
	rm -rf *.pdf *.usage

.PHONY: qlean
qlean: clean
	find . -type f -empty -delete

.PHONY: nuke
nuke: clean
	rm -rf *.txt *.json *.dot *.dat
