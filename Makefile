TEMPLATES=templates
OUT=out

PROG = ./ruling.py

all:	$(OUT)/A4/grid-5.pdf \
	$(OUT)/A4/copperplate-winters.pdf $(OUT)/A4/copperplate-winters-l.pdf \
	$(OUT)/A4/copperplate-1.pdf $(OUT)/A4/copperplate-1-l.pdf \
	$(OUT)/A4/copperplate-2.pdf $(OUT)/A4/copperplate-2-l.pdf \
	$(OUT)/A4/italic-3-5-3.pdf $(OUT)/A4/italic-3-5-3-l.pdf \
	$(OUT)/A4/ruled-5.pdf $(OUT)/A4/ruled-8.pdf $(OUT)/A4/ruled-10.pdf \
	$(OUT)/A4/ruled-alt-10.pdf \
	$(OUT)/A4/slant-52.pdf $(OUT)/A4/slant-52-l.pdf \
	$(OUT)/A4/slant-55.pdf $(OUT)/A4/slant-55-l.pdf \
	$(OUT)/A4/zaner-1.pdf $(OUT)/A4/zaner-1-l.pdf \
	$(OUT)/A5/slant-52.pdf $(OUT)/A5/slant-52-l.pdf $(OUT)/A5/slant-pair.pdf


$(OUT)/A4/grid-5.pdf:	Makefile $(PROG) $(TEMPLATES)/grid
	$(PROG) @$(TEMPLATES)/grid --pagesize A4 --nib-width 5 -o $@


$(OUT)/A4/copperplate-winters.pdf:	Makefile $(PROG) $(TEMPLATES)/copperplate-winters
	$(PROG) @$(TEMPLATES)/copperplate-winters --pagesize A4 -o $@
	$(PROG) @$(TEMPLATES)/copperplate-winters --pagesize A4 --mirror -o mirror-$@

$(OUT)/A4/copperplate-winters-l.pdf:	Makefile $(PROG) $(TEMPLATES)/copperplate-winters
	$(PROG) @$(TEMPLATES)/copperplate-winters --pagesize A4 --landscape -o $@
	$(PROG) @$(TEMPLATES)/copperplate-winters --pagesize A4 --landscape --mirror -o mirror-$@


$(OUT)/A4/copperplate-1.pdf:	Makefile $(PROG) $(TEMPLATES)/copperplate
	$(PROG) @$(TEMPLATES)/copperplate --gap 1.0 --pagesize A4 -o $@

$(OUT)/A4/copperplate-1-l.pdf:	Makefile $(PROG) $(TEMPLATES)/copperplate
	$(PROG) @$(TEMPLATES)/copperplate --gap 1.0 --pagesize A4 --landscape -o $@


$(OUT)/A4/copperplate-2.pdf:	Makefile $(PROG) $(TEMPLATES)/copperplate
	$(PROG) @$(TEMPLATES)/copperplate --nib-width 10 --gap 2 --pagesize A4 -o $@

$(OUT)/A4/copperplate-2-l.pdf:	Makefile $(PROG) $(TEMPLATES)/copperplate
	$(PROG) @$(TEMPLATES)/copperplate --nib-width 10 --gap 1.5 --pagesize A4 --landscape -o $@


$(OUT)/A4/italic-3-5-3.pdf:	Makefile $(PROG) $(TEMPLATES)/italic-3-5-3
	$(PROG) @$(TEMPLATES)/italic-3-5-3 --pagesize A4 --nib-width 1.1 -o $@

$(OUT)/A4/italic-3-5-3-l.pdf:	Makefile $(PROG) $(TEMPLATES)/italic-3-5-3
	$(PROG) @$(TEMPLATES)/italic-3-5-3 --pagesize A4 --nib-width 1.1 --landscape -o $@


