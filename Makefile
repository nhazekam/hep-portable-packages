NAME = paper

# Bibliographies used
BIBLIOGRAPHIES = cclpapers.bib otherpapers.bib

all: prepress.pdf

$(NAME).pdf: $(NAME).tex ${GRAPHS} ${BIBLIOGRAPHIES} ${LATEX_STY}
	pdflatex $(NAME)
	bibtex $(NAME)
	pdflatex $(NAME)
	pdflatex $(NAME)

graphs: ${GRAPHS}

prepress.pdf: $(NAME).pdf
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=$@ $<

%.sty : %.ins
	pdflatex $<

%.pdf: %.svg
	inkscape $< --export-pdf $@

%.pdf: %.eps
	epstopdf $< --outfile=$@

%.pdf: %.png
	convert $< $@

./loop_results/%.pdf: ./loop_results/%.eps
	epstopdf $< --outfile=$@

#%.svg: %.dot
#	dot -Tsvg <$< >$@

%.eps: %.dot
	dot -Teps <$< >$@

%.gif: %.eps
	convert $< $@

%.png: %.eps
	convert -density 300 $< -resize 2048x2048 $@

%.pdf: %.fig
	fig2dev -L pdf $< $@

%.eps: %.gnuplot %.dat
	gnuplot  -e "filename='$*.dat'" $< >$@

cclpapers.bib:
	wget -O $@ http://ccl.cse.nd.edu/research/papers/bibtex.php

clean: clean_results clean_paper

clean_results:
	echo "No results yet"

clean_paper:
	rm -f $(NAME).aux $(NAME).bbl $(NAME).blg $(NAME).dvi $(NAME).log *.log *.pdf $(LATEX_STY)


