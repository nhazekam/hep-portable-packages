CACHE = 2
REQUEST = 500
USES = 5

CACHE_DAT = $(foreach cache, 0 1 2 5 10 ,lxplus.$(cache).$(REQUEST).$(USES).dat)
REQUEST_DAT = $(foreach req, 100 500 1000 ,lxplus.$(CACHE).$(req).$(USES).dat)
USES_DAT = $(foreach uses, 1 5 10 25 ,lxplus.$(CACHE).$(REQUEST).$(uses).dat)


%_cache_percent_plt.pdf : span.generic.percent.plt ${CACHE_DAT} common.plt
	gnuplot -c  $< $@ $* ${CACHE_DAT}

%_request_percent_plt.pdf : span.generic.percent.3.plt ${REQUEST_DAT} common.plt
	gnuplot -c  $< $@ $* ${REQUEST_DAT}

%_uses_percent_plt.pdf : span.generic.percent.plt ${USES_DAT} common.plt
	gnuplot -c  $< $@ $* ${USES_DAT}

SPAN_PERCENT_GRAPHS = $(foreach type, cache request uses,$(foreach field, cache_efficiency container_efficiency , $(field)_$(type)_percent_plt.pdf))

.PHONY: all
all : ${SPAN_PERCENT_GRAPHS}

.PHONY: clean
clean:
	rm -rf *.pdf
