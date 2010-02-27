#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright 1999-2010 by LivingLogic AG, Bayreuth/Germany.
## Copyright 1999-2010 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/__init__.py for the license


"""
:mod:`ll.url` contains an :rfc:`2396` compliant implementation of URLs and
classes for accessing resource metadata as well as file like classes for
reading and writing resource data.

These three levels of functionality are implemented in three classes:

	:class:`URL`
		:class:`URL` objects are the names of resources and can be used and
		modified, regardless of the fact whether these resources actually exits.
		:class:`URL` objects never hits the hard drive or the net.

	:class:`Connection`
		:class:`Connection` objects contain functionality that accesses and
		changes file metadata (like last modified date, permission bits,
		directory structure etc.). A connection object can be created by calling
		the :meth:`connect` method on a :class:`URL` object.

	:class:`Resource`
		:class:`Resource` objects are file like objects that work with the actual
		bytes that make up the file data. This functionality lives in the
		:class:`Resource` class and its subclasses. Creating a resource is done
		by calling the :meth:`open` method on a :class:`Connection` or a
		:class:`URL`.
"""


import sys, os, urllib, urllib2, types, mimetypes, mimetools, cStringIO, warnings
import datetime, cgi, fnmatch, cPickle, errno, threading

try:
	from email import utils as emutils
except ImportError:
	from email import Utils as emutils

# don't fail when :mod:`pwd` or :mod:`grp` can't be imported, because if this
# doesn't work, we're probably on Windows and :func:`os.chown` won't work anyway.
try:
	import pwd, grp
except ImportError:
	pass

try:
	import py
except ImportError:
	py = None

try:
	import Image
except ImportError:
	pass

try:
	import astyle
except ImportError:
	from ll import astyle

from ll import misc


__docformat__ = "reStructuredText"


os.stat_float_times(True)


def mime2dt(s):
	return datetime.datetime(*emutils.parsedate(s)[:7])


weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
monthname = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def httpdate(dt):
	"""
	Return a string suitable for a "Last-Modified" and "Expires" header.
	
	:var:`dt` is a :class:`datetime.datetime` object in UTC.
	"""
	return "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (weekdayname[dt.weekday()], dt.day, monthname[dt.month], dt.year, dt.hour, dt.minute, dt.second)


try:
	from _url import escape as _escape, unescape as _unescape, normalizepath as _normalizepath
except ImportError:
	def _normalizepath(path_segments):
		new_path_segments = []
		l = len(path_segments)
		for i in xrange(l):
			segment = path_segments[i]
			if segment==(".",) or segment==("",):
				if i==l-1:
					new_path_segments.append(("",))
			elif segment==("..",) and len(new_path_segments) and new_path_segments[-1]!=("..",):
				new_path_segments.pop()
				if i==l-1:
					new_path_segments.append(("",))
			else:
				new_path_segments.append(segment)
		return new_path_segments

	def _escape(s, safe=""):
		if not safe:
			safe = "".join(chr(c) for c in xrange(128))
		return urllib.quote_plus(s.encode("utf-8"), safe)

	def _unescape(s):
		s = urllib.unquote_plus(s)
		try:
			return s.decode("utf-8")
		except UnicodeError:
			return s.decode("latin-1")


alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphanum = alpha + "0123456789"
mark = "-_.!~*'()"
additionalsafe = "[]"
safe = alphanum + mark + additionalsafe
pathsafe = safe + ":@&=+$," + "|" # add "|" for Windows paths
querysafe = alphanum
fragsafe = alphanum

schemecharfirst = alpha
schemechar = alphanum + "+-."


def _urlencode(query_parts):
	if query_parts is not None:
		res = []
		items = query_parts.items()
		# generate a canonical order for the names
		items.sort()
		for (name, values) in items:
			if not isinstance(values, (list, tuple)):
				values = (values,)
			else:
				# generate a canonical order for the values
				values.sort()
			for value in values:
				res.append("%s=%s" % (_escape(name, querysafe), _escape(value, querysafe)))
		return "&".join(res)
	else:
		return None


class Context(object):
	"""
	Calling :meth:`URL.open` or :meth:`URL.connect` :class:`Connection` object.
	To avoid constantly creating new connections you can pass a :class:`Context`
	object to those methods. Connections will be stored in the :class:`Context`
	object and will be reused by those methods.

	A :class:`Context` object can also be used as a context manager
	(see :pep:`346` for more info). This context object will be used for all
	:meth:`open` and :meth:`connect` calls inside the ``with`` block. (Note that
	after the end of the ``with`` block, all connections will be closed.)
	"""
	def __init__(self):
		self.schemes = {}

	def closeall(self):
		"""
		Close and drop all connections in this context.
		"""
		for scheme in self.schemes:
			schemereg[scheme].closeall(self)
		self.schemes = {}

	def __enter__(self):
		self.prev = threadlocalcontext.context
		threadlocalcontext.context = self

	def __exit__(self, type, value, traceback):
		threadlocalcontext.context = self.prev
		del self.prev
		self.closeall()


class ThreadLocalContext(threading.local):
	context = Context()

threadlocalcontext = ThreadLocalContext()


def getcontext(context):
	if context is None:
		return threadlocalcontext.context
	return context


class Connection(object):
	"""
	A :class:`Connection` object is used for accessing and modifying the
	metadata associated with a file. It it created by calling the
	:meth:`connect` method on a :class:`URL` object.
	"""

	@misc.notimplemented
	def stat(self, url):
		"""
		Return the result of a :func:`stat` call on the file :var:`url`.
		"""

	@misc.notimplemented
	def lstat(self, url):
		"""
		Return the result of a :func:`stat` call on the file :var:`url`. Like
		:meth:`stat`, but does not follow symbolic links.
		"""

	@misc.notimplemented
	def chmod(self, url, mode):
		"""
		Set the access mode of the file :var:`url` to :var:`mode`.
		"""

	@misc.notimplemented
	def chown(self, url, owner=None, group=None):
		"""
		Change the owner and/or group of the file :var:`url`.
		"""

	@misc.notimplemented
	def lchown(self, url, owner=None, group=None):
		"""
		Change the owner and/or group of the file :var:`url`
		(ignoring symbolic links).
		"""

	@misc.notimplemented
	def uid(self, url):
		"""
		Return the user id of the owner of the file :var:`url`.
		"""

	@misc.notimplemented
	def gid(self, url):
		"""
		Return the group id the file :var:`url` belongs to.
		"""

	@misc.notimplemented
	def owner(self, url):
		"""
		Return the name of the owner of the file :var:`url`.
		"""

	@misc.notimplemented
	def group(self, url):
		"""
		Return the name of the group the file :var:`url` belongs to.
		"""

	def mimetype(self, url):
		"""
		Return the mimetype of the file :var:`url`.
		"""
		name = self._url2filename(url)
		mimetype = mimetypes.guess_type(name)[0]
		return mimetype or "application/octet-stream"

	@misc.notimplemented
	def exists(self, url):
		"""
		Test whether the file :var:`url` exists.
		"""

	@misc.notimplemented
	def isfile(self, url):
		"""
		Test whether the resource :var:`url` is a file.
		"""

	@misc.notimplemented
	def isdir(self, url):
		"""
		Test whether the resource :var:`url` is a directory.
		"""

	@misc.notimplemented
	def islink(self, url):
		"""
		Test whether the resource :var:`url` is a link.
		"""

	@misc.notimplemented
	def ismount(self, url):
		"""
		Test whether the resource :var:`url` is a mount point.
		"""

	@misc.notimplemented
	def access(self, url, mode):
		"""
		Test for access to the file/resource :var:`url`.
		"""

	def size(self, url):
		"""
		Return the size of the file :var:`url`.
		"""
		return self.stat(url).st_size

	def imagesize(self, url):
		"""
		Return the size of the image :var:`url` (if the resource is an image file)
		as a ``(width, height)`` tuple. This requires the PIL__.

		__ http://www.pythonware.com/products/pil/
		"""
		stream = self.open(url, "rb")
		img = Image.open(stream) # Requires PIL
		imagesize = img.size
		stream.close()
		return imagesize

	def cdate(self, url):
		"""
		Return the "metadate change" date of the file/resource :var:`url`
		as a :class:`datetime.datetime` object in UTC.
		"""
		return datetime.datetime.utcfromtimestamp(self.stat(url).st_ctime)

	def adate(self, url):
		"""
		Return the last access date of the file/resource :var:`url` as a
		:class:`datetime.datetime` object in UTC.
		"""
		return datetime.datetime.utcfromtimestamp(self.stat(url).st_atime)

	def mdate(self, url):
		"""
		Return the last modification date of the file/resource :var:`url`
		as a :class:`datetime.datetime` object in UTC.
		"""
		return datetime.datetime.utcfromtimestamp(self.stat(url).st_mtime)

	def resheaders(self, url):
		"""
		Return the MIME headers for the file/resource :var:`url`.
		"""
		return mimetools.Message(
			cStringIO.StringIO(
				"Content-Type: %s\nContent-Length: %d\nLast-modified: %s\n" %
				(self.mimetype(url), self.size(url), httpdate(self.mdate(url)))
			)
		)

	@misc.notimplemented
	def remove(self, url):
		"""
		Remove the file :var:`url`.
		"""

	@misc.notimplemented
	def rmdir(self, url):
		"""
		Remove the directory :var:`url`.
		"""

	@misc.notimplemented
	def rename(self, url, target):
		"""
		Renames :var:`url` to :var:`target`. This might not work if :var:`target`
		has a different scheme than :var:`url` (or is on a different server).
		"""

	@misc.notimplemented
	def link(self, url, target):
		"""
		Create a hard link from :var:`url` to :var:`target`. This will not work
		if :var:`target` has a different scheme than :var:`url` (or is on a
		different server).
		"""

	@misc.notimplemented
	def symlink(self, url, target):
		"""
		Create a symbolic link from :var:`url` to :var:`target`. This will not
		work if :var:`target` has a different scheme than :var:`url` (or is on a
		different server).
		"""

	@misc.notimplemented
	def chdir(self, url):
		"""
		Change the current directory to :var:`url`.
		"""
		os.chdir(self.name)

	@misc.notimplemented
	def mkdir(self, url, mode=0777):
		"""
		Create the directory :var:`url`.
		"""
		
	@misc.notimplemented
	def makedirs(self, url, mode=0777):
		"""
		Create the directory :var:`url` and all intermediate ones.
		"""

	@misc.notimplemented
	def listdir(self, url, pattern=None):
		"""
		Return a list of items in the directory :var:`url`. The elements of the
		list are :class:`URL` objects relative to :var:`url`. With the optional
		:var:`pattern` argument, this only lists items whose names match the
		given pattern.
		"""

	@misc.notimplemented
	def files(self, url, pattern=None):
		"""
		Return a list of files in the directory :var:`url`. The elements of the
		list are :class:`URL` objects relative to :var:`url`. With the optional
		:var:`pattern` argument, this only lists items whose names match the
		given pattern.
		"""

	@misc.notimplemented
	def dirs(self, url, pattern=None):
		"""
		Return a list of directories in the directory :var:`url`. The elements
		of the list are :class:`URL` objects relative to :var:`url`. With the
		optional :var:`pattern` argument, this only lists items whose names match
		the given pattern.
		"""

	@misc.notimplemented
	def walk(self, url, pattern=None):
		"""
		Return a recursive iterator over files and subdirectories. The iterator
		yields :class:`URL` objects naming each child URL of the directory
		:var:`url` and its descendants relative to :var:`url`. This performs
		a depth-first traversal, returning each directory before all its children.
		With the optional :var:`pattern` argument, only yield items whose
		names match the given pattern.
		"""

	@misc.notimplemented
	def walkfiles(self, url, pattern=None):
		"""
		Return a recursive iterator over files in the directory :var:`url`. With
		the optional :var:`pattern` argument, only yield files whose names match
		the given pattern.
		"""

	@misc.notimplemented
	def walkdirs(self, url, pattern=None):
		"""
		Return a recursive iterator over subdirectories in the directory
		:var:`url`. With the optional :var:`pattern` argument, only yield
		directories whose names match the given pattern.
		"""

	@misc.notimplemented
	def open(self, url, *args, **kwargs):
		"""
		Open :var:`url` for reading or writing. :meth:`open` returns a
		:class:`Resource` object.

		Which additional parameters are supported depends on the actual
		resource created. Some common parameters are:

			:var:`mode` : string
				A string indicating how the file is to be opened (just like the
				mode argument for the builtin :func:`open` (e.g. ``"rb"`` or
				``"wb"``).

			:var:`headers` : mapping
				Additional headers to use for an HTTP request.

			:var:`data` : byte string
				Request body to use for an HTTP POST request.

			:var:`remotepython` : string
				Name of the Python interpreter to use on the remote side (used by
				``ssh`` URLs)

			:var:`ssh_config` : string
				SSH configuration file (used by ``ssh`` URLs)
		"""


