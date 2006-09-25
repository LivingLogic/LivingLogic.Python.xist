# $Header$


WINPYTHON := C:\\\\Programme\\\\Python24\\\\


.PHONY: develop install test text dist register upload wintext windist livinglogic


install:
	python$(PYVERSION) setup.py install


develop:
	python$(PYVERSION) setup.py develop


test: install
	py.test


text:
	python$(PYVERSION) `which doc2txt.py` --title History NEWS.xml NEWS
	python$(PYVERSION) `which doc2txt.py` --title "Requirements and installation" INSTALL.xml INSTALL
	python$(PYVERSION) `which doc2txt.py` --title "Howto" HOWTO.xml HOWTO
	python$(PYVERSION) `which doc2txt.py` --title "Examples" EXAMPLES.xml EXAMPLES
	python$(PYVERSION) `which doc2txt.py` --title "Migration and modernization guide" MIGRATION.xml MIGRATION


dist: test text
	rm -rf dist/*
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar
	python$(PYVERSION) setup.py sdist --formats=zip
	python$(PYVERSION) setup.py bdist --formats=egg
	cd dist && scp.py -v -uftp -gftp *.tar.gz *.tar.bz2 *.zip *.egg root@isar.livinglogic.de:~ftp/pub/livinglogic/xist/


register:
	python$(PYVERSION) setup.py register


upload: text
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar upload
	python$(PYVERSION) setup.py sdist --formats=zip upload
	python$(PYVERSION) setup.py bdist --formats=egg upload


livinglogic: text
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar
	python$(PYVERSION) setup.py sdist --formats=zip
	python$(PYVERSION) setup.py bdist --formats=egg
	scp dist/*.tar.gz dist/*.tar.bz2 dist/*.zip dist/*.egg intranet@intranet.livinglogic.de:~/documentroot/intranet.livinglogic.de/python-downloads/


wintext:
	python$(PYVERSION) $(WINPYTHON)\\\\Scripts\\\\doc2txt.py --title History NEWS.xml NEWS
	python$(PYVERSION) $(WINPYTHON)\\\\Scripts\\\\doc2txt.py --title "Requirements and installation" INSTALL.xml INSTALL
	python$(PYVERSION) $(WINPYTHON)\\\\Scripts\\\\doc2txt.py --title "Howto" HOWTO.xml HOWTO
	python$(PYVERSION) $(WINPYTHON)\\\\Scripts\\\\doc2txt.py --title "Examples" EXAMPLES.xml EXAMPLES
	python$(PYVERSION) $(WINPYTHON)\\\\Scripts\\\\doc2txt.py --title "Migration and modernization guide" MIGRATION.xml MIGRATION


windist: wintext
	python$(PYVERSION) setup.py bdist --formats=wininst
	python$(PYVERSION) setup.py bdist --formats=egg
	cd dist && python$(PYVERSION) -mscp -v -uftp -gftp *.exe *.egg root@isar.livinglogic.de:~ftp/pub/livinglogic/xist/


winupload: wintext
	python$(PYVERSION) setup.py bdist --formats=wininst upload
	python$(PYVERSION) setup.py bdist --formats=egg upload


winlivinglogic: wintext
	python$(PYVERSION) setup.py bdist --formats=wininst
	python$(PYVERSION) setup.py bdist --formats=egg
	cd dist && python$(PYVERSION) -mscp -v -uintranet -gintranet *.exe *.egg intranet@intranet.livinglogic.de:~/documentroot/intranet.livinglogic.de/python-downloads/
