#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2005-2016 by LivingLogic AG, Bayreuth/Germany
## Copyright 2005-2016 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


from ll import url


def test_fileext():
	u = url.URL("/gurk/hurz")
	assert u.file == "hurz"
	assert u.ext is None
	u.file = "nöx.png"
	assert u.file == "nöx.png"
	assert u.ext == "png"
	assert str(u.path) == "/gurk/n%C3%B6x.png"
	u.ext = "gif"
	assert u.file == "nöx.gif"
	assert u.ext == "gif"

	u = url.URL("/gurk/hurz.")
	assert u.file == "hurz."
	assert u.ext == ""
	u.ext = "gif"
	assert u.file == "hurz.gif"
	assert u.ext == "gif"

	u = url.URL("/gurk/hurz.png")
	assert u.file == "hurz.png"
	assert u.ext == "png"

	u = url.URL("/gurk/hurz/")
	assert u.file == ""
	assert u.ext is None
	u.ext = "gif"
	assert u.file == ".gif"
	assert u.ext == "gif"

	assert url.URL(".gif").withoutext() == url.URL("./")


def test_join_list():
	assert ["", "gurk", "gurk/"]/url.URL("index.html") == [url.URL(s) for s in ["index.html", "index.html", "gurk/index.html"]]

	assert url.URL("gurk/")/["", "hinz", "kunz"] == [url.URL(s) for s in ["gurk/", "gurk/hinz", "gurk/kunz"]]


def test_withfile():
	def check(org, file, exp):
		org = url.URL(org)
		exp = url.URL(exp)
		res = org.withfile(file)
		assert exp == res

	yield check, "", "gurk", "gurk"
	yield check, "/", "gurk", "/gurk"
	yield check, "/hurz", "gurk", "/gurk"
	yield check, "/hurz.gif", "gurk.gif", "/gurk.gif"


def test_withoutfile():
	def check(org, exp):
		org = url.URL(org)
		exp = url.URL(exp)
		res = org.withoutfile()
		assert exp == res

	yield check, "", "./"
	yield check, "/", "/"
	yield check, "/hurz", "/"
	yield check, "hurz", "./"
	yield check, "/gurk/hurz/hinz/", "/gurk/hurz/hinz/"
	yield check, "/gurk/hurz/hinz/kunz", "/gurk/hurz/hinz/"


def test_withext():
	def check(org, ext, exp):
		org = url.URL(org)
		exp = url.URL(exp)
		res = org.withext(ext)
		assert exp == res

	yield check, "", "py", ".py"
	yield check, "/", "py", "/.py"
	yield check, "/hurz", "py", "/hurz.py"
	yield check, "/hurz.", "py", "/hurz.py"
	yield check, "/hurz.gif", "py", "/hurz.py"
	yield check, "/hurz.gif.png", "py", "/hurz.gif.py"
	yield check, "/hurz.gif.png", "pyc.py", "/hurz.gif.pyc.py"


def test_withoutext():
	def check(org, exp):
		org = url.URL(org)
		exp = url.URL(exp)
		res = org.withoutext()
		assert exp == res

	yield check, "", ""
	yield check, "/", "/"
	yield check, "/gurk.1/hurz", "/gurk.1/hurz"
	yield check, "/gurk.2/hurz.gif", "/gurk.2/hurz"
	yield check, "/gurk.3/hurz.gif.png", "/gurk.3/hurz.gif"
	yield check, "/gurk.4/hurz.", "/gurk.4/hurz"


def test_parse():
	base = "http://a/b/c/d;p?q#f"
	u = url.URL(base)
	assert u.scheme == "http"
	assert u.userinfo is None
	assert u.host == "a"
	assert u.port is None
	assert u.hostport == "a"
	assert u.server == "a"
	assert u.authority == "a"
	assert u.reg_name is None
	assert u.path == "/b/c/d;p"
	assert u.path.segments == ["b", "c", "d;p"]
	assert u.isabspath is True
	assert u.query == "q"
	assert u.query_parts is False
	assert u.frag == "f"
	assert u.opaque_part is None
	assert u.url == base

	base = "http://a/b/c/d;p?q=x#f"
	u = url.URL(base)
	assert u.query == "q=x"
	assert u.query_parts == {"q": ["x"]}