class LocalConnection(Connection):
	def _url2filename(self, url):
		return os.path.expanduser(url.local())

	def stat(self, url):
		return os.stat(self._url2filename(url))

	def lstat(self, url):
		return os.lstat(self._url2filename(url))

	def chmod(self, url, mode):
		name = self._url2filename(url)
		os.chmod(name, mode)

	def _chown(self, func, url, owner, group):
		name = self._url2filename(url)
		if owner is not None or group is not None:
			if owner is None or group is None:
				stat = os.stat(name)
			if owner is None:
				owner = stat.st_uid
			elif isinstance(owner, basestring):
				owner = pwd.getpwnam(owner)[2]
			if group is None:
				group = stat.st_gid
			elif isinstance(group, basestring):
				group = grp.getgrnam(group)[2]
			func(name, owner, group)

	def chown(self, url, owner=None, group=None):
		self._chown(os.chown, url, owner, group)

	def lchown(self, url, owner=None, group=None):
		self._chown(os.lchown, url, owner, group)

	def chdir(self, url):
		os.chdir(self._url2filename(url))

	def mkdir(self, url, mode=0777):
		os.mkdir(self._url2filename(url), mode)

	def makedirs(self, url, mode=0777):
		os.makedirs(self._url2filename(url), mode)

	def uid(self, url):
		return self.stat(url).st_uid

	def gid(self, url):
		return self.stat(url).st_gid

	def owner(self, url):
		return pwd.getpwuid(self.uid(url))[0]

	def group(self, url):
		return grp.getgrgid(self.gid(url))[0]

	def exists(self, url):
		return os.path.exists(self._url2filename(url))

	def isfile(self, url):
		return os.path.isfile(self._url2filename(url))

	def isdir(self, url):
		return os.path.isdir(self._url2filename(url))

	def islink(self, url):
		return os.path.islink(self._url2filename(url))

	def ismount(self, url):
		return os.path.ismount(self._url2filename(url))

	def access(self, url, mode):
		return os.access(self._url2filename(url), mode)

	def remove(self, url):
		return os.remove(self._url2filename(url))

	def rmdir(self, url):
		return os.rmdir(self._url2filename(url))

	def rename(self, url, target):
		name = self._url2filename(url)
		if not isinstance(target, URL):
			target = URL(target)
		targetname = self._url2filename(target)
		os.rename(name, target)

	def link(self, url, target):
		name = self._url2filename(url)
		if not isinstance(target, URL):
			target = URL(target)
		target = self._url2filename(target)
		os.link(name, target)

	def symlink(self, url, target):
		name = self._url2filename(url)
		if not isinstance(target, URL):
			target = URL(target)
		target = self._url2filename(target)
		os.symlink(name, target)

	def listdir(self, url, pattern=None):
		name = self._url2filename(url)
		result = []
		for childname in os.listdir(name):
			if pattern is None or fnmatch.fnmatch(childname, pattern):
				if os.path.isdir(os.path.join(name, childname)):
					result.append(Dir(childname, scheme=url.scheme))
				else:
					result.append(File(childname, scheme=url.scheme))
		return result

	def files(self, url, pattern=None):
		name = self._url2filename(url)
		result = []
		for childname in os.listdir(name):
			if pattern is None or fnmatch.fnmatch(childname, pattern):
				if os.path.isfile(os.path.join(name, childname)):
					result.append(File(childname, scheme=url.scheme))
		return result

	def dirs(self, url, pattern=None):
		name = self._url2filename(url)
		result = []
		for childname in os.listdir(name):
			if pattern is None or fnmatch.fnmatch(childname, pattern):
				if os.path.isdir(os.path.join(name, childname)):
					result.append(Dir(childname, scheme=url.scheme))
		return result

	def _walk(self, base, name, pattern, which):
		if name:
			fullname = os.path.join(base, name)
		else:
			fullname = base
		for childname in os.listdir(fullname):
			ful4childname = os.path.join(fullname, childname)
			relchildname = os.path.join(name, childname)
			isdir = os.path.isdir(ful4childname)
			if (pattern is None or fnmatch.fnmatch(childname, pattern)) and which[isdir]:
				url = urllib.pathname2url(relchildname)
				if isdir:
					url += "/"
				yield URL(url)
			if isdir:
				for subchild in self._walk(base, relchildname, pattern, which):
					yield subchild

	def walk(self, url, pattern=None):
		return self._walk(self._url2filename(url), "", pattern, (True, True))

	def walkfiles(self, url, pattern=None):
		return self._walk(self._url2filename(url), "", pattern, (True, False))

	def walkdirs(self, url, pattern=None):
		return self._walk(self._url2filename(url), "", pattern, (False, True))

	def open(self, url, mode="rb"):
		return FileResource(url, mode)


