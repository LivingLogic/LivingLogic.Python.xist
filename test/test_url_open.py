#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2005-2021 by LivingLogic AG, Bayreuth/Germany
## Copyright 2005-2021 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


import io, os, datetime

from ll import url

import pytest


@pytest.mark.net
def test_remove():
	def check(u):
		with url.Context():
			u = url.URL(u)
			u2 = u/"foo_remove"
			r = u2.open("wb")
			try:
				r.write(b"testing...")
				r.close()
				assert u2.exists()
			finally:
				u2.remove()
			assert not u2.exists()

	check(__file__.rstrip("c"))
	check(url.URL(__file__.rstrip("c")))
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/")


@pytest.mark.net
def test_link():
	def check(u):
		with url.Context():
			u = url.URL(u)
			u2 = u/"foo_link"
			try:
				u.link(u2)
				assert u2.exists()
				assert u2.isfile()
				assert not u2.islink() # A hardlink is indistinguisable from the real thing
			finally:
				u2.remove()
			assert not u2.exists()

	check(__file__.rstrip("c"))
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/setup.py")


@pytest.mark.net
def test_symlink():
	def check(u):
		with url.Context():
			u = url.URL(u)
			u2 = u/"foo_symlink"
			try:
				u.symlink(u2)
				assert u2.exists()
				assert u2.islink()
			finally:
				u2.remove()
			assert not u2.exists()

	check(__file__.rstrip("c"))
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/setup.py")


@pytest.mark.net
def test_chmod():
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

	check("~/foo_chmod")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/foo")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/foo")


@pytest.mark.net
def test_chown():
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

	check("ssh://livpython@python.livinglogic.de/~/foo_chown", "ssh://livpython@python.livinglogic.de/~/bar", "livpython", "livpython")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/foo_chown", "ssh-nocheck://livpython@python.livinglogic.de:22/~/bar", "livpython", "livpython")


@pytest.mark.net
def test_size():
	def check(u):
		with url.Context():
			u = url.URL(u)
			assert len(u.open("rb").read()) == u.open("rb").size() == u.size() == 1479

	check("~/checkouts/LivingLogic.Python.xist/docs/_static/favicon.png")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/docs/_static/favicon.png")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/docs/_static/favicon.png")
	check("http://python.livinglogic.de/_static/favicon.png")


@pytest.mark.net
def test_imagesize():
	def check(u):
		with url.Context():
			u = url.URL(u)
			assert u.imagesize() == (32, 32)

	check("~/checkouts/LivingLogic.Python.xist/docs/_static/favicon.png")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/docs/_static/favicon.png")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/docs/_static/favicon.png")
	check("http://python.livinglogic.de/_static/favicon.png")


@pytest.mark.net
def test_mimetype():
	def check(u, mt):
		with url.Context():
			u = url.URL(u)
			assert u.mimetype() == u.open().mimetype() == mt

	check(__file__.rstrip("c"), "text/x-python")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py", "text/x-python")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/setup.py", "text/x-python")
	check("http://python.livinglogic.de/", "text/html")


@pytest.mark.net
def test_readline():
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

	check(__file__.rstrip("c"), b"#!/usr/bin/env python\n")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py", b"#! /usr/bin/env python\n")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/setup.py", b"#! /usr/bin/env python\n")
	check("http://python.livinglogic.de/_static/css/overwrite.css", b'@import url("theme.css");\n')


@pytest.mark.net
def test_iter():
	def check(u, firstline):
		with url.Context():
			u = url.URL(u)
			r = u.open("rb")
			assert next(iter(r)) == firstline
			list(r)

	check(__file__.rstrip("c"), b"#!/usr/bin/env python\n")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py", b"#! /usr/bin/env python\n")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/setup.py", b"#! /usr/bin/env python\n")
	check("http://python.livinglogic.de/_static/css/overwrite.css", b'@import url("theme.css");\n')


@pytest.mark.net
def test_autocreate_dir():
	def check(u):
		with url.Context():
			try:
				u = url.URL(u)
				with u.openwrite() as f:
					f.write(b"Hurz!")
			finally:
				u.remove()
				u.withoutfile().rmdir()

	check("gurk/hurz.txt")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/gurk/hurz.txt")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/gurk/hurz.txt")


