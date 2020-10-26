.PHONY: install develop parser test build dist upload windist winupload livinglogic


install:
	python$(PYVERSION) setup.py install


develop:
	python$(PYVERSION) setup.py develop


parser:
	java org.antlr.v4.Tool src/ll/UL4Lexer.g4 src/ll/UL4Parser.g4 -Dlanguage=Python3 -visitor -no-listener


test: install
	python$(PYVERSION) -mpytest


build:
	rm -rf dist/*
	python$(PYVERSION) setup.py sdist --formats=gztar bdist_wheel

dist: build
	LL_URL_SSH_PYTHON=python3.2 python$(PYVERSION) -mll.scripts.ucp -vyes -ulivpython -glivpython dist/*.tar.gz dist/*.whl ssh://livpython@python.livinglogic.de/~/public_downloads/xist/


upload: build
	twine upload dist/*


livinglogic:
	rm -rf dist/*
	python$(PYVERSION) setup.py sdist --formats=bztar,gztar,zip
	python$(PYVERSION) setup.py bdist_wheel
	python$(PYVERSION) -mll.scripts.ucp -vyes dist/*.tar.gz dist/*.tar.bz2 dist/*.zip dist/*.whl ssh://intranet@intranet.livinglogic.de/~/documentroot/intranet.livinglogic.de/python-downloads/


windist:
	python$(PYVERSION) setup.py bdist --formats=wininst
	python -mll.scripts.ucp -vyes -cno -ulivpython -glivpython dist/*.exe ssh://livpython@python.livinglogic.de/~/public_downloads/xist/


winupload:
	python$(PYVERSION) setup.py bdist --formats=wininst upload


winlivinglogic:
	python$(PYVERSION) setup.py bdist --formats=wininst
	python$(PYVERSION) -mll.scripts.ucp -vyes -cno -uintranet -gintranet dist/*.exe ssh://intranet@intranet.livinglogic.de/~/documentroot/intranet.livinglogic.de/python-downloads/
