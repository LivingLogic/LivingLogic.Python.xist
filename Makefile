.PHONY: develop install test dist register upload windist livinglogic


install:
	python$(PYVERSION) setup.py install


develop:
	python$(PYVERSION) setup.py develop

parser:
	java org.antlr.Tool src/ll/UL4.g
	python -c 'import sys; d = open("src/ll/UL4Lexer.py", "r").read(); d=d.replace(chr(117)+chr(34), chr(34)); open("src/ll/UL4Lexer.py", "w").write(d)'

test: install
	python$(PYVERSION) -mpytest


dist:
	rm -rf dist/*
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar,zip bdist_wheel
	LL_URL_SSH_PYTHON=python3.2 python$(PYVERSION) -mll.scripts.ucp -vyes -uftp -gftp dist/*.tar.gz dist/*.tar.bz2 dist/*.zip  dist/*.whl ssh://root@isar.livinglogic.de/~ftp/pub/livinglogic/xist/


register:
	python$(PYVERSION) setup.py register


upload:
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar,zip bdist_wheel upload


livinglogic:
	rm -rf dist/*
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar,zip
	python$(PYVERSION) setup.py bdist_wheel
	python$(PYVERSION) -mll.scripts.ucp -vyes dist/*.tar.gz dist/*.tar.bz2 dist/*.zip dist/*.whl ssh://intranet@intranet.livinglogic.de/~/documentroot/intranet.livinglogic.de/python-downloads/


windist:
	python$(PYVERSION) setup.py bdist --formats=wininst
	python -mll.scripts.ucp -vyes -cno -uftp -gftp dist/*.exe ssh://root@isar.livinglogic.de/~ftp/pub/livinglogic/xist/


winupload:
	python$(PYVERSION) setup.py bdist --formats=wininst upload


winlivinglogic:
	python$(PYVERSION) setup.py bdist --formats=wininst
	python$(PYVERSION) -mll.scripts.ucp -vyes -cno -uintranet -gintranet dist/*.exe ssh://intranet@intranet.livinglogic.de/~/documentroot/intranet.livinglogic.de/python-downloads/
