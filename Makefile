# $Header$

# List of pseudo targets
.PHONY: all clean dist

# Output directory
OUTPUTDIR=$(HOME)/pythonroot

# Install directory for globally callable scripts
SCRIPTDIR=$(HOME)/pythonscripts

# collect all source files in SRC
SRC := $(patsubst ./%,%,$(shell find . -print))

# list of all files that just have to be copied
SRC_PY      := $(sort $(filter _xist/%.py,$(SRC)))
SRC_SCRIPTS := $(sort $(filter tools/%.py,$(SRC)))
SRC_CP      := $(SRC_PY)

DEP_CP      := $(patsubst _xist/%,$(OUTPUTDIR)/xist/%,$(SRC_CP))
DEP_SCRIPTS := $(patsubst tools/%,$(SCRIPTDIR)/%,$(SRC_SCRIPTS))
DEP_PYC     := $(patsubst _xist/%.py,$(OUTPUTDIR)/xist/%.pyc,$(SRC_PY))

SRC := $(SRC_CP) $(SRC_SCRIPTS)

DEP := $(DEP_CP) $(DEP_SCRIPTS)

all: $(OUTPUTDIR)/xist $(OUTPUTDIR)/xist/ns $(SCRIPTDIR) $(DEP) $(OUTPUTDIR)/xist/helpers.so

dist:
	docbooklite2text.py --title History --import xist.ns.abbr --import xist.ns.docbooklite --import xist.ns.specials NEWS.xml NEWS
	python setup.py sdist --formats=bztar,gztar
	rm NEWS

$(OUTPUTDIR)/xist:
	mkdir -p $(OUTPUTDIR)/xist

$(OUTPUTDIR)/xist/ns:
	mkdir -p $(OUTPUTDIR)/xist/ns

$(SCRIPTDIR):
	mkdir -p $(SCRIPTDIR)

clean:
	rm $(DEP) $(DEP_PYC) $(OUTPUTDIR)/xist/helpers.so _xist/helpers.o

$(DEP_CP): $(OUTPUTDIR)/xist/% : _xist/%
	cp $< $(patsubst _xist/%, $(OUTPUTDIR)/xist/%, $<)

$(DEP_SCRIPTS): $(SCRIPTDIR)/% : tools/%
	cp $< $(patsubst tools/%, $(SCRIPTDIR)/%, $<)

$(OUTPUTDIR)/xist/helpers.so: _xist/helpers.c
	gcc -c -I/usr/local/include/python2.1 -g -O6 -fpic _xist/helpers.c -o _xist/helpers.o
	gcc -shared _xist/helpers.o -o $(OUTPUTDIR)/xist/helpers.so

