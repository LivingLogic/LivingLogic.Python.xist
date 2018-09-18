# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

"""
This module provides a class :class:`Call` that allows you to use Oracle PL/SQL
procedures/functions as CherryPy__ response handlers. A :class:`Call` objects
wraps a :class:`ll.orasql.Procedure` or :class:`ll.orasql.Function` object from
the :mod:`ll.orasql` module.

__ http://www.cherrypy.org/

For example, you might have the following PL/SQL function:

.. sourcecode:: sql

	create or replace function helloworld
	(
		who varchar2
	)
	return varchar2
	as
	begin
		return '<html><head><h>Hello ' || who || '</h></head><body><h1>Hello, ' || who || '!</h1></body></html>';
	end;

Using this function as a CherryPy response handler can be done like this:

.. sourcecode:: python

	import cherrypy

	from ll import orasql, nightshade

	proc = nightshade.Call(orasql.Function("helloworld"), connectstring="user/pwd")

	class HelloWorld:
		@cherrypy.expose
		def default(self, who="World"):
			cherrypy.response.headers["Content-Type"] = "text/html"
			return proc(who=who)

	cherrypy.quickstart(HelloWorld())
"""

import time, datetime, functools

import cherrypy

from ll import orasql


__docformat__ = "reStructuredText"


weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
monthname = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class UTC(datetime.tzinfo):
	"""
	Timezone object for UTC
	"""
	def utcoffset(self, dt):
		return datetime.timedelta(0)

	def dst(self, dt):
		return datetime.timedelta(0)

	def tzname(self, dt):
		return "UTC"

utc = UTC()


def getnow():
	"""
	Get the current date and time as a :class:`datetime.datetime` object in UTC
	with timezone info.
	"""
	return datetime.datetime.utcnow().replace(tzinfo=utc)


def httpdate(dt):
	"""
	Return a string suitable for a "Last-Modified" and "Expires" header.

	:obj:`dt` is a :class:`datetime.datetime` object. If ``:obj:`dt`.tzinfo`` is
	:const:`None` :obj:`dt` is assumed to be in the local timezone (using the
	current UTC offset which might be different from the one used by :obj:`dt`).
	"""
	if dt.tzinfo is None:
		dt += datetime.timedelta(seconds=[time.timezone, time.altzone][time.daylight])
	else:
		dt -= dt.tzinfo.utcoffset(dt)
	return f"{weekdayname[dt.weekday()]}, {dt.day:02d} {monthname[dt.month]:3s} {dt.year:4d} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d} GMT"