@pytest.mark.net
def test_seek_tell():
	def check(u):
		with url.Context():
			u = url.URL(u)
			r = u.open("rb")
			r.read()
			assert r.tell() == 1479
			r.seek(0)
			assert r.tell() == 0
			r.seek(100, os.SEEK_SET)
			assert r.tell() == 100
			r.seek(0, os.SEEK_END)
			assert r.tell() == 1479
			r.seek(-479, os.SEEK_END)
			assert r.tell() == 1000
			r.seek(479, os.SEEK_CUR)
			assert r.tell() == 1479
			assert r.read() == b""

	check("~/checkouts/LivingLogic.Python.xist/docs/_static/favicon.png")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/docs/_static/favicon.png")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/docs/_static/favicon.png")


@pytest.mark.net
def test_truncate():
	def check(u):
		with url.Context():
			u = url.URL(u)/"foo_truncate"
			try:
				r = u.open("wb")
				r.write(b"testing...")
				r.seek(-3, os.SEEK_CUR)
				r.truncate()
				r.close()
				assert u.open("rb").read() == b"testing"
			finally:
				u.remove()

	check(__file__)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/")


@pytest.mark.net
def test_owner():
	def check(u, owner):
		with url.Context():
			u = url.URL(u)
			assert u.owner() == owner
			assert u.stat().st_uid == u.uid()

	check(__file__, "walter")
	check("/", "root")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", "livpython")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", "livpython")


@pytest.mark.net
def test_stat():
	def check(u):
		with url.Context():
			u = url.URL(u)
			stat = u.stat()
			assert stat.st_size > 1000
			assert stat.st_mode & 0o600 == 0o600

	check(url.File(__file__)/"../README.rst")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst")


@pytest.mark.net
def test_group():
	def check(u, *groups):
		with url.Context():
			u = url.URL(u)
			assert u.group() in groups
			assert u.stat().st_gid == u.gid()

	check(__file__, "users", "staff", "walter")
	check("/", "root", "admin", "wheel")
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", "livpython")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", "livpython")


@pytest.mark.net
def test_cdate():
	def check(u, *args):
		with url.Context():
			assert url.URL(u).cdate() >= datetime.datetime(*args)

	check(__file__.rstrip("c"), 2006, 10, 24)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29)


@pytest.mark.net
def test_mdate():
	def check(u, *args):
		with url.Context():
			u = url.URL(u)
			assert u.mdate() == u.open().mdate() >= datetime.datetime(*args)

	check(__file__.rstrip("c"), 2006, 10, 24)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29)
	check("http://python.livinglogic.de/XIST.html", 2006, 10, 3)


@pytest.mark.net
def test_adate():
	def check(u, *args):
		with url.Context():
			assert url.URL(u).adate() >= datetime.datetime(*args)

	check(__file__.rstrip("c"), 2006, 10, 24)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29)


@pytest.mark.net
def test_exists():
	def check(u, exists):
		with url.Context():
			u = url.URL(u)
			assert u.exists() == exists

	check(__file__, True)
	check(__file__ + "no", False)
	check("/", True)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", True)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", True)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/DONTREADME.rst", False)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/DONTREADME.rst", False)


@pytest.mark.net
def test_isfile():
	def check(u, isfile):
		with url.Context():
			u = url.URL(u)
			assert u.isfile() == isfile

	check(__file__, True)
	check(__file__ + "no", False)
	check("/", False)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", True)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", True)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", False)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/", False)


@pytest.mark.net
def test_isdir():
	def check(u, isdir):
		with url.Context():
			u = url.URL(u)
			assert u.isdir() == isdir

	check(__file__, False)
	check(__file__ + "no", False)
	check("/", True)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", False)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", False)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", True)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/", True)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/", True)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/", True)


@pytest.mark.net
def test_islink():
	def check(u, islink):
		with url.Context():
			u = url.URL(u)
			assert u.islink() == islink

	check(__file__, False)
	check("/", False)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", False)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", False)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", False)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/", False)


