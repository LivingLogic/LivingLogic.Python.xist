#! /usr/bin/env python

"""URL class.

This module contains only one useful variable: the URL class
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import types
import urlparse
import urllib
import xsc

def _isPathMarker(dir):
	"""
	_isPathMarker(dir) -> bool
	
	returns if the directory name dir is a path marker.
	"""
	return dir.startswith("*")

def _isNoPathMarker(dir):
	"""
	_isNoPathMarker(dir) -> bool
	
	returns not _isPathMarker(dir)
	"""
	return not _isPathMarker(dir)

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

	def __init__(self, url = None, scheme = None, server = None, port = None, path = None, file = None, ext = None, parameters = None, query = None, fragment = None):
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
			self.__path     = url.__path[:]
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
			self.__path = map(xsc.stringFromCode, path)
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
			value = xsc.stringFromCode(value)
		self.__dict__[name] = value

	def __setitem__(self, index, value):
		"""
		allows you to replace the index'th path entry
		"""
		self.__path[index] = xsc.stringFromCode(value)
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
		self.__path[index1:index2] = map(xsc.stringFromCode, sequence)
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
			self.__path.append(xsc.stringFromCode(other))
		self.__normalize()

	def insert(self, index, *others):
		"""
		inserts all items in <argref>others</argref> at the position <argref>index</argref> in the path.
		(this is the same as <code><self/>[<argref>index</argref>:<argref>index</argref>] = <argref>others</argref></code>)
		"""
		for other in others:
			self.__path.insert(index, xsc.stringFromCode(other))
			index += 1

	def __repr__(self):
		v = []
		if self.scheme:
			v.append("scheme=" + repr(self.scheme))
		if self.server:
			v.append("server=" + repr(self.server))
		if self.port:
			v.append("port=" + repr(self.port))
		if self.__path:
			v.append("path=" + repr(self.__path))
		if self.file:
			v.append("file=" + repr(self.file))
		if self.ext:
			v.append("ext=" + repr(self.ext))
		if self.parameters:
			v.append("parameters=" + repr(self.parameters))
		if self.query:
			v.append("query=" + repr(self.query))
		if self.fragment:
			v.append("fragment=" + repr(self.fragment))
		return "URL(%s)" % ", ".join(v)

	def __str__(self):
		return self.__asString(1)

	def asString(self):
		return self.__asString(0)

	def __add__(self, other):
		"""
		joins two URLs together. When the second URL is
		absolute (i.e. contains a scheme other than "server"
		or "", you'll get a copy of the second URL.
		"""
		return self.clone().__join(URL(other))

	def __radd__(self, other):
		return URL(other).__join(self.clone())

	__radd__.__doc__ = __add__.__doc__

	def clone(self):
		"""
		returns an identical clone of this URL.
		"""
		return URL(scheme = self.scheme, server = self.server, port = self.port, path = self.__path, file = self.file, ext = self.ext, parameters = self.parameters, query = self.query, fragment = self.fragment)

	def isRemote(self):
		if self.scheme == u"":
			return 0
		elif self.scheme == u"server" and self.server == u"localhost":
			return 0
		else:
			return 1

	def relativeTo(self, other):
		"""
		<par nointent>returns <self/> interpreted relative
		to <code>other</code>+<self/>.</par>

		<par>Note that remote URLs won't be modified in any way,
		because although the file you've read might have been
		remote, the parsed XSC file that you output, probably
		isn't. The resulting URL won't have any path markers
		in it.</par>
		"""
		new = other + self
		new.__path = filter(_isNoPathMarker, new.__path)
		if not new.scheme:
			otherpath = filter(_isNoPathMarker, other.__path)
			while len(otherpath) and len(new.__path) and otherpath[0]==new.__path[0]: # throw away identical directories in both paths (we don't have to go up from file and down to path for these identical directories)
				del otherpath[0]
				del new.__path[0]
			new.__path[:0] = [u".."]*len(otherpath) # now for the rest of the path we have to go up from file and down to path (the directories for this are still in path)
			new.scheme = None
		new.__normalize() # Now that the path markers are gone, we try to normalize again
		return new

	def __cmp__(self, other):
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
		scheme = xsc.stringFromCode(scheme)
		server = xsc.stringFromCode(server)
		__path = map(xsc.stringFromCode, path)
		parameters = xsc.stringFromCode(parameters)
		query = xsc.stringFromCode(query)
		fragment = xsc.stringFromCode(fragment)
		if scheme == u"": # do we have a local file?
			if len(path):
				if path[0] == u"/": # this is a server relative URL
					path = path[1:] # drop the empty string in front of the first "/" ...
					scheme = u"server" # ... and use a special scheme for that
		elif scheme in (u"ftp", u"http", u"https"):
			if len(path):
				path = path[1:] # the path from urlparse started with "/" too
		port = None
		pos = server.rfind(u":")
		if pos != -1:
			port = int(server[pos+1:])
			server = server[:pos]
		path = path.split(u"/")
		file = path[-1]
		path = path[:-1]

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

	def __asString(self, for__str__):
		scheme = self.scheme or u""
		server = self.server or u""
		if self.port:
			server += u":" + str(self.port)
		path = []
		if scheme == u"server":
			scheme = u"" # remove our own private scheme name
			path.append(u"") # make sure that there's a "/" at the start
		for dir in self.__path:
			if for__str__ or not _isPathMarker(dir):
				path.append(dir)
		file = self.file or u""
		if self.ext:
			file += u"." + self.ext
		path.append(file)
		url = urlparse.urlunparse((scheme, server, u"/".join(path), self.parameters or u"", self.query or u"", self.fragment or u""))
		return url

	def __quote(self):
		"""
		encodes the URL with % escapes
		"""
		url = self.asString().encode("utf8")
		v = []
		for c in url:
			if c in self.__safe:
				v.append(c)
			else:
				v.append("%%%02x" % ord(c))
		return "".join(v)

	def __join(self, other):
		if not other.scheme:
			if len(other.__path) and _isPathMarker(other.__path[0]):
				for i in xrange(len(self.__path)-1):
					if _isPathMarker(self.__path[i]) and self.__path[i] == other.__path[0]:
						self.__path[i:] = other.__path
						break
				else:
					self.__path.extend(other.__path)
			else:
				self.__path.extend(other.__path)
			self.file       = other.file
			self.ext        = other.ext
			self.parameters = other.parameters
			self.query      = other.query
			self.fragment   = other.fragment
		elif other.scheme == u"server":
			if not self.scheme:
				self.scheme = u"server"
			self.__path     = other.__path[:]
			self.file       = other.file
			self.ext        = other.ext
			self.parameters = other.parameters
			self.query      = other.query
			self.fragment   = other.fragment
		else: # URL to be joined is absolute, so we return the second URL
			return other
		self.__normalize()
		return self

	def __normalize(self):
		"""
		normalize the path by removing combinations of down/up
		and removing duplicate path markers.
		"""

		# remove duplicate path markers: first find the position of all names
		dirs = {}
		lenpath = len(self.__path)
		for i in xrange(lenpath):
			dir = self.__path[i]
			try:
				dirs[dir].append(i)
			except KeyError:
				dirs[dir] = [i]

		# if there are duplicate path markers only keep the last one
		path = [None] * lenpath
		for name in dirs.keys():
			if _isPathMarker(name):
				path[max(dirs[name])] = name
			else:
				for i in dirs[name]:
					path[i] = name

		# put back together what we have

		# remove "foo/.." combinations
		for i in xrange(len(path)):
			if path[i]==u".." and i>0 and path[i-1]!=u".." and _isNoPathMarker(path[i-1]): # found a down/up
				path[i-1] = None # remove both directory names
				path[i] = None
		self.__path = [ x for x in path if x is not None ]
