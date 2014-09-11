PROG = ./ruling.py

all:	grid-5.pdf italic-3-5-3.pdf italic-3-5-3-l.pdf

grid-5.pdf:	$(PROG) grid
	$(PROG) @grid --pagesize A4 --nib-width 5 -o $@

italic-3-5-3.pdf:	$(PROG) italic-3-5-3
	$(PROG) @italic-3-5-3 --pagesize A4 --nib-width 1.1 -o $@

italic-3-5-3-l.pdf:	$(PROG) italic-3-5-3
	$(PROG) @italic-3-5-3 --pagesize A4 --nib-width 1.1 --landscape -o $@
