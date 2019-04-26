# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 1999-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 1999-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


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


import os, urllib.request, urllib.error, urllib.parse as urlparse, mimetypes, io, warnings
import datetime, cgi, re, fnmatch, pickle, errno, threading
import email
from email import utils

default_ssh_python = os.environ.get("LL_URL_SSH_PYTHON")

# don't fail when :mod:`pwd` or :mod:`grp` can't be imported, because if this
# doesn't work, we're probably on Windows and :func:`os.chown` won't work anyway.
try:
	import pwd, grp
except ImportError:
	pass

try:
	import execnet
except ImportError:
	pass

try:
	from PIL import Image
except ImportError:
	pass

from ll import misc


__docformat__ = "reStructuredText"


def mime2dt(s):
	return datetime.datetime(*utils.parsedate(s)[:7])


weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
monthname = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def httpdate(dt):
	"""
	Return a string suitable for a "Last-Modified" and "Expires" header.

	:obj:`dt` is a :class:`datetime.datetime` object in UTC.
	"""
	return f"{weekdayname[dt.weekday()]}, {dt.day:02d} {monthname[dt.month]:3} {dt.year:4} {dt.hour:02}:{dt.minute:02}:{dt.second:02} GMT"


def _normalizepath(path_segments):
	"""
	Internal helper function for normalizing a path list.

	Should be equivalent to RFC2396, Section 5.2 (6) (c)-(f) with the exception
	of removing empty path_segments.
	"""
	new_path_segments = []
	l = len(path_segments)
	for i in range(l):
		segment = path_segments[i]
		if not segment or segment == ".":
			if i == l-1:
				new_path_segments.append("")
		elif segment == ".." and len(new_path_segments) and new_path_segments[-1] != "..":
			new_path_segments.pop()
			if i == l-1:
				new_path_segments.append("")
		else:
			new_path_segments.append(segment)
	return new_path_segments


def _escape(s, safe="".join(chr(c) for c in range(128))):
	return urlparse.quote(s, safe)


_unescape = urlparse.unquote


alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphanum = alpha + "0123456789"
mark = "-_.!~*'()"
additionalsafe = "[]"
safe = alphanum + mark + additionalsafe
pathsafe = safe + ":@&=$,;+" + "|" # add "|" for Windows paths
querysafe = alphanum
fragsafe = alphanum

schemecharfirst = alpha
schemechar = alphanum + "+-."


def _urlencode(query_parts):
	if query_parts is not None:
		res = []
		# generate a canonical order for the names
		items = sorted(query_parts.items())
		for (name, values) in items:
			if not isinstance(values, (list, tuple)):
				values = (values,)
			else:
				# generate a canonical order for the values
				values.sort()
			for value in values:
				res.append(f"{_escape(name, querysafe)}={_escape(value, querysafe)}")
		return "&".join(res)
	else:
		return None


def compilepattern(pattern, ignorecase=False):
	if pattern is None:
		return None
	elif isinstance(pattern, str):
		return (re.compile(fnmatch.translate(pattern), re.I if ignorecase else 0).match,)
	else:
		return tuple(re.compile(fnmatch.translate(p), re.I if ignorecase else 0).match for p in pattern)


def matchpatterns(name, include, exclude):
	if include and not any(matcher(name) is not None for matcher in include):
		return False
	if exclude and any(matcher(name) is not None for matcher in exclude):
		return False
	return True