@pytest.mark.net
def test_ismount():
	def check(u, ismount):
		with url.Context():
			u = url.URL(u)
			assert u.ismount() == ismount

	check(__file__, False)
	check("/", True)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", False)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", False)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", False)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/", False)
	check("ssh://livpython@python.livinglogic.de/~livpython", False)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~livpython", False)


@pytest.mark.net
def test_access():
	def check(u, mode, result):
		with url.Context():
			u = url.URL(u)
			assert u.access(mode) == result

	check(__file__, os.F_OK, True)
	check(__file__ + "no", os.F_OK, False)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", os.F_OK, True)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", os.F_OK, True)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/DONTREADME.rst", os.F_OK, False)
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/DONTREADME.rst", os.F_OK, False)


@pytest.mark.net
def test_resheaders():
	def check(u, headers):
		with url.Context():
			u = url.URL(u)
			realheaders = u.resheaders()
			for (k, v) in headers.items():
				assert realheaders[k] == v

	check(url.File(__file__)/"../README.rst", {"Content-type": "application/octet-stream"})
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", {"Content-Type": "application/octet-stream"})
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/README.rst", {"Content-Type": "application/octet-stream"})
	check("http://python.livinglogic.de/XIST.html", {"Content-type": "text/html", "Connection": "close", "Server": "nginx/1.10.3"})


@pytest.mark.net
def test_resdata():
	def check(u, firstline):
		with url.Context():
			u = url.URL(u)
			realdata = u.open("rb").resdata()
			assert realdata.splitlines(True)[0] == firstline

	check("http://python.livinglogic.de/_static/css/overwrite.css", b'@import url("theme.css");\n')


@pytest.mark.net
def test_mkdir_rmdir():
	def check(u):
		with url.Context():
			u = url.URL(u)/"foo_mkdir_rmdir/"
			u.mkdir(0o755)
			try:
				assert u.isdir()
				assert u.stat().st_mode & 0o777 == 0o755
			finally:
				u.rmdir()

	check(__file__)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/")


@pytest.mark.net
def test_makedirs():
	def check(u):
		with url.Context():
			u = url.URL(u)/"foo_makedirs/bar/"
			u.makedirs(0o755)
			try:
				assert u.isdir()
				assert u.stat().st_mode & 0o777 == 0o755
			finally:
				u.rmdir()
				(u/"../").rmdir()

	check(__file__)
	check("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/")
	check("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/")


@pytest.mark.net
def test_dir():
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

	check(os.path.basename(__file__), os.path.dirname(__file__), True)
	check("lib/", "/usr/", False)
	check("README.rst", "ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", True)
	check("README.rst", "ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/", True)
	check("LivingLogic/", "ssh://livpython@python.livinglogic.de/~/", False)
	check("LivingLogic/", "ssh-nocheck://livpython@python.livinglogic.de:22/~/", False)
	check("lib/", "/usr/", False, "lib")
	check("lib/", "/usr/", False, None, "nolib")


@pytest.mark.net
def test_walk():
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

	check(os.path.basename(__file__), os.path.dirname(__file__), True)
	check("src/ll/xist/", url.Dir("~/checkouts/LivingLogic.Python.xist/"), False)
	check("ll/xist/ns/html.py", "ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/src/", True)
	check("ll/xist/ns/html.py", "ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/src/", True)
	check("ll/xist/ns/", "ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/src/", False)
	check("ll/xist/ns/", "ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/src/", False)


@pytest.mark.net
def test_ssh_params():
	with url.Context():
		u1 = url.URL("ssh://livpython@python.livinglogic.de/~/checkouts/LivingLogic.Python.xist/")
		assert u1.isdir(python="/usr/local/bin/python3.2") is True
		assert u1.isdir(nice=20) is True
		assert u1.isdir(check=False) is True
		assert u1.isdir(check=True) is True

		u2 = url.URL("ssh-nocheck://livpython@python.livinglogic.de:22/~/checkouts/LivingLogic.Python.xist/")
		assert u2.isdir(python="/usr/local/bin/python3.2") is True
		assert u2.isdir(nice=20) is True
		assert u2.isdir(check=False) is True
		assert u2.isdir(check=True) is True
