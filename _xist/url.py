#! /usr/bin/env python

## Copyright 1999-2001 by LivingLogic AG, Bayreuth, Germany.
## Copyright 1999-2001 by Walter Dörwald
##
## All Rights Reserved
##
## Permission to use, copy, modify, and distribute this software and its documentation
## for any purpose and without fee is hereby granted, provided that the above copyright
## notice appears in all copies and that both that copyright notice and this permission
## notice appear in supporting documentation, and that the name of LivingLogic AG or
## the author not be used in advertising or publicity pertaining to distribution of the
## software without specific, written prior permission.
##
## LIVINGLOGIC AG AND THE AUTHOR DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
## INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL
## LIVINGLOGIC AG OR THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
## DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
## IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
## IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""URL class.

This module contains only one useful variable: the URL class
"""

__version__ = tuple(map(int, "$Revision$"[11:-2].split(".")))
# $Source$

try:
	import Image
except ImportError:
	Image = None

import os, stat, types, urlparse, urllib

from xist import options

urlparse.uses_relative.extend(("root", "server", None))
urlparse.uses_params.extend(("root", "server"))
urlparse.uses_query.extend(("root", "server"))
urlparse.uses_fragment.extend(("root", "server"))
urlparse.non_hierarchical.append("javascript")

def _normalize(path):
	"""
	normalize the path by removing combinations of down/up,
	empty path components or '.'.
	"""

	if path in ([], [u'.']): # shortcut for very common cases
		return path[:] # return a copy

	wasAbsolutePath = len(path) and path[0] == u'' # the first element of absolute paths '', preserve it

	newpath = []
	for dir in path:
		if dir and dir != ".":
			if dir == u".." and newpath and newpath[-1] != "..":
				newpath.pop()
			else:
				newpath.append(dir)
	if wasAbsolutePath:
		newpath.insert(0, u'')

	return newpath

class URL:
	"""
	This class represents XSC URLs.
	Every instance has the following instance variables:
	scheme -- The scheme (e.g. "http" or "ftp"); there's a special scheme "server" for server relative URLs and "root" for URLs relative to the current directory
	server -- The server name
	port -- The port number
	path -- The path to the file as a list of strings
	file -- The filename including the extension
	params -- The parametes
	query -- The query
	fragment -- The fragment
	These variables form a URL in the following way
	<scheme>://<server>:<port>/<path>/<file>;<params>?<query>#<fragment>

	There is one additional feature supported by this class: the scheme root
	is used for URLs that are relative to the current directory.
	"""

	__safe = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_,.-:/"

	def __init__(self, url=None, scheme=None, server=None, port=None, path=None, file=None, params=None, query=None, fragment=None):
		# initialize the defaults
		self.scheme = self.server = self.port = None
		self.path = []
		self.file = self.params = self.query = self.fragment = None
		if url is None:
			pass
		elif type(url) in (types.StringType, types.UnicodeType):
			self.__fromString(url)
		elif isinstance(url, URL):
			self.scheme   = url.scheme
			self.server   = url.server
			self.port     = url.port
			self.path     = url.path[:] # make copy of list
			self.file     = url.file
			self.params   = url.params
			self.query    = url.query
			self.fragment = url.fragment
		else:
			raise ValueError("URL argument must be either a string or an URL or None not %s" % type(url))

		if scheme is not None:
			self.scheme = scheme
		if server is not None:
			self.server = server
		if port is not None:
			self.port = port
		if path is not None:
			self.path = path
		if file is not None:
			self.file = file
		if params is not None:
			self.params = params
		if query is not None:
			self.query = query
		if fragment is not None:
			self.fragment = fragment
		self.path = _normalize(self.path)

	def __repr__(self):
		v = []
		if self.scheme is not None:
			v.append("scheme=%r" % self.scheme)
		if self.server is not None:
			v.append("server=%r" % self.server)
		if self.port is not None:
			v.append("port=%r" % self.port)
		if self.path is not None:
			v.append("path=%r" % self.path)
		if self.file is not None:
			v.append("file=%r" % self.file)
		if self.params is not None:
			v.append("params=%r" % self.params)
		if self.query is not None:
			v.append("query=%r" % self.query)
		if self.fragment is not None:
			v.append("fragment=%r" % self.fragment)
		return "URL(%s)" % ", ".join(v)

	def asString(self):
		return self._asString(0)

	def asPlainString(self):
		return self._asString(1)

	def _asString(self, plain):
		if self.scheme:
			scheme = self.scheme.lower()
		else:
			scheme = u""
		if self.server:
			server = self.server.lower()
		else:
			server = u""
		if self.port is not None:
			server += u":%d" % self.port
		path = _normalize(self.path)
		if scheme==u"server":
			scheme = u"" # remove our own private scheme name
			path.insert(0, u"") # make sure that there's a "/" at the start
		if plain:
			if scheme == u"root":
				scheme = u""
		if self.scheme in urlparse.uses_netloc and (self.server is not None or self.port is not None) and not path:
			path = [""]
		if not len(path) and self.file == u"" and (self.params or self.query or self.fragment):
			path = [u"."]
		file = self.file or u""
		path.append(file)
		return urlparse.urlunparse((scheme, server, u"/".join(path), self.params or u"", self.query or u"", self.fragment or u""))

	def __div__(self, other):
		"""Join a base URL and a possibly relative URL to form
		an absolute interpretation of the latter."""

		other = URL(other) # this implies clone/coerce

		if other.scheme==u"root":
			return other
		if other.scheme==u"server":
			other.scheme = None
			other.path.insert(0,u"")
		if other.file == u"" and not len(other.path) and not other.scheme:
			other.path.append(u".")
		return URL(urlparse.urljoin(self.asString(), other.asString()))

	def clone(self):
		"""
		returns an identical clone of this URL.
		"""
		return URL(self)

	def isRemote(self):
		if not self.scheme: # may be None or ""
			return 0
		elif self.scheme == u"server" and self.server == u"localhost":
			return 0
		else:
			return 1

	def relativeTo(self, other):
		"""
		<par nointent>returns <self/> interpreted relative
		to <code>other</code>, i.e. return a mimimal URL <code>rel</code>,
		such that <code>other/rel == <self/></code>.</par>
		"""
		new = self.clone() # make a copy and modify it
		if new.scheme in urlparse.uses_relative and (other.scheme==new.scheme or (new.scheme=="root" and other.scheme is None)) and other.server==new.server and other.port==new.port: # test if the URL uses the same scheme and goes to the same machine
			# if yes, the url is a relative one
			new.scheme = None
			new.server = None
			new.port = None
			# we construct the path from one file to the other
			otherpath = other.path[:]
			newpath = new.path[:]
			if newpath==[u'.']: newpath = []
			if otherpath==[u'.']: otherpath = []
			while len(otherpath) and len(newpath) and otherpath[0]==newpath[0]:
				# throw away identical directories in both paths (we don't have to go up
				# one dir in one path and down in the other for these identical directories)
				del otherpath[0]
				del newpath[0]
			# now for the rest of the path we have to go
			# up from file and down to path (the
			# directories for this are still in path)
			newpath[:0] = [u".."]*len(otherpath)
			if not len(newpath):
				# the link goes to the same URL ... we can throw away the filename, if we have a fragment in it
				if new.fragment is not None and new.file==other.file and new.query==other.query and new.params==other.params:
					new.file = None
			new.path = newpath
		return new

	def __cmp__(self, other):
		assert isinstance(other, URL), "URLs can only be compared with URLs"
		scheme1 = self.scheme
		if scheme1 is not None:
			scheme1 = scheme1.lower()
		scheme2 = other.scheme
		if scheme2 is not None:
			scheme2 = scheme2.lower()
		server1 = self.server
		if server1 is not None:
			server1 = server1.lower()
		server2 = other.server
		if server2 is not None:
			server2 = server2.lower()
		return cmp(scheme1, scheme2) or cmp(server1, server2) or cmp(self.port, other.port) or cmp(self.path, other.path) or cmp(self.file, other.file) or cmp(self.params, other.params) or cmp(self.query, other.query) or cmp(self.fragment, other.fragment)

	def __nonzero__(self):
		"""
		return if the URL is not empty (i.e. URL())
		"""
		return self.scheme is not None or self.server is not None or self.port is not None or len(self.path) != 0 or self.file is not None or self.params is not None or self.query is not None or self.fragment is not None

	def open(self):
		return urllib.urlopen(self.__quote())

	def retrieve(self):
		return urllib.urlretrieve(self.__quote())

	def info(self):
		file = urllib.urlopen(self.__quote())
		info = file.info()
		file.close()
		return info

	def read(self):
		file = self.open()
		data = file.read()
		file.close()
		return data

	def readlines(self):
		file = self.open()
		data = file.readlines()
		file.close()
		return data

	def __fromString(self, url):
		(scheme, server, path, params, query, fragment) = urlparse.urlparse(url)
		if scheme == u"": # do we have a local file?
			if path[:1] == u"/": # this is a server relative URL
				path = path[1:] # drop the empty string in front of the first "/" ...
				scheme = u"server" # ... and use a special scheme for that
		elif scheme in urlparse.uses_netloc:
			if len(path) and len(server):
				path = path[1:] # the path from urlparse started with "/" too
		port = None
		pos = server.rfind(u":")
		if pos != -1:
			port = int(server[pos+1:])
			server = server[:pos]
		path = path.split(u"/")
		file = path[-1]
		if file not in (u".", u".."):
			path = path[:-1]
		else:
			file = u""

		self.scheme = scheme or None
		self.server = server or None
		self.port = port
		self.path = path
		if (params or query or fragment) and not file and not scheme and not server and not port: # file in URL("#foo") should be unset, but in URL("root:#foo") it should be set
			self.file = None
		elif scheme and not path and not file and not params and not query and not fragment:
			self.file = None
		else:
			self.file = file
		self.params = params or None
		self.query = query or None
		self.fragment = fragment or None

	def __quote(self):
		"""
		encodes the URL with % escapes
		"""
		url = self.asPlainString().encode("utf8")
		#v = []
		#for c in url:
		#	if c in self.__safe:
		#		v.append(c)
		#	else:
		#		v.append("%%%02x" % ord(c))
		#return "".join(v)
		return url

	def isRetrieve(self):
		"""
		returns if the file specified by the URL should be retrieved or not
		according to the "remoteness" of the URL and the retrieve options.
		"""
		remote = self.isRemote()
		if (options.retrieveremote and remote) or (options.retrievelocal and (not remote)):
			return 1
		else:
			return 0

	def fileSize(self):
		"""
		returns the size of a file in bytes or None if the file shouldn't be read
		"""
		size = None
		if self.isRetrieve():
			try:
				(filename, headers) = self.retrieve()
				size = os.stat(filename)[stat.ST_SIZE]
			finally:
				urllib.urlcleanup()
		return size

	def imageSize(self):
		"""
		returns the size of an image as a tuple or None if the image shouldn't be read
		"""
		size = None
		if Image is not None:
			if self.isRetrieve():
				try:
					(filename, headers) = self.retrieve()
					if headers.maintype == "image":
						img = Image.open(filename)
						size = img.size
						del img
				finally:
					urllib.urlcleanup()
		return size

def test_normalize(input, output):
	"""
	Tests whether '_normalize' returns the expected results.
	"""
	test = "/".join(_normalize(input.split("/")))
	if test != output:
		raise str('normalize test failed. %r -> %r -> %r != %r' % (input, input.split('/'), test, output))

def test_url(o_lhs, o_rhs):
	"""
	Test whether instantiation, '/' and others have the expected effect.

	Check is done via comparing against another URL or a string; in the
	later case, the URL is converted using asString().
	"""
	import types
	lhs = o_lhs
	rhs = o_rhs
	if type(lhs) != type(rhs):
		if type(rhs) is types.StringType:
			if isinstance(lhs, URL):
				lhs = o_lhs.asString()
			else:
				lhs = str(lhs)
		elif type(lhs) is types.StringType:
			if isinstance(rhs, URL):
				rhs = o_rhs.asString()
			else:
				rhs = str(rhs)
	if lhs != rhs:
		raise str('Test failed. %r (%r) != %r (%r)' % (o_lhs, lhs, o_rhs, rhs))

def test_relativeTo(from_, to, should):
	"""
	Test correctness of relativeTo().
	"""
	relu = URL(to).relativeTo(URL(from_))
	u = relu.asString()
	#print "\t".join((`URL(to)`, `URL(from_)`, u, should))
	if u != should:
		raise str('Test failed: %r.relativeTo(%r) is %r but should be %r' % (to, from_, u, should))
	#if from_/relu != from_/to:
	#	raise str('Invariance test failed: from/rel=%r != from/to=%r' % (from_/relu, from_/to))

test_input = urlparse.test_input

def test_url2():
	base = __empty = URL('')
	for line in test_input.splitlines():
		words = line.split()
		if not words:
			continue
		url = words[0]
		parts = URL(url)
		print '%-10s : %s' % (url, parts)
		abs = base/url
		if base is __empty:
			base = abs
		wrapped = '<URL:%s>' % abs.asString()
		print '%-10s = %s' % (url, wrapped)
		if len(words) == 3 and words[1] == '=':
			if wrapped != words[2]:
				print 'EXPECTED', words[2], '!!!!!!!!!!'

if __name__ == '__main__':
	test_normalize('', '')
	test_normalize('./', '')
	#test_normalize('/./', '/') # _normalize does not handle absolute paths
	test_normalize('xx', 'xx')
	test_normalize('xx/yy', 'xx/yy')
	test_normalize('xx/..', '')
	test_normalize('xx/../.', '')
	test_normalize('./xx/..', '')
	test_normalize('./xx/../.', '')
	test_normalize('xx/./..', '')
	test_normalize('xx/yy/..', 'xx')
	test_normalize('xx//yy/../..', '')
	test_normalize('xx//yy/./..', 'xx')
	test_normalize('xx//yy//../', 'xx')
	test_normalize('xx/../..//', '..')
	test_normalize('xx/.././..', '..')
	test_normalize('xx/.', 'xx')
	test_normalize('./xx', 'xx')
	#test_normalize('/xx', '/xx') # _normalize does not handle absolute paths
	#test_normalize('/./xx', '/xx') # dito
	print 'test passed: _normalize'

	test_url(URL("."), "./")
	test_url(URL("./"), "./")
	test_url(URL(".."), "../")
	test_url(URL("../"), "../")
	test_url(URL("http://aa/bb/cc.html"), "http://aa/bb/cc.html")
	test_url(URL("/aa/bb/cc.html"), "server:aa/bb/cc.html")
	test_url(URL("http:bb/cc/"), "http:bb/cc/")
	# these two fail, should they?
	#test_url(URL("http:/bb/cc/"), "http:/bb/cc/")
	#test_url(URL("http:") / URL("/bb/cc/"), "http:/bb/cc/")
	test_url(URL("http://test.com/index.html") / URL("impress.html"), "http://test.com/impress.html")
	test_url(URL("/bb/cc/") / URL("http:"), "http:")
	test_url(URL("mailto:x@y.z") / URL("index.html"), "index.html")
	test_url(URL("javascript: return ':/:/:';") / URL("index.html"), "index.html")
	test_url(URL("http://test.com/gurk/hurz.gif") / URL("/index.html"), "http://test.com/index.html")
	test_url(URL("http://test.com/gurk/hurz.gif") / URL("../"), "http://test.com/")
	test_url(URL("http://test.com/gurk/hurz.gif") / URL("../gurk.gif?foo=bar#nix"), "http://test.com/gurk.gif?foo=bar#nix")
	test_url(URL("http://test.com/gurk/hurz.gif") / URL("../../gurk.gif?foo=bar#nix"), "http://test.com/../gurk.gif?foo=bar#nix")
	test_url(URL("http://test.com/gurk/hurz.gif") / URL("root:gurk.gif"), "root:gurk.gif")
	test_url(URL("root:gurk.gif") / URL("http://test.com/gurk/hurz.gif"), "http://test.com/gurk/hurz.gif")
	test_url(URL("root:gurk/hurz/hinz.gif") / URL("hinz/kunz.gif"), "root:gurk/hurz/hinz/kunz.gif")
	test_url(URL("root:gurk/hurz/hinz.gif") / URL("root:hinz/kunz.gif"), "root:hinz/kunz.gif")
	test_url(URL("#mark"), "#mark")
	print 'test passed: URL()'

	test_relativeTo('./', './', '')
	test_relativeTo('cc.html', './', '')
	test_relativeTo('./cc.html', './', '')
	test_relativeTo("root:xist/Documentation.html", "http://www.livinglogic.de/", "http://www.livinglogic.de/")
	test_relativeTo('root:cc.html', 'root:', '')
	test_relativeTo('root:cc.html', './', '')
	test_relativeTo('cc.html', '#mark', '#mark')
	test_relativeTo('root:cc.html', 'root:#mark', './#mark')
	test_relativeTo('root:cc.html', '#mark', '#mark')
	test_relativeTo('root:cc.html', 'root:cc.html#mark', '#mark')
	test_relativeTo('root:cc.html', 'root:dd.html#mark', 'dd.html#mark')
	test_relativeTo('root:aa/bb/cc.html', 'root:', '../../')
	#test_relativeTo('', '', '')
	test_relativeTo('http://server/aa/bb.html', 'http://server/aa/cc.html', 'cc.html')
	test_relativeTo('/aa/bb.html', '/xx.html', '../xx.html')
	print 'test passed: relativeTo()'

	test_url2()