def test_join_rfc2396():
	base = "http://a/b/c/d;p?q"
	baseurl = url.URL(base)

	def check(rel, res):
		relurl = url.URL(rel)
		resurl = url.URL(res)
		assert baseurl/relurl == resurl, "{!r}/{!r} is {!r}, but should be {!r}".format(baseurl, relurl, baseurl/relurl, resurl)
		# This checks rdiv
		assert str(baseurl)/relurl == resurl, "{!r}/{!r} is {!r}, but should be {!r}".format(baseurl, relurl, str(baseurl)/relurl, resurl)

	# RFC2396 Section C.1: Normal Examples
	yield check, "g:h",           "g:h"
	yield check, "g",             "http://a/b/c/g"
	yield check, "./g",           "http://a/b/c/g"
	yield check, "g/",            "http://a/b/c/g/"
	yield check, "/g",            "http://a/g"
	yield check, "//g",           "http://g"
	yield check, "?y",            "http://a/b/c/?y"
	yield check, "g?y",           "http://a/b/c/g?y"
	yield check, "#s",            "http://a/b/c/d;p?q#s"
	yield check, "g#s",           "http://a/b/c/g#s"
	yield check, "g?y#s",         "http://a/b/c/g?y#s"
	yield check, ";x",            "http://a/b/c/;x"
	yield check, "g;x",           "http://a/b/c/g;x"
	yield check, "g;x?y#s",       "http://a/b/c/g;x?y#s"
	yield check, ".",             "http://a/b/c/"
	yield check, "./",            "http://a/b/c/"
	yield check, "..",            "http://a/b/"
	yield check, "../",           "http://a/b/"
	yield check, "../g",          "http://a/b/g"
	yield check, "../..",         "http://a/"
	yield check, "../../",        "http://a/"
	yield check, "../../g",       "http://a/g"

	# RFC2396 Section C.2: Abnormal Examples
	yield check, "",              "http://a/b/c/d;p?q"
	yield check, "../../../g",    "http://a/../g"
	yield check, "../../../../g", "http://a/../../g"
	yield check, "/./g",          "http://a/./g"
	yield check, "/../g",         "http://a/../g"
	yield check, "g.",            "http://a/b/c/g."
	yield check, ".g",            "http://a/b/c/.g"
	yield check, "g..",           "http://a/b/c/g.."
	yield check, "..g",           "http://a/b/c/..g"
	yield check, "./../g",        "http://a/b/g"
	yield check, "./g/.",         "http://a/b/c/g/"
	yield check, "g/./h",         "http://a/b/c/g/h"
	yield check, "g/../h",        "http://a/b/c/h"
	yield check, "g;x=1/./y",     "http://a/b/c/g;x=1/y"
	yield check, "g;x=1/../y",    "http://a/b/c/y"
	yield check, "g?y/./x",       "http://a/b/c/g?y/./x"
	yield check, "g?y/../x",      "http://a/b/c/g?y/../x"
	yield check, "g#s/./x",       "http://a/b/c/g#s/./x"
	yield check, "g#s/../x",      "http://a/b/c/g#s/../x"
	yield check, "http:g",        "http:g" # use the validating version here


