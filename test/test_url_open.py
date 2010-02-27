#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 2005-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 2005-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


import os, warnings, datetime

import py.test

from ll import url


def setup_module(module):
	module.context = url.Context()


def teardown_module(module):
	del module.context


def test_rename():
	def check(u):
		with context:
			u = url.URL(u)
			u2 = u/"foo"
			r = u2.open("wb")
			try:
				r.write("testing...")
				r.close()
				assert u2.exists()
			finally:
				u2.remove()
			assert not u2.exists()

	yield check, __file__.rstrip("c")
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/"


def test_link():
	def check(u):
		with context:
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
	def check(u):
		with context:
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
	def check(u):
		with context:
			u = url.URL(u)
			r = u.open("wb")
			try:
				try:
					r.write("testing ...")
				finally:
					r.close()
				u.chmod(0444)
				assert u.stat().st_mode & 0777 == 0444
			finally:
				u.remove()

	yield check, "~/foo"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/foo"


def test_chown():
	def check(u1, u2, owner, group):
		with context:
			u1 = url.URL(u1)
			u2 = url.URL(u2)
			r = u1.open("wb")
			try:
				try:
					r.write("foo")
				finally:
					r.close()
				try:
					# Might have been left over from previous run
					u2.remove()
				except Exception:
					pass
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
	def check(u):
		with context:
			u = url.URL(u)
			assert len(u.open().read()) == u.open().size() == u.size() == 601

	yield check, "~/checkouts/LivingLogic.Python.WWW/site/images/favicon.gif"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.WWW/site/images/favicon.gif"
	yield check, "http://www.livinglogic.de/Python/images/favicon.gif"


def test_imagesize():
	def check(u):
		with context:
			u = url.URL(u)
			assert u.imagesize() == (16, 16)

	yield check, "~/checkouts/LivingLogic.Python.WWW/site/images/favicon.gif"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.WWW/site/images/favicon.gif"
	yield check, "http://www.livinglogic.de/Python/images/favicon.gif"


def test_mimetype():
	def check(u, mt):
		with context:
			u = url.URL(u)
			assert u.mimetype() == u.open().mimetype() == mt

	yield check, __file__.rstrip("c"), "text/x-python"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py", "text/x-python"
	yield check, "http://www.livinglogic.de/Python/xist/", "text/html"


def test_readline():
	def check(u, firstline):
		with context:
			u = url.URL(u)
			r = u.open()
			canseektell = hasattr(r, "tell") and hasattr(r, "seek")
			assert r.readline() == firstline
			if canseektell:
				assert r.tell() == len(firstline)
				r.seek(0)
				assert r.readline() == firstline
				r.seek(0)
			else:
				r = u.open() # reopen
			assert r.read(len(firstline)) == firstline
			if canseektell:
				r.seek(0)
			else:
				r = u.open() # reopen
			assert r.read().startswith(firstline)

	yield check, __file__.rstrip("c"), "#!/usr/bin/env python\n"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py", "#! /usr/bin/env python\n"
	yield check, "http://www.livinglogic.de/Python/", '<?xml version="1.0" encoding="utf-8"?>\n'


def test_iter():
	def check(u, firstline):
		with context:
			u = url.URL(u)
			r = u.open()
			assert r.next() == firstline
			list(r)

	yield check, __file__.rstrip("c"), "#!/usr/bin/env python\n"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/setup.py", "#! /usr/bin/env python\n"
	yield check, "http://www.livinglogic.de/Python/", '<?xml version="1.0" encoding="utf-8"?>\n'


def test_seek_tell():
	def check(u):
		with context:
			u = url.URL(u)
			r = u.open()
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
			assert r.read() == ""

	yield check, "~/checkouts/LivingLogic.Python.WWW/site/images/favicon.gif"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.WWW/site/images/favicon.gif"


def test_truncate():
	def check(u):
		with context:
			u = url.URL(u)/"foo"
			try:
				r = u.open("wb")
				r.write("testing...")
				r.seek(-3, os.SEEK_CUR)
				r.truncate()
				r.close()
				assert u.open().read() == "testing"
			finally:
				u.remove()

	yield check, __file__
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/"


def test_owner():
	def check(u, owner):
		with context:
			u = url.URL(u)
			assert u.owner() == owner
			assert u.stat().st_uid == u.uid()

	yield check, __file__, "walter"
	yield check, "/", "root"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", "livpython"


def test_stat():
	def check(u):
		with context:
			u = url.URL(u)
			stat = u.stat()
			assert stat.st_size > 1000
			assert stat.st_mode & 0600 == 0600

	yield check, url.File(__file__)/"../README.rst"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst"


def test_group():
	def check(u, *groups):
		with context:
			u = url.URL(u)
			assert u.group() in groups
			assert u.stat().st_gid == u.gid()

	yield check, __file__, "users", "staff"
	yield check, "/", "root", "admin"
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", "livpython"


