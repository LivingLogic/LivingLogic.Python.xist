#! /usr/bin/env python

"""URL class.

This module contains only one useful variable: the URL class
"""

__version__ = "$Revision$"[11:-2]
# $Source$

import types
import urlparse
import urllib

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
	def __init__(self,url = None,scheme = None,server = None,port = None,path = None,file = None,ext = None,parameters = None,query = None,fragment = None):
		# initialize the defaults
		self.scheme = self.server = self.port = None
		self.__path = []
		self.file = self.ext = self.parameters = self.query = self.fragment = None
		if url is None:
			pass
		elif type(url) is types.StringType:
			self.__fromString(url)
		elif isinstance(url,URL):
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
			self.__path = path[:]
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

	def __getitem__(self,index):
		"""
		returns the index'th path entry
		"""
		return self.__path[index]

	def __setitem__(self,index,value):
		"""
		allows you to replace the index'th path entry
		"""
		self.__path[index] = value
		self.__normalize()

	def __delitem__(self,index):
		"""
		removes the index'th path entry
		"""
		del self.__path[index]
		self.__normalize()

	def __getslice__(self,index1,index2):
		"""
		returns a slice of the path
		"""
		return self.__path[index1:index2]

	def __setslice__(self,index1,index2,sequence):
		"""
		replaces a slice of the path
		"""
		self.__path[index1:index2] = sequence
		self.__normalize()

	def __delslice__(self,index1,index2):
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

	def append(self,*others):
		"""
		appends all directory names in <argref>others</argref> to the path.
		"""
		for other in others:
			self.__path.append(other)
		self.__normalize()

	def insert(self,index,*others):
		"""
		inserts all items in <argref>others</argref> at the position <argref>index</argref> in the path.
		(this is the same as <code><self/>[<argref>index</argref>:<argref>index</argref>] = <argref>others</argref></code>)
		"""
		for other in others:
			self.__path.insert(index,other)
			index = index + 1

	def isPathMarker(self,dir):
		"""
		isPathMarker(self,dir) -> bool
		
		returns if the directory name dir is a path marker.
		"""
		return dir[0] == "*"

	def isNoPathMarker(self,dir):
		"""
		isNoPathMarker(self,dir) -> bool
		
		returns not isPathMarker(self,dir)
		"""
		return not self.isPathMarker(dir)

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
		return "URL(" + ", ".join(v) + ")"

	def __str__(self):
		return self.__asString(1)

	def asString(self):
		return self.__asString(0)

	def __add__(self,other):
		"""
		joins two URLs together. When the second URL is
		absolute (i.e. contains a scheme other than "server"
		or "", you'll get a copy of the second URL.
		"""
		return self.clone().__join(URL(other))

	def __radd__(self,other):
		return URL(other).__join(self.clone())

	__radd__.__doc__ = __add__.__doc__

	def clone(self):
		"""
		returns an identical clone of this URL.
		"""
		return URL(scheme = self.scheme,server = self.server,port = self.port,path = self.__path,file = self.file,ext = self.ext,parameters = self.parameters,query = self.query,fragment = self.fragment)

	def isRemote(self):
		if self.scheme == "":
			return 0
		elif self.scheme == "server" and self.server == "localhost":
			return 0
		else:
			return 1

	def relativeTo(self,other):
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
		new.__path = filter(new.isNoPathMarker,new.__path)
		if not new.scheme:
			otherpath = filter(other.isNoPathMarker,other.__path)
			while len(otherpath) and len(new.__path) and otherpath[0]==new.__path[0]: # throw away identical directories in both paths (we don't have to go up from file and down to path for these identical directories)
				del otherpath[0]
				del new.__path[0]
			new.__path[:0] = [".."]*len(otherpath) # now for the rest of the path we have to go up from file and down to path (the directories for this are still in path)
			new.scheme = None
		new.__normalize() # Now that the path markers are gone, we try to normalize again
		return new

	def __cmp__(self,other):
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
		return cmp(scheme1,scheme2) or cmp(server1,server2) or cmp(self.port,other.port) or cmp(self.__path,other.__path) or cmp(self.file,other.file) or cmp(self.ext,other.ext) or cmp(self.parameters,other.parameters) or cmp(self.query,other.query) or cmp(self.fragment,other.fragment)

	def open(self):
		return urllib.urlopen(self.asString())

	def read(self):
		return self.open().read()

	def readlines(self):
		return self.open().readlines()

	def __fromString(self,url):
		(self.scheme,self.server,self.__path,self.parameters,self.query,self.fragment) = urlparse.urlparse(url)
		if self.scheme == "": # do we have a local file?
			if len(self.__path):
				if self.__path[0] == "/": # this is a server relative URL
					self.__path = self.__path[1:] # drop the empty string in front of the first "/" ...
					self.scheme = "server" # ... and use a special scheme for that
		elif self.scheme in ( "ftp" , "http" , "https" ):
			if len(self.__path):
				self.__path = self.__path[1:] # the path from urlparse started with "/" too
		pos = self.server.rfind(":")
		if pos != -1:
			self.port = int(self.server[pos+1:])
			self.server = self.server[:pos]
		self.__path = self.__path.split("/")
		self.file = self.__path[-1]
		self.__path = self.__path[:-1]

		if self.scheme in [ "ftp" , "http" , "https" , "server", "" ]:
			pos = self.file.rfind(".")
			if pos != -1:
				self.ext = self.file[pos+1:]
				self.file = self.file[:pos]

		self.scheme = self.scheme or None
		self.server = self.server or None
		self.file = self.file or None
		self.parameters = self.parameters or None
		self.query = self.query or None
		self.fragment = self.fragment or None

	def __asString(self,withPathMarkers):
		scheme = self.scheme or ""
		server = self.server or ""
		if self.port:
			server = server + ":" + str(self.port)
		path = []
		if scheme == "server":
			scheme = "" # remove our own private scheme name
			path.append("") # make sure that there's a "/" at the start
		for dir in self.__path:
			if withPathMarkers or not self.isPathMarker(dir):
				path.append(dir)
		file = self.file or ""
		if self.ext:
			file = file + "." + self.ext
		path.append(file)
		return urlparse.urlunparse((scheme,server,"/".join(path),self.parameters or "",self.query or "",self.fragment or ""))

	def __join(self,other):
		if not other.scheme:
			if len(other.__path) and self.isPathMarker(other.__path[0]):
				for i in xrange(len(self.__path)-1):
					if self.isPathMarker(self.__path[i]) and self.__path[i] == other.__path[0]:
						self.__path[i:] = other.__path
						break
				else:
					self.__path.extend(other.__path)
			else:
				self.__path.extend(other.__path)
			self.file       = other.file or self.file
			self.ext        = other.ext or self.ext
			self.parameters = other.parameters
			self.query      = other.query
			self.fragment   = other.fragment
		elif other.scheme == "server":
			if not self.scheme:
				self.scheme = "server"
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
				dirs[dir] = [ i ]

		# if there are duplicate path markers only keep the last one
		path = [ None ] * lenpath
		for name in dirs.keys():
			if self.isPathMarker(name):
				path[max(dirs[name])] = name
			else:
				for i in dirs[name]:
					path[i] = name

		# put back together what we have

		# remove "foo/.." combinations
		for i in xrange(len(path)):
			if path[i]==".." and i>0 and path[i-1]!=".." and self.isNoPathMarker(path[i-1]): # found a down/up
				path[i-1] = None # remove both directory names
				path[i] = None
		self.__path = filter(lambda x: x is not None,path)
