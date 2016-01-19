#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2005-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2005-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import io, os, datetime

from ll import url

import pytest


def test_remove():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)
			u2 = u/"foo"
			r = u2.open("wb")
			try:
				r.write(b"testing...")
				r.close()
				assert u2.exists()
			finally:
				u2.remove()
			assert not u2.exists()

	yield check, __file__.rstrip("c")
	yield check, url.URL(__file__.rstrip("c"))
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/"


def test_link():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)
			u2 = u/"foo"
			try:
				u.link(u2)
				assert u2.exists()
				assert u2.isfile()
				assert not u2.islink() # A hardlink is indistinguisable from the real thing
			finally:
				u2.remove()
			assert not u2.exists()

	yield check, __file__.rstrip("c")
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py"


def test_symlink():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)
			u2 = u/"foo"
			try:
				u.symlink(u2)
				assert u2.exists()
				assert u2.islink()
			finally:
				u2.remove()
			assert not u2.exists()

	yield check, __file__.rstrip("c")
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py"


def test_chmod():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)
			r = u.open("wb")
			try:
				try:
					r.write(b"testing ...")
				finally:
					r.close()
				u.chmod(0o444)
				assert u.stat().st_mode & 0o777 == 0o444
			finally:
				u.remove()

	yield check, "~/foo"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/foo"


def test_chown():
	@pytest.mark.net
	def check(u1, u2, owner, group):
		with url.Context():
			u1 = url.URL(u1)
			u2 = url.URL(u2)
			r = u1.open("wb")
			try:
				try:
					r.write(b"foo")
				finally:
					r.close()
				# Might have been left over from previous run
				if u2.exists():
					u2.remove()
				try:
					u1.symlink(u2)
					u2.lchown(owner, group)
					assert u1.owner() == owner
					assert u1.group() == group
					assert u2.owner() == owner
					assert u2.group() == group

					u2.chown(owner, group)
					assert u1.owner() == owner
					assert u1.group() == group
					assert u2.owner() == owner
					assert u2.group() == group
				finally:
					u2.remove()
			finally:
				u1.remove()

	yield check, "ssh://livpython@www.livinglogic.de/~/foo", "ssh://livpython@www.livinglogic.de/~/bar", "livpython", "livpython"


def test_size():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)
			assert len(u.open("rb").read()) == u.open("rb").size() == u.size() == 601

	yield check, "~/checkouts/LivingLogic.Python.WWW/site/static/favicon.gif"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.WWW/site/static/favicon.gif"
	yield check, "http://www.livinglogic.de/Python/static/favicon.gif"


def test_imagesize():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)
			assert u.imagesize() == (16, 16)

	yield check, "~/checkouts/LivingLogic.Python.WWW/site/static/favicon.gif"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.WWW/site/static/favicon.gif"
	yield check, "http://www.livinglogic.de/Python/static/favicon.gif"


def test_mimetype():
	@pytest.mark.net
	def check(u, mt):
		with url.Context():
			u = url.URL(u)
			assert u.mimetype() == u.open().mimetype() == mt

	yield check, __file__.rstrip("c"), "text/x-python"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py", "text/x-python"
	yield check, "http://www.livinglogic.de/Python/xist/", "text/html"


def test_readline():
	@pytest.mark.net
	def check(u, firstline):
		with url.Context():
			u = url.URL(u)
			r = u.open("rb")
			canseektell = hasattr(r, "tell") and hasattr(r, "seek")
			if canseektell:
				try:
					r.tell()
				except io.UnsupportedOperation:
					canseektell = False
			assert r.readline() == firstline
			if canseektell:
				assert r.tell() == len(firstline)
				r.seek(0)
				assert r.readline() == firstline
				r.seek(0)
			else:
				r = u.open("rb") # reopen
			assert r.read(len(firstline)) == firstline
			if canseektell:
				r.seek(0)
			else:
				r = u.open("rb") # reopen
			assert r.read().startswith(firstline)

	yield check, __file__.rstrip("c"), b"#!/usr/bin/env python\n"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py", b"#! /usr/bin/env python\n"
	yield check, "http://www.livinglogic.de/Python/", b'<?xml version="1.0" encoding="utf-8"?>\n'


