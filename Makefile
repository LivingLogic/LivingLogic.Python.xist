# $Header$

# List of pseudo targets
.PHONY: all clean dist windist

# Output directory
OUTPUTDIR=$(HOME)/pythonroot

# Install directory for globally callable scripts
SCRIPTDIR=$(HOME)/pythonscripts

all:
	python$(VERSION) setup.py install --install-lib $(OUTPUTDIR) --install-scripts $(SCRIPTDIR)

install:
	python$(VERSION) setup.py install

clean:
	python$(VERSION) setup.py clean

dist:
	doc2txt.py --title History --import xist.ns.specials --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials NEWS.xml NEWS
	doc2txt.py --title "Requirements and installation" --import xist.ns.specials --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials INSTALL.xml INSTALL
	doc2txt.py --title "Documentation" --import xist.ns.specials --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials HOWTO.xml HOWTO
	python$(VERSION) setup.py sdist --formats=bztar,gztar
	python$(VERSION) setup.py bdist --formats=rpm
	#rm NEWS INSTALL HOWTO

windist:
	python$(VERSION) C:\\\\Programme\\\\Python22\\\\Scripts\\\\doc2txt.py --title History --import xist.ns.specials --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials NEWS.xml NEWS
	python$(VERSION) C:\\\\Programme\\\\Python22\\\\Scripts\\\\doc2txt.py --title "Requirements and installation" --import xist.ns.specials --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials INSTALL.xml INSTALL
	python$(VERSION) C:\\\\Programme\\\\Python22\\\\Scripts\\\\doc2txt.py --title "Documentation" --import xist.ns.specials --import xist.ns.abbr --import xist.ns.doc --import xist.ns.specials HOWTO.xml HOWTO
	python$(VERSION) setup.py sdist --formats=zip
	python$(VERSION) setup.py bdist --formats=wininst
	rm NEWS INSTALL HOWTO
