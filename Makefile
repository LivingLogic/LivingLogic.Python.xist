# $Header$

# List of pseudo targets
.PHONY: all clean dist windist

# Output directory
OUTPUTDIR=$(HOME)/pythonroot

# Install directory for globally callable scripts
SCRIPTDIR=$(HOME)/pythonscripts

all:
	python$(PYVERSION) setup.py install --install-lib $(OUTPUTDIR) --install-scripts $(SCRIPTDIR)

install:
	python$(PYVERSION) setup.py install

clean:
	python$(PYVERSION) setup.py clean

dist:
	python$(PYVERSION) `which doc2txt.py` --title History --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials NEWS.xml NEWS
	python$(PYVERSION) `which doc2txt.py` --title "Requirements and installation" --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials INSTALL.xml INSTALL
	python$(PYVERSION) `which doc2txt.py` --title "Documentation" --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials HOWTO.xml HOWTO
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar
	python$(PYVERSION) setup.py bdist --formats=rpm
	rm NEWS INSTALL HOWTO

windist:
	python$(PYVERSION) C:\\\\Programme\\\\Python22\\\\Scripts\\\\doc2txt.py --title History --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials NEWS.xml NEWS
	python$(PYVERSION) C:\\\\Programme\\\\Python22\\\\Scripts\\\\doc2txt.py --title "Requirements and installation" --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials INSTALL.xml INSTALL
	python$(PYVERSION) C:\\\\Programme\\\\Python22\\\\Scripts\\\\doc2txt.py --title "Documentation" --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials HOWTO.xml HOWTO
	python$(PYVERSION) setup.py sdist --formats=zip
	python$(PYVERSION) setup.py bdist --formats=wininst
	rm NEWS INSTALL HOWTO
