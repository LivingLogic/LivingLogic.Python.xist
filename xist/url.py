#! /usr/bin/env python

"""URL class.

This module contains only one useful variable: the URL class
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import types
import urlparse
import urllib
from xist import utils

uses_relative = urlparse.uses_relative + [None]
uses_netloc = urlparse.uses_netloc

def _isPathMarker(dir):
	"""
	_isPathMarker(dir) -> bool
	
	returns if the directory name dir is a path marker.
	"""
	return dir is not None and dir.startswith("*")

def _isNoPathMarker(dir):
	"""
	_isNoPathMarker(dir) -> bool
	
	returns not _isPathMarker(dir)
	"""
	return not _isPathMarker(dir)


def removeDuplicateMarkers(path):
	"""remove duplicate path markers, keep only the last"""

	path = path[:] # make a copy, since path will be modified
	markers = {} # todo: use a list here ?

	# iterate of path from back to front, None-ing all
	# path markers which already occured
	for i in range(len(path)-1, -1, -1): # iterate backwards
		dir = path[i]
		if dir in (u'.', u''):
			path[i] = None
		elif _isPathMarker(dir):
			if markers.has_key(dir): # already occured
				path[i] = None
			markers[dir] = 1 # mark as used
	# remove all None-ed path parts
	return filter(lambda x: x is not None, path)

def isUsefullPathPart(dir):
	"""
	returns true if this path part is significant,
	that is: neither empty, nor '.' or a pathmarker
	"""
	# use 'or' for short evaluation (avoid call)
	return not (dir in (u'.', u'') or _isPathMarker(dir))

def _normalize(path, removeAllMarkers=0):
	"""
	normalize the path by removing combinations of down/up
	and removing duplicate path markers.

	If removeAllMarkers == 1, all path markers will be removed, not
	only duplicates.
	"""

	if path in ([], [u'.']): # shortcut for very common cases
		return path[:] # return a copy
	
	# the first element of absolute pathes '', preserve it
	wasAbsolutePath = len(path) and path[0] == u''
	if removeAllMarkers:
		path = filter(isUsefullPathPart, path)
	else:
		path = removeDuplicateMarkers(path)
	if wasAbsolutePath:
		path[:0] = [u'']

	# remove "foo/.." combinations
	# this works by using two pointers: 'i' for the up-dir part
	# and 'j' for the potential '..' part. After removing one
	# "foo/.." combination, 'i' and 'j' are set to the
	# predecessor or successor respectivly. Example:
	#	aa/bb/cc/../xx			i = 3; j = 4
	#	aa/bb/<None>/<None>/xx		i = 2; j = 5
	# This allows reduction of 'aa/bb/cc/../../' to 'aa/'
	i = 0; j = 1
	while j < len(path):
		if path[j] == u".." and path[i] != u".." and _isNoPathMarker(path[i]):
			# up/down combination found, None it out
			path[i] = path[j] = None
			i -= 1 ; j += 1
			if i < 0:
				# all leading dirs have been removed,
				# so continue behind this part at 'j'
				i = j; j += 1
		else:
			# nothing to do, move on one step
			i = j; j += 1
#### this is from urlparse.urljoin():  todo: implement here
## 	if len(segments) == 2 and segments[1] == '..' and segments[0] == '':
## 		segments[-1] = ''
## 	elif len(segments) >= 2 and segments[-1] == '..':
## 		segments[-2:] = ['']
	return [ x for x in path if x is not None ] or [u'.']

class URL:
	"""
	This class represents XSC URLs.
	Every instance has the following instance variables:
	scheme -- The scheme (e.g. "http" or "ftp"); there's a special scheme "server" for server relative URLs
	server -- The server name
	port -- The port number
	path -- The path to the file as a list of strings
	file -- The filename without extension
	ext -- The file extension
	parameters -- The parametes
	query -- The query
	fragment -- The fragment
	These variables form a URL in the following way
	<scheme>://<server>:<port>/<path>/<file>.<ext>;<params>?<query>#<fragment>

	There is one additional feature supported by this class: path markers
	A path marker is a directory name beginning with *. A path marker is
	not treated as a real directory name, but marks a position in a path.
	When you combine two URLs and the second URL begins with a path marker
	the path will be relative to the directory path to the left of the same
	path marker in the first URL. Example:
		URL("/foo/bar/*root/cgi/baz.py") + URL("*root/cgi2/baz2.py")
	will be an URL equivalent to
		URL("/foo/bar/*root/cgi2/baz2.py")
	"""

	__safe = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_,.-:/"

	def __init__(self, url=None, scheme=None, server=None, port=None, path=None, file=None, ext=None, parameters=None, query=None, fragment=None):
		# initialize the defaults
		self.scheme = self.server = self.port = None
		self.__path = []
		self.file = self.ext = self.parameters = self.query = self.fragment = None
		if url is None:
			pass
		elif type(url) in (types.StringType, types.UnicodeType):
			self.__fromString(url)
		elif isinstance(url, URL):
			self.scheme     = url.scheme
			self.server     = url.server
			self.port       = url.port
			self.__path     = url.__path[:] # make copy of list
			self.file       = url.file
			self.ext        = url.ext
			self.parameters = url.parameters
			self.query      = url.query
			self.fragment   = url.fragment
		else:
			raise ValueError("URL argument must be either a string or an URL or None")

		if scheme is not None:
			self.scheme = scheme
		if server is not None:
			self.server = server
		if port is not None:
			self.port = port
		if path is not None:
			self.__path = map(utils.stringFromCode, path)
		if ext is not None:
			self.ext = ext
		if file is not None:
			self.file = file
		if parameters is not None:
			self.parameters = parameters
		if query is not None:
			self.query = query
		if fragment is not None:
			self.fragment = fragment

		self.__normalize()

	def __setattr__(self, name, value):
		if name in ("scheme", "server", "file", "ext", "parameters", "query", "fragment"):
			value = utils.stringFromCode(value)
		self.__dict__[name] = value

	def __getitem__(self, index):
		"""
		return the <argref>index</argref>th directory from the path (including path markers)
		"""
		return self.__path[index]

	def __setitem__(self, index, value):
		"""
		allows you to replace the <argref>index</argref>th path entry
		"""
		self.__path[index] = utils.stringFromCode(value)
		self.__normalize()

	def __delitem__(self, index):
		"""
		removes the index'th path entry
		"""
		del self.__path[index]
		self.__normalize()

	def __getslice__(self, index1, index2):
		"""
		returns a slice of the path
		"""
		return self.__path[index1:index2]

	def __setslice__(self, index1, index2, sequence):
		"""
		replaces a slice of the path
		"""
		self.__path[index1:index2] = map(utils.stringFromCode, sequence)
		self.__normalize()

	def __delslice__(self, index1, index2):
		"""
		removes a slice of the path
		"""
		del self.__path[index1:index2]
		self.__normalize()

	def __len__(self):
		"""
		return the length of the path
		"""
		return len(self.__path)

	def append(self, *others):
		"""
		appends all directory names in <argref>others</argref> to the path.
		"""
		for other in others:
			self.__path.append(utils.stringFromCode(other))
		self.__normalize()

	def insert(self, index, *others):
		"""
		inserts all items in <argref>others</argref> at the position <argref>index</argref> in the path.
		(this is the same as <code><self/>[<argref>index</argref>:<argref>index</argref>] = <argref>others</argref></code>)
		"""
		for other in others:
			self.__path.insert(index, utils.stringFromCode(other))
			index += 1

	def __repr__(self):
		v = []
		if self.scheme is not None:
			v.append("scheme=" + repr(self.scheme))
		if self.server is not None:
			v.append("server=" + repr(self.server))
		if self.port is not None:
			v.append("port=" + repr(self.port))
		if self.__path is not None:
			v.append("path=" + repr(self.__path))
		if self.file is not None:
			v.append("file=" + repr(self.file))
		if self.ext is not None:
			v.append("ext=" + repr(self.ext))
		if self.parameters is not None:
			v.append("parameters=" + repr(self.parameters))
		if self.query is not None:
			v.append("query=" + repr(self.query))
		if self.fragment is not None:
			v.append("fragment=" + repr(self.fragment))
		return "URL(%s)" % ", ".join(v)

	def asPlainString(self):
		return self.__asString(0)

	def asString(self):
		return self.__asString(1)

	def __add__(left, right):
		"""
		joins two URLs together. When the second URL is
		absolute (i.e. contains a scheme other than "server"
		or ""), you'll get a copy of the second URL.
		"""
		return left.__join(right)

	def __radd__(left, right):
		return URL(right).__join(left)

	__radd__.__doc__ = __add__.__doc__

	def clone(self):
		"""
		returns an identical clone of this URL.
		"""
		return URL(self)

	def isRemote(self):
		if not self.scheme:	# may be None
			return 0
		elif self.scheme == u"server" and self.server == u"localhost":
			return 0
		else:
			return 1

	def __hasPath(self):
		"""returns true if path or file is given"""
		return self.__path or self.scheme == "server" or self.file or self.ext is not None

	def __requiresPath(self):
		a = self.server or self.file or self.ext is not None
		if self.__path:
			return not a
		else:
			return not (a or self.fragment or self.parameters)

	
	def relativeTo(self, other):
		"""
		<par nointent>returns <self/> interpreted relative
		to <code>other</code>.</par>

		<par>Note that remote URLs won't be modified in any way,
		because although the file you've read might have been
		remote, the parsed XSC file that you output, probably
		isn't. The resulting URL won't have any path markers
		in it.</par>
		"""
		if not self.__hasPath():
			new = other + self # make eventually absolute URL
		else: # self has only some of params, query, fragment 
			new = self.clone()
		newpath = _normalize(new.__path, removeAllMarkers=1)
		if not new.scheme:
			otherpath =_normalize(other.__path, removeAllMarkers=1)
			if newpath == [u'.']: newpath = []
			if otherpath == [u'.']: otherpath = []
			while len(otherpath) and len(newpath) and otherpath[0] == newpath[0]:
				# throw away identical directories in
				# both paths (we don't have to go up
				# from file and down to path for these
				# identical directories)
				del otherpath[0]
				del newpath[0]
			# now for the rest of the path we have to go
			# up from file and down to path (the
			# directories for this are still in path)
			newpath[:0] = [u".."]*len(otherpath)
			if newpath == [] and new.__requiresPath():
				newpath = [u'.']
			if new.file == other.file and new.ext == other.ext:
				new.file = u''; new.ext = None
		new.__path = newpath
		return new

	def __cmp__(self, other):
		assert isinstance(other, URL), 'URLs can only be compared with URLs'
		scheme1 = self.scheme
		if scheme1 is not None:
			scheme1 = scheme1.lower()
		scheme2 = self.scheme
		if scheme2 is not None:
			scheme2 = scheme2.lower()
		server1 = self.server
		if server1 is not None:
			server1 = server1.lower()
		server2 = self.server
		if server2 is not None:
			server2 = server2.lower()
		return cmp(scheme1, scheme2) or cmp(server1, server2) or cmp(self.port, other.port) or cmp(self.__path, other.__path) or cmp(self.file, other.file) or cmp(self.ext, other.ext) or cmp(self.parameters, other.parameters) or cmp(self.query, other.query) or cmp(self.fragment, other.fragment)

	def open(self):
		return urllib.urlopen(self.__quote())

	def retrieve(self):
		return urllib.urlretrieve(self.__quote())

	def read(self):
		return self.open().read()

	def readlines(self):
		return self.open().readlines()

	def __fromString(self, url):
		(scheme, server, path, parameters, query, fragment) = urlparse.urlparse(url)
		scheme = utils.stringFromCode(scheme)
		server = utils.stringFromCode(server)
		__path = map(utils.stringFromCode, path)
		parameters = utils.stringFromCode(parameters)
		query = utils.stringFromCode(query)
		fragment = utils.stringFromCode(fragment)
		if scheme == u"": # do we have a local file?
			if len(path):
				if path[0] == u"/": # this is a server relative URL
					path = path[1:] # drop the empty string in front of the first "/" ...
					scheme = u"server" # ... and use a special scheme for that
		elif scheme in (u"ftp", u"http", u"https"):
			if len(path) and len(server):
				path = path[1:] # the path from urlparse started with "/" too
		port = None
		pos = server.rfind(u":")
		if pos != -1:
			port = int(server[pos+1:])
			server = server[:pos]
		path = path.split(u"/")
		file = path[-1]
		if file not in (u'.', u'..'):
			path = path[:-1]
		else:
			file = ''

		ext = None
		if scheme in (u"ftp", u"http", u"https", u"server", u""):
			pos = file.rfind(u".")
			if pos != -1:
				ext = file[pos+1:]
				file = file[:pos]

		self.scheme = scheme or None
		self.server = server or None
		self.port = port
		self.__path = path
		self.file = file or None
		self.ext = ext
		self.parameters = parameters or None
		self.query = query or None
		self.fragment = fragment or None

	def __asString(self, withPathMarkers):
		scheme = self.scheme or u""
		server = self.server or u""
		if self.port:
			server += u":" + str(self.port)
		if withPathMarkers:
			path = self.__path[:] # make a copy
		else:
			path = _normalize(self.__path, removeAllMarkers=1)
		if scheme == u"server":
			scheme = u"" # remove our own private scheme name
			path[:0] = [u""] # make sure that there's a "/" at the start
		if not self.__requiresPath() and path == [u'.']:
			path = []
		file = self.file or u""
		if self.ext is not None:
			file = u"%s.%s" % (file, self.ext)
		path.append(file)
		url = urlparse.urlunparse((scheme, server, u"/".join(path), self.parameters or u"", self.query or u"", self.fragment or u""))
		return url

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

	def __join(base, url):
		"""Join a base URL and a possibly relative URL to form
		an absolute interpretation of the latter."""

		def do_join(base, url):
			if not url.scheme:
				url.scheme = base.scheme
			if not base: # todo: gibt es das?
				return url
			if url.scheme != base.scheme or url.scheme not in uses_relative:
				return url
			if url.scheme in uses_netloc:
				if url.server:
					return url
				url.server = base.server
			if len(url.__path) and url.__path[0] == u'':
				return url
			if not url.__path and not url.file and url.ext is None:
				# neither path nor filename set
				url.__path = base.__path[:] # copy
				url.file = base.file
				url.ext = base.ext
				url.query = url.query or base.query
				return url
			path = base.__path[:]
			if len(url.__path) and _isPathMarker(url.__path[0]):
				try:
					pos = path.index(url.__path[0])
				except ValueError:
					pass
				else:
					del path[pos:]
			url.__path = _normalize(path + url.__path, removeAllMarkers=0)
			return url

		url = URL(url)  # this implies clone/coerce
		if url.scheme == 'server':
			url.scheme = None
			url.__path[:0] = [u""]
		if base.scheme == 'server':
			base = base.clone()
			base.scheme = None
			base.__path[:0] = [u""]
		url = do_join(base, url)
		if not url.scheme and url.__path[:1] == [u""]:
			url.scheme = u'server'
			del url.__path[0]
		return url

	def __normalize(self):
		"""
		normalize the path by removing combinations of down/up
		and removing duplicate path markers.
		"""
		self.__path = _normalize(self.__path, removeAllMarkers=0)


def test_normalize():
	"""
	Tests whether '_normalize' returns the expected results.
	"""
	for removeMarkers, input, output in (
		# Tuple format: removeMakers, input, output
		(0, '', ''),
		(0, './', '.'),
		#(0, '/./', '/'), # _normalize doe not handle absolute pathes
		(0, 'xx', 'xx'),
		(0, 'xx/yy', 'xx/yy'),
		(0, 'xx/..', '.'),
		(0, 'xx/../.', '.'),
		(0, './xx/..', '.'),
		(0, './xx/../.', '.'),
		(0, 'xx/./..', '.'),
		(0, 'xx/yy/..', 'xx'),
		(0, 'xx//yy/../..', '.'),
		(0, 'xx/../..//', '..'),
		(0, 'xx/.././..', '..'),
		(0, 'xx/.', 'xx'),
		(0, './xx', 'xx'),
		#(0, '/xx', '/xx'), # _normalize doe not handle absolute pathes
		#(0, '/./xx', '/xx'), # dito

		(0, '*XX', '*XX'),
		(0, 'xx/*XX', 'xx/*XX'),
		(0, 'xx/*XX/yy', 'xx/*XX/yy'),
		(0, 'xx/*XX/..', 'xx/*XX/..'),
		(0, 'xx/*XX/../.', 'xx/*XX/..'),
		(0, 'xx/*XX/./..', 'xx/*XX/..'),
		(0, './xx//*XX/..', 'xx/*XX/..'),
		(0, './xx/*XX/../.', 'xx/*XX/..'),
		(0, 'xx/*XX/yy/..', 'xx/*XX'),
		(0, 'xx/*XX/yy/../..', 'xx/*XX/..'),
		(0, 'xx/yy/*XX/../..', 'xx/yy/*XX/../..'),
		(0, 'xx/../*XX/..', '*XX/..'),

		(1, '*XX', '.'),
		(1, 'xx/*XX', 'xx'),
		(1, 'xx/*XX/yy', 'xx/yy'),
		(1, 'xx/*XX/..', '.'),
		(1, 'xx/*XX//..', '.'),
		(1, 'xx/*XX/../.', '.'),
		(1, 'xx/*XX/./..', '.'),
		(1, './xx//*XX/..', '.'),
		(1, './xx/*XX/../.', '.'),
		(1, 'xx//*XX/yy/..', 'xx'),
		(1, 'xx/*XX/./yy/../..', '.'),
		(1, 'xx/../*XX/..', '..'),

		):
		#print `in_`, '\t', `out`
		test = "/".join(_normalize(input.split("/"), removeMarkers))
		if test != output:
			raise str('Test failed. %r -> %r -> %r != %r' % (input, input.split('/'), test, output))
	print 'test passed: _normalize'

def test_url():
	"""
	Test whether instaziation, '+' and others have the expected effect.

	Check is done via comparing against another URL or a string; in the
	later case, the URL is converted using asString().
	"""
	import types
	for num, o_lhs, o_rhs in (
		(10, URL('.'), './'),
		(11, URL('./'), './'),
		(20, URL('..'), '../'),
		(21, URL('../'), '../'),
		(30, URL('http://aa/bb/cc.html'), 'http://aa/bb/cc.html'),
		(40, URL('http://aa/*BB/bb/cc.html'), 'http://aa/bb/cc.html'),
		(50, URL('/aa/bb/cc.html'), '/aa/bb/cc.html'),
		(60, URL('http:bb/cc/'), 'http:bb/cc/'),
		# these fail, should they?
		(69, URL('http:/bb/cc/'), 'http:/bb/cc/'),
		(70, URL('http:') + URL('/bb/cc/'), 'http:/bb/cc/'),
		# is this what is expected?
		(80, URL('/bb/cc/') + URL('http:'), 'http:'),
		(90, URL('#mark'), '#mark')
		):
		lhs = o_lhs
		rhs = o_rhs
		if type(lhs) != type(rhs):
			if type(rhs) is types.StringType:
				if isinstance(lhs, URL):
					lhs = o_lhs.asPlainString()
				else:
					lhs = str(lhs)
			elif type(lhs) is types.StringType:
				if isinstance(rhs, URL):
					rhs = o_rhs.asPlainString()
				else:
					rhs = str(rhs)
		if lhs != rhs:
			raise str('Test %s failed. %r (%r) != %r (%r)' % (num, o_lhs, lhs, o_rhs, rhs))
	print 'test passed: URL()'

def test_relativeTo():
	"""
	Test correctness of relativeTo().
	"""
	for From, to, should in (
		('./', './', './'),
		('cc.html', './', './'),
		('./cc.html', './', './'),
		('*/cc.html', '*/', './'),
		('*/cc.html', './', './'),

		('cc.html', '#mark', '#mark'),
		('*/cc.html', '*/#mark', './#mark'),
		('*/cc.html', '#mark', '#mark'),
		('*/cc.html', '*/cc.html#mark', '#mark'),
		('*/cc.html', '*/dd.html#mark', 'dd.html#mark'),
		('*/aa/bb/cc.html', '*/', '../../'),
		#('', '', ''),
		#('', '', ''),

		# relativeTo() does not really handle urls with scheme set
		('http://server/aa/bb.html', 'http://server/aa/cc.html', 'http://server/aa/cc.html'),

		# testing absolute pathes is worthless, since they have
		# a scheme = 'server' and thus are not really handled
		('/aa/bb.html', '/xx.html', '/xx.html'),
		):
		u = URL(to).relativeTo(URL(From)).asString()
		#print "\t".join((`URL(to)`, `URL(From)`, u, should))
		if u != should:
			raise str('Test failed:\n%r != %r\n(%r -> %r)' % (u, should, From, to))
	print 'test passed: relativeTo()'

test_input = urlparse.test_input

def test_url2():
	base = __empty = URL('')
	for line in test_input.split('\n'):
		words = line.split()
		if not words:
			continue
		url = words[0]
		parts = URL(url)
		print '%-10s : %s' % (url, parts)
		abs = base + url
		if base is __empty:
			base = abs
		wrapped = '<URL:%s>' % abs.asString()
		print '%-10s = %s' % (url, wrapped)
		if len(words) == 3 and words[1] == '=':
			if wrapped != words[2]:
				print 'EXPECTED', words[2], '!!!!!!!!!!'

if __name__ == '__main__':
	test_normalize()
	test_url()
	test_relativeTo()
	test_url2()
