# $Header$

# List of pseudo targets
.PHONY: all clean

# Output directory
OUTPUTDIR=/data/pythonroot/xsc/

# collect all source files in SRC
SRC := $(patsubst ./%,%,$(shell find . -print))

# list of all files that just have to be copied
SRC_PY  := $(sort $(filter %.py,$(SRC)))
SRC_CP  := $(SRC_PY)

DEP_CP  := $(patsubst %,$(OUTPUTDIR)%,$(SRC_CP))
DEP_PYC := $(patsubst %.py,$(OUTPUTDIR)%.pyc,$(SRC_PY))

SRC := $(SRC_CP)

DEP := $(DEP_CP)

all: $(DEP)

clean:
	rm $(DEP) $(DEP_PYC)

$(DEP_CP): $(OUTPUTDIR)% : %
	cp --parents $< $(OUTPUTDIR)
