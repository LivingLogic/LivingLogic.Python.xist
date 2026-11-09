.PHONY: install develop parser test dist upload build windist winupload livinglogic


install:
	python setup.py install


develop:
	python setup.py develop


parser:
	java org.antlr.Tool src/ll/UL4.g
	python -c 'import sys; d = open("src/ll/UL4Lexer.py", "r").read(); d=d.replace(chr(117)+chr(34), chr(34)); open("src/ll/UL4Lexer.py", "w").write(d)'


test: install
	python -mpytest


build:
	rm -rf dist/* src/*.egg-info
	_PYTHON_HOST_PLATFORM=macosx-11.0-arm64 MACOSX_DEPLOYMENT_TARGET=11.0 python -m build --no-isolation

dist: build
	LL_URL_SSH_PYTHON=python3.2 python -mll.scripts.ucp -vyes -ulivpython -glivpython dist/*.tar.gz dist/*.whl ssh://livpython@python-downloads.livinglogic.de/~/public_downloads/xist/


upload: build
	twine upload dist/*


livinglogic:
	rm -rf dist/*
	python -m build
	LL_URL_SSH_PYTHON=python3 python -mll.scripts.ucp -vyes dist/*.tar.gz dist/*.whl ssh://intranet@intranet.livinglogic.de/~/documentroot/intranet.livinglogic.de/python-downloads/


windist:
	python setup.py bdist --formats=wininst
	LL_URL_SSH_PYTHON=python3 python -mll.scripts.ucp -vyes -cno -ulivpython -glivpython dist/*.exe ssh://livpython@python-downloads.livinglogic.de/~/public_downloads/xist/


winupload:
	python setup.py bdist --formats=wininst upload


winlivinglogic:
	python setup.py bdist --formats=wininst
	LL_URL_SSH_PYTHON=python3 python -mll.scripts.ucp -vyes -cno -uintranet -gintranet dist/*.exe ssh://intranet@intranet.livinglogic.de/~/documentroot/intranet.livinglogic.de/python-downloads/
