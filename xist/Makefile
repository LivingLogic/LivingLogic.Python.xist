# $Header$

# List of pseudo targets
.PHONY: all clean

# Output directory
OUTPUTDIR=$(HOME)/pythonroot/xist

# collect all source files in SRC
SRC := $(patsubst ./%,%,$(shell find . -print))

# list of all files that just have to be copied
SRC_PY  := $(sort $(filter %.py,$(SRC)))
SRC_CP  := $(SRC_PY)

DEP_CP  := $(patsubst %,$(OUTPUTDIR)/%,$(SRC_CP))
DEP_PYC := $(patsubst %.py,$(OUTPUTDIR)/%.pyc,$(SRC_PY))

SRC := $(SRC_CP)

DEP := $(DEP_CP)

all: $(OUTPUTDIR) $(DEP) $(OUTPUTDIR)/helpers.so

$(OUTPUTDIR):
	mkdir $(OUTPUTDIR)

clean:
	rm $(DEP) $(DEP_PYC) $(OUTPUTDIR)/helpers.so helpers.o

$(DEP_CP): $(OUTPUTDIR)/% : %
	cp --parents $< $(OUTPUTDIR)/

$(OUTPUTDIR)/helpers.so: helpers.c
	gcc -c -I/usr/local/include/python2.0 -g -O2 -fpic helpers.c -o helpers.o
	gcc -shared helpers.o -o $(OUTPUTDIR)/helpers.so