if py is not None:
	class SshConnection(Connection):
		remote_code = py.code.Source("""
			import os, urllib, cPickle, fnmatch

			os.stat_float_times(True)
			files = {}
			iterators = {}

			def ownergroup(filename, owner=None, group=None):
				if owner is not None or group is not None:
					if owner is None or group is None:
						if isinstance(filename, basestring):
							stat = os.stat(filename)
						else:
							stat = os.fstat(files[filename].fileno())
					if owner is None:
						owner = stat.st_uid
					elif isinstance(owner, basestring):
						import pwd
						owner = pwd.getpwnam(owner)[2]

					if group is None:
						group = stat.st_gid
					elif isinstance(group, basestring):
						import grp
						group = grp.getgrnam(group)[2]
				return (owner, group)

			def _walk(base, name, pattern, which):
				if name:
					fullname = os.path.join(base, name)
				else:
					fullname = base
				for childname in os.listdir(fullname):
					ful4childname = os.path.join(fullname, childname)
					relchildname = os.path.join(name, childname)
					isdir = os.path.isdir(ful4childname)
					if (pattern is None or fnmatch.fnmatch(childname, pattern)) and which[isdir]:
						url = urllib.pathname2url(relchildname)
						if isdir:
							url += "/"
						yield url
					if isdir:
						for subchild in _walk(base, relchildname, pattern, which):
							yield subchild
		
			def walk(filename, pattern=None):
				return _walk(filename, "", pattern, (True, True))

			def walkfiles(filename, pattern=None):
				return _walk(filename, "", pattern, (True, False))

			def walkdirs(filename, pattern=None):
				return _walk(filename, "", pattern, (False, True))

			while True:
				(filename, cmdname, args, kwargs) = channel.receive()
				if isinstance(filename, basestring):
					filename = os.path.expanduser(urllib.url2pathname(filename))
				data = None
				try:
					if cmdname == "open":
						try:
							stream = open(filename, *args, **kwargs)
						except IOError, exc:
							if "w" not in args[0] or exc[0] != 2: # didn't work for some other reason than a non existing directory
								raise
							(splitpath, splitname) = os.path.split(filename)
							if splitpath:
								os.makedirs(splitpath)
								stream = open(filename, *args, **kwargs)
							else:
								raise # we don't have a directory to make so pass the error on
						data = id(stream)
						files[data] = stream
					elif cmdname == "stat":
						if isinstance(filename, basestring):
							data = tuple(os.stat(filename))
						else:
							data = tuple(os.fstat(files[filename].fileno()))
					elif cmdname == "lstat":
						data = os.lstat(filename)
					elif cmdname == "close":
						try:
							stream = files[filename]
						except KeyError:
							pass
						else:
							stream.close()
							del files[filename]
					elif cmdname == "chmod":
						data = os.chmod(filename, *args, **kwargs)
					elif cmdname == "chown":
						(owner, group) = ownergroup(filename, *args, **kwargs)
						if owner is not None:
							data = os.chown(filename, owner, group)
					elif cmdname == "lchown":
						(owner, group) = ownergroup(filename, *args, **kwargs)
						if owner is not None:
							data = os.lchown(filename, owner, group)
					elif cmdname == "uid":
						stat = os.stat(filename)
						data = stat.st_uid
					elif cmdname == "gid":
						stat = os.stat(filename)
						data = stat.st_gid
					elif cmdname == "owner":
						import pwd
						stat = os.stat(filename)
						data = pwd.getpwuid(stat.st_uid)[0]
					elif cmdname == "group":
						import grp
						stat = os.stat(filename)
						data = grp.getgrgid(stat.st_gid)[0]
					elif cmdname == "exists":
						data = os.path.exists(filename)
					elif cmdname == "isfile":
						data = os.path.isfile(filename)
					elif cmdname == "isdir":
						data = os.path.isdir(filename)
					elif cmdname == "islink":
						data = os.path.islink(filename)
					elif cmdname == "ismount":
						data = os.path.ismount(filename)
					elif cmdname == "access":
						data = os.access(filename, *args, **kwargs)
					elif cmdname == "remove":
						data = os.remove(filename)
					elif cmdname == "rmdir":
						data = os.rmdir(filename)
					elif cmdname == "rename":
						data = os.rename(filename, os.path.expanduser(args[0]))
					elif cmdname == "link":
						data = os.link(filename, os.path.expanduser(args[0]))
					elif cmdname == "symlink":
						data = os.symlink(filename, os.path.expanduser(args[0]))
					elif cmdname == "chdir":
						data = os.chdir(filename)
					elif cmdname == "mkdir":
						data = os.mkdir(filename)
					elif cmdname == "makedirs":
						data = os.makedirs(filename)
					elif cmdname == "makefifo":
						data = os.makefifo(filename)
					elif cmdname == "listdir":
						data = []
						for f in os.listdir(filename):
							if args[0] is None or fnmatch.fnmatch(f, args[0]):
								data.append((os.path.isdir(os.path.join(filename, f)), f))
					elif cmdname == "files":
						data = []
						for f in os.listdir(filename):
							if args[0] is None or fnmatch.fnmatch(f, args[0]):
								if os.path.isfile(os.path.join(filename, f)):
									data.append(f)
					elif cmdname == "dirs":
						data = []
						for f in os.listdir(filename):
							if args[0] is None or fnmatch.fnmatch(f, args[0]):
								if os.path.isdir(os.path.join(filename, f)):
									data.append(f)
					elif cmdname == "walk":
						iterator = walk(filename, *args, **kwargs)
						data = id(iterator)
						iterators[data] = iterator
					elif cmdname == "walkfiles":
						iterator = walkfiles(filename, *args, **kwargs)
						data = id(iterator)
						iterators[data] = iterator
					elif cmdname == "walkdirs":
						iterator = walkdirs(filename, *args, **kwargs)
						data = id(iterator)
						iterators[data] = iterator
					elif cmdname == "iteratornext":
						try:
							data = iterators[filename].next()
						except StopIteration:
							del iterators[filename]
							raise
					else:
						data = getattr(files[filename], cmdname)
						data = data(*args, **kwargs)
				except Exception, exc:
					if exc.__class__.__module__ != "exceptions":
						raise
					channel.send((True, cPickle.dumps(exc)))
				else:
					channel.send((False, data))
		""")
		def __init__(self, context, server, remotepython="python", ssh_config=None):
			# We don't have to store the context (this avoids cycles)
			self.server = server
			gateway = py.execnet.SshGateway(server, remotepython=remotepython, ssh_config=ssh_config)
			self._channel = gateway.remote_exec(self.remote_code)

		def close(self):
			if not self._channel.isclosed():
				self._channel.close()
				self._channel.gateway.exit()
				self._channel.gateway.join()

		def _url2filename(self, url):
			if url.scheme != "ssh":
				raise ValueError("URL %r is not an ssh URL" % url)
			filename = str(url.path)
			if filename.startswith("/~"):
				filename = filename[1:]
			return filename

		def _send(self, filename, cmd, *args, **kwargs):
			self._channel.send((filename, cmd, args, kwargs))
			(isexc, data) = self._channel.receive()
			if isexc:
				raise cPickle.loads(data)
			else:
				return data

		def stat(self, url):
			filename = self._url2filename(url)
			data = self._send(filename, "stat")
			return os.stat_result(data) # channel returned a tuple => wrap it

		def lstat(self):
			filename = self._url2filename(url)
			data = self._send(filename, "lstat")
			return os.stat_result(data) # channel returned a tuple => wrap it

		def chmod(self, url, mode):
			return self._send(self._url2filename(url), "chmod", mode)

		def chown(self, url, owner=None, group=None):
			return self._send(self._url2filename(url), "chown", owner, group)

		def lchown(self, url, owner=None, group=None):
			return self._send(self._url2filename(url), "lchown", owner, group)

		def chdir(self, url):
			return self._send(self._url2filename(url), "chdir")

		def mkdir(self, url, mode=0777):
			return self._send(self._url2filename(url), "mkdir", mode)

		def makedirs(self, url, mode=0777):
			return self._send(self._url2filename(url), "makedirs", mode)

		def uid(self, url):
			return self._send(self._url2filename(url), "uid")

		def gid(self, url):
			return self._send(self._url2filename(url), "gid")

		def owner(self, url):
			return self._send(self._url2filename(url), "owner")

		def group(self, url):
			return self._send(self._url2filename(url), "group")

		def exists(self, url):
			return self._send(self._url2filename(url), "exists")

		def isfile(self, url):
			return self._send(self._url2filename(url), "isfile")

		def isdir(self, url):
			return self._send(self._url2filename(url), "isdir")

		def islink(self, url):
			return self._send(self._url2filename(url), "islink")

		def ismount(self, url):
			return self._send(self._url2filename(url), "ismount")

		def access(self, url, mode):
			return self._send(self._url2filename(url), "access", mode)

		def remove(self, url):
			return self._send(self._url2filename(url), "remove")

		def rmdir(self, url):
			return self._send(self._url2filename(url), "rmdir")

		def _cmdwithtarget(self, cmdname, url, target):
			filename = self._url2filename(url)
			if not isinstance(target, URL):
				target = URL(target)
			targetname = self._url2filename(target)
			if target.server != url.server:
				raise OSError(errno.EXDEV, os.strerror(errno.EXDEV))
			return self._send(filename, cmdname, targetname)

		def rename(self, url, target):
			return self._cmdwithtarget("rename", url, target)

		def link(self, url, target):
			return self._cmdwithtarget("link", url, target)

		def symlink(self, url, target):
			return self._cmdwithtarget("symlink", url, target)

		def listdir(self, url, pattern=None):
			filename = self._url2filename(url)
			result = []
			for (isdir, name) in self._send(filename, "listdir", pattern):
				name = urllib.pathname2url(name)
				if isdir:
					name += "/"
				result.append(URL(name))
			return result

		def files(self, url, pattern=None):
			filename = self._url2filename(url)
			return [URL(urllib.pathname2url(name)) for name in self._send(filename, "files", pattern)]

		def dirs(self, url, pattern=None):
			filename = self._url2filename(url)
			return [URL(urllib.pathname2url(name)+"/") for name in self._send(filename, "dirs", pattern)]

		def walk(self, url, pattern=None):
			filename = self._url2filename(url)
			iterator = self._send(filename, "walk", pattern)
			while True:
				yield URL(self._send(iterator, "iteratornext"))

		def walkfiles(self, url, pattern=None):
			filename = self._url2filename(url)
			iterator = self._send(filename, "walkfiles", pattern)
			while True:
				yield URL(self._send(iterator, "iteratornext"))

		def walkdirs(self, url, pattern=None):
			filename = self._url2filename(url)
			iterator = self._send(filename, "walkdirs", pattern)
			while True:
				yield URL(self._send(iterator, "iteratornext"))

		def open(self, url, mode="rb"):
			return RemoteFileResource(self, url, mode)

		def __repr__(self):
			return "<%s.%s to %r at 0x%x>" % (self.__class__.__module__, self.__class__.__name__, self.server, id(self))


class URLConnection(Connection):
	def mimetype(self, url):
		return url.open().mimetype()

	def size(self, url):
		return url.open().size()

	def imagesize(self, url):
		return url.open().imagesize()

	def mdate(self, url):
		return url.open().mdate()

	def resheaders(self, url):
		return url.open().resheaders()

	def open(self, url, mode="rb", headers=None, data=None):
		if mode != "rb":
			raise NotImplementedError("mode %r not supported" % mode)
		return URLResource(url, headers=headers, data=data)


def here(scheme="file"):
	"""
	Return the current directory as an :class:`URL` object.
	"""
	return Dir(os.getcwd(), scheme)


def home(user="", scheme="file"):
	"""
	Return the home directory of the current user (or the user named :var:`user`,
	if :var:`user` is specified) as an :class:`URL` object::

		>>> url.home()
		URL('file:/home/walter/')
		>>> url.home("andreas")
		URL('file:/home/andreas/')
	"""
	return Dir("~%s" % user, scheme)


def root():
	"""
	Return a blank ``root`` :class:`URL`, i.e. ``URL("root:")``.
	"""
	return URL("root:")


def File(name, scheme="file"):
	"""
	Turn a filename into an :class:`URL` object::

		>>> url.File("a#b")
		URL('file:a%23b')
	"""
	name = urllib.pathname2url(os.path.expanduser(name))
	if name.startswith("///"):
		name = name[2:]
	url = URL(name)
	url.scheme = scheme
	return url


def Dir(name, scheme="file"):
	"""
	Turns a directory name into an :class:`URL` object, just like :func:`File`,
	but ensures that the path is terminated with a ``/``::

		>>> url.Dir("a#b")
		URL('file:a%23b/')
	"""
	name = urllib.pathname2url(os.path.expanduser(name))
	if not name.endswith("/"):
		name += "/"
	if name.startswith("///"):
		name = name[2:]
	url = URL(name)
	url.scheme = scheme
	return url