class Context(object):
	"""
	Working with URLs (e.g. calling :meth:`URL.open` or :meth:`URL.connect`)
	involves :class:`Connection` objects. To avoid constantly creating new
	connections you can pass a :class:`Context` object to those methods.
	Connections will be stored in the :class:`Context` object and will be
	reused by those methods.

	A :class:`Context` object can also be used as a context manager. This context
	object will be used for all :meth:`open` and :meth:`connect` calls inside the
	:keyword:`with` block. (Note that after the end of the :keyword:`with` block
	all connections will be closed.)
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

	def __exit__(self, *exc_info):
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


###
### Cursor for the :meth:`walk` method
###

class Cursor(object):
	"""
	A :class:`Cursor` object is used by the :meth:`walk` method during directory
	traversal. It contains information about the state of the traversal and can
	be used to influence which directories are traversed and in which order.

	Information about the state of the traversal is provided in the following
	attributes:

	``rooturl``
		The URL where traversal has been started (i.e. the object for which the
		:meth:`walk` method has been called)

	``url``
		The current URL being traversed.

	``event``
		A string that specifies which event is currently handled. Possible values
		are: ``"beforedir"``, ``"afterdir"`` and ``"file"``. A ``"beforedir"``
		event is emitted before a directory is entered. ``"afterdir"``
		is emitted after a directory has been entered. ``"file"`` is emitted when
		a file is encountered.

	``isdir``
		True if ``url`` refers to a directory.

	``isfile``
		Tur if ``url`` refers to a regular file.

	The following attributes specify which part of the tree should be traversed:

	``beforedir``
		Should the generator yield ``"beforedir"`` events?

	``afterdir``
		Should the generator yield ``"afterdir"`` events?

	``file``
		Should the generator yield ``"file"`` events?

	``enterdir``
		Should the directory be entered?

	Note that if any of these attributes is changed by the code consuming the
	generator, this new value will be used for the next traversal step once the
	generator is resumed and will be reset to its initial value (specified in
	the constructor) afterwards.
	"""
	def __init__(self, url, beforedir=True, afterdir=False, file=True, enterdir=False):
		"""
		Create a new :class:`Cursor` object for a tree traversal rooted at the node
		:obj:`node`.

		The arguments :obj:`beforedir`, :obj:`afterdir`, :obj:`file` and
		:obj:`enterdir` are used as the initial values for the attributes of
		the same name. (see the class docstring for info about their use).
		"""
		self.rooturl = self.url = url
		self.event = None
		self.beforedir = self._beforedir = beforedir
		self.afterdir = self._afterdir = afterdir
		self.file = self._file = file
		self.enterdir = self._enterdir = enterdir
		self.isdir = self.isfile = None

	def restore(self):
		"""
		Restore the attributes ``beforedir``, ``afterdir``, ``file`` and
		``enterdir`` to their initial value.
		"""
		self.beforedir = self._beforedir
		self.afterdir = self._afterdir
		self.file = self._file
		self.enterdir = self._enterdir


class Connection(object):
	"""
	A :class:`Connection` object is used for accessing and modifying the
	metadata associated with a file. It is created by calling the
	:meth:`connect` method on a :class:`URL` object.
	"""

	@misc.notimplemented
	def stat(self, url):
		"""
		Return the result of a :func:`stat` call on the file :obj:`url`.
		"""

	@misc.notimplemented
	def lstat(self, url):
		"""
		Return the result of a :func:`stat` call on the file :obj:`url`. Like
		:meth:`stat`, but does not follow symbolic links.
		"""

	@misc.notimplemented
	def chmod(self, url, mode):
		"""
		Set the access mode of the file :obj:`url` to :obj:`mode`.
		"""

	@misc.notimplemented
	def chown(self, url, owner=None, group=None):
		"""
		Change the owner and/or group of the file :obj:`url`.
		"""

	@misc.notimplemented
	def lchown(self, url, owner=None, group=None):
		"""
		Change the owner and/or group of the file :obj:`url`
		(ignoring symbolic links).
		"""

	@misc.notimplemented
	def uid(self, url):
		"""
		Return the user id of the owner of the file :obj:`url`.
		"""

	@misc.notimplemented
	def gid(self, url):
		"""
		Return the group id the file :obj:`url` belongs to.
		"""

	@misc.notimplemented
	def owner(self, url):
		"""
		Return the name of the owner of the file :obj:`url`.
		"""

	@misc.notimplemented
	def group(self, url):
		"""
		Return the name of the group the file :obj:`url` belongs to.
		"""

	def mimetype(self, url):
		"""
		Return the mimetype of the file :obj:`url`.
		"""
		name = self._url2filename(url)
		mimetype = mimetypes.guess_type(name)[0]
		return mimetype or "application/octet-stream"

	@misc.notimplemented
	def exists(self, url):
		"""
		Test whether the file :obj:`url` exists.
		"""

	@misc.notimplemented
	def isfile(self, url):
		"""
		Test whether the resource :obj:`url` is a file.
		"""

	@misc.notimplemented
	def isdir(self, url):
		"""
		Test whether the resource :obj:`url` is a directory.
		"""

	@misc.notimplemented
	def islink(self, url):
		"""
		Test whether the resource :obj:`url` is a link.
		"""

	@misc.notimplemented
	def ismount(self, url):
		"""
		Test whether the resource :obj:`url` is a mount point.
		"""

	@misc.notimplemented
	def access(self, url, mode):
		"""
		Test for access to the file/resource :obj:`url`.
		"""

	def size(self, url):
		"""
		Return the size of the file :obj:`url`.
		"""
		return self.stat(url).st_size

	def imagesize(self, url):
		"""
		Return the size of the image :obj:`url` (if the resource is an image file)
		as a ``(width, height)`` tuple. This requires the PIL__.

		__ http://www.pythonware.com/products/pil/
		"""
		stream = self.open(url, mode="rb")
		img = Image.open(stream) # Requires PIL
		imagesize = img.size
		stream.close()
		return imagesize

	def cdate(self, url):
		"""
		Return the "metadate change" date of the file/resource :obj:`url`
		as a :class:`datetime.datetime` object in UTC.
		"""
		return datetime.datetime.utcfromtimestamp(self.stat(url).st_ctime)

	def adate(self, url):
		"""
		Return the last access date of the file/resource :obj:`url` as a
		:class:`datetime.datetime` object in UTC.
		"""
		return datetime.datetime.utcfromtimestamp(self.stat(url).st_atime)

	def mdate(self, url):
		"""
		Return the last modification date of the file/resource :obj:`url`
		as a :class:`datetime.datetime` object in UTC.
		"""
		return datetime.datetime.utcfromtimestamp(self.stat(url).st_mtime)

	def resheaders(self, url):
		"""
		Return the MIME headers for the file/resource :obj:`url`.
		"""
		return email.message_from_string(f"Content-Type: {self.mimetype(url)}\nContent-Length: {self.size(url)}\nLast-modified: {httpdate(self.mdate(url))}\n")

	@misc.notimplemented
	def remove(self, url):
		"""
		Remove the file :obj:`url`.
		"""

	@misc.notimplemented
	def rmdir(self, url):
		"""
		Remove the directory :obj:`url`.
		"""

	@misc.notimplemented
	def rename(self, url, target):
		"""
		Renames :obj:`url` to :obj:`target`. This might not work if :obj:`target`
		has a different scheme than :obj:`url` (or is on a different server).
		"""

	@misc.notimplemented
	def link(self, url, target):
		"""
		Create a hard link from :obj:`url` to :obj:`target`. This will not work
		if :obj:`target` has a different scheme than :obj:`url` (or is on a
		different server).
		"""

	@misc.notimplemented
	def symlink(self, url, target):
		"""
		Create a symbolic link from :obj:`url` to :obj:`target`. This will not
		work if :obj:`target` has a different scheme than :obj:`url` (or is on a
		different server).
		"""

	@misc.notimplemented
	def chdir(self, url):
		"""
		Change the current directory to :obj:`url`.
		"""
		os.chdir(self.name)

	@misc.notimplemented
	def mkdir(self, url, mode=0o777):
		"""
		Create the directory :obj:`url`.
		"""

	@misc.notimplemented
	def makedirs(self, url, mode=0o777):
		"""
		Create the directory :obj:`url` and all intermediate ones.
		"""

	@misc.notimplemented
	def walk(self, url, beforedir=True, afterdir=False, file=True, enterdir=True):
		"""
		Return an iterator for traversing the directory hierarchy rooted at
		the directory :obj:`url`.

		Each item produced by the iterator is a :class:`Cursor` object.
		It contains information about the state of the traversal and can be used
		to influence which parts of the directory hierarchy are traversed and in
		which order.

		The arguments :obj:`beforedir`, :obj:`afterdir`,
		:obj:`file` and :obj:`enterdir` specify how the directory hierarchy should
		be traversed. For more information see the :class:`Cursor` class.

		Note that the :class:`Cursor` object is reused by :meth:`walk`, so you
		can't rely on any attributes remaining the same across calls to
		:func:`next`.

		The following example shows how to traverse the current directory, print
		all files except those in certain directories::

			from ll import url

			for cursor in url.here().walk(beforedir=True, afterdir=False, file=True):
				if cursor.isdir:
					if cursor.url.path[-2] in (".git", "build", "dist", "__pycache__"):
						cursor.enterdir = False
				else:
					print(cursor.url)
		"""

	def listdir(self, url, include=None, exclude=None, ignorecase=False):
		"""
		Iterates over items in the directory :obj:`url`. The items produced are
		:class:`URL` objects relative to :obj:`url`.

		With the optional :obj:`include` argument, this only lists items whose
		names match the given pattern. Items matching the optional pattern
		:obj:`exclude` will not be listed. :obj:`include` and :obj:`exclude` can
		be strings (which will be interpreted as :mod:`fnmatch` style filename
		patterns) or lists of strings. If :obj:`ignorecase` is true
		case-insensitive name matching will be performed.
		"""
		include = compilepattern(include, ignorecase)
		exclude = compilepattern(exclude, ignorecase)
		for cursor in self.walk(url, beforedir=True, afterdir=False, file=True, enterdir=False):
			if matchpatterns(cursor.url.path[-1-cursor.isdir], include, exclude):
				yield cursor.url

	def files(self, url, include=None, exclude=None, ignorecase=False):
		"""
		Iterates over files in the directory :obj:`url`. The items produced
		are :class:`URL` objects relative to :obj:`url`.

		With the optional :obj:`include` argument, this only lists files whose
		names match the given pattern. Files matching the optional pattern
		:obj:`exclude` will not be listed. :obj:`include` and :obj:`exclude` can
		be strings (which will be interpreted as :mod:`fnmatch` style filename
		patterns) or lists of strings. If :obj:`ignorecase` is true
		case-insensitive name matching will be performed.
		"""
		include = compilepattern(include, ignorecase)
		exclude = compilepattern(exclude, ignorecase)
		for cursor in self.walk(url, beforedir=False, afterdir=False, file=True, enterdir=False):
			if cursor.isfile and matchpatterns(cursor.url.path[-1], include, exclude):
				yield cursor.url

	def dirs(self, url, include=None, exclude=None, ignorecase=False):
		"""
		Iterates over directories in the directory :obj:`url`. The items produced
		are :class:`URL` objects relative to :obj:`url`.

		With the optional :obj:`include` argument, this only directories items
		whose names match the given pattern. Directories matching the optional
		pattern :obj:`exclude` will not be listed. :obj:`include` and
		:obj:`exclude` can be strings (which will be interpreted as :mod:`fnmatch`
		style filename patterns) or lists of strings.  If :obj:`ignorecase` is
		true case-insensitive name matching will be performed.
		"""
		include = compilepattern(include, ignorecase)
		exclude = compilepattern(exclude, ignorecase)
		for cursor in self.walk(url, beforedir=True, afterdir=False, file=False, enterdir=False):
			if cursor.isdir and matchpatterns(cursor.url.path[-2], include, exclude):
				yield cursor.url

	def walkall(self, url, include=None, exclude=None, enterdir=None, skipdir=None, ignorecase=False):
		"""
		Recursively iterate over files and subdirectories. The iterator
		yields :class:`URL` objects naming each child URL of the directory
		:obj:`url` and its descendants relative to :obj:`url`. This performs
		a depth-first traversal, returning each directory before all its children.

		With the optional :obj:`include` argument, only yield items whose
		names match the given pattern. Items matching the optional pattern
		:obj:`exclude` will not be listed. Directories that don't match the
		optional pattern :obj:`enterdir` or match the pattern :obj:`skipdir`
		will not be traversed. :obj:`include`, :obj:`exclude`, :obj:`enterdir`
		and :obj:`skipdir` can be strings (which will be interpreted as
		:mod:`fnmatch` style filename patterns) or lists of strings.
		If :obj:`ignorecase` is true case-insensitive name matching will be
		performed.
		"""
		include = compilepattern(include, ignorecase)
		exclude = compilepattern(exclude, ignorecase)
		enterdir = compilepattern(enterdir, ignorecase)
		skipdir = compilepattern(skipdir, ignorecase)
		for cursor in self.walk(url, beforedir=True, afterdir=False, file=True, enterdir=True):
			name = cursor.url.path[-1-cursor.isdir]
			if matchpatterns(name, include, exclude):
				yield cursor.url
			if cursor.isdir:
				cursor.enterdir = matchpatterns(name, enterdir, skipdir)

	def walkfiles(self, url, include=None, exclude=None, enterdir=None, skipdir=None, ignorecase=False):
		"""
		Return a recursive iterator over files in the directory :obj:`url`.

		With the optional :obj:`include` argument, only yield files whose names
		match the given pattern. Files matching the optional pattern
		:obj:`exclude` will not be listed. Directories that don't match the
		optional pattern :obj:`enterdir` or match the pattern :obj:`skipdir`
		will not be traversed. :obj:`include`, :obj:`exclude`, :obj:`enterdir`
		and :obj:`skipdir` can be strings (which will be interpreted as
		:mod:`fnmatch` style filename patterns) or lists of strings.
		If :obj:`ignorecase` is true case-insensitive name matching will be
		performed.
		"""
		include = compilepattern(include, ignorecase)
		exclude = compilepattern(exclude, ignorecase)
		enterdir = compilepattern(enterdir, ignorecase)
		skipdir = compilepattern(skipdir, ignorecase)
		for cursor in self.walk(url, beforedir=True, afterdir=False, file=True, enterdir=True):
			if cursor.isfile:
				if matchpatterns(cursor.url.path[-1], include, exclude):
					yield cursor.url
			else:
				cursor.enterdir = matchpatterns(cursor.url.path[-2], enterdir, skipdir)

	def walkdirs(self, url, include=None, exclude=None, enterdir=None, skipdir=None, ignorecase=False):
		"""
		Return a recursive iterator over subdirectories in the directory
		:obj:`url`.

		With the optional :obj:`include` argument, only yield directories whose
		names match the given pattern. Items matching the optional pattern
		:obj:`exclude` will not be listed. Directories that don't match the
		optional pattern :obj:`enterdir` or match the pattern :obj:`skipdir`
		will not be traversed. :obj:`include`, :obj:`exclude`, :obj:`enterdir`
		and :obj:`skipdir` can be strings (which will be interpreted as
		:mod:`fnmatch` style filename patterns) or lists of strings.
		If :obj:`ignorecase` is true case-insensitive name matching will be
		performed.
		"""
		include = compilepattern(include, ignorecase)
		exclude = compilepattern(exclude, ignorecase)
		enterdir = compilepattern(enterdir, ignorecase)
		skipdir = compilepattern(skipdir, ignorecase)
		for cursor in self.walk(url, beforedir=True, afterdir=False, file=False, enterdir=True):
			name = cursor.url.path[-2]
			if matchpatterns(name, include, exclude):
				yield cursor.url
			cursor.enterdir = matchpatterns(name, enterdir, skipdir)

	@misc.notimplemented
	def open(self, url, *args, **kwargs):
		"""
		Open :obj:`url` for reading or writing. :meth:`open` returns a
		:class:`Resource` object.

		Which additional parameters are supported depends on the actual
		resource created. Some common parameters are:

			:obj:`mode` : string
				A string indicating how the file is to be opened (just like the
				mode argument for the builtin :func:`open` (e.g. ``"rb"`` or
				``"wb"``).

			:obj:`headers` : mapping
				Additional headers to use for an HTTP request.

			:obj:`data` : byte string
				Request body to use for an HTTP POST request.

			:obj:`python` : string or :const:`None`
				Name of the Python interpreter to use on the remote side (used by
				``ssh`` URLs)

			:obj:`nice` : int or :const:`None`
				Nice level for the remote python (used by ``ssh`` URLs)
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
			elif isinstance(owner, str):
				owner = pwd.getpwnam(owner)[2]
			if group is None:
				group = stat.st_gid
			elif isinstance(group, str):
				group = grp.getgrnam(group)[2]
			func(name, owner, group)

	def chown(self, url, owner=None, group=None):
		self._chown(os.chown, url, owner, group)

	def lchown(self, url, owner=None, group=None):
		self._chown(os.lchown, url, owner, group)

	def chdir(self, url):
		os.chdir(self._url2filename(url))

	def mkdir(self, url, mode=0o777):
		os.mkdir(self._url2filename(url), mode)

	def makedirs(self, url, mode=0o777):
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
		target = self._url2filename(target)
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

	def _walk(self, cursor, base, name):
		def _event(url, event):
			cursor.url = url
			cursor.event = event
			cursor.isdir = event != "file"
			cursor.isfile = not cursor.isdir
			return cursor

		if name:
			fullname = os.path.join(base, name)
		else:
			fullname = base
		for childname in sorted(os.listdir(fullname)):
			fullchildname = os.path.join(fullname, childname)
			isdir = os.path.isdir(fullchildname)
			relchildname = os.path.join(name, childname) if name else childname
			emitbeforedir = cursor.beforedir
			emitafterdir = cursor.afterdir
			emitfile = cursor.file
			enterdir = cursor.enterdir
			if isdir:
				if emitbeforedir or emitafterdir:
					dirurl = Dir(relchildname, scheme=None)
				if emitbeforedir:
					yield _event(dirurl, "beforedir")
					# The user may have altered ``cursor`` attributes outside the generator, so we refetch them
					emitbeforedir = cursor.beforedir
					emitafterdir = cursor.afterdir
					emitfile = cursor.file
					enterdir = cursor.enterdir
					cursor.restore()
				if enterdir:
					yield from self._walk(cursor, base, relchildname)
				if emitafterdir:
					yield _event(dirurl, "afterdir")
					cursor.restore()
			else:
				if emitfile:
					yield _event(File(relchildname, scheme=None), "file")
					cursor.restore()

	def walk(self, url, beforedir=True, afterdir=False, file=True, enterdir=True):
		cursor = Cursor(url, beforedir=beforedir, afterdir=afterdir, file=file, enterdir=enterdir)
		return self._walk(cursor, url.local(), "")

	def open(self, url, *args, **kwargs):
		return FileResource(url, *args, **kwargs)


class SshConnection(Connection):
	remote_code = """
		import sys, os, pickle, re, fnmatch
		try:
			from urllib import request
		except ImportError:
			import urllib as request
		try:
			next
		except NameError:
			def next(iter):
				return iter.next()
		try:
			unicode
		except NameError:
			unicode = str

		files = {}

		def ownergroup(filename, owner=None, group=None):
			if owner is not None or group is not None:
				if owner is None or group is None:
					if isinstance(filename, unicode):
						stat = os.stat(filename)
					else:
						stat = os.fstat(files[filename].fileno())
				if owner is None:
					owner = stat.st_uid
				elif isinstance(owner, unicode):
					import pwd
					owner = pwd.getpwnam(owner)[2]

				if group is None:
					group = stat.st_gid
				elif isinstance(group, unicode):
					import grp
					group = grp.getgrnam(group)[2]
			return (owner, group)

		def compilepattern(pattern, ignorecase=False):
			if pattern is None:
				return None
			elif isinstance(pattern, unicode):
				return (re.compile(fnmatch.translate(pattern), re.I if ignorecase else 0).match,)
			else:
				return tuple(re.compile(fnmatch.translate(p), re.I if ignorecase else 0).match for p in pattern)

		def matchpatterns(name, include, exclude):
			if include and not any(matcher(name) is not None for matcher in include):
				return False
			if exclude and any(matcher(name) is not None for matcher in exclude):
				return False
			return True

		def listdir(dirname):
			result = []
			for childname in sorted(os.listdir(dirname)):
				fullchildname = os.path.join(dirname, childname)
				isdir = os.path.isdir(fullchildname)
				result.append((isdir, childname))
			return result

		while True:
			(filename, cmdname, args, kwargs) = channel.receive()
			if isinstance(filename, unicode):
				filename = os.path.expanduser(request.url2pathname(filename))
			data = None
			try:
				if cmdname == "open":
					try:
						stream = open(filename, *args, **kwargs)
					except IOError:
						exc = sys.exc_info()[1]
						if args:
							mode = args[0]
						else:
							mode = kwargs.get("mode", "rb")
						if "w" not in mode or exc.errno != 2: # didn't work for some other reason than a non existing directory
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
					if isinstance(filename, unicode):
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
					data = unicode(pwd.getpwuid(stat.st_uid)[0])
				elif cmdname == "group":
					import grp
					stat = os.stat(filename)
					data = unicode(grp.getgrgid(stat.st_gid)[0])
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
					data = listdir(filename)
				elif cmdname == "next":
					data = next(files[filename])
				else:
					data = getattr(files[filename], cmdname)
					data = data(*args, **kwargs)
			except StopIteration:
				exc = sys.exc_info()[1]
				channel.send((True, pickle.dumps(exc)))
			except Exception:
				exc = sys.exc_info()[1]
				channel.send((True, pickle.dumps(exc)))
			else:
				channel.send((False, data))
	"""

	def __init__(self, context, server, python=None, nice=None):
		# We don't have to store the context (this avoids cycles)
		self.server = server
		self.python = python
		self.nice = nice
		self._channel = None

	def close(self):
		if self._channel is not None and not self._channel.isclosed():
			self._channel.close()
			self._channel.gateway.exit()
			self._channel.gateway.join()

	def _url2filename(self, url):
		if url.scheme != "ssh":
			raise ValueError(f"URL {url!r} is not an ssh URL")
		filename = str(url.path)
		if filename.startswith("/~"):
			filename = filename[1:]
		return filename

	def _send(self, filename, cmd, *args, **kwargs):
		if self._channel is None:
			server = f"ssh={self.server}"
			python = self.python
			if python is None:
				python = default_ssh_python
			if python is not None:
				server += f"//python={python}"
			if self.nice is not None:
				server += f"//nice={self.nice}"
			gateway = execnet.makegateway(server) # This requires ``execnet`` (http://codespeak.net/execnet/)
			gateway.reconfigure(py2str_as_py3str=False, py3str_as_py2str=False)
			self._channel = gateway.remote_exec(self.remote_code)
		self._channel.send((filename, cmd, args, kwargs))
		(isexc, data) = self._channel.receive()
		if isexc:
			raise pickle.loads(data, fix_imports=True)
		else:
			return data

	def stat(self, url):
		filename = self._url2filename(url)
		data = self._send(filename, "stat")
		return os.stat_result(data) # channel returned a tuple => wrap it

	def lstat(self, url):
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

	def mkdir(self, url, mode=0o777):
		return self._send(self._url2filename(url), "mkdir", mode)

	def makedirs(self, url, mode=0o777):
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

	def _walk(self, cursor, base, name):
		def _event(url, event):
			cursor.url = url
			cursor.event = event
			cursor.isdir = event != "file"
			cursor.isfile = not cursor.isdir
			return cursor

		if name:
			fullname = os.path.join(base, name)
		else:
			fullname = base
		for (isdir, childname) in self._send(fullname, "listdir"):
			fullchildname = os.path.join(fullname, childname)
			relchildname = os.path.join(name, childname) if name else childname
			emitbeforedir = cursor.beforedir
			emitafterdir = cursor.afterdir
			emitfile = cursor.file
			enterdir = cursor.enterdir
			if isdir:
				if emitbeforedir or emitafterdir:
					dirurl = Dir(relchildname, scheme=None)
				if emitbeforedir:
					yield _event(dirurl, "beforedir")
					# The user may have altered ``cursor`` attributes outside the generator, so we refetch them
					emitbeforedir = cursor.beforedir
					emitafterdir = cursor.afterdir
					emitfile = cursor.file
					enterdir = cursor.enterdir
					cursor.restore()
				if enterdir:
					yield from self._walk(cursor, base, relchildname)
				if emitafterdir:
					yield _event(dirurl, "afterdir")
					cursor.restore()
			else:
				if emitfile:
					yield _event(File(relchildname, scheme=None), "file")
					cursor.restore()

	def walk(self, url, beforedir=True, afterdir=False, file=True, enterdir=True):
		cursor = Cursor(url, beforedir=beforedir, afterdir=afterdir, file=file, enterdir=enterdir)
		return self._walk(cursor, self._url2filename(url), "")

	def open(self, url, *args, **kwargs):
		return RemoteFileResource(self, url, *args, **kwargs)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__name__} to {self.server!r} at {id(self):#x}>"


class URLConnection(Connection):
	def mimetype(self, url):
		return url.open().mimetype()

	def size(self, url):
		return url.open().size()

	def imagesize(self, url):
		return url.open(mode="rb").imagesize()

	def mdate(self, url):
		return url.open(mode="rb").mdate()

	def resheaders(self, url):
		return url.open(mode="rb").resheaders()

	def isdir(self, url):
		# URLs never are directories (even if they might be (for URLs ending in ``/``), there's no way to call :meth:`listdir`)
		return False

	def open(self, url, mode="rb", headers=None, data=None):
		if mode != "rb":
			raise NotImplementedError(f"mode {mode!r} not supported")
		return URLResource(url, headers=headers, data=data)


def here(scheme="file"):
	"""
	Return the current directory as an :class:`URL` object.
	"""
	return Dir(os.getcwd(), scheme)


def home(user="", scheme="file"):
	"""
	Return the home directory of the current user (or the user named :obj:`user`,
	if :obj:`user` is specified) as an :class:`URL` object::

		>>> url.home()
		URL('file:/home/walter/')
		>>> url.home("andreas")
		URL('file:/home/andreas/')
	"""
	return Dir(f"~{user}", scheme)


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
	name = urllib.request.pathname2url(os.path.expanduser(name))
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
	name = urllib.request.pathname2url(os.path.expanduser(name))
	if name:
		if not name.endswith("/"):
			name += "/"
	else:
		name = "./"
	if name.startswith("///"):
		name = name[2:]
	url = URL(name)
	url.scheme = scheme
	return url


def Ssh(user, host, path="~/"):
	"""
	Return a ssh :class:`URL` for the user :obj:`user` on the host :obj:`host`
	with the path :obj:`path`.:obj:`path` (defaulting to the users home
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
	Return the first URL from :obj:`urls` that exists as a real file or
	directory. :const:`None` entries in :obj:`urls` will be skipped.
	"""
	for url in urls:
		if url is not None:
			if url.exists():
				return url


def firstdir(urls):
	"""
	Return the first URL from :obj:`urls` that exists as a real directory.
	:const:`None` entries in :obj:`urls` will be skipped.
	"""
	for url in urls:
		if url is not None:
			if url.isdir():
				return url


def firstfile(urls):
	"""
	Return the first URL from :obj:`urls` that exists as a real file.
	:const:`None` entries in :obj:`urls` will be skipped.
	"""
	for url in urls:
		if url is not None:
			if url.isfile():
				return url


class Resource(object):
	"""
	A :class:`Resource` is a base class that provides a file-like interface
	to local and remote files, URLs and other resources.

	Each resource object has the following attributes:

		:attr:`url`
			The URL for which this resource has been opened (i.e.
			``foo.open().url is foo`` if ``foo`` is a :class:`URL` object);

		:attr:`name`
			A string version of :attr:`url`;

		:attr:`closed`
			A :class:`bool` specifying whether the resource has been closed
			(i.e. whether the :meth:`close` method has been called).

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

	def __enter__(self):
		return self

	def __exit__(self, *exc_info):
		self.close()

	def __repr__(self):
		return f"<{'closed' if self.closed else 'open'} {self.__class__.__module__}.{self.__class__.__name__} {self.name}, mode {self.mode!r} at {id(self):#x}>"


class FileResource(Resource):
	"""
	A subclass of :class:`Resource` that handles local files.
	"""
	def __init__(self, url, mode="rb", *args, **kwargs):
		url = URL(url)
		self.name = os.path.expanduser(url.local())
		self.mode = mode
		try:
			file = open(self.name, mode, *args, **kwargs)
		except IOError as exc:
			if "w" not in mode or exc.errno != 2: # didn't work for some other reason than a non existing directory
				raise
			(splitpath, splitname) = os.path.split(self.name)
			if splitpath:
				os.makedirs(splitpath)
				file = open(self.name, mode, *args, **kwargs)
			else:
				raise # we don't have a directory to make so pass the error on
		self.file = file
		self.url = url

	def __getattr__(self, name):
		return getattr(self.file, name)

	def __iter__(self):
		return iter(self.file)

	def close(self):
		if self.file is not None:
			self.file.close()
			self.file = None

	@property
	def closed(self):
		return self.file is None

	def size(self):
		# Forward to the connection
		return LocalSchemeDefinition._connection.size(self.url)

	def mdate(self):
		# Forward to the connection
		return LocalSchemeDefinition._connection.mdate(self.url)

	def mimetype(self):
		# Forward to the connection
		return LocalSchemeDefinition._connection.mimetype(self.url)


class RemoteFileResource(Resource):
	"""
	A subclass of :class:`Resource` that handles remote files (those using
	the ``ssh`` scheme).
	"""
	def __init__(self, connection, url, mode="rb", *args, **kwargs):
		self.connection = connection
		self.url = URL(url)
		self.mode = mode
		self.args = args
		self.kwargs = kwargs
		filename = self.connection._url2filename(url)
		self.name = str(self.url)
		self.remoteid = self._send(filename, "open", mode, *args, **kwargs)

	def __repr__(self):
		return f"<{'closed' if self.connection is None else 'open'} {self.__class__.__module__}.{self.__class__.__name__} {self.name}, mode {self.mode!r} at {id(self):#x}>"

	def _send(self, filename, cmd, *args, **kwargs):
		if self.connection is None:
			raise ValueError("I/O operation on closed file")
		return self.connection._send(filename, cmd, *args, **kwargs)

	def close(self):
		if self.connection is not None:
			self._send(self.remoteid, "close")
			self.connection = None # close the channel too as there are no longer any meaningful operations

	@property
	def closed(self):
		return self.connection is None

	def read(self, size=None):
		return self._send(self.remoteid, "read", size) if size is not None else self._send(self.remoteid, "read")

	def readline(self, size=-1):
		return self._send(self.remoteid, "readline", size) if size is not None else self._send(self.remoteid, "readline")

	def readlines(self, size=-1):
		return self._send(self.remoteid, "readlines", size) if size is not None else self._send(self.remoteid, "readlines")

	def __iter__(self):
		return self

	def __next__(self):
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
			raise ValueError(f"writing mode {mode!r} not supported")
		self.url = URL(url)
		self.name = str(self.url)
		self.mode = mode
		self.reqheaders = headers
		self.reqdata = data
		self._finalurl = None
		if data is not None:
			data = urlparse.urlencode(data)
		if headers is None:
			headers = {}
		req = urllib.request.Request(url=self.name, data=data, headers=headers)
		self._stream = urllib.request.urlopen(req)
		self._finalurl = URL(self._stream.url) # Remember the final URL in case of a redirect
		self._resheaders = self._stream.info()
		self._mimetype = None
		self._encoding = None
		contenttype = self._resheaders.get("Content-Type")
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
		self._buffer = io.BytesIO()

	def __getattr__(self, name):
		function = getattr(self._stream, name)
		def call(*args, **kwargs):
			return function(*args, **kwargs)
		return call

	def close(self):
		if self._stream is not None:
			self._stream.close()
			self._stream = None

	@property
	def closed(self):
		return self._stream is None

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

	def read(self, size=None):
		data = self._stream.read(size) if size is not None else self._stream.read()
		self._buffer.write(data)
		return data

	def readline(self, size=None):
		data = self._stream.readline(size) if size is not None else self._stream.readline()
		self._buffer.write(data)
		return data

	def resdata(self):
		data = self._stream.read()
		self._buffer.write(data)
		return self._buffer.getvalue()

	def imagesize(self):
		img = Image.open(io.BytesIO(self.resdata())) # Requires PIL
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

		*	:obj:`scheme`: The name of the scheme;

		*	:obj:`usehierarchy`: Specifies whether this scheme uses hierarchical
			URLs or opaque URLs (i.e. whether ``hier_part`` or ``opaque_part``
			from the BNF in :rfc:`2396` is used);

		*	:obj:`useserver`: Specifies whether this scheme uses an Internet-based
			server :attr:`authority` component or a registry of naming authorities
			(only for hierarchical URLs);

		*	:obj:`usefrag`: Specifies whether this scheme uses fragments
			(according to the BNF in :rfc:`2396` every scheme does, but it doesn't
			make sense for e.g. ``"javascript"``, ``"mailto"`` or ``"tel"``);

		*	:obj:`islocal`: Specifies whether URLs with this scheme refer to
			local files;

		*	:obj:`isremote`: Specifies whether URLs with this scheme refer to
			remote files (there may be schemes which are neither local nor remote,
			e.g. ``"mailto"``);

		*	:obj:`defaultport`: The default port for this scheme (only for schemes
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
		Create a :class:`Connection` for the :class:`URL` :obj:`url` (which must
		have :obj:`self` as the scheme).
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
		Close all connections active for this scheme in the context :obj:`context`.
		"""

	def __repr__(self):
		return f"<{self.__class__.__name__} instance scheme={self.scheme!r} usehierarchy={self.usehierarchy!r} useserver={self.useserver!r} usefrag={self.usefrag!r} at {id(self):#x}>"


class LocalSchemeDefinition(SchemeDefinition):
	# Use a different connection than the base class (but still one single connection for all URLs)
	_connection = LocalConnection()

	def open(self, *args, **kwargs):
		return FileResource(*args, **kwargs)


class SshSchemeDefinition(SchemeDefinition):
	def _connect(self, url, context=None, **kwargs):
		if "python" in kwargs or "nice" in kwargs:
			kwargs = kwargs.copy()
			python = kwargs.pop("python", None)
			nice = kwargs.pop("nice", None)
		else:
			python = None
			nice = None

		context = getcontext(context)
		if context is threadlocalcontext.__class__.context:
			raise ValueError("ssh URLs need a custom context")
		# Use one :class:`SshConnection` for each user/host/python combination
		server = url.server
		try:
			connections = context.schemes["ssh"]
		except KeyError:
			connections = context.schemes["ssh"] = {}
		try:
			connection = connections[(server, python, nice)]
		except KeyError:
			connection = connections[(server, python, nice)] = SshConnection(context, server, python, nice)
		return (connection, kwargs)

	def open(self, url, mode="rb", context=None, python=None, nice=None):
		(connection, kwargs) = self._connect(url, context=context, python=python, nice=nice)
		return RemoteFileResource(connection, url, mode, **kwargs)

	def closeall(self, context):
		for connection in context.schemes["ssh"].values():
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

	def _prefix(cls, path):
		if path.startswith("/"):
			return "/"
		else:
			return ""

	def insert(self, index, *others):
		segments = self.segments
		segments[index:index] = map(_unescape, others)
		self.segments = segments

	def startswith(self, prefix):
		"""
		Return whether :obj:`self` starts with the path :obj:`prefix`.
		:obj:`prefix` will be converted to a :class:`Path` if it isn't one.
		"""
		if not isinstance(prefix, Path):
			prefix = Path(prefix)
		segments = prefix.segments
		if self.isabs != prefix.isabs:
			return False
		if segments and not segments[-1] and len(self.segments) > len(segments):
			return self.segments[:len(segments)-1] == segments[:-1]
		else:
			return self.segments[:len(segments)] == segments

	def endswith(self, suffix):
		"""
		Return whether :obj:`self` ends with the path :obj:`suffix`. :obj:`suffix`
		will be converted to a :class:`Path` if it isn't one. If :obj:`suffix` is
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
		return f"Path({self._path!r})"

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
		if isinstance(index, slice):
			# Return of slice of the path. The resulting path will always be relative, i.e. the leading ``/`` will be dropped.
			return Path(self.segments[index])
		else:
			return self.segments[index]

	def __setitem__(self, index, value):
		segments = self.segments
		if isinstance(index, slice):
			segments[index] = map(_unescape, value)
			self._path = self._prefix(self._path) + self._segments2path(segments)
		else:
			segments[index] = _unescape(value)
			self._path = self._prefix(self._path) + self._segments2path(segments)
		self._segments = segments

	def __delitem__(self, index):
		if isinstance(index, slice):
			del self.segments[index]
		else:
			segments = self.segments
			del segments[index]
			self._path = self._segments2path(segments)
			self._segments = segments

	def __contains__(self, item):
		return _unescape(item) in self.segments

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
		return "/".join(_escape(segment, pathsafe) for segment in segments)

	@classmethod
	def _path2segments(cls, path):
		if path.startswith("/"):
			path = path[1:]
		return list(map(_unescape, path.split("/")))

	def _setpathorsegments(self, path):
		if path is None:
			self._path = ""
			self._segments = []
		elif isinstance(path, Path):
			self._path = path._path
			self._segments = None
		elif isinstance(path, (list, tuple)):
			self._segments = list(map(_unescape, path))
			self._path = self._prefix(self._path) + self._segments2path(self._segments)
		else:
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
		of :attr:`path`. The ``baz.html`` part of
		``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			try:
				return self[-1]
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
				self[-1] = file
			else:
				self.segments = [file]

		def __delete__(self):
			"""
			Deleting the filename preserves the parameter in the last segment.
			"""
			segments = self.segments
			if segments:
				self[-1] = ""

	class ext(misc.propclass):
		"""
		The filename extension of the last segment of the path. The ``html`` part
		of ``http://user@www.example.com/bar/baz.html;xyzzy?spam=eggs#frag``.
		"""
		def __get__(self):
			ext = None
			segments = self.segments
			if segments:
				segment = segments[-1]
				pos = segment.rfind(".")
				if pos != -1:
					ext = segment[pos+1:]
			return ext

		def __set__(self, ext):
			if ext is None:
				del self.ext
			segments = self.segments
			if segments:
				segment = segments[-1]
				pos = segment.rfind(".")
				if pos != -1:
					segment = segment[:pos+1] + ext
				else:
					segment = segment + "." + ext
				self[-1] = segment

		def __delete__(self):
			segments = self.segments
			if segments:
				segment = segments[-1]
				pos = segment.rfind(".")
				if pos != -1:
					segment = segment[:pos]
					self[-1] = segment

	def withext(self, ext):
		"""
		Return a new :class:`Path` where the filename extension has been replaced
		with :obj:`ext`.
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
		component of :attr:`segments`) has been replaced with :obj:`file`.
		"""
		path = self.clone()
		path.file = file
		return path

	def withoutfile(self):
		"""
		Return a new :class:`Path` where the filename (i.e. the name of the last
		component of :attr:`segments`) has been removed.
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

	def __truediv__(self, other):
		"""
		Join two paths.
		"""
		if isinstance(other, str):
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

	def __rtruediv__(self, other):
		"""
		Right hand version of :meth:`__div__`. This supports list and generators
		as the left hand side too.
		"""
		if isinstance(other, str):
			other = Path(other)
		if isinstance(other, Path):
			return other/self
		elif isinstance(other, (list, tuple)):
			return other.__class__(path/self for path in other)
		else:
			return (path/self for path in other)

	def relative(self, basepath):
		"""
		Return an relative :class:`Path` :obj:`rel` such that
		``basepath/rel == self``, i.e. this is the inverse operation of
		:meth:`__div__`.

		If :obj:`self` is relative, an identical copy of :obj:`self` will be
		returned.
		"""
		# if :obj:`self` is relative don't do anything
		if not self.isabs:
			pass # FIXME return self.clone()
		basepath = Path(basepath) # clone/coerce
		self_segments = _normalizepath(self.segments)
		base_segments = _normalizepath(basepath.segments)
		while len(self_segments) > 1 and len(base_segments) > 1 and self_segments[0] == base_segments[0]:
			del self_segments[0]
			del base_segments[0]
		# build a path from one file to the other
		self_segments[:0] = [".."]*(len(base_segments)-1)
		if not len(self_segments) or self_segments == [""]:
			self_segments = [".", ""]
		return Path(self._segments2path(self_segments))

	def reverse(self):
		segments = self.segments
		segments.reverse()
		if segments and not segments[0]:
			del segments[0]
			segments.append("")
		self.segments = segments

	def normalize(self):
		self.segments = _normalizepath(self.segments)

	def normalized(self):
		new = self.clone()
		new.normalize()
		return new

	def local(self):
		"""
		Return :obj:`self` converted to a filename using the file naming
		conventions of the OS. Parameters will be dropped in the resulting string.
		"""
		localpath = _unescape(self._path)
		if self._path.endswith("/") and not (localpath.endswith(os.sep) or (os.altsep is not None and localpath.endswith(os.altsep))):
			localpath += os.sep
		return localpath

	def abs(self):
		"""
		Return an absolute version of :obj:`self`.
		"""
		path = os.path.abspath(self.local())
		path = path.rstrip(os.sep)
		if path.startswith("///"):
			path = path[2:]
		path = urllib.request.pathname2url(path)
		if len(self) and not self.segments[-1]:
			path += "/"
		return Path(path)

	def real(self):
		"""
		Return the canonical version of :obj:`self`, eliminating all symbolic
		links.
		"""
		path = os.path.realpath(self.local())
		path = path.rstrip(os.sep)
		path = urllib.request.pathname2url(path)
		if path.startswith("///"):
			path = path[2:]
		if len(self) and not self.segments[-1]:
			path += "/"
		return Path(path)