$(OUT)/A4/ruled-5.pdf:	Makefile $(PROG) $(TEMPLATES)/ruled
	$(PROG) @$(TEMPLATES)/ruled --pagesize A4 --nib-width 5 -o $@

$(OUT)/A4/ruled-8.pdf:	Makefile $(PROG) $(TEMPLATES)/ruled
	$(PROG) @$(TEMPLATES)/ruled --pagesize A4 --nib-width 8 -o $@

$(OUT)/A4/ruled-10.pdf:	Makefile $(PROG) $(TEMPLATES)/ruled
	$(PROG) @$(TEMPLATES)/ruled --pagesize A4 --nib-width 10 -o $@


$(OUT)/A4/ruled-alt-10.pdf:	Makefile $(PROG) $(TEMPLATES)/ruled-alt
	$(PROG) @$(TEMPLATES)/ruled-alt --pagesize A4 --nib-width 10 -o $@


$(OUT)/A4/slant-55.pdf:	Makefile $(PROG) $(TEMPLATES)/slant-55
	$(PROG) @$(TEMPLATES)/slant-55 --pagesize A4 -o $@
	$(PROG) @$(TEMPLATES)/slant-55 --pagesize A4 --mirror -o mirror-$@

$(OUT)/A4/slant-55-l.pdf:	Makefile $(PROG) $(TEMPLATES)/slant-55
	$(PROG) @$(TEMPLATES)/slant-55 --pagesize A4 --landscape -o $@
	$(PROG) @$(TEMPLATES)/slant-55 --pagesize A4 --landscape --mirror -o mirror-$@


$(OUT)/A4/slant-52.pdf:	Makefile $(PROG) $(TEMPLATES)/slant-52
	$(PROG) @$(TEMPLATES)/slant-52 --pagesize A4 -o $@
	$(PROG) @$(TEMPLATES)/slant-52 --pagesize A4 --mirror -o mirror-$@

$(OUT)/A4/slant-52-l.pdf:	Makefile $(PROG) $(TEMPLATES)/slant-52
	$(PROG) @$(TEMPLATES)/slant-52 --pagesize A4 --landscape -o $@
	$(PROG) @$(TEMPLATES)/slant-52 --pagesize A4 --landscape --mirror -o mirror-$@


$(OUT)/A5/slant-52.pdf:	Makefile $(PROG) $(TEMPLATES)/slant-52
	$(PROG) @$(TEMPLATES)/slant-52 --pagesize A5 -o $@
	$(PROG) @$(TEMPLATES)/slant-52 --pagesize A5 --mirror -o mirror-$@

$(OUT)/A5/slant-52-l.pdf:	Makefile $(PROG) $(TEMPLATES)/slant-52
	$(PROG) @$(TEMPLATES)/slant-52 --pagesize A5 --landscape -o $@
	$(PROG) @$(TEMPLATES)/slant-52 --pagesize A5 --landscape --mirror -o mirror-$@

$(OUT)/A5/slant-pair.pdf:	Makefile $(PROG) $(TEMPLATES)/slant-52 $(TEMPLATES)/slant-38
	$(PROG) @$(TEMPLATES)/slant-52 --pagesize A5 --bleed full -o .pair-1.pdf
	$(PROG) @$(TEMPLATES)/slant-38 --pagesize A5 --bleed full -o .pair-2.pdf
	pdfflip .pair-2.pdf
	pdfnup --nup 2x1 --paper a4paper -o $@ .pair-1.pdf .pair-2-flipped.pdf
	rm -f .pair*


$(OUT)/A4/zaner-1.pdf:	Makefile $(PROG) $(TEMPLATES)/zaner-1
	$(PROG) @$(TEMPLATES)/zaner-1 --pagesize A4 -o $@

$(OUT)/A4/zaner-1-l.pdf:	Makefile $(PROG) $(TEMPLATES)/zaner-1
	$(PROG) @$(TEMPLATES)/zaner-1 --pagesize A4 --landscape -o $@