def Ssh(user, host, path="~/"):
	"""
	Return a ssh :class:`URL` for the user :var:`user` on the host :var:`host`
	with the path :var:`path`.:var:`path` (defaulting to the users home
	directory) must be a path in URL notation (i.e. use ``/`` as directory
	separator)::

		>>> url.Ssh("root", "www.example.com", "~joe/public_html/index.html")
		URL('ssh://root@www.example.com/~joe/public_html/index.html')

	If the path starts with ``~/`` it is relative to this users home directory,
	if it starts with ``~user`` it's relative to the home directory of the user
	``user``. In all othercases the path is considered to be absolute.
	"""
	url = URL()
	url.scheme = "ssh"
	url.userinfo = user
	url.host = host
	if path.startswith("~"):
		path = "/" + path
	url.path = path
	return url


def first(urls):
	"""
	Return the first URL from :var:`urls` that exists as a real file or
	directory. :const:`None` entries in :var:`urls` will be skipped.
	"""
	for url in urls:
		if url is not None:
			if url.exists():
				return url


def firstdir(urls):
	"""
	Return the first URL from :var:`urls` that exists as a real directory.
	:const:`None` entries in :var:`urls` will be skipped.
	"""
	for url in urls:
		if url is not None:
			if url.isdir():
				return url


def firstfile(urls):
	"""
	Return the first URL from :var:`urls` that exists as a real file.
	:const:`None` entries in :var:`urls` will be skipped.
	"""
	for url in urls:
		if url is not None:
			if url.isfile():
				return url


class importcache(dict):
	def remove(self, mod):
		try:
			dict.__delitem__(self, mod.__file__)
		except KeyError:
			pass

importcache = importcache()


def _import(filename):
	(path, name) = os.path.split(filename)
	(name, ext) = os.path.splitext(name)

	if ext != ".py":
		raise ImportError("Can only import .py files, not %s" % ext)

	oldmod = sys.modules.get(name, None) # get any existing module out of the way
	sys.modules[name] = mod = types.ModuleType(name) # create module and make sure it can find itself in sys.module
	mod.__file__ = filename
	execfile(filename, mod.__dict__)
	mod = sys.modules.pop(name) # refetch the module if it has replaced itself with a custom object
	if oldmod is not None: # put old module back
		sys.modules[name] = oldmod
	return mod


class Resource(object):
	"""
	A :class:`Resource` is a base class that provides a file-like interface
	to local and remote files, URLs and other resources.
	
	Attributes
	----------
	Each resource object has the following attributes:

		:attr:`url`
			The URL for which this resource has been opened (i.e.
			``foo.open().url is foo`` if ``foo`` is a :class:`URL` object);

		:attr:`name`
			A string version of :attr:`url`;

		:attr:`closed`
			A :class:`bool` specifying whether the resource has been closed
			(i.e. whether the :meth:`close` method has been called).

	Methods
	-------
	In addition to file methods (like :meth:`read`, :meth:`readlines`,
	:meth:`write` and :meth:`close`) a resource object might provide the
	following methods:

		:meth:`finalurl`
			Return the real URL of the resource (this might be different from the
			:attr:`url` attribute in case of a redirect).

		:meth:`size`
			Return the size of the file/resource.

		:meth:`mdate`
			Return the last modification date of the file/resource as a
			:class:`datetime.datetime` object in UTC.

		:meth:`mimetype`
			Return the mimetype of the file/resource.

		:meth:`imagesize`
			Return the size of the image (if the resource is an image file) as a
			``(width, height)`` tuple. This requires the PIL__.

			__ http://www.pythonware.com/products/pil/
	"""

	def finalurl(self):
		return self.url

	def imagesize(self):
		pos = self.tell()
		self.seek(0)
		img = Image.open(self) # Requires PIL
		imagesize = img.size
		self.seek(pos)
		return imagesize

	def __repr__(self):
		if self.closed:
			state = "closed"
		else:
			state = "open"
		return "<%s %s.%s %r, mode %r at 0x%x>" % (state, self.__class__.__module__, self.__class__.__name__, self.name, self.mode, id(self))


class FileResource(Resource, file):
	"""
	A subclass of :class:`Resource` that handles local files.
	"""
	def __init__(self, url, mode="rb"):
		url = URL(url)
		name = os.path.expanduser(url.local())
		try:
			file.__init__(self, name, mode)
		except IOError, exc:
			if "w" not in mode or exc[0] != 2: # didn't work for some other reason than a non existing directory
				raise
			(splitpath, splitname) = os.path.split(name)
			if splitpath:
				os.makedirs(splitpath)
				file.__init__(self, name, mode)
			else:
				raise # we don't have a directory to make so pass the error on
		self.url = url

	def size(self):
		# Forward to the connection
		return LocalSchemeDefinition._connection.size(self.url)

	def mdate(self):
		# Forward to the connection
		return LocalSchemeDefinition._connection.mdate(self.url)

	def mimetype(self):
		# Forward to the connection
		return LocalSchemeDefinition._connection.mimetype(self.url)


if py is not None:
	class RemoteFileResource(Resource):
		"""
		A subclass of :class:`Resource` that handles remote files (those using
		the ``ssh`` scheme).
		"""
		def __init__(self, connection, url, mode="rb"):
			self.connection = connection
			self.url = URL(url)
			self.mode = mode
			self.closed = False
			filename = self.connection._url2filename(url)
			self.name = str(self.url)
			self.remoteid = self._send(filename, "open", mode)

		def _send(self, filename, cmd, *args, **kwargs):
			if self.closed:
				raise ValueError("I/O operation on closed file")
			return self.connection._send(filename, cmd, *args, **kwargs)
	
		def close(self):
			if not self.closed:
				self._send(self.remoteid, "close")
				self.connection = None # close the channel too as there are no longer any meaningful operations
				self.closed = True

		def read(self, size=-1):
			return self._send(self.remoteid, "read", size)

		def readline(self, size=-1):
			return self._send(self.remoteid, "readline", size)

		def readlines(self, size=-1):
			return self._send(self.remoteid, "readlines", size)

		def __iter__(self):
			return self

		def next(self):
			return self._send(self.remoteid, "next")

		def seek(self, offset, whence=0):
			return self._send(self.remoteid, "seek", offset, whence)

		def tell(self):
			return self._send(self.remoteid, "tell")

		def truncate(self, size=None):
			if size is None:
				return self._send(self.remoteid, "truncate")
			else:
				return self._send(self.remoteid, "truncate", size)

		def write(self, string):
			return self._send(self.remoteid, "write", string)

		def writelines(self, strings):
			return self._send(self.remoteid, "writelines", strings)

		def flush(self):
			return self._send(self.remoteid, "flush")

		def size(self):
			# Forward to the connection
			return self.connection.size(self.url)

		def mdate(self):
			# Forward to the connection
			return self.connection.mdate(self.url)

		def mimetype(self):
			# Forward to the connection
			return self.connection.mimetype(self.url)


class URLResource(Resource):
	"""
	A subclass of :class:`Resource` that handles HTTP, FTP and other URLs
	(i.e. those that are not handled by :class:`FileResource` or
	:class:`RemoteFileResource`.
	"""
	def __init__(self, url, mode="rb", headers=None, data=None):
		if "w" in mode:
			raise ValueError("writing mode %r not supported" % mode)
		self.url = URL(url)
		self.name = str(self.url)
		self.mode = mode
		self.reqheaders = headers
		self.reqdata = data
		self._finalurl = None
		self.closed = False
		self._stream = None
		if data is not None:
			data = urllib.urlencode(data)
		if headers is None:
			headers = {}
		req = urllib2.Request(url=self.name, data=data, headers=headers)
		self._stream = urllib2.urlopen(req)
		self._finalurl = URL(self._stream.url) # Remember the final URL in case of a redirect
		self._resheaders = self._stream.info()
		self._mimetype = None
		self._encoding = None
		contenttype = self._resheaders.getheader("Content-Type")
		if contenttype is not None:
			(mimetype, options) = cgi.parse_header(contenttype)
			self._mimetype = mimetype
			self._encoding = options.get("charset")

		cl = self._resheaders.get("Content-Length")
		if cl:
			cl = int(cl)
		self._size = cl
		lm = self._resheaders.get("Last-Modified")
		if lm is not None:
			lm = mime2dt(lm)
		self._mdate = lm
		self._buffer = cStringIO.StringIO()

	def __getattr__(self, name):
		function = getattr(self._stream, name)
		def call(*args, **kwargs):
			return function(*args, **kwargs)
		return call

	def close(self):
		if not self.closed:
			self._stream.close()
			self._stream = None
			self.closed = True

	def __iter__(self):
		return iter(self._stream)

	def finalurl(self):
		return self._finalurl

	def mimetype(self):
		return self._mimetype

	def resheaders(self):
		return self._resheaders

	def encoding(self):
		return self._encoding

	def mdate(self):
		return self._mdate

	def size(self):
		return self._size

	def read(self, size=-1):
		data = self._stream.read(size)
		self._buffer.write(data)
		return data

	def readline(self, size=-1):
		data = self._stream.readline(size)
		self._buffer.write(data)
		return data

	def resdata(self):
		data = self._stream.read()
		self._buffer.write(data)
		return self._buffer.getvalue()

	def imagesize(self):
		img = Image.open(cStringIO.StringIO(self.resdata())) # Requires PIL
		return img.size

	def __iter__(self):
		while True:
			data = self._stream.readline()
			if not data:
				break
			self._buffer.write(data)
			yield data