def test_join():
	def check(base, rel, res):
		baseurl = url.URL(base)
		relurl = url.URL(rel)
		resurl = url.URL(res)
		assert baseurl/relurl == resurl, "{!r}/{!r} is {!r}, but should be {!r}".format(baseurl, relurl, baseurl/relurl, resurl)
		# This checks rdiv
		assert str(baseurl)/relurl == resurl, "{!r}/{!r} is {!r}, but should be {!r}".format(baseurl, relurl, str(baseurl)/relurl, resurl)

	yield check, "http://test.com/index.html", "impress.html", "http://test.com/impress.html"
	yield check, "http://test.com/index.html", "", "http://test.com/index.html"
	yield check, "/bb/cc/", "http:", "http:"
	yield check, "mailto:x@y.z", "index.html", "index.html"
	yield check, "mailto:x@y.z", "", "mailto:x@y.z"
	yield check, "javascript:return ':/:/:';", "index.html", "index.html"
	yield check, "javascript:document.write('http://foo@bar.com:81/foo;bar/bar;foo?x=y#frag');", "index.html", "index.html"
	yield check, "mailto:x@y", "", "mailto:x@y"
	yield check, "http://test.com/gurk/hurz.gif", "/index.html", "http://test.com/index.html"
	yield check, "http://test.com/gurk/hurz.gif", "../", "http://test.com/"
	yield check, "http://test.com/gurk/hurz.gif", "../gurk.gif?foo=bar#nix", "http://test.com/gurk.gif?foo=bar#nix"
	yield check, "http://test.com/gurk/hurz.gif", "../../gurk.gif?foo=bar#nix", "http://test.com/../gurk.gif?foo=bar#nix"
	yield check, "http://test.com/gurk/hurz.gif", "root:gurk.gif", "root:gurk.gif"
	yield check, "root:gurk.gif", "http://test.com/gurk/hurz.gif", "http://test.com/gurk/hurz.gif"
	yield check, "root:gurk/hurz/hinz.gif", "hinz/kunz.gif", "root:gurk/hurz/hinz/kunz.gif"
	yield check, "root:gurk/hurz/hinz.gif", "root:hinz/kunz.gif", "root:hinz/kunz.gif"
	yield check, "http://test.com", "gurk", "http://test.com/gurk"


def test_normalize():
	def check(u, u2):
		u = url.URL(u)
		u1 = u.clone()
		u1.path.normalize()
		u2 = url.URL(u2)
		assert u1 == u2, "{!r} normalized is {!r}, but should be {!r}".format(u, u1, u2)

	yield check, "", ""
	yield check, "./", ""
	yield check, "/./", "/"
	yield check, "xx", "xx"
	yield check, "xx/yy", "xx/yy"
	yield check, "xx/..", ""
	yield check, "xx/../.", ""
	yield check, "./xx/..", ""
	yield check, "./xx/../.", ""
	yield check, "xx/./..", ""
	yield check, "xx/yy/..", "xx/"
	yield check, "xx//yy/../..", ""
	yield check, "xx//yy/./..", "xx/"
	yield check, "xx//yy//../", "xx/"
	yield check, "xx/../..//", "../"
	yield check, "xx/.././..", ".." # ".." parts above the root loose their "directoryness", otherwise this would be "../"
	yield check, "xx/.", "xx/"
	yield check, "./xx", "xx"
	yield check, "/xx", "/xx"
	yield check, "/./xx", "/xx"
	yield check, "xx/../xx/../xx", "xx"


def test_str():
	s = "ftp://ftp.livinglogic.de/pub/livinglogic/xist/XIST-42.105.tar.bz2"
	u = url.URL(s)
	assert str(u) == s
	assert str(u) == s


def test_relative():
	def check(base, rel, res):
		baseurl = url.URL(base)
		relurl = url.URL(rel)
		resurl = url.URL(res)
		assert relurl.relative(baseurl) == resurl, "{!r}.relative({!r}) is {!r}, but should be {!r}".format(relurl, baseurl, relurl.relative(baseurl), resurl)

	yield check, "./", "./", "./"
	yield check, "cc.html", "./", "./"
	yield check, "./cc.html", "./", "./"
	yield check, "file:./cc.html", "file:./", "./"
	yield check, "root:./cc.html", "file:./", "file:./"
	yield check, "root:xist/Documentation.html", "http://server/", "http://server/"
	yield check, "root:cc.html", "root:", "./"
	yield check, "root:cc.html", "./", "./"
	yield check, "cc.html", "#mark", "#mark"
	yield check, "root:cc.html", "root:#mark", "./#mark"
	yield check, "root:cc.html", "#mark", "#mark"
	yield check, "root:cc.html", "root:cc.html#mark", "#mark"
	yield check, "root:cc.html", "root:dd.html#mark", "dd.html#mark"
	yield check, "root:aa/bb/cc.html", "root:", "../../"
	yield check, "", "", ""
	yield check, "http://server/aa/bb.html", "http://server/aa/cc.html", "cc.html"
	yield check, "/aa/bb.html", "/xx.html", "/xx.html" # we don't handle URLs without scheme