def test_iter():
	@pytest.mark.net
	def check(u, firstline):
		with url.Context():
			u = url.URL(u)
			r = u.open("rb")
			assert next(iter(r)) == firstline
			list(r)

	yield check, __file__.rstrip("c"), b"#!/usr/bin/env python\n"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py", b"#! /usr/bin/env python\n"
	yield check, "http://www.livinglogic.de/Python/", b'<?xml version="1.0" encoding="utf-8"?>\n'


def test_autocreate_dir():
	@pytest.mark.net
	def check(u):
		with url.Context():
			try:
				u = url.URL(u)
				with u.openwrite() as f:
					f.write(b"Hurz!")
			finally:
				u.remove()
				u.withoutfile().rmdir()

	yield check, "gurk/hurz.txt"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/gurk/hurz.txt"


def test_seek_tell():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)
			r = u.open("rb")
			r.read()
			assert r.tell() == 601
			r.seek(0)
			assert r.tell() == 0
			r.seek(100, os.SEEK_SET)
			assert r.tell() == 100
			r.seek(0, os.SEEK_END)
			assert r.tell() == 601
			r.seek(-101, os.SEEK_END)
			assert r.tell() == 500
			r.seek(101, os.SEEK_CUR)
			assert r.tell() == 601
			assert r.read() == b""

	yield check, "~/checkouts/LivingLogic.Python.WWW/site/static/favicon.gif"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.WWW/site/static/favicon.gif"


def test_truncate():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)/"foo"
			try:
				r = u.open("wb")
				r.write(b"testing...")
				r.seek(-3, os.SEEK_CUR)
				r.truncate()
				r.close()
				assert u.open("rb").read() == b"testing"
			finally:
				u.remove()

	yield check, __file__
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/"


def test_owner():
	@pytest.mark.net
	def check(u, owner):
		with url.Context():
			u = url.URL(u)
			assert u.owner() == owner
			assert u.stat().st_uid == u.uid()

	yield check, __file__, "walter"
	yield check, "/", "root"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", "livpython"


def test_stat():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)
			stat = u.stat()
			assert stat.st_size > 1000
			assert stat.st_mode & 0o600 == 0o600

	yield check, url.File(__file__)/"../README.rst"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst"


def test_group():
	@pytest.mark.net
	def check(u, *groups):
		with url.Context():
			u = url.URL(u)
			assert u.group() in groups
			assert u.stat().st_gid == u.gid()

	yield check, __file__, "users", "staff", "walter"
	yield check, "/", "root", "admin", "wheel"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", "livpython"


def test_cdate():
	@pytest.mark.net
	def check(u, *args):
		with url.Context():
			assert url.URL(u).cdate() >= datetime.datetime(*args)

	yield check, __file__.rstrip("c"), 2006, 10, 24
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29


def test_mdate():
	@pytest.mark.net
	def check(u, *args):
		with url.Context():
			u = url.URL(u)
			assert u.mdate() == u.open().mdate() >= datetime.datetime(*args)

	yield check, __file__.rstrip("c"), 2006, 10, 24
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29
	yield check, "http://www.livinglogic.de/Python/xist", 2006, 10, 3


def test_adate():
	@pytest.mark.net
	def check(u, *args):
		with url.Context():
			assert url.URL(u).adate() >= datetime.datetime(*args)

	yield check, __file__.rstrip("c"), 2006, 10, 24
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29


def test_exists():
	@pytest.mark.net
	def check(u, exists):
		with url.Context():
			u = url.URL(u)
			assert u.exists() == exists

	yield check, __file__, True
	yield check, __file__ + "no", False
	yield check, "/", True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/DONTREADME.rst", False


def test_isfile():
	@pytest.mark.net
	def check(u, isfile):
		with url.Context():
			u = url.URL(u)
			assert u.isfile() == isfile

	yield check, __file__, True
	yield check, __file__ + "no", False
	yield check, "/", False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", False
	yield check, "ssh://root@www.livinglogic.de/~livpython", False
	yield check, "ssh://root@www.livinglogic.de/", False


def test_isdir():
	@pytest.mark.net
	def check(u, isdir):
		with url.Context():
			u = url.URL(u)
			assert u.isdir() == isdir

	yield check, __file__, False
	yield check, __file__ + "no", False
	yield check, "/", True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", True
	yield check, "ssh://root@www.livinglogic.de/~livpython", True
	yield check, "ssh://root@www.livinglogic.de/", True