class SchemeDefinition(object):
	"""
	A :class:`SchemeDefinition` instance defines the properties of a particular
	URL scheme.
	"""
	_connection = URLConnection()

	def __init__(self, scheme, usehierarchy, useserver, usefrag, islocal=False, isremote=False, defaultport=None):
		"""
		Create a new :class:`SchemeDefinition` instance. Arguments are:

		*	:var:`scheme`: The name of the scheme;

		*	:var:`usehierarchy`: Specifies whether this scheme uses hierarchical
			URLs or opaque URLs (i.e. whether ``hier_part`` or ``opaque_part``
			from the BNF in :rfc:`2396` is used);

		*	:var:`useserver`: Specifies whether this scheme uses an Internet-based
			server :prop:`authority` component or a registry of naming authorities
			(only for hierarchical URLs);

		*	:var:`usefrag`: Specifies whether this scheme uses fragments
			(according to the BNF in :rfc:`2396` every scheme does, but it doesn't
			make sense for e.g. ``"javascript"``, ``"mailto"`` or ``"tel"``);

		*	:var:`islocal`: Specifies whether URLs with this scheme refer to
			local files;

		*	:var:`isremote`: Specifies whether URLs with this scheme refer to
			remote files (there may be schemes which are neither local nor remote,
			e.g. ``"mailto"``);

		*	:var:`defaultport`: The default port for this scheme (only for schemes
			using server based authority).
		"""
		self.scheme = scheme
		self.usehierarchy = usehierarchy
		self.useserver = useserver
		self.usefrag = usefrag
		self.islocal = islocal
		self.isremote = isremote
		self.defaultport = defaultport

	def connect(self, url, context=None, **kwargs):
		"""
		Create a :class:`Connection` for the :class:`URL` :var:`url` (which must
		have :var:`self` as the scheme).
		"""
		return self._connect(url, context, **kwargs)[0]

	def _connect(self, url, context=None, **kwargs):
		# Returns a tuple ``(connect, kwargs)`` (some of the keyword arguments
		# might have been consumed by the connect call, the rest can be passed
		# on the whatever call will be made on the connection itself)
		# We can always use the same connection here, because the connection for
		# local files and real URLs doesn't use any resources.
		# This will be overwritten by :class:`SshSchemeDefinition`
		return (self._connection, kwargs)

	def open(self, *args, **kwargs):
		return URLConnection(*args, **kwargs)

	def closeall(self, context):
		"""
		Close all connections active for this scheme in the context :var:`context`.
		"""

	def __repr__(self):
		return "<%s instance scheme=%r usehierarchy=%r useserver=%r usefrag=%r at 0x%x>" % (self.__class__.__name__, self.scheme, self.usehierarchy, self.useserver, self.usefrag, id(self))


class LocalSchemeDefinition(SchemeDefinition):
	# Use a different connection than the base class (but still one single connection for all URLs)
	_connection = LocalConnection()

	def open(self, *args, **kwargs):
		return FileResource(*args, **kwargs)


class SshSchemeDefinition(SchemeDefinition):
	def _connect(self, url, context=None, **kwargs):
		if "remotepython" in kwargs or "ssh_config" in kwargs:
			kwargs = kwargs.copy()
			remotepython = kwargs.pop("remotepython", "python")
			ssh_config = kwargs.pop("ssh_config", None)
		else:
			remotepython = "python"
			ssh_config = None
			
		context = getcontext(context)
		if context is threadlocalcontext.__class__.context:
			raise ValueError("ssh URLs need a custom context")
		# Use one :class:`SshConnection` for each user/host/remotepython combination
		server = url.server
		try:
			connections = context.schemes["ssh"]
		except KeyError:
			connections = context.schemes["ssh"] = {}
		try:
			connection = connections[(server, remotepython)]
		except KeyError:
			connection = connections[(server, remotepython)] = SshConnection(context, server, remotepython, ssh_config)
		return (connection, kwargs)

	def open(self, url, mode="rb", context=None, remotepython="python", ssh_config=None):
		(connection, kwargs) = self._connect(url, context, remotepython=remotepython, ssh_config=ssh_config)
		return RemoteFileResource(connection, url, mode, **kwargs)

	def closeall(self, context):
		for connection in context.schemes["ssh"].itervalues():
			connection.close()


schemereg = {
	"http": SchemeDefinition("http", usehierarchy=True, useserver=True, usefrag=True, isremote=True, defaultport=80),
	"https": SchemeDefinition("https", usehierarchy=True, useserver=True, usefrag=True, isremote=True, defaultport=443),
	"ftp": SchemeDefinition("ftp", usehierarchy=True, useserver=True, usefrag=True, isremote=True, defaultport=21),
	"file": LocalSchemeDefinition("file", usehierarchy=True, useserver=False, usefrag=True, islocal=True),
	"root": LocalSchemeDefinition("root", usehierarchy=True, useserver=False, usefrag=True, islocal=True),
	"javascript": SchemeDefinition("javascript", usehierarchy=False, useserver=False, usefrag=False),
	"mailto": SchemeDefinition("mailto", usehierarchy=False, useserver=False, usefrag=False),
	"tel": SchemeDefinition("tel", usehierarchy=False, useserver=False, usefrag=False),
	"fax": SchemeDefinition("fax", usehierarchy=False, useserver=False, usefrag=False),
	"ssh": SshSchemeDefinition("ssh", usehierarchy=True, useserver=True, usefrag=True, islocal=False, isremote=True),
}
defaultreg = LocalSchemeDefinition("", usehierarchy=True, useserver=True, islocal=True, usefrag=True)


