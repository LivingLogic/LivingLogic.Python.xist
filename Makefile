# $Header$

# List of pseudo targets
.PHONY: all test install clean dist windist

all:
	python$(PYVERSION) setup.py install

test: all
	py.test

clean:
	python$(PYVERSION) setup.py clean

dist: test
	python$(PYVERSION) `which doc2txt.py` --title History NEWS.xml NEWS
	python$(PYVERSION) `which doc2txt.py` --title "Requirements and installation" INSTALL.xml INSTALL
	python$(PYVERSION) `which doc2txt.py` --title "Howto" HOWTO.xml HOWTO
	python$(PYVERSION) `which doc2txt.py` --title "Examples" EXAMPLES.xml EXAMPLES
	python$(PYVERSION) `which doc2txt.py` --title "Migration and modernization guide" MIGRATION.xml MIGRATION
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar
	python$(PYVERSION) setup.py bdist --formats=rpm
	rm NEWS INSTALL HOWTO EXAMPLES MIGRATION

windist:
	python$(PYVERSION) C:\\\\Programme\\\\Python24\\\\Scripts\\\\doc2txt.py --title History NEWS.xml NEWS
	python$(PYVERSION) C:\\\\Programme\\\\Python24\\\\Scripts\\\\doc2txt.py --title "Requirements and installation" INSTALL.xml INSTALL
	python$(PYVERSION) C:\\\\Programme\\\\Python24\\\\Scripts\\\\doc2txt.py --title "Howto" HOWTO.xml HOWTO
	python$(PYVERSION) C:\\\\Programme\\\\Python24\\\\Scripts\\\\doc2txt.py --title "Examples" EXAMPLES.xml EXAMPLES
	python$(PYVERSION) C:\\\\Programme\\\\Python24\\\\Scripts\\\\doc2txt.py --title "Migration and modernization guide" MIGRATION.xml MIGRATION
	python$(PYVERSION) setup.py sdist --formats=zip
	python$(PYVERSION) setup.py bdist --formats=wininst
	rm NEWS INSTALL HOWTO EXAMPLES MIGRATION
