# Paper 2 LaTeX Build
# Requires: pdflatex, bibtex

MAIN = main
LATEX = pdflatex
BIBTEX = bibtex

.PHONY: all clean view

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex sections/*.tex bib/*.bib
	$(LATEX) $(MAIN)
	$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk
	rm -f sections/*.aux

view: $(MAIN).pdf
	open $(MAIN).pdf

# Quick build (no bibtex)
quick:
	$(LATEX) $(MAIN)