class Path(object):
	__slots__ = ("_path", "_segments")

	def __init__(self, path=None):
		self._path = ""
		self._segments = []
		self.path = path

	@classmethod
	def _fixsegment(cls, segment):
		if isinstance(segment, basestring):
			if isinstance(segment, unicode):
				segment = _escape(segment)
			return tuple(_unescape(name) for name in segment.split(";", 1))
		else:
			assert 1 <= len(segment) <= 2, "path segment %r must have length 1 or 2, not %d" % (segment, len(segment))
			return tuple(map(unicode, segment))

	def _prefix(cls, path):
		if path.startswith("/"):
			return "/"
		else:
			return ""

	def insert(self, index, *others):
		segments = self.segments
		segments[index:index] = map(self._fixsegment, others)
		self.segments = segments

	def startswith(self, prefix):
		"""
		Return whether :var:`self` starts with the path :var:`prefix`.
		:var:`prefix` will be converted to a :class:`Path` if it isn't one.
		"""
		if not isinstance(prefix, Path):
			prefix = Path(prefix)
		segments = prefix.segments
		if self.isabs != prefix.isabs:
			return False
		if segments and segments[-1] == (u"",) and len(self.segments)>len(segments):
			return self.segments[:len(segments)-1] == segments[:-1]
		else:
			return self.segments[:len(segments)] == segments

	def endswith(self, suffix):
		"""
		Return whether :var:`self` ends with the path :var:`suffix`. :var:`suffix`
		will be converted to a :class:`Path` if it isn't one. If :var:`suffix` is
		absolute a normal comparison will be done.
		"""
		if not isinstance(suffix, Path):
			suffix = Path(suffix)
		if suffix.isabs:
			return self == suffix
		else:
			segments = suffix.segments
			return self.segments[-len(segments):] == segments

	def clone(self):
		return Path(self)

	def __repr__(self):
		return "Path(%r)" % self._path

	def __str__(self):
		return self.path

	def __eq__(self, other):
		if not isinstance(other, Path):
			other = Path(other)
		return self._path == other._path

	def __ne__(self, other):
		return not self == other

	def __hash__(self):
		return hash(self._path)

	def __len__(self):
		return len(self.segments)

	def __getitem__(self, index):
		return self.segments[index]

	def __setitem__(self, index, value):
		segments = self.segments
		segments[index] = self._fixsegment(value)
		self._path = self._prefix(self._path) + self._segments2path(segments)
		self._segments = segments

	def __delitem__(self, index):
		segments = self.segments
		del segments[index]
		self._path = self._segments2path(segments)
		self._segments = segments

	def __contains__(self, item):
		return self._fixsegment(item) in self.segments

	def __getslice__(self, index1, index2):
		"""
		Return of slice of the path. The resulting path will always be relative,
		i.e. the leading ``/`` will be dropped.
		"""
		return Path(self.segments[index1:index2])

	def __setslice__(self, index1, index2, seq):
		segments = self.segments
		segments[index1:index2] = map(self._fixsegment, seq)
		self._path = self._prefix(self._path) + self._segments2path(segments)
		self._segments = segments

	def __delslice__(self, index1, index2):
		del self.segments[index1:index2]

	class isabs(misc.propclass):
		"""
		Is the path absolute?
		"""
		def __get__(self):
			return self._path.startswith("/")
	
		def __set__(self, isabs):
			isabs = bool(isabs)
			if isabs != self._path.startswith("/"):
				if isabs:
					self._path = "/" + self._path
				else:
					self._path = self._path[1:]
	
		def __delete__(self):
			if self._path.startswith("/"):
				self._path = self._path[1:]

	@classmethod
	def _segments2path(cls, segments):
		return "/".join(";".join(_escape(value, pathsafe) for value in segment) for segment in segments)

	@classmethod
	def _path2segments(cls, path):
		if path.startswith("/"):
			path = path[1:]
		return map(cls._fixsegment, path.split("/"))

	def _setpathorsegments(self, path):
		if path is None:
			self._path = ""
			self._segments = []
		elif isinstance(path, Path):
			self._path = path._path
			self._segments = None
		elif isinstance(path, (list, tuple)):
			self._segments = map(self._fixsegment, path)
			self._path = self._prefix(self._path) + self._segments2path(self._segments)
		else:
			if isinstance(path, unicode):
				path = _escape(path)
			prefix = self._prefix(path)
			if prefix:
				path = path[1:]
			self._segments = self._path2segments(path)
			self._path = prefix + self._segments2path(self._segments)

	class path(misc.propclass):
		"""
		The complete path as a string.
		"""
		def __get__(self):
			return self._path

		def __set__(self, path):
			self._setpathorsegments(path)
	
		def __delete__(self):
			self.clear()

	class segments(misc.propclass):
		"""
		The path as a list of (name, param) tuples.
		"""
		def __get__(self):
			if self._segments is None:
				self._segments = self._path2segments(self._path)
			return self._segments
	
		def __set__(self, path):
			self._setpathorsegments(path)

		def __delete__(self):
			self._path = self._prefix(self._path)
			self._segments = []

	class file(misc.propclass):
		"""
		The filename without the path, i.e. the name part of the last component
		of :prop:`path`. The ``baz.html`` part of
		``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			try:
				return self[-1][0]
			except IndexError:
				return None
	
		def __set__(self, file):
			"""
			Setting the filename preserves the parameter in the last segment.
			"""
			if file is None:
				del self.file
			segments = self.segments
			if segments:
				if len(segments[-1]) == 1:
					self[-1] = (file, )
				else:
					self[-1] = (file, segments[-1][1])
			else:
				self.segments = [(file,)]
	
		def __delete__(self):
			"""
			Deleting the filename preserves the parameter in the last segment.
			"""
			segments = self.segments
			if segments:
				if len(segments[-1]) == 1:
					self[-1] = ("", )
				else:
					self[-1] = ("", segments[-1][1])

	class ext(misc.propclass):
		"""
		The filename extension of the last segment of the path. The ``html`` part
		of ``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			ext = None
			segments = self.segments
			if segments:
				name = segments[-1][0]
				pos = name.rfind(".")
				if pos != -1:
					ext = name[pos+1:]
			return ext
	
		def __set__(self, ext):
			"""
			Setting the extension preserves the parameter in the last segment.
			"""
			if ext is None:
				del self.ext
			segments = self.segments
			if segments:
				segment = segments[-1]
				name = segment[0]
				pos = name.rfind(".")
				if pos != -1:
					name = name[:pos+1] + ext
				else:
					name = name + "." + ext
				if len(segment)>1:
					self[-1] = (name, segment[1])
				else:
					self[-1] = (name, )
	
		def __delete__(self):
			"""
			Deleting the extension preserves the parameter in the last segment.
			"""
			segments = self.segments
			if segments:
				segment = segments[-1]
				name = segment[0]
				pos = name.rfind(".")
				if pos != -1:
					name = name[:pos]
					if len(segment)>1:
						self[-1] = (name, segment[1])
					else:
						self[-1] = (name, )

	def withext(self, ext):
		"""
		Return a new :class:`Path` where the filename extension has been replaced
		with :var:`ext`.
		"""
		path = self.clone()
		path.ext = ext
		return path

	def withoutext(self):
		"""
		Return a new :class:`Path` where the filename extension has been removed.
		"""
		if "/" not in self._path and self._path.rfind(".")==0:
			return Path("./")
		else:
			path = self.clone()
			del path.ext
			return path

	def withfile(self, file):
		"""
		Return a new :class:`Path` where the filename (i.e. the name of the last
		component of :prop:`segments`) has been replaced with :var:`file`.
		"""
		path = self.clone()
		path.file = file
		return path

	def withoutfile(self):
		"""
		Return a new :class:`Path` where the filename (i.e. the name of the last
		component of :prop:`segments`) has been removed.
		"""
		if "/" not in self._path:
			return Path("./")
		else:
			path = Path(self)
			del path.file
			return path

	def clear(self):
		self._path = ""
		self._segments = []

	def __div__(self, other):
		"""
		Join two paths.
		"""
		if isinstance(other, basestring):
			other = Path(other)
		if isinstance(other, Path):
			newpath = Path()
			# RFC2396, Section 5.2 (5)
			if other.isabs:
				newpath._path = other._path
				newpath._segments = None
			else:
				# the following should be equivalent to RFC2396, Section 5.2 (6) (c)-(f)
				newpath._path = self._prefix(self._path) + self._segments2path(
					_normalizepath(
						self.segments[:-1] + # RFC2396, Section 5.2 (6) (a)
						other.segments # RFC2396, Section 5.2 (6) (b)
					)
				)
				newpath._segments = None
			return newpath
		elif isinstance(other, (list, tuple)): # this makes path/list possible
			return other.__class__(self/path for path in other)
		else: # this makes path/generator possible
			return (self/path for path in other)

	def __rdiv__(self, other):
		"""
		Right hand version of :meth:`__div__`. This supports list and generators
		as the left hand side too.
		"""
		if isinstance(other, basestring):
			other = Path(other)
		if isinstance(other, Path):
			return other/self
		elif isinstance(other, (list, tuple)):
			return other.__class__(path/self for path in other)
		else:
			return (path/self for path in other)

	def relative(self, basepath):
		"""
		Return an relative :class:`Path` :var:`rel` such that
		``basepath/rel == self```, i.e. this is the inverse operation of
		:meth:`__div__`.

		If :var:`self` is relative, an identical copy of :var:`self` will be
		returned.
		"""
		# if :var:`self` is relative don't do anything
		if not self.isabs:
			pass # FIXME return self.clone()
		basepath = Path(basepath) # clone/coerce
		self_segments = _normalizepath(self.segments)
		base_segments = _normalizepath(basepath.segments)
		while len(self_segments)>1 and len(base_segments)>1 and self_segments[0]==base_segments[0]:
			del self_segments[0]
			del base_segments[0]
		# build a path from one file to the other
		self_segments[:0] = [(u"..",)]*(len(base_segments)-1)
		if not len(self_segments) or self_segments==[(u"",)]:
			self_segments = [(u".",), (u"",)]
		return Path(self._segments2path(self_segments))

	def reverse(self):
		segments = self.segments
		segments.reverse()
		if segments and segments[0] == (u"",):
			del segments[0]
			segments.append((u"",))
		self.segments = segments

	def normalize(self):
		self.segments = _normalizepath(self.segments)

	def normalized(self):
		new = self.clone()
		new.normalize()
		return new

	def local(self):
		"""
		Return :var:`self` converted to a filename using the file naming
		conventions of the OS. Parameters will be dropped in the resulting string.
		"""
		path = Path(self._prefix(self._path) + "/".join(segment[0] for segment in self))
		path = path._path
		localpath = urllib.url2pathname(path)
		if path.endswith("/") and not (localpath.endswith(os.sep) or (os.altsep is not None and localpath.endswith(os.altsep))):
			localpath += os.sep
		return localpath

	def abs(self):
		"""
		Return an absolute version of :var:`self`.
		"""
		path = os.path.abspath(self.local())
		path = path.rstrip(os.sep)
		if path.startswith("///"):
			path = path[2:]
		path = urllib.pathname2url(path.encode("utf-8"))
		if len(self) and self.segments[-1] == ("",):
			path += "/"
		return Path(path)

	def real(self):
		"""
		Return the canonical version of :var:`self`, eliminating all symbolic
		links.
		"""
		path = os.path.realpath(self.local())
		path = path.rstrip(os.sep)
		path = urllib.pathname2url(path.encode("utf-8"))
		if path.startswith("///"):
			path = path[2:]
		if len(self) and self.segments[-1] == ("",):
			path += "/"
		return Path(path)


class Query(dict):
	__slots__= ()
	def __init__(self, arg=None, **kwargs):
		if arg is not None:
			if isinstance(arg, dict):
				for (key, value) in arg.iteritems():
					self.add(key, value)
			else:
				for (key, value) in arg:
					self.add(key, value)
		for (key, value) in kwargs.iteritems():
			self.add(key, value)

	def __setitem__(self, key, value):
		dict.__setitem__(self, unicode(key), [unicode(value)])

	def add(self, key, *values):
		key = unicode(key)
		values = map(unicode, values)
		self.setdefault(key, []).extend(values)

	def __xrepr__(self, mode="default"):
		if mode == "cell":
			yield (astyle.style_url, str(self))
		else:
			yield (astyle.style_url, repr(self))