def test_islink():
	@pytest.mark.net
	def check(u, islink):
		with url.Context():
			u = url.URL(u)
			assert u.islink() == islink

	yield check, __file__, False
	yield check, "/", False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", False


def test_ismount():
	@pytest.mark.net
	def check(u, ismount):
		with url.Context():
			u = url.URL(u)
			assert u.ismount() == ismount

	yield check, __file__, False
	yield check, "/", True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", False
	yield check, "ssh://root@www.livinglogic.de/~livpython", False
	yield check, "ssh://root@www.livinglogic.de/", True


def test_access():
	@pytest.mark.net
	def check(u, mode, result):
		with url.Context():
			u = url.URL(u)
			assert u.access(mode) == result

	yield check, __file__, os.F_OK, True
	yield check, __file__ + "no", os.F_OK, False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", os.F_OK, True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/DONTREADME.rst", os.F_OK, False


def test_resheaders():
	@pytest.mark.net
	def check(u, headers):
		with url.Context():
			u = url.URL(u)
			realheaders = u.resheaders()
			for (k, v) in headers.items():
				assert realheaders[k] == v

	yield check, url.File(__file__)/"../README.rst", {"Content-type": "application/octet-stream"}
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", {"Content-Type": "application/octet-stream"}
	yield check, "http://www.livinglogic.de/Python/xist/", {"Content-type": "text/html", "Connection": "close", "Server": "Apache"}


def test_resdata():
	@pytest.mark.net
	def check(u, firstline):
		with url.Context():
			u = url.URL(u)
			realdata = u.open("rb").resdata()
			assert realdata.splitlines(True)[0] == firstline

	yield check, "http://www.livinglogic.de/Python/", b'<?xml version="1.0" encoding="utf-8"?>\n'


def test_mkdir_rmdir():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)/"foo/"
			u.mkdir(0o755)
			try:
				assert u.isdir()
				assert u.stat().st_mode & 0o777 == 0o755
			finally:
				u.rmdir()

	yield check, __file__
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/"


def test_makedirs():
	@pytest.mark.net
	def check(u):
		with url.Context():
			u = url.URL(u)/"foo/bar/"
			u.makedirs(0o755)
			try:
				assert u.isdir()
				assert u.stat().st_mode & 0o777 == 0o755
			finally:
				u.rmdir()
				(u/"../").rmdir()

	yield check, __file__
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/"


def test_dir():
	@pytest.mark.net
	def check(u, pu, isfile, include=None, exclude=None):
		with url.Context():
			u = url.URL(u)
			pu = url.URL(pu)
			assert u in pu.listdir(include=include, exclude=exclude)
			if isfile:
				assert u in pu.files(include=include, exclude=exclude)
				assert u not in pu.dirs(include=include, exclude=exclude)
			else:
				assert u not in pu.files(include=include, exclude=exclude)
				assert u in pu.dirs(include=include, exclude=exclude)

	yield check, os.path.basename(__file__), os.path.dirname(__file__), True
	yield check, "lib/", "/usr/", False
	yield check, "README.rst", "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", True
	yield check, "LivingLogic/", "ssh://livpython@www.livinglogic.de/~/", False
	yield check, "lib/", "/usr/", False, "lib"
	yield check, "lib/", "/usr/", False, None, "nolib"


def test_walk():
	@pytest.mark.net
	def check(u, pu, isfile, include=None, exclude=None):
		with url.Context():
			u = url.URL(u)
			pu = url.URL(pu)
			assert any(u==wu for wu in pu.walkall(include=include, exclude=exclude))
			if isfile:
				assert any(u==wu for wu in pu.walkfiles(include=include, exclude=exclude))
				assert all(u!=wu for wu in pu.walkdirs(include=include, exclude=exclude))
			else:
				assert all(u!=wu for wu in pu.walkfiles(include=include, exclude=exclude))
				assert any(u==wu for wu in pu.walkdirs(include=include, exclude=exclude))

	yield check, os.path.basename(__file__), os.path.dirname(__file__), True
	yield check, "src/ll/xist/", url.Dir("~/checkouts/LivingLogic.Python.xist/"), False
	yield check, "ll/xist/ns/html.py", "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/src/", True
	yield check, "ll/xist/ns/", "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/src/", False


@pytest.mark.net
def test_ssh_params():
	with url.Context():
		u = url.URL("ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/")
		assert u.isdir(python="/usr/local/bin/python3.2") is True
		assert u.isdir(nice=20) is True