class Query(dict):
	__slots__ = ()

	def __init__(self, arg=None, **kwargs):
		if arg is not None:
			if isinstance(arg, dict):
				for (key, value) in arg.items():
					self.add(key, value)
			else:
				for (key, value) in arg:
					self.add(key, value)
		for (key, value) in kwargs.items():
			self.add(key, value)

	def __setitem__(self, key, value):
		dict.__setitem__(self, str(key), [str(value)])

	def add(self, key, *values):
		key = str(key)
		values = map(str, values)
		self.setdefault(key, []).extend(values)


class URL(object):
	"""
	An :rfc:`2396` compliant URL.
	"""
	def __init__(self, url=None):
		"""
		Create a new :class:`URL` instance. :obj:`url` may be a :class:`str`
		object, or an :class:`URL` (in which case you'll get a copy of :obj:`url`),
		or :const:`None` (which will create an :class:`URL` referring to the
		"current document").
		"""
		self.url = url

	def _clear(self):
		# internal helper method that makes :obj:`self` empty.
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
		Return an identical copy :obj:`self`.
		"""
		return URL(self)

	@staticmethod
	def _checkscheme(scheme):
		# Check whether :obj:`scheme` contains only legal characters.
		if not scheme or scheme[0] not in schemecharfirst:
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
			The scheme will be converted to lowercase on setting (if :obj:`scheme`
			is not :const:`None`, otherwise the scheme will be deleted).
			"""
			if scheme is None:
				self._scheme = None
			else:
				scheme = scheme.lower()
				# check if the scheme only has allowed characters
				if not self._checkscheme(scheme):
					raise ValueError(f"Illegal scheme char in scheme {scheme!r}")
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
					hostport += f":{self.port}"
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
			Setting the server always works even if the current :attr:`scheme`
			does use :attr:`opaque_part` or :attr:`reg_name` but will be ignored
			when reassembling the URL for the :attr:`url` property.
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
		a name based :attr:`authority` instead of :attr:`server`.
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
		Depending on the scheme, this is either :attr:`server` or
		:attr:`reg_name`.
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
		absolute if an :attr:`authority` is specified.
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
		of :attr:`path`. The ``baz.html`` part of
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
				for part in query.split("&"):
					namevalue = part.split("=", 1)
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
			Getting :attr:`url` reassembles the URL from the components.
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
			Setting :attr:`url` parses :obj:`url` into the components. :obj:`url`
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
						if pos != -1:
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
		with :obj:`ext`.
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
		component of :attr:`path_segments`) has been replaced with
		:obj:`file`.
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
		:obj:`frag`.
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

	def __truediv__(self, other):
		"""
		Join :obj:`self` with another (possible relative) :class:`URL`
		:obj:`other`, to form a new :class:`URL`.

		:obj:`other` may be a :class:`str` or :class:`URL` object. It may be
		:const:`None` (referring to the "current document") in which case
		:obj:`self` will be returned. It may also be a list or other iterable.
		For this case a list (or iterator) will be returned where
		:meth:`__div__` will be applied to every item in the list/iterator. E.g.
		the following expression returns all the files in the current directory
		as absolute URLs (see the method :meth:`files` and the function
		:func:`here` for further explanations)::

			>>> here = url.here()
			>>> for f in here/here.files():
			... 	print(f)
		"""
		if isinstance(other, str):
			other = URL(other)
		if isinstance(other, URL):
			newurl = URL()
			# RFC2396, Section 5.2 (2)
			if other.scheme is None and other.authority is None and not str(other.path) and other.query is None:
				newurl = URL(self)
				newurl.frag = other.frag
				return newurl
			if not self.reg.usehierarchy: # e.g. "mailto:x@y"/"file:foo"
				return other
			# In violation of RFC2396 we treat file URLs as relative ones (if the base is a local URL)
			if other.scheme == "file" and self.islocal():
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

	def __rtruediv__(self, other):
		"""
		Right hand version of :meth:`__div__`. This supports lists and iterables
		as the left hand side too.
		"""
		if isinstance(other, str):
			other = URL(other)
		if isinstance(other, URL):
			return other/self
		elif isinstance(other, (list, tuple)):
			return other.__class__(item/self for item in other)
		else:
			return (item/self for item in other)

	def relative(self, baseurl, allowschemerel=False):
		"""
		Return an relative :class:`URL` :obj:`rel` such that
		``baseurl/rel == self``, i.e. this is the inverse operation of
		:meth:`__div__`.

		If :obj:`self` is relative, has a different :attr:`scheme` or
		:attr:`authority` than :obj:`baseurl` or a non-hierarchical scheme, an
		identical copy of :obj:`self` will be returned.

		If :obj:`allowschemerel` is true, scheme relative URLs are allowed, i.e.
		if both :obj:`self` and :obj:`baseurl` use the same hierarchical scheme,
		but a different authority (i.e. server), a scheme relative url
		(``//server/path/file.html``) will be returned.
		"""
		# if :obj:`self` is relative don't do anything
		if self.scheme is None:
			return URL(self)
		# javascript etc.
		if not self.reg.usehierarchy:
			return URL(self)
		baseurl = URL(baseurl) # clone/coerce
		newurl = URL(self) # clone
		# only calculate a new URL if to the same scheme/server, else use the original (or a scheme relative one)
		if self.authority != baseurl.authority:
			if self.scheme == baseurl.scheme and allowschemerel:
				del newurl.scheme
			return newurl
		elif self.scheme != baseurl.scheme:
			return newurl
		del newurl.scheme
		del newurl.authority
		selfpath_segments = _normalizepath(self._path.segments)
		basepath_segments = _normalizepath(baseurl._path.segments)
		while len(selfpath_segments) > 1 and len(basepath_segments) > 1 and selfpath_segments[0] == basepath_segments[0]:
			del selfpath_segments[0]
			del basepath_segments[0]
		# does the URL go to the same file?
		if selfpath_segments == basepath_segments and self.query == baseurl.query:
			# only return the frag
			del newurl.path
			del newurl.query
		else:
			# build a path from one file to the other
			selfpath_segments[:0] = [".."]*(len(basepath_segments)-1)
			if not len(selfpath_segments) or selfpath_segments == [""]:
				selfpath_segments = [".", ""]
			newurl._path.segments = selfpath_segments
			newurl._path = self.path.relative(baseurl.path)
		newurl._path.isabs = False
		return newurl

	def __str__(self):
		return self.url

	def __repr__(self):
		return f"URL({self.url!r})"

	def __bool__(self):
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
		return not self == other

	def __hash__(self):
		"""
		Return a hash value for :obj:`self`, to be able to use :class:`URL`
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
		Return an absolute version of :obj:`self` (works only for local URLs).

		If the argument :obj:`scheme` is specified, it will be used for the
		resulting URL otherwise the result will have the same scheme as
		:obj:`self`.
		"""
		self._checklocal()
		new = self.clone()
		new.path = self.path.abs()
		if scheme != -1:
			new.scheme = scheme
		return new

	def real(self, scheme=-1):
		"""
		Return the canonical version of :obj:`self`, eliminating all symbolic
		links (works only for local URLs).

		If the argument :obj:`scheme` is specified, it will be used for the
		resulting URL otherwise the result will have the same scheme as
		:obj:`self`.
		"""
		self._checklocal()
		new = self.clone()
		new.path = self.path.real()
		if scheme != -1:
			new.scheme = scheme
		return new

	def islocal(self):
		"""
		Return whether :obj:`self` refers to a local file, i.e. whether
		:obj:`self` is a relative :class:`URL` or the scheme is ``root`` or
		``file``).
		"""
		return self.reg.islocal

	def _checklocal(self):
		if not self.islocal():
			raise ValueError(f"URL {self!r} is not local")

	def local(self):
		"""
		Return :obj:`self` as a local filename (which will only works if
		:obj:`self` is local (see :meth:`islocal`).
		"""
		self._checklocal()
		return self.path.local()

	def _connect(self, context=None, **kwargs):
		return self.reg._connect(self, context=context, **kwargs)

	def connect(self, context=None, **kwargs):
		"""
		Return a :class:`Connection` object for accessing and modifying the
		metadata of :obj:`self`.

		Whether you get a new connection object, or an existing one depends on
		the scheme, the URL itself, and the context passed in (as the
		:obj:`context` argument).
		"""
		return self._connect(context, **kwargs)[0]

	def open(self, *args, **kwargs):
		"""
		Open :obj:`self` for reading or writing. :meth:`open` returns a
		:class:`Resource` object.

		Which additional parameters are supported depends on the actual resource
		created. Some common parameters are:

			:obj:`mode` (supported by all resources)
				A string indicating how the file is to be opened (just like the
				mode argument for the builtin :func:`open`; e.g. ``"rb"`` or
				``"wb"``).

			:obj:`context` (supported by all resources)
				:meth:`open` needs a :class:`Connection` for this URL which it gets
				from a :class:`Context` object.

			:obj:`headers`
				Additional headers to use for an HTTP request.

			:obj:`data`
				Request body to use for an HTTP POST request.

			:obj:`python`
				Name of the Python interpreter to use on the remote side
				(used by ``ssh`` URLs)

			:obj:`nice`
				Nice level for the remove python (used by ``ssh`` URLs)
		"""
		(connection, kwargs) = self._connect(**kwargs)
		if "context" in kwargs:
			kwargs = kwargs.copy()
			del kwargs["context"]
		return connection.open(self, *args, **kwargs)

	def openread(self, *args, **kwargs):
		return self.open(mode="rb", *args, **kwargs)

	def openwrite(self, *args, **kwargs):
		return self.open(mode="wb", *args, **kwargs)

	def import_(self, name=None):
		"""
		Import the content of the URL :obj:`self` as a Python module.

		:obj:`name` can be used the specify the module name (i.e. the ``__name__``
		attribute of the module). The default determines it from the URL.
		"""
		if self.islocal():
			filename = self.real().local()
		else:
			filename = f"/{self.scheme}/{self.server}{self.path}"
		return misc.module(self.openread().read(), filename, name)

	def __iter__(self):
		try:
			isdir = self.isdir()
		except AttributeError:
			isdir = False
		if isdir:
			return iter(self/self.listdir())
		else:
			return iter(self.open())

	# All the following methods need a connection and simply forward the operation to the connection
	def stat(self, **kwargs):
		return self.connect(**kwargs).stat(self)

	def lstat(self, **kwargs):
		return self.connect(**kwargs).lstat(self)

	def chmod(self, mode, **kwargs):
		return self.connect(**kwargs).chmod(self, mode)

	def chown(self, owner=None, group=None, **kwargs):
		return self.connect(**kwargs).chown(self, owner=owner, group=group)

	def lchown(self, owner=None, group=None, **kwargs):
		return self.connect(**kwargs).lchown(self, owner=owner, group=group)

	def uid(self, **kwargs):
		return self.connect(**kwargs).uid(self)

	def gid(self, **kwargs):
		return self.connect(**kwargs).gid(self)

	def owner(self, **kwargs):
		return self.connect(**kwargs).owner(self)

	def group(self, **kwargs):
		return self.connect(**kwargs).group(self)

	def mimetype(self, **kwargs):
		return self.connect(**kwargs).mimetype(self)

	def exists(self, **kwargs):
		return self.connect(**kwargs).exists(self)

	def isfile(self, **kwargs):
		return self.connect(**kwargs).isfile(self)

	def isdir(self, **kwargs):
		return self.connect(**kwargs).isdir(self)

	def islink(self, **kwargs):
		return self.connect(**kwargs).islink(self)

	def ismount(self, **kwargs):
		return self.connect(**kwargs).ismount(self)

	def access(self, mode, **kwargs):
		return self.connect(**kwargs).access(self, mode)

	def size(self, **kwargs):
		return self.connect(**kwargs).size(self)

	def imagesize(self, **kwargs):
		return self.connect(**kwargs).imagesize(self)

	def cdate(self, **kwargs):
		return self.connect(**kwargs).cdate(self)

	def adate(self, **kwargs):
		return self.connect(**kwargs).adate(self)

	def mdate(self, **kwargs):
		return self.connect(**kwargs).mdate(self)

	def resheaders(self, **kwargs):
		return self.connect(**kwargs).resheaders(self)

	def remove(self, **kwargs):
		return self.connect(**kwargs).remove(self)

	def rmdir(self, **kwargs):
		return self.connect(**kwargs).rmdir(self)

	def rename(self, target, **kwargs):
		return self.connect(**kwargs).rename(self, target)

	def link(self, target, **kwargs):
		return self.connect(**kwargs).link(self, target)

	def symlink(self, target, **kwargs):
		return self.connect(**kwargs).symlink(self, target)

	def chdir(self, **kwargs):
		return self.connect(**kwargs).chdir(self)

	def mkdir(self, mode=0o777, **kwargs):
		return self.connect(**kwargs).mkdir(self, mode=mode)

	def makedirs(self, mode=0o777, **kwargs):
		return self.connect(**kwargs).makedirs(self, mode=mode)

	def walk(self, beforedir=True, afterdir=False, file=True, enterdir=True, **kwargs):
		return self.connect(**kwargs).walk(self, beforedir=beforedir, afterdir=afterdir, file=file, enterdir=enterdir)

	def listdir(self, include=None, exclude=None, ignorecase=False, **kwargs):
		return self.connect(**kwargs).listdir(self, include=include, exclude=exclude, ignorecase=ignorecase)

	def files(self, include=None, exclude=None, ignorecase=False, **kwargs):
		return self.connect(**kwargs).files(self, include=include, exclude=exclude, ignorecase=ignorecase)

	def dirs(self, include=None, exclude=None, ignorecase=False, **kwargs):
		return self.connect(**kwargs).dirs(self, include=include, exclude=exclude, ignorecase=ignorecase)

	def walkall(self, include=None, exclude=None, enterdir=None, skipdir=None, ignorecase=False, **kwargs):
		return self.connect(**kwargs).walkall(self, include=include, exclude=exclude, enterdir=enterdir, skipdir=skipdir, ignorecase=ignorecase)

	def walkfiles(self, include=None, exclude=None, enterdir=None, skipdir=None, ignorecase=False, **kwargs):
		return self.connect(**kwargs).walkfiles(self, include=include, exclude=exclude, enterdir=enterdir, skipdir=skipdir, ignorecase=ignorecase)

	def walkdirs(self, include=None, exclude=None, enterdir=None, skipdir=None, ignorecase=False, **kwargs):
		return self.connect(**kwargs).walkdirs(self, include=include, exclude=exclude, enterdir=enterdir, skipdir=skipdir, ignorecase=ignorecase)

warnings.filterwarnings("always", module="url")