def test_cdate():
	def check(u, *args):
		with context:
			assert url.URL(u).cdate() >= datetime.datetime(*args)

	yield check, __file__.rstrip("c"), 2006, 10, 24
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29


def test_mdate():
	def check(u, *args):
		with context:
			u = url.URL(u)
			assert u.mdate() == u.open().mdate() >= datetime.datetime(*args)

	yield check, __file__.rstrip("c"), 2006, 10, 24
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29
	yield check, "http://www.livinglogic.de/Python/xist", 2006, 10, 3


def test_adate():
	def check(u, *args):
		with context:
			assert url.URL(u).adate() >= datetime.datetime(*args)

	yield check, __file__.rstrip("c"), 2006, 10, 24
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", 2006, 6, 29


def test_exists():
	def check(u, exists):
		with context:
			u = url.URL(u)
			assert u.exists() == exists

	yield check, __file__, True
	yield check, __file__ + "no", False
	yield check, "/", True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/DONTREADME.rst", False


def test_isfile():
	def check(u, isfile):
		with context:
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
	def check(u, isdir):
		with context:
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
	def check(u, islink):
		with context:
			u = url.URL(u)
			assert u.islink() == islink

	yield check, __file__, False
	yield check, "/", False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", False


def test_ismount():
	def check(u, ismount):
		with context:
			u = url.URL(u)
			assert u.ismount() == ismount

	yield check, __file__, False
	yield check, "/", True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", False
	yield check, "ssh://root@www.livinglogic.de/~livpython", False
	yield check, "ssh://root@www.livinglogic.de/", True


def test_access():
	def check(u, mode, result):
		with context:
			u = url.URL(u)
			assert u.access(mode) == result

	yield check, __file__, os.F_OK, True
	yield check, __file__ + "no", os.F_OK, False
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", os.F_OK, True
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/DONTREADME.rst", os.F_OK, False


def test_resheaders():
	def check(u, headers):
		with context:
			u = url.URL(u)
			realheaders = u.resheaders()
			for (k, v) in headers.iteritems():
				assert realheaders[k] == v

	yield check, url.File(__file__)/"../README.rst", {"Content-type": "application/octet-stream"}
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/README.rst", {"Content-Type": "application/octet-stream"}
	yield check, "http://www.livinglogic.de/Python/xist/", {"Content-type": "text/html", "Connection": "close", "Server": "Apache"}


def test_resdata():
	def check(u, firstline):
		with context:
			u = url.URL(u)
			realdata = u.open("rb").resdata()
			assert realdata.splitlines(True)[0] == firstline

	yield check, "http://www.livinglogic.de/Python/", '<?xml version="1.0" encoding="utf-8"?>\n'


def test_mkdir_rmdir():
	def check(u):
		with context:
			u = url.URL(u)/"foo/"
			u.mkdir(0755)
			try:
				assert u.isdir()
				assert u.stat().st_mode & 0777 == 0755
			finally:
				u.rmdir()

	yield check, __file__
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/"


def test_makedirs():
	def check(u):
		with context:
			u = url.URL(u)/"foo/bar/"
			u.makedirs(0755)
			try:
				assert u.isdir()
				assert u.stat().st_mode & 0777 == 0755
			finally:
				u.rmdir()
				(u/"../").rmdir()

	yield check, __file__
	yield check, "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/"


def test_dir():
	def check(u, pu, isfile):
		with context:
			u = url.URL(u)
			pu = url.URL(pu)
			assert u in pu.listdir()
			if isfile:
				assert u in pu.files()
				assert u not in pu.dirs()
			else:
				assert u not in pu.files()
				assert u in pu.dirs()

	yield check, os.path.basename(__file__), os.path.dirname(__file__), True
	yield check, "lib/", "/usr/", False
	yield check, "README.rst", "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/", True
	yield check, "LivingLogic/", "ssh://livpython@www.livinglogic.de/~/", False


def test_walk():
	def check(u, pu, isfile):
		with context:
			u = url.URL(u)
			pu = url.URL(pu)
			assert any(u==wu for wu in pu.walk())
			if isfile:
				assert any(u==wu for wu in pu.walkfiles())
				assert all(u!=wu for wu in pu.walkdirs())
			else:
				assert all(u!=wu for wu in pu.walkfiles())
				assert any(u==wu for wu in pu.walkdirs())

	yield check, os.path.basename(__file__), os.path.dirname(__file__), True
	yield check, "src/ll/xist/", url.Dir("~/checkouts/LivingLogic.Python.xist/"), False
	yield check, "ll/xist/ns/html.py", "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/src/", True
	yield check, "ll/xist/ns/", "ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/src/", False


def test_ssh_config():
	ssh_config = "/private/etc/ssh_config"
	if not os.path.exists(ssh_config):
		ssh_config = "/etc/ssh_config"
	with context:
		assert url.URL("ssh://livpython@www.livinglogic.de/~/checkouts/LivingLogic.Python.xist/").isdir(ssh_config=ssh_config) is True