class URL(object):
	"""
	An :rfc:`2396` compliant URL.
	"""
	def __init__(self, url=None):
		"""
		Create a new :class:`URL` instance. :var:`url` may be a :class:`str` or
		:class:`unicode` instance, or an :class:`URL` (in which case you'll get a
		copy of :var:`url`), or :const:`None` (which will create an :class:`URL`
		referring to the "current document").
		"""
		self.url = url

	def _clear(self):
		# internal helper method that makes :var:`self` empty.
		self.reg = defaultreg
		self._scheme = None
		self._userinfo = None
		self._host = None
		self._port = None
		self._path = Path()
		self._reg_name = None
		self._query = None
		self._query_parts = None
		self._opaque_part = None
		self._frag = None

	def clone(self):
		"""
		Return an identical copy :var:`self`.
		"""
		return URL(self)

	@staticmethod
	def _checkscheme(scheme):
		# Check whether :var:`scheme` contains only legal characters.
		if scheme[0] not in schemecharfirst:
			return False
		for c in scheme[1:]:
			if c not in schemechar:
				return False
		return True

	class scheme(misc.propclass):
		"""
		The URL scheme (e.g. ``ftp``, ``ssh``, ``http`` or ``mailto``). The
		scheme will be :const:`None` if the URL is a relative one.
		"""
		def __get__(self):
			return self._scheme
		def __set__(self, scheme):
			"""
			The scheme will be converted to lowercase on setting (if :var:`scheme`
			is not :const:`None`, otherwise the scheme will be deleted).
			"""
			if scheme is None:
				self._scheme = None
			else:
				scheme = scheme.lower()
				# check if the scheme only has allowed characters
				if not self._checkscheme(scheme):
					raise ValueError("Illegal scheme char in scheme %r" % (scheme, ))
				self._scheme = scheme
			self.reg = schemereg.get(scheme, defaultreg)
		def __delete__(self):
			"""
			Deletes the scheme, i.e. makes the URL relative.
			"""
			self._scheme = None
			self.reg = defaultreg

	class userinfo(misc.propclass):
		"""
		The user info part of the :class:`URL`; i.e. the ``user`` part of
		``http://user@www.example.com:8080/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			return self._userinfo
		def __set__(self, userinfo):
			self._userinfo = userinfo
		def __delete__(self):
			self._userinfo = None

	class host(misc.propclass):
		"""
		The host part of the :class:`URL`; i.e. the ``www.example.com`` part of
		``http://user@www.example.com:8080/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			return self._host
		def __set__(self, host):
			if host is not None:
				host = host.lower()
			self._host = host
		def __delete__(self):
			self._host = None

	class port(misc.propclass):
		"""
		The port number of the :class:`URL` (as an :class:`int`) or :const:`None`
		if the :class:`URL` has none. The ``8080`` in
		``http://user@www.example.com:8080/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			return self._port
		def __set__(self, port):
			if port is not None:
				port = int(port)
			self._port = port
		def __delete__(self):
			self._port = None

	class hostport(misc.propclass):
		"""
		The host and (if specified) the port number of the :class:`URL`, i.e. the
		``www.example.com:8080`` in
		``http://user@www.example.com:8080/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			if self.host is not None:
				hostport = _escape(self.host, safe)
				if self.port is not None:
					hostport += ":%d" % self.port
				return hostport
			else:
				return None
		def __set__(self, hostport):
			# find the port number (RFC2396, Section 3.2.2)
			if hostport is None:
				del self.hostport
			else:
				del self.port
				pos = hostport.rfind(":")
				if pos != -1:
					if pos != len(hostport)-1:
						self.port = hostport[pos+1:]
					hostport = hostport[:pos]
				self.host = _unescape(hostport)
		def __delete__(self):
			del self.host
			del self.port

	class server(misc.propclass):
		"""
		The server part of the :class:`URL`; i.e. the ``user@www.example.com``
		part of ``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			if self.hostport is not None:
				userinfo = self.userinfo
				if userinfo is not None:
					return _escape(userinfo, safe) + "@" + self.hostport
				else:
					return self.hostport
			else:
				return None
		def __set__(self, server):
			"""
			Setting the server always works even if the current :prop:`scheme`
			does use :prop:`opaque_part` or :prop:`reg_name` but will be ignored
			when reassembling the URL for the :prop:`url` property.
			"""
			if server is None:
				del self.server
			else:
				# find the userinfo (RFC2396, Section 3.2.2)
				pos = server.find("@")
				if pos != -1:
					self.userinfo = _unescape(server[:pos])
					server = server[pos+1:]
				else:
					del self.userinfo
				self.hostport = server
		def __delete__(self):
			del self.userinfo
			del self.hostport

	class reg_name(misc.propclass):
		"""
		The reg_name part of the :class:`URL` for hierarchical schemes that use
		a name based :prop:`authority` instead of :prop:`server`.
		"""
		def __get__(self):
			return self._reg_name
		def __set__(self, reg_name):
			if reg_name is None:
				del self.reg_name
			else:
				self._reg_name = reg_name
		def __delete__(self):
			self._reg_name = None

	class authority(misc.propclass):
		"""
		The authority part of the :class:`URL` for hierarchical schemes.
		Depending on the scheme, this is either :prop:`server` or
		:prop:`reg_name`.
		"""
		def __get__(self):
			if self.reg.useserver:
				return self.server
			else:
				return self.reg_name
		def __set__(self, authority):
			if self.reg.useserver:
				self.server = authority
			else:
				self.reg_name = authority
		def __delete__(self):
			if self.reg.useserver:
				del self.server
			else:
				del self.reg_name

	class isabspath(misc.propclass):
		"""
		Specifies whether the path of a hierarchical :class:`URL` is absolute,
		(i.e. it has a leading ``"/"``). Note that the path will always be
		absolute if an :prop:`authority` is specified.
		"""
		def __get__(self):
			return (self.authority is not None) or self.path.isabs
		def __set__(self, isabspath):
			self.path.isabs = isabspath

	class path(misc.propclass):
		"""
		The path segments of a hierarchical :class:`URL` as a :class:`Path` object.
		"""
		def __get__(self):
			return self._path
		def __set__(self, path):
			self._path = Path(path)
		def __delete__(self):
			self._path = Path()

	class file(misc.propclass):
		"""
		The filename without the path, i.e. the name part of the last component
		of :prop:`path`. The ``baz.html`` part of
		``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			return self.path.file
		def __set__(self, file):
			"""
			Setting the filename preserves the parameter in the last segment.
			"""
			self.path.file = file
		def __delete__(self):
			"""
			Deleting the filename preserves the parameter in the last segment.
			"""
			del self.path.file

	class ext(misc.propclass):
		"""
		The filename extension of the last segment of the path. The ``html`` part
		of ``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			return self.path.ext
		def __set__(self, ext):
			"""
			Setting the extension preserves the parameter in the last segment.
			"""
			self.path.ext = ext
		def __delete__(self):
			"""
			Deleting the extension preserves the parameter in the last segment.
			"""
			del self.path.ext

	class query_parts(misc.propclass):
		"""
		The query component as a dictionary, i.e. ``{u"spam": u"eggs"}`` from
		``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.

		If the query component couldn't be parsed, ``query_parts`` will be
		:const:`False`.
		"""
		def __get__(self):
			return self._query_parts
		def __set__(self, query_parts):
			self._query = _urlencode(query_parts)
			self._query_parts = query_parts
		def __delete__(self):
			self._query = None
			self._query_parts = None

	class query(misc.propclass):
		"""
		The query component, i.e. the ``spam=eggs`` part of
		``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			if self._query_parts is False:
				return self._query
			else:
				return _urlencode(self._query_parts)
		def __set__(self, query):
			self._query = query
			if query is not None:
				parts = {}
				for part in query.split(u"&"):
					namevalue = part.split(u"=", 1)
					name = _unescape(namevalue[0].replace("+", " "))
					if len(namevalue) == 2:
						value = _unescape(namevalue[1].replace("+", " "))
						parts.setdefault(name, []).append(value)
					else:
						parts = False
						break
				query = parts
			self._query_parts = query
		def __delete__(self):
			self._query = None
			self._query_parts = None

	class opaque_part(misc.propclass):
		"""
		The opaque part (for schemes like ``mailto`` that are not hierarchical).
		"""
		def __get__(self):
			return self._opaque_part
		def __set__(self, opaque_part):
			self._opaque_part = opaque_part
		def __delete__(self):
			self._opaque_part = None

	class frag(misc.propclass):
		"""
		The fragment identifier, which references a part of the resource, i.e.
		the ``frag`` part of
		``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			return self._frag
		def __set__(self, frag):
			self._frag = frag
		def __delete__(self):
			self._frag = None

	class url(misc.propclass):
		"""
		The complete URL
		"""
		def __get__(self):
			"""
			Getting :prop:`url` reassembles the URL from the components.
			"""
			result = ""
			if self.scheme is not None:
				result += self.scheme + ":"
			if self.reg.usehierarchy:
				if self.authority is not None:
					result += "//" + self.authority
					if not self.path.isabs:
						result += "/"
				result += str(self.path)
				if self.query is not None:
					result += "?" + self.query
			else:
				result += self.opaque_part
			if self.reg.usefrag and self.frag is not None:
				result += "#" + _escape(self.frag, fragsafe)
			return result

		def __set__(self, url):
			"""
			Setting :prop:`url` parses :var:`url` into the components. :var:`url`
			may also be an :class:`URL` instance, in which case the URL will be
			copied.
			"""
			self._clear()
			if url is None:
				return
			elif isinstance(url, URL):
				self.scheme = url.scheme
				self.userinfo = url.userinfo
				self.host = url.host
				self.port = url.port
				self.path = url.path.clone()
				self.reg_name = url.reg_name
				self.opaque_part = url.opaque_part
				self.query = url.query
				self.frag = url.frag
			else:
				if isinstance(url, unicode):
					url = _escape(url)
				# find the scheme (RFC2396, Section 3.1)
				pos = url.find(":")
				if pos != -1:
					scheme = url[:pos]
					if self._checkscheme(scheme): # if the scheme is illegal assume there is none (e.g. "/foo.php?x=http://www.bar.com", will *not* have the scheme "/foo.php?x=http")
						self.scheme = scheme # the info about what we have to expect in the rest of the URL can be found in self.reg now
						url = url[pos+1:]
	
				# find the fragment (RFC2396, Section 4.1)
				if self.reg.usefrag:
					# the fragment itself may not contain a "#", so find the last "#"
					pos = url.rfind("#")
					if pos != -1:
						self.frag = _unescape(url[pos+1:])
						url = url[:pos]
	
				if self.reg.usehierarchy:
					# find the query (RFC2396, Section 3.4)
					pos = url.rfind("?")
					if pos != -1:
						self.query = url[pos+1:]
						url = url[:pos]
					if url.startswith("//"):
						url = url[2:]
						# find the authority part (RFC2396, Section 3.2)
						pos = url.find("/")
						if pos!=-1:
							authority = url[:pos]
							url = url[pos:] # keep the "/"
						else:
							authority = url
							url = "/"
						self.authority = authority
					self.path = Path(url)
				else:
					self.opaque_part = url
		def __delete__(self):
			"""
			After deleting the URL the resulting object will refer to the
			"current document".
			"""
			self._clear()

	def withext(self, ext):
		"""
		Return a new :class:`URL` where the filename extension has been replaced
		with :var:`ext`.
		"""
		url = URL(self)
		url.path = url.path.withext(ext)
		return url

	def withoutext(self):
		"""
		Return a new :class:`URL` where the filename extension has been removed.
		"""
		url = URL(self)
		url.path = url.path.withoutext()
		return url

	def withfile(self, file):
		"""
		Return a new :class:`URL` where the filename (i.e. the name of last
		component of :prop:`path_segments`) has been replaced with
		:var:`file`.
		"""
		url = URL(self)
		url.path = url.path.withfile(file)
		return url

	def withoutfile(self):
		url = URL(self)
		url.path = url.path.withoutfile()
		return url

	def withfrag(self, frag):
		"""
		Return a new :class:`URL` where the fragment has been replaced with
		:var:`frag`.
		"""
		url = URL(self)
		url.frag = frag
		return url

	def withoutfrag(self):
		"""
		Return a new :class:`URL` where the frag has been dropped.
		"""
		url = URL(self)
		del url.frag
		return url

	def __div__(self, other):
		"""
		Join :var:`self` with another (possible relative) :class:`URL`
		:var:`other`, to form a new :class:`URL`.
		
		:var:`other` may be a :class:`str`, :class:`unicode` or :class:`URL`
		object. It may be :const:`None` (referring to the "current document")
		in which case :var:`self` will be returned. It may also be a list or
		other iterable. For this case a list (or iterator) will be returned where
		:meth:`__div__` will be applied to every item in the list/iterator. E.g.
		the following expression returns all the files in the current directory
		as absolute URLs (see the method :meth:`files` and the function
		:func:`here` for further explanations)::

			>>> here = url.here()
			>>> for f in here/here.files():
			... 	print f
		"""
		if isinstance(other, basestring):
			other = URL(other)
		if isinstance(other, URL):
			newurl = URL()
			# RFC2396, Section 5.2 (2)
			if other.scheme is None and other.authority is None and str(other.path)=="" and other.query is None:
				newurl = URL(self)
				newurl.frag = other.frag
				return newurl
			if not self.reg.usehierarchy: # e.g. "mailto:x@y"/"file:foo"
				return other
			# In violation of RFC2396 we treat file URLs as relative ones (if the base is a local URL)
			if other.scheme=="file" and self.islocal():
				other = URL(other)
				del other.scheme
				del other.authority
			# RFC2396, Section 5.2 (3)
			if other.scheme is not None:
				return other
			newurl.scheme = self.scheme
			newurl.query = other.query
			newurl.frag = other.frag
			# RFC2396, Section 5.2 (4)
			if other.authority is None:
				newurl.authority = self.authority
				# RFC2396, Section 5.2 (5) & (6) (a) (b)
				newurl._path = self._path/other._path
			else:
				newurl.authority = other.authority
				newurl._path = other._path.clone()
			return newurl
		elif isinstance(other, (list, tuple)): # this makes path/list possible
			return other.__class__(self/path for path in other)
		else: # this makes path/generator possible
			return (self/path for path in other)

	def __rdiv__(self, other):
		"""
		Right hand version of :meth:`__div__`. This supports lists and iterables
		as the left hand side too.
		"""
		if isinstance(other, basestring):
			other = URL(other)
		if isinstance(other, URL):
			return other/self
		elif isinstance(other, (list, tuple)):
			return other.__class__(item/self for item in other)
		else:
			return (item/self for item in other)

	def relative(self, baseurl):
		"""
		Return an relative :class:`URL` :var:`rel` such that
		``baseurl/rel == self``, i.e. this is the inverse operation of
		:meth:`__div__`.

		If :var:`self` is relative, has a different :prop:`scheme` or
		:prop:`authority` than :var:`baseurl` or a non-hierarchical scheme, an
		identical copy of :var:`self` will be returned.
		"""
		# if :var:`self` is relative don't do anything
		if self.scheme is None:
			return URL(self)
		# javascript etc.
		if not self.reg.usehierarchy:
			return URL(self)
		baseurl = URL(baseurl) # clone/coerce
		# only calculate a new URL if to the same server, else use the original
		if self.scheme != baseurl.scheme or self.authority != baseurl.authority:
			return URL(self)
		newurl = URL(self) # clone
		del newurl.scheme
		del newurl.authority
		selfpath_segments = _normalizepath(self._path.segments)
		basepath_segments = _normalizepath(baseurl._path.segments)
		while len(selfpath_segments)>1 and len(basepath_segments)>1 and selfpath_segments[0]==basepath_segments[0]:
			del selfpath_segments[0]
			del basepath_segments[0]
		# does the URL go to the same file?
		if selfpath_segments==basepath_segments and self.query==baseurl.query:
			# only return the frag
			del newurl.path
			del newurl.query
		else:
			# build a path from one file to the other
			selfpath_segments[:0] = [(u"..",)]*(len(basepath_segments)-1)
			if not len(selfpath_segments) or selfpath_segments==[(u"",)]:
				selfpath_segments = [(u".",), (u"",)]
			newurl._path.segments = selfpath_segments
			newurl._path = self.path.relative(baseurl.path)
		newurl._path.isabs = False
		return newurl

	def __str__(self):
		return self.url

	def __unicode__(self):
		return self.url

	def __repr__(self):
		return "URL(%r)" % self.url

	def __nonzero__(self):
		"""
		Return whether the :class:`URL` is not empty, i.e. whether it is not the
		:class:`URL` referring to the start of the current document.
		"""
		return self.url != ""

	def __eq__(self, other):
		"""
		Return whether two :class:`URL` objects are equal. Note that only
		properties relevant for the current scheme will be compared.
		"""
		if self.__class__ != other.__class__:
			return False
		if self.scheme != other.scheme:
			return False
		if self.reg.usehierarchy:
			if self.reg.useserver:
				selfport = self.port or self.reg.defaultport
				otherport = other.port or other.reg.defaultport
				if self.userinfo != other.userinfo or self.host != other.host or selfport != otherport:
					return False
			else:
				if self.reg_name != other.reg_name:
					return False
			if self._path != other._path:
				return False
		else:
			if self.opaque_part != other.opaque_part:
				return False
		# Use canonical version of (i.e. sorted names and values)
		if self.query != other.query:
			return False
		if self.frag != other.frag:
			return False
		return True

	def __ne__(self, other):
		"""
		Return whether two :class:`URL` objects are *not* equal.
		"""
		return not self==other

	def __hash__(self):
		"""
		Return a hash value for :var:`self`, to be able to use :class:`URL`
		objects as dictionary keys. You must be careful not to modify an
		:class:`URL` as soon as you use it as a dictionary key.
		"""
		res = hash(self.scheme)
		if self.reg.usehierarchy:
			if self.reg.useserver:
				res ^= hash(self.userinfo)
				res ^= hash(self.host)
				res ^= hash(self.port or self.reg.defaultport)
			else:
				res ^= hash(self.reg_name)
			res ^= hash(self._path)
		else:
			res ^= hash(self.opaque_part)
		res ^= hash(self.query)
		res ^= hash(self.frag)
		return res

	def abs(self, scheme=-1):
		"""
		Return an absolute version of :var:`self` (works only for local URLs).

		If the argument :var:`scheme` is specified, it will be used for the
		resulting URL otherwise the result will have the same scheme as
		:var:`self`.
		"""
		self._checklocal()
		new = self.clone()
		new.path = self.path.abs()
		if scheme != -1:
			new.scheme = scheme
		return new

	def real(self, scheme=-1):
		"""
		Return the canonical version of :var:`self`, eliminating all symbolic
		links (works only for local URLs).

		If the argument :var:`scheme` is specified, it will be used for the
		resulting URL otherwise the result will have the same scheme as
		:var:`self`.
		"""
		self._checklocal()
		new = self.clone()
		new.path = self.path.real()
		if scheme != -1:
			new.scheme = scheme
		return new

	def islocal(self):
		"""
		Return whether :var:`self` refers to a local file, i.e. whether
		:var:`self` is a relative :class:`URL` or the scheme is ``root`` or
		``file``).
		"""
		return self.reg.islocal

	def _checklocal(self):
		if not self.islocal():
			raise ValueError("URL %r is not local" % self)

	def local(self):
		"""
		Return :var:`self` as a local filename (which will only works if
		:var:`self` is local (see :meth:`islocal`).
		"""
		self._checklocal()
		return self.path.local()

	def _connect(self, context=None, **kwargs):
		return self.reg._connect(self, context=context, **kwargs)

	def connect(self, context=None, **kwargs):
		"""
		Return a :class:`Connection` object for accessing and modifying the
		metadata of :var:`self`.

		Whether you get a new connection object, or an existing one depends on
		the scheme, the URL itself, and the context passed in (as the
		:var:`context` argument).
		"""
		return self._connect(context, **kwargs)[0]

	def open(self, mode="rb", context=None, *args, **kwargs):
		"""
		Open :var:`self` for reading or writing. :meth:`open` returns a
		:class:`Resource` object.

		Which additional parameters are supported depends on the actual resource
		created. Some common parameters are:

			:var:`mode` (supported by all resources)
				A string indicating how the file is to be opened (just like the
				mode argument for the builtin :func:`open`; e.g. ``"rb"`` or
				``"wb"``).

			:var:`context` (supported by all resources)
				:meth:`open` needs a :class:`Connection` for this URL which it gets
				from a :class:`Context` object.

			:var:`headers`
				Additional headers to use for an HTTP request.

			:var:`data`
				Request body to use for an HTTP POST request.

			:var:`remotepython`
				Name of the Python interpreter to use on the remote side
				(used by ``ssh`` URLs)

			:var:`ssh_config`
				SSH configuration file (used by ``ssh`` URLs)
		"""
		(connection, kwargs) = self._connect(context=context, **kwargs)
		return connection.open(self, mode, *args, **kwargs)

	def openread(self, context=None, *args, **kwargs):
		return self.open("rb", context, *args, **kwargs)

	def openwrite(self, context=None, *args, **kwargs):
		return self.open("wb", context, *args, **kwargs)

	def __getattr__(self, name):
		"""
		:meth:`__getattr__` forwards every unresolved attribute access to the
		appropriate connection. This makes it possible to call :class:`Connection`
		methods directly on :class:`URL` objects::

			>>> from ll import url
			>>> u = url.URL("file:README")
			>>> u.size()
			1584L

		instead of::

			>>> from ll import url
			>>> u = url.URL("file:README")
			>>> u.connect().size(u)
			1584L
		"""
		def realattr(*args, **kwargs):
			try:
				context = kwargs["context"]
			except KeyError:
				context = None
			else:
				kwargs = kwargs.copy()
				del kwargs["context"]
			(connection, kwargs) = self._connect(context=context, **kwargs)
			return getattr(connection, name)(self, *args, **kwargs)
		return realattr

	def import_(self, mode="always"):
		"""
		import the file as a Python module. The file extension will be ignored,
		which means that you might not get exactly the file you specified.
		:var:`mode` can have the following values:

		``"always"`` (the default)
			The module will be imported on every call;

		``"once"``
			The module will be imported only on the first call;

		``"new"``
			The module will be imported every time it has changed since the
			last call.
		"""
		filename = self.real().local()
		if mode=="always":
			mdate = self.mdate()
		elif mode=="once":
			try:
				return importcache[filename][1]
			except KeyError:
				mdate = self.mdate()
		elif mode=="new":
			mdate = self.mdate()
			try:
				(oldmdate, module) = importcache[filename]
			except KeyError:
				pass
			else:
				if mdate<=oldmdate:
					return module
		else:
			raise ValueError, "mode %r unknown" % mode
		module = _import(filename)
		importcache[filename] = (mdate, module)
		return module

	def __iter__(self):
		try:
			isdir = self.isdir()
		except AttributeError:
			isdir = False
		if isdir:
			return iter(self/self.listdir())
		else:
			return iter(self.open())

	def __xrepr__(self, mode="default"):
		if mode == "cell":
			yield (astyle.style_url, str(self))
		else:
			yield (astyle.style_url, repr(self))


warnings.filterwarnings("always", module="url")