def test_query():
	u = url.URL("/search?id=13&id")
	assert u.query == "id=13&id"
	assert u.query_parts == 0

	u.query += "=17"
	assert u.query == "id=13&id=17"
	assert u.query_parts == {"id": ["13", "17"]}

	del u.query_parts["id"]
	u.query_parts["name"] = "gurk"
	assert u.query == "name=gurk"
	assert u.query_parts == {"name": "gurk"}

	u.query_parts["name"] = ["gürk"]
	assert u.query == "name=g%C3%BCrk"
	assert u.query_parts == {"name": ["gürk"]}

	u.query_parts["name"] = "gürk"
	assert u.query == "name=g%C3%BCrk"
	assert u.query_parts == {"name": "gürk"}


def test_eq():
	u1 = url.URL("HTTP://www.FOO.com/gurk")
	u2 = url.URL("http://www.foo.com:80/gurk")
	assert u1 == u2
	assert hash(u1) == hash(u2)

	u1 = url.URL("http://www.foo.com/gurk?id=13&id=17")
	u2 = url.URL("http://www.foo.com/gurk?id=17&id=13")
	assert u1 == u2
	assert hash(u1) == hash(u2)

	u1 = url.URL("http://www.foo.com/gurk?gurk=hurz&hinz=kunz")
	u2 = url.URL("http://www.foo.com/gurk?hinz=kunz&gurk=hurz")
	assert u1 == u2
	assert hash(u1) == hash(u2)


def test_withfrag():
	u1a = url.URL("x#y")
	u1b = url.URL("x#y")
	u2 = url.URL("x#z")
	assert u1a.withfrag("z") == u2
	assert u1a == u1b # make sure withfrag created a new URL


def test_without():
	u1a = url.URL("x#y")
	u1b = url.URL("x#y")
	u2 = url.URL("x")
	u3 = url.URL("x#")
	assert u1a.withoutfrag() == u2
	assert u1a.withoutfrag() != u3
	assert u1a == u1b # make sure withoutfrag created a new URL


def test_relpathauthority():
	u = url.URL("http://www.foo.com/bar/baz;baz")
	u2 = u.clone()
	u2.path = [ seg.upper() for seg in u2.path.segments ]
	assert not u2.path.isabs
	assert str(u2) == "http://www.foo.com/BAR/BAZ;BAZ"

	del u2.scheme
	del u2.authority
	assert str(u2) == "BAR/BAZ;BAZ"


def test_space_and_plus_in_name():
	assert url.URL("+").local() == "+"
	assert url.URL(" ").local() == " "
	assert url.URL("%20").local() == " "
	assert url.File("+").local() == "+"
	assert url.File(" ").local() == " "
	assert str(url.File(" ")) in ("file:%20", "file:+")


def test_schemerelurls():
	u1 = url.URL("http://www.example.org/about/index.html")
	u2 = url.URL("http://www.example.com/images/logo.png")
	u3 = u2.relative(u1, allowschemerel=True)
	assert u3.scheme is None
	assert str(u3) == "//www.example.com/images/logo.png"

	u1 = url.URL("http://www.example.org/about/index.html")
	u2 = url.URL("http://www.example.org/images/logo.png")
	u3 = u2.relative(u1, allowschemerel=True)
	assert u3.scheme is None
	assert str(u3) == "../images/logo.png"