class Connect:
	"""
	:class:`Connect` objects can be used as decorators that wraps a function
	that needs a database connection.

	If calling the wrapped function results in a database exception that has
	been caused by a lost connection to the database or similar problems,
	the function is retried with a new database connection.
	"""
	_badoracleexceptions = {
		28,    # your session has been killed
		1012,  # not logged on
		1014,  # Oracle shutdown in progress
		1033,  # Oracle startup or shutdown in progress
		1034,  # Oracle not available
		1035,  # Oracle only available to users with RESTRICTED SESSION privilege
		1089,  # immediate shutdown in progress - no operations are permitted
		1090,  # Shutdown in progress - connection is not permitted
		1092,  # ORACLE instance terminated. Disconnection forced
		3106,  # fatal two-task communication protocol error
		3113,  # end-of-file on communication channel
		3114,  # not connected to ORACLE
		3135,  # connection lost contact
		12154, # TNS:could not resolve the connect identifier specified
		12540, # TNS:internal limit restriction exceeded
		12541, # TNS:no listener
		12543, # TNS:destination host unreachable
	}

	def __init__(self, connectstring=None, pool=None, retry=3, **kwargs):
		"""
		Create a new parameterized :class:`Connect` decorator. Either
		:obj:`connectstring` or :obj:`pool` (a database pool object) must be
		specified. :obj:`retry` specifies how often to retry calling the wrapped
		function after a database exception. :obj:`kwargs` will be passed on to
		the :func:`connect` call.
		"""
		if (connectstring is not None) == (pool is not None):
			raise TypeError("either connectstring or pool must be specified")
		self.pool = pool
		self._connection = None
		self.connectstring = connectstring
		self.retry = retry
		self.kwargs = kwargs

	def _isbadoracleexception(self, exc):
		try:
			code = getattr(exc.args[0], "code", 0)
		except Exception:
			return False
		else:
			return code in self._badoracleexceptions

	def _getconnection(self):
		if self.pool is not None:
			return self.pool.acquire()
		elif self._connection is None:
			self._connection = orasql.connect(self.connectstring, threaded=True, **self.kwargs)
		return self._connection

	def _dropconnection(self, connection):
		if self.pool is not None:
			self.pool.drop(connection)
		else:
			self._connection = None

	def cursor(self, **kwargs):
		connection = self._getconnection()
		return connection.cursor(**kwargs)

	def commit(self):
		self._getconnection().commit()

	def rollback(self):
		self._getconnection().rollback()

	def close(self):
		connection = self._getconnection()
		connection.close()
		self._dropconnection(connection)

	def cancel(self):
		self._getconnection().cancel()

	def __call__(self, func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			for i in range(self.retry):
				connection = self._getconnection()
				try:
					# This only works if func is using the same connection
					return func(*args, **kwargs)
				except orasql.OperationalError as exc:
					if i < self.retry-1:
						# Drop bad connection and retry
						self._dropconnection(connection)
					else:
						raise
				except orasql.DatabaseError as exc:
					if i < self.retry-1 and self._isbadoracleexception(exc):
						# Drop bad connection and retry
						self._dropconnection(connection)
					else:
						raise
		return wrapper


class Call:
	"""
	Wrap an Oracle procedure or function in a CherryPy handler.

	A :class:`Call` object wraps a procedure or function object from
	:mod:`ll.orasql` and makes it callable just like a CherryPy handler.
	"""
	def __init__(self, callable, connection):
		"""
		Create a :class:`Call` object wrapping the function or procedure
		:obj:`callable`.
		"""
		self.callable = callable
		# Calculate parameter mapping now, so we don't get concurrency problems later
		self.connection = connection
		callable._calcargs(connection.cursor())

	def __call__(self, *args, **kwargs):
		"""
		Call the procedure/function with the arguments :obj:`args` and
		:obj:`kwargs` mapping Python function arguments to
		Oracle procedure/function arguments. On return from the procedure the
		:obj:`c_out` parameter is mapped to the CherryPy response body, and the
		parameters :obj:`p_expires` (the number of days from now),
		:obj:`p_lastmodified` (a date in UTC), :obj:`p_mimetype` (a string),
		:obj:`p_encoding` (a string), :obj:`p_etag` (a string) and
		:obj:`p_cachecontrol` (a string) are mapped to the appropriate CherryPy
		response headers. If :obj:`p_etag` is not specified a value is calculated.

		If the procedure/function raised a PL/SQL exception with a code between
		20200 and 20599, 20000 will be subtracted from this value and the
		resulting value will be used as the HTTP response code, i.e. 20404 will
		give a "Not Found" response.
		"""

		@self.connection
		def call(*args, **kwargs):
			cursor = self.connection.cursor()
			try:
				if isinstance(self.callable, orasql.Procedure):
					result = (None, self.callable(cursor, *args, **kwargs))
				else:
					result = self.callable(cursor, *args, **kwargs)
				cursor.connection.commit()
				return result
			except orasql.DatabaseError as exc:
				if exc.args:
					code = getattr(exc[0], "code", 0)
					if 20200 <= code <= 20599:
						raise cherrypy.HTTPError(code-20000)
					else:
						raise

		now = getnow()
		(body, result) = call(*args, **kwargs)

		# Get response body
		if "c_out" in result:
			body = result.c_out
		if hasattr(body, "read"):
			body = body.read()

		# Set HTTP headers from parameters
		expires = result.get("p_expires", None)
		if expires is not None:
			cherrypy.response.headers["Expires"] = httpdate(now + datetime.timedelta(days=expires))
		lastmodified = result.get("p_lastmodified", None)
		if lastmodified is not None:
			cherrypy.response.headers["Last-Modified"] = httpdate(lastmodified)
		mimetype = result.get("p_mimetype", None)
		if mimetype is None:
			mimetype = "text/html" if isinstance(body, str) else "application/octet-stream"

		encoding = result.get("p_encoding", None)
		if encoding is None and isinstance(body, str):
			encoding = "utf-8"
		if encoding is not None:
			cherrypy.response.headers["Content-Type"] = f"{mimetype}; charset={encoding}"
		else:
			cherrypy.response.headers["Content-Type"] = mimetype
		hasetag = False
		etag = result.get("p_etag", None)
		if etag is not None:
			cherrypy.response.headers["ETag"] = etag
			hasetag = True
		cachecontrol = result.get("p_cachecontrol", None)
		if cachecontrol is not None:
			cherrypy.response.headers["Cache-Control"] = cachecontrol

		# Get status code
		status = result.get("p_status", None)
		if status is not None:
			cherrypy.response.status = status

		# Set ETag
		if not hasetag:
			cherrypy.response.headers["ETag"] = f'"{hash(body):x}"'

		if isinstance(body, str):
			body = body.encode(encoding)
		return body
