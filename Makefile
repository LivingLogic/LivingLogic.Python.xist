# $Header$

# List of pseudo targets
.PHONY: all clean dist windist

# Output directory
OUTPUTDIR=$(HOME)/pythonroot

# Install directory for globally callable scripts
SCRIPTDIR=$(HOME)/pythonscripts

all:
	python$(PYVERSION) setup.py install --install-lib $(OUTPUTDIR) --install-scripts $(SCRIPTDIR)

test: all
	python$(PYVERION) test/test.py -v

install:
	python$(PYVERSION) setup.py install

clean:
	python$(PYVERSION) setup.py clean

dist: test
	python$(PYVERSION) `which doc2txt.py` --title History NEWS.xml NEWS
	python$(PYVERSION) `which doc2txt.py` --title "Requirements and installation" INSTALL.xml INSTALL
	python$(PYVERSION) `which doc2txt.py` --title "Documentation" HOWTO.xml HOWTO
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar
	python$(PYVERSION) setup.py bdist --formats=rpm
	rm NEWS INSTALL HOWTO

windist:
	python$(PYVERSION) C:\\\\Programme\\\\Python22\\\\Scripts\\\\doc2txt.py --title History NEWS.xml NEWS
	python$(PYVERSION) C:\\\\Programme\\\\Python22\\\\Scripts\\\\doc2txt.py --title "Requirements and installation" INSTALL.xml INSTALL
	python$(PYVERSION) C:\\\\Programme\\\\Python22\\\\Scripts\\\\doc2txt.py --title "Documentation" HOWTO.xml HOWTO
	python$(PYVERSION) setup.py sdist --formats=zip
	python$(PYVERSION) setup.py bdist --formats=wininst
	rm NEWS INSTALL HOWTO
