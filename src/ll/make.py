# -*- coding: utf-8 -*-
# cython: language_level=3, always_allow_keywords=True

## Copyright 2002-2019 by LivingLogic AG, Bayreuth/Germany
## Copyright 2002-2019 by Walter Dörwald
##
## All Rights Reserved
##
## See ll/xist/__init__.py for the license


"""
:mod:`!ll.make` provides tools for building projects.

Like make it allows you to specify dependencies between files and actions to be
executed when files don't exist or are out of date with respect to one of their
sources. But unlike make you can do this in an object oriented way and targets
are not only limited to files.

Relevant classes are:

*	:class:`Project`, which is the container for all actions in a project and

*	:class:`Action` (and subclasses), which are used to transform input data
	and read and write files (or other entities like database records).

A simple script that copies a file :file:`foo.txt` to :file:`bar.txt`
reencoding it from ``"latin-1"`` to ``"utf-8"`` in the process looks like
this:

.. sourcecode:: python

	from ll import make

	class MyProject(make.Project):
		name = "Acme.MyProject"

		def create(self):
			make.Project.create(self)
			source = self.add(make.FileAction("foo.txt"))
			temp = source.callattr("decode", "iso-8859-1")
			temp = temp.callattr("encode", "utf-8")
			target = self.add(make.FileAction("bar.txt", temp))
			self.writecreatedone()

	p = MyProject()
	p.create()

	if __name__ == "__main__":
		p.build("bar.txt")
"""


import os, os.path, argparse, warnings, datetime, tempfile, operator, gc, contextlib

from ll import misc, url, astyle


__docformat__ = "reStructuredText"


###
### Constants and helpers
###

nodata = misc.Const("nodata", "ll.make") # marker object for "no new data available"

bigbang = datetime.datetime(1900, 1, 1) # there can be no timestamp before this one
bigcrunch = datetime.datetime(3000, 1, 1) # there can be no timestamp after this one


def filechanged(key):
	"""
	Get the last modified date (or :const:`bigbang`, if the file doesn't exist).
	"""
	try:
		return key.mdate()
	except (IOError, OSError):
		return bigbang


class Level:
	"""
	Stores information about the recursive execution of :class:`Action`\s.
	"""
	__slots__ = ("action", "since", "reportable", "reported")

	def __init__(self, action, since, reportable, reported=False):
		self.action = action
		self.since = since
		self.reportable = reportable
		self.reported = reported

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object action={self.action!r} since={self.since!r} reportable={self.reportable!r} reported={self.reported} at {id(self):#x}>"


def report(func):
	"""
	Standard decorator for :meth:`Action.get` methods.

	This decorator handles proper reporting of nested action calls. If it isn't
	used, only the output of calls to :meth:`Project.writestep` will be visible
	to the user.
	"""
	def reporter(self, project, since):
		reported = False
		reportable = project.showaction is not None and isinstance(self, project.showaction)
		if reportable:
			if project.showidle:
				args = ["Starting ", project.straction(self)]
				if project.showtimestamps:
					args.append(" since ")
					args.append(project.strdatetime(since))
				project.writestack(*args)
				reported = True
		level = Level(self, since, reportable, reported)
		project.stack.append(level)
		t1 = datetime.datetime.utcnow()
		try:
			data = func(self, project, since)
		except Exception as exc:
			project.actionsfailed += 1
			if project.ignoreerrors: # ignore changes in failed subgraphs
				data = nodata # Return "everything is up to date" in this case
				error = exc.__class__
			else:
				raise
		else:
			project.actionscalled += 1
			error = None
		finally:
			project.stack.pop(-1)
		t2 = datetime.datetime.utcnow()
		if level.reportable or error is not None:
			if (not project.showidle and data is not nodata) or error is not None:
				project._writependinglevels() # Only outputs something if the action hasn't called writestep()
			if level.reported:
				if error is not None:
					text1 = "Failed"
					text2 = " after "
				else:
					text1 = "Finished"
					text2 = " in "
				args = [text1, " ", project.straction(self)]
				if project.showtime:
					args.append(text2)
					args.append(project.strtimedelta(t2-t1))
				if project.showtimestamps:
					args.append(" (changed ")
					args.append(project.strdatetime(self.changed))
					args.append(")")
				if project.showdata:
					args.append(": ")
					if error is not None:
						text = f"{error.__module__}.{error.__name__}" if error.__module__ != "exceptions" else error.__name__
						args.append(s4error(text))
					else:
						args.append(project.strdata(data))
				project.writestack(*args)
		return data
	reporter.__dict__.update(func.__dict__)
	reporter.__doc__ = func.__doc__
	reporter.__name__ = func.__name__
	return reporter


###
### exceptions & warnings
###

class RedefinedTargetWarning(Warning):
	"""
	Warning that will be issued when a target is added to a project and a target
	with the same key already exists.
	"""

	def __init__(self, key):
		self.key = key

	def __str__(self):
		return f"target with key={self.key!r} redefined"


class UndefinedTargetError(KeyError):
	"""
	Exception that will be raised when a target with the specified key doesn't
	exist within the project.
	"""

	def __init__(self, key):
		self.key = key

	def __str__(self):
		return f"target {self.key!r} undefined"


###
### Actions
###

def getoutputs(project, since, input):
	"""
	Recursively iterate through the object :obj:`input` (if it's a
	:class:`tuple`, :class:`list` or :class:`dict`) and return a tuple
	containing:

	*	An object (:obj:`data`) of the same structure as :obj:`input`, where every
		action object encountered is replaced with the output of that action;

	*	A timestamp (:obj:`changed`) which the newest timestamp among all the
		change timestamps of the actions encountered.

	If none of the actions has any data newer than :obj:`since` (i.e. none of
	the actions produced any new data) :obj:`data` will be :const:`nodata`.
	"""
	if isinstance(input, Action):
		return (input.get(project, since), input.changed)
	elif isinstance(input, (list, tuple)):
		resultdata = []
		havedata = False
		resultchanged = bigbang
		for item in input:
			(data, changed) = getoutputs(project, since, item)
			resultchanged = max(resultchanged, changed)
			if data is not nodata and not havedata: # The first real output
				since = bigbang # force inputs to produce data for the rest of the loop
				resultdata = [getoutputs(project, since, item)[0] for item in input[:len(resultdata)]] # refetch data from previous inputs
				havedata = True
			resultdata.append(data)
		if since is bigbang and not input:
			resultdata = input.__class__()
		elif not havedata:
			resultdata = nodata
		elif isinstance(input, tuple):
			resultdata = tuple(resultdata)
		return (resultdata, resultchanged)
	elif isinstance(input, dict) and not isinstance(input, Project):
		resultdata = {}
		havedata = False
		resultchanged = bigbang
		for (key, value) in input.items():
			(data, changed) = getoutputs(project, since, value)
			resultchanged = max(resultchanged, changed)
			if data is not nodata and not havedata: # The first real output
				since = bigbang # force inputs to produce data for the rest of the loop
				resultdata = dict((key, getoutputs(project, since, input[key])[0]) for key in resultdata) # refetch data from previous inputs
				havedata = True
			resultdata[key] = data
		if since is bigbang and not input:
			resultdata = {}
		elif not havedata:
			resultdata = nodata
		return (resultdata, resultchanged)
	else:
		return (input if since is bigbang else nodata, bigbang)


class Action:
	"""
	An :class:`Action` is responsible for transforming input data into output
	data. It may have no, one or many inputs which themselves may be other actions.
	It fetches, combines and transforms the output data of those actions and
	returns its own output data.
	"""

	key = None

	def __init__(self):
		"""
		Create a new :class:`Action` instance.
		"""
		self.changed = bigbang

	@report
	def get(self, project, since):
		"""
		This method (i.e. the implementations in subclasses) is the workhorse of
		:mod:`!ll.make`. :meth:`get` must return the output data of the action if
		this data has changed since :obj:`since` (which is a
		:class:`datetime.datetime` object in UTC). If the data hasn't changed
		since :obj:`since` the special object :const:`nodata` must be returned.

		In both cases the action must make sure that the data is internally
		consistent, i.e. if the input data is the output data of other actions
		:obj:`self` has to ensure that those other actions update their data too,
		independent from the fact whether :meth:`get` will return new data or not.

		Two special values can be passed for :obj:`since`:

		:const:`bigbang`
			This timestamp is older than any timestamp that can appear in real
			life. Since all data is newer than this, :meth:`get` must always
			return output data.

		:const:`bigcrunch`
			This timestamp is newer than any timestamp that can appear in real
			life. Since there can be no data newer than this, :meth:`get` can
			only return output data in this case if ensuring internal consistency
			resulted in new data.

		In all cases :meth:`get` must set the instance attribute :attr:`changed`
		to the timestamp of the last change to the data before returning. In most
		cases this if the newest :attr:`changed` timestamp of the input actions.
		"""
		input = (self.getargs(), self.getkwargs())
		(data, self.changed) = getoutputs(project, since, input)
		if data is not nodata:
			data = self.execute(project, *data[0], **data[1])
		return data

	@misc.notimplemented
	def execute(self, project, *args, **kwargs):
		"""
		Execute the action: transform the input data in :obj:`args` and
		:obj:`kwargs` and return the resulting output data. This method must be
		implemented in subclasses.
		"""

	def getkey(self):
		"""
		Get the nearest key from :obj:`self` or its inputs. This is used by
		:class:`ModuleAction` for the filename.
		"""
		return self.key

	def getargs(self):
		return ()

	def getkwargs(self):
		return {}

	def call(self, *args, **kwargs):
		"""
		Return a :class:`CallAction` for calling :obj:`self`\s output with
		positional arguments from :obj:`args` and keyword arguments from
		:obj:`kwargs`.
		"""
		return CallAction(self, *args, **kwargs)

	def getattr(self, attrname):
		"""
		Return a :class:`GetAttrAction` for getting :obj:`self`\s attribute
		named :obj:`attrname`.
		"""
		return GetAttrAction(self, attrname)

	def callattr(self, attrname, *args, **kwargs):
		"""
		Return a :class:`CallAttrAction` for calling :obj:`self`\s attribute
		named :obj:`attrname` with positional arguments from :obj:`args` and
		keyword arguments from :obj:`kwargs`.
		"""
		return CallAttrAction(self, attrname, *args, **kwargs)

	def __repr__(self):
		def format(arg):
			if isinstance(arg, Action):
				return f" from {arg.__class__.__module__}.{arg.__class__.__qualname__}"
			elif isinstance(arg, tuple):
				return "=(?)"
			elif isinstance(arg, list):
				return "=[?]"
			elif isinstance(arg, dict):
				return "={?}"
			else:
				return f"={arg!r}"

		output = [f"arg {i}{format(arg)}" for (i, arg) in enumerate(self.getargs())]
		for (argname, arg) in self.getkwargs().items():
			output.append(f"arg {argname}{format(arg)}")

		if output:
			output = f" with {', '.join(output)}"
		else:
			output = ""
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object{output} at {id(self):#x}>"

	@misc.notimplemented
	def __iter__(self):
		"""
		Return an iterator over the input actions of :obj:`self`.
		"""

	def iterallinputs(self):
		"""
		Return an iterator over all input actions of :obj:`self`
		(i.e. recursively).
		"""
		for input in self:
			yield input
			yield from input.iterallinputs()

	def findpaths(self, input):
		"""
		Find dependency paths leading from :obj:`self` to the other action
		:obj:`input`. I.e. if :obj:`self` depends directly or indirectly on
		:obj:`input`, this generator will produce all paths ``p`` where
		``p[0] is self`` and ``p[-1] is input`` and ``p[i+1] in p[i]`` for all
		``i`` in ``range(len(p)-1)``.
		"""
		if input is self:
			yield [self]
		else:
			for myinput in self:
				if isinstance(myinput, Action):
					for path in myinput.findpaths(input):
						yield [self] + path
				else:
					if myinput == input:
						yield [self, myinput]


class ObjectAction(Action):
	"""
	An :class:`ObjectAction` returns an object.
	"""
	def __init__(self, object=None):
		Action.__init__(self)
		self.object = object

	def __iter__(self):
		yield from ()

	@report
	def get(self, project, since):
		(data, self.changed) = getoutputs(project, since, self.object)
		return data


class TransformAction(Action):
	"""
	A :class:`TransformAction` depends on exactly one input action and transforms
	the input data into output data.
	"""
	def __init__(self, input=None):
		Action.__init__(self)
		self.input = input

	def getkey(self):
		return self.input.getkey()

	def __iter__(self):
		yield self.input

	def getkwargs(self):
		return dict(data=self.input)


class CollectAction(TransformAction):
	"""
	A :class:`CollectAction` is a :class:`TransformAction` that simply outputs its
	input data unmodified, but updates a number of other actions in the process.
	"""
	def __init__(self, input=None, *otherinputs):
		TransformAction.__init__(self, input)
		self.otherinputs = list(otherinputs)

	def addinputs(self, *otherinputs):
		"""
		Register all actions in :obj:`otherinputs` as additional actions that have
		to be updated before :obj:`self` is updated.
		"""
		self.otherinputs.extend(otherinputs)
		return self

	def __iter__(self):
		yield from TransformAction.__iter__(self)
		yield from self.otherinputs

	@report
	def get(self, project, since):
		# We don't need the data itself, so don't use getoutputs(), which would collect all inputs in a list.
		havedata = False
		changedinputs = bigbang
		for item in self.otherinputs:
			(data, changed) = getoutputs(project, since, item)
			changedinputs = max(changedinputs, changed)
			if data is not nodata: # The first real output
				havedata = True
		if havedata:
			since = bigbang
		(data, changedinput) = getoutputs(project, since, self.input)
		self.changed = max(changedinputs, changedinput)
		return data

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object at {id(self):#x}>"


class PhonyAction(Action):
	"""
	A :class:`PhonyAction` doesn't do anything. It may depend on any number of
	additional input actions which will be updated when this action gets updated.
	If there's new data from any of these actions, a :class:`PhonyAction` will
	return :const:`None` (and :const:`nodata` otherwise as usual).
	"""
	def __init__(self, *inputs, **kwargs):
		"""
		Create a :class:`PhonyAction` object. :obj:`doc` describes the action and
		is printed by the method :meth:`Project.writephonytargets`.
		"""
		Action.__init__(self)
		self.doc = kwargs.get("doc")
		self.inputs = list(inputs)
		self.buildno = None

	def addinputs(self, *inputs):
		"""
		Register all actions in :obj:`inputs` as additional actions that have to
		be updated once :obj:`self` is updated.
		"""
		self.inputs.extend(inputs)
		return self

	def __iter__(self):
		return iter(self.inputs)

	@report
	def get(self, project, since):
		# Caching the result object of a :class:`PhonyAction` is cheap (it's either :const:`None` or :const:`nodata`),
		# so we always do the caching as this optimizes away the traversal of a complete subgraph
		# for subsequent calls to :meth:`get` during the same build round
		if self.buildno != project.buildno:
			havedata = False
			resultchanged = bigbang
			# We don't need the data itself, so don't use getoutputs(), which would collect all inputs in a list.
			for item in self.inputs:
				(data, changed) = getoutputs(project, since, item)
				resultchanged = max(resultchanged, changed)
				if data is not nodata: # The first real output
					havedata = True
			self.buildno = project.buildno
			self.changed = resultchanged
			return None if havedata else nodata
		else:
			return None if self.changed > since else nodata

	def __repr__(self):
		s = f"<{self.__class__.__module__}.{self.__class__.__qualname__} object"
		if self.key is not None:
			s += f" with key={self.key!r}"
		s += f" at {id(self):#x}>"
		return s


class FileAction(TransformAction):
	"""
	A :class:`FileAction` is used for reading and writing files (and other
	objects providing the appropriate interface).
	"""
	def __init__(self, key, input=None, encoding=None, errors=None):
		"""
		Create a :class:`FileAction` object with :obj:`key` as the "filename".
		:obj:`key` must be an object that provides a method :meth:`open` for
		opening readable and writable streams to the file. :obj:`input` is the
		data written to the file (or the action producing the data). :obj:`encoding`
		is the encoding to be used for reading/writing. If :obj:`encoding` is
		:const:`None` binary i/o will be used. :obj:`errors` is the codec error
		handling name for encoding/decoding text.
		"""
		TransformAction.__init__(self, input)
		self.key = url.URL(key)
		self.encoding = encoding
		self.errors = errors
		self.buildno = None

	def getkey(self):
		return self.key

	def getkwargs(self):
		return dict(data=self.input, encoding=self.encoding, errors=errors)

	def write(self, project, data):
		"""
		Write :obj:`data` to the file and return it.
		"""
		project.writestep(self, "Writing ", format(len(data), ","), " ", ("bytes" if isinstance(data, bytes) else "chars"), " to ", project.strkey(self.key))
		with contextlib.closing(self.key.open(mode="wb" if self.encoding is None else "w", encoding=self.encoding, errors=self.errors)) as file:
			file.write(data)
			project.fileswritten += 1
			project.byteswritten += len(data)

	def read(self, project):
		"""
		Read the content from the file and return it.
		"""
		project.writestep(self, "Reading ", project.strkey(self.key))
		with contextlib.closing(self.key.open(mode="rb" if self.encoding is None else "r", encoding=self.encoding, errors=self.errors)) as file:
			data = file.read()
			project.filesread += 1
			project.bytesread += len(data)
			return data

	@report
	def get(self, project, since):
		"""
		If a :class:`FileAction` object doesn't have an input action it reads the
		input file and returns the content if the file has changed since
		:obj:`since` (otherwise :const:`nodata` is returned).

		If a :class:`FileAction` object does have an input action and the output
		data from this input action is newer than the file ``self.key`` the data
		will be written to the file. Otherwise (i.e. the file is up to date) the
		data will be read from the file.
		"""
		if self.buildno != project.buildno: # a new build round
			self.changed = filechanged(self.key) # Get timestamp of the file (or :const:`bigbang` if it doesn't exist)
			self.buildno = project.buildno

		if self.input is not None:
			(data, self.changed) = getoutputs(project, self.changed, self.input)
			if data is not nodata: # We've got new data from our input =>
				self.write(project, data) # write new data to disk
				self.changed = filechanged(self.key) # update timestamp
				return data
		else: # We have no inputs (i.e. this is a "source" file)
			if self.changed is bigbang:
				raise ValueError(f"source file {self.key!r} doesn't exist")
		if self.changed > since: # We are up to date now and newer than the output action
			return self.read(project) # return file data (to output action or client)
		# else fail through and return :const:`nodata`
		return nodata

	def chmod(self, mode=0o644):
		"""
		Return a :class:`ModeAction` that will change the file permissions of
		:obj:`self` to :obj:`mode`.
		"""
		return ModeAction(self, mode)

	def chown(self, user=None, group=None):
		"""
		Return an :class:`OwnerAction` that will change the user and/or group
		ownership of :obj:`self`.
		"""
		return OwnerAction(self, user, group)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object key={self.key!r} at {id(self):#x}>"


class MkDirAction(TransformAction):
	"""
	This action creates the a directory (passing through its input data).
	"""

	def __init__(self, key, mode=0o777):
		"""
		Create a :class:`MkDirAction` instance. :obj:`mode` (which defaults to
		:const:`0o777`) will be used as the permission bit pattern for the new
		directory.
		"""
		TransformAction.__init__(self)
		self.key = key
		self.mode = mode

	def execute(self, project, data):
		"""
		Create the directory with the permission bits specified in the
		constructor.
		"""
		project.writestep(self, "Making directory ", project.strkey(self.key), " with mode ", oct(self.mode))
		self.key.makedirs(self.mode)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object with mode={self.mode:#03o} at {id(self):#x}>"


class PipeAction(TransformAction):
	"""
	This action pipes the input through an external shell command.
	"""

	def __init__(self, input, command):
		"""
		Create a :class:`PipeAction` instance. :obj:`command` is the shell command
		to be executed (which must read it's input from stdin and write its output
		to stdout).
		"""
		TransformAction.__init__(self, input)
		self.command = command

	def getkwargs(self):
		return dict(data=self.input, command=self.command)

	def execute(self, project, data, command):
		project.writestep(self, "Calling command ", command)
		(stdin, stdout) = os.popen2(command)

		stdin.write(data)
		stdin.close()
		output = stdout.read()
		stdout.close()
		return output

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object with command={self.command!r} at {id(self):#x}>"


class CacheAction(TransformAction):
	"""
	A :class:`CacheAction` is a :class:`TransformAction` that passes through its
	input data, but caches it, so that it can be reused during the same build
	round.
	"""
	def __init__(self, input=None):
		TransformAction.__init__(self, input)
		self.since = bigcrunch
		self.data = nodata
		self.buildno = None

	@report
	def get(self, project, since):
		if self.buildno != project.buildno or (since < self.since and self.data is nodata): # If this is a new build round or we're asked about an earlier date and didn't return data last time
			(self.data, self.changed) = getoutputs(project, since, self.input)
			project.writenote(self, "Caching data")
			self.since = since
			self.buildno = project.buildno
		if since < self.changed or since is bigbang:
			project.writenote(self, "Reusing cached data")
			return self.data
		return nodata


class GetAttrAction(TransformAction):
	"""
	This action gets an attribute from its input object.
	"""

	def __init__(self, input=None, attrname=None):
		TransformAction.__init__(self, input)
		self.attrname = attrname

	def __iter__(self):
		yield from TransformAction.__iter__(self)
		yield self.attrname

	def getkwargs(self):
		return dict(data=self.input, attrname=self.attrname)

	def execute(self, project, data, attrname):
		project.writestep(self, "Getting attribute ", attrname)
		return getattr(data, attrname)


class CallAction(Action):
	"""
	This action calls a function or any other callable object with a number of
	arguments. Both positional and keyword arguments are supported and the
	function and the arguments can be static objects or actions.
	"""
	def __init__(self, func, *args, **kwargs):
		Action.__init__(self)
		self.func = func
		self.args = args
		self.kwargs = kwargs

	def __iter__(self):
		yield self.func
		yield from self.args
		yield from self.kwargs.values()

	def getargs(self):
		return (self.func,) + self.args

	def getkwargs(self):
		return self.kwargs

	def execute(self, project, func, *args, **kwargs):
		if args:
			if len(args) == 1:
				argsmsg = " with 1 arg"
			else:
				argsmsg = f" with {len(args)} args"
		else:
			argsmsg = " without args"
		if kwargs:
			kwargsstr = ", ".join(kwargs)
			kwargsmsg = f" and keyword {kwargsstr}" if len(kwargs) == 1 else f" and keywords {kwargsstr}"
		else:
			kwargsmsg = ""
		project.writestep(self, f"Calling {func!r}", argsmsg, kwargsmsg)
		return func(*args, **kwargs)


class CallAttrAction(Action):
	"""
	This action calls an attribute of an object with a number of arguments. Both
	positional and keyword arguments are supported and the object, the attribute
	name and the arguments can be static objects or actions.
	"""
	def __init__(self, obj, attrname, *args, **kwargs):
		Action.__init__(self)
		self.obj = obj
		self.attrname = attrname
		self.args = args
		self.kwargs = kwargs

	def __iter__(self):
		yield self.obj
		yield self.attrname
		yield from self.args
		yield from self.kwargs.values()

	def getargs(self):
		return (self.obj, self.attrname) + self.args

	def getkwargs(self):
		return self.kwargs

	def execute(self, project, obj, attrname, *args, **kwargs):
		func = getattr(obj, attrname)
		project.writestep(self, f"Calling {func!r}")
		return func(*args, **kwargs)


class CommandAction(TransformAction):
	"""
	This action executes a system command (via :func:`os.system`) and passes
	through the input data.
	"""

	def __init__(self, command, input=None):
		"""
		Create a new :class:`CommandAction` object. :obj:`command` is the command
		that will executed when :meth:`execute` is called.
		"""
		TransformAction.__init__(self, input)
		self.command = command

	def execute(self, project, data):
		project.writestep(self, "Executing command ", self.command)
		os.system(self.command)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object command={self.command!r} at {id(self):#x}>"


class ModeAction(TransformAction):
	"""
	:class:`ModeAction` changes file permissions and passes through the input data.
	"""

	def __init__(self, input=None, mode=0o644):
		"""
		Create an :class:`ModeAction` object. :obj:`mode` (which defaults to
		:const:`0644`) will be use as the permission bit pattern.
		"""
		TransformAction.__init__(self, input)
		self.mode = mode

	def __iter__(self):
		yield from TransformAction.__iter__(self)
		yield self.mode

	def getkwargs(self):
		return dict(data=self.input, mode=self.mode)

	def execute(self, project, data, mode):
		"""
		Change the permission bits of the file ``self.getkey()``.
		"""
		key = self.getkey()
		project.writestep(self, "Changing mode of ", project.strkey(key), f" to {mode:#03o}")
		key.chmod(mode)
		return data


class OwnerAction(TransformAction):
	"""
	:class:`OwnerAction` changes the user and/or group ownership of a file and
	passes through the input data.
	"""

	def __init__(self, input=None, user=None, group=None):
		"""
		Create a new :class:`OwnerAction` object. :obj:`user` can either be a
		numerical user id or a user name or :const:`None`. If it is :const:`None`
		no user ownership will be changed. The same applies to :obj:`group`.
		"""
		TransformAction.__init__(self, input)
		self.id = id
		self.user = user
		self.group = group

	def __iter__(self):
		yield from TransformAction.__iter__(self)
		yield self.user
		yield self.group

	def getkwargs(self):
		return dict(data=self.input, user=self.user, group=self.group)

	def execute(self, project, data, user, group):
		"""
		Change the ownership of the file ``self.getkey()``.
		"""
		key = self.getkey()
		project.writestep(self, "Changing owner of ", project.strkey(key), " to ", user, " and group to ", group)
		key.chown(user, group)
		return data


class ModuleAction(TransformAction):
	"""
	This action will turn the input string into a Python module.
	"""
	def __init__(self, input=None):
		"""
		Create an :class:`ModuleAction`.

		This object must have an input action (which might be a :class:`FileAction`
		that creates the source file).
		"""
		TransformAction.__init__(self, input)
		self.inputs = []
		self.changed = bigbang
		self.data = nodata
		self.buildno = None

	def addinputs(self, *inputs):
		"""
		Register all actions in :obj:`inputs` as modules used by this module.
		These actions must be :class:`ModuleAction` objects too.

		Normally it isn't necessary to call the method directly. Instead
		fetch the required module inside your module like this::

			from ll import make

			mymodule = make.currentproject.get("mymodule.py")

		This will record your module as depending on :mod:`mymodule`, so if
		:mod:`mymodule` changes, your module will be reloaded too. For this to
		work you need to have an :class:`ModuleAction` added to the project with
		the key ``"mymodule.py"``.
		"""
		self.inputs.extend(inputs)
		return self

	def __iter__(self):
		yield from TransformAction.__iter__(self)
		yield from self.inputs

	def execute(self, project, data):
		key = self.getkey()
		project.writestep(self, "Importing module as ", project.strkey(key))

		if key is None:
			filename = name = "<string>"
		elif isinstance(key, url.URL):
			try:
				filename = key.local()
			except ValueError: # is not local
				filename = str(key)
			name = key.withoutext().file.encode("ascii", "ignore").decode("ascii")
		else:
			filename = name = str(key)

		del self.inputs[:] # The module will be reloaded => drop all dependencies (they will be rebuilt during import)

		try:
			project.importstack.append(self)
			mod = misc.module(data, filename, name)
		finally:
			project.importstack.pop()
		return mod

	@report
	def get(self, project, since):
		# Is this module required by another?
		if project.importstack:
			if self not in project.importstack[-1].inputs:
				project.importstack[-1].addinputs(self) # Append to inputs of other module

		# Is this a new build round?
		if self.buildno != project.buildno:
			(data, changed) = getoutputs(project, self.changed, self.input) # Get the source code
			if data is not nodata or self.data is nodata: # The file itself has changed or this is the first call
				needimport = True
			else: # Only check the required inputs, if ``self.input`` has *not* changed
				(data2, changed2) = getoutputs(project, self.changed, self.inputs)
				needimport = data2 is not nodata

			if needimport:
				if data is nodata:
					(data, changed) = getoutputs(project, bigbang, self.input) # We *really* need the source
				self.data = self.execute(project, data) # This will (re)create dependencies
				gc.collect() # Make sure classes from the previous module (which have cycles via the :attr:`__mro__`) are gone
				# Timestamp of import is the timestamp of the newest module file
				self.changed = changed
				if self.inputs:
					changed = max(changed, max(input.changed for input in self.inputs))
				self.changed = changed
			self.buildno = project.buildno
			if self.changed > since:
				return self.data
		# Are we newer then the specified date?
		elif self.changed > since:
			key = self.getkey()
			project.writenote(self, "Reusing cached module ", project.strkey(key))
			return self.data
		return nodata

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} object key={self.getkey()!r} at {id(self):#x}>"


class FOPAction(TransformAction):
	"""
	This action transforms an XML string (containing XSL-FO) into PDF. For it
	to work `Apache FOP`__ is required. The command line is hardcoded but it's
	simple to overwrite the class attribute :attr:`command` in a subclass.

	__ http://xmlgraphics.apache.org/fop/
	"""
	command = "/usr/local/src/fop-0.20.5/fop.sh -q -c /usr/local/src/fop-0.20.5/conf/userconfig.xml -fo {src} -pdf {dst}"

	def execute(self, project, data):
		project.writestep(self, "FOPping input")
		(infd, inname) = tempfile.mkstemp(suffix=".fo")
		(outfd, outname) = tempfile.mkstemp(suffix=".pdf")
		try:
			infile = os.fdopen(infd, "wb")
			os.fdopen(outfd).close()
			infile.write(data)
			infile.close()
			os.system(self.command.format(src=inname, dst=outname))
			data = open(outname, "rb").read()
		finally:
			os.remove(inname)
			os.remove(outname)
		return data


class AlwaysAction(Action):
	"""
	This action always returns :const:`None` as new data.
	"""
	def __init__(self):
		Action.__init__(self)
		self.changed = bigbang

	def __iter__(self):
		yield None

	@report
	def get(self, project, since):
		project.writestep(self, "Returning None")
		return None
alwaysaction = AlwaysAction() # this action can be reused as it has no inputs


class NeverAction(Action):
	"""
	This action never returns new data.
	"""
	def __iter__(self):
		yield None

	@report
	def get(self, project, since):
		return nodata
neveraction = NeverAction() # this action can be reused as it has no inputs


###
### Colors for output
###

s4indent = astyle.Style.fromenv("LL_MAKE_REPRANSI_INDENT", "black:black:bold")
s4key = astyle.Style.fromenv("LL_MAKE_REPRANSI_KEY", "yellow:black")
s4action = astyle.Style.fromenv("LL_MAKE_REPRANSI_ACTION", "green:black")
s4time = astyle.Style.fromenv("LL_MAKE_REPRANSI_TIME", "magenta:black")
s4data = astyle.Style.fromenv("LL_MAKE_REPRANSI_DATA", "cyan:black")
s4size = astyle.Style.fromenv("LL_MAKE_REPRANSI_SIZE", "magenta:black")
s4counter = astyle.Style.fromenv("LL_MAKE_REPRANSI_COUNTER", "red:black:bold")
s4error = astyle.Style.fromenv("LL_MAKE_REPRANSI_ERROR", "red:black:bold")


###
### The project class
###

class Project(dict):
	"""
	A :class:`Project` collects all :class:`Action` objects from a project. It
	is responsible for initiating the build process and for generating a report
	about the progress of the build process.
	"""

	# Will be used in log messages and notifications
	name = "ll.make"

	def __init__(self):
		super().__init__()
		self.actionscalled = 0
		self.actionsfailed = 0
		self.stepsexecuted = 0
		self.bytesread = 0
		self.filesread = 0
		self.byteswritten = 0
		self.fileswritten = 0
		self.starttime = None
		self.ignoreerrors = False
		self.here = None # cache the current directory during builds (used for shortening URLs)
		self.home = None # cache the home directory during builds (used for shortening URLs)
		self.stack = [] # keep track of the recursion during calls to :meth:`Action.get`
		self.importstack = [] # keep track of recursive imports
		self.indent = os.environ.get("LL_MAKE_INDENT", "   ") # Indentation string to use for output of nested actions
		self.buildno = 0 # Build number; This gets incremented on each call to :meth:`build`. Can be used by actions to determine the start of a new build round

		self.showsummary = self._getenvbool("LL_MAKE_SHOWSUMMARY", True)
		self.showaction = os.environ.get("LL_MAKE_SHOWACTION", "filephony")
		self.showstep = os.environ.get("LL_MAKE_SHOWSTEP", "all")
		self.shownote = os.environ.get("LL_MAKE_SHOWNOTE", "none")
		self.color = self._getenvbool("LL_MAKE_COLOR", True)
		self.showidle = self._getenvbool("LL_MAKE_SHOWIDLE", False)
		self.showregistration = os.environ.get("LL_MAKE_SHOWREGISTRATION", "phony")
		self.showtime = self._getenvbool("LL_MAKE_SHOWTIME", True)
		self.showtimestamps = self._getenvbool("LL_MAKE_SHOWTIMESTAMPS", False)
		self.showdata = self._getenvbool("LL_MAKE_SHOWDATA", False)
		self.notify = self._getenvbool("LL_MAKE_NOTIFY", False)

	def __repr__(self):
		return f"<{self.__class__.__module__}.{self.__class__.__qualname__} with {len(self)} targets at {id(self):#x}>"

	class showaction(misc.propclass):
		"""
		This property specifies which actions should be reported during the build
		process. On setting, the value can be:

		:const:`None` or ``"none"``
			No actions will be reported;

		``"file"``
			Only :class:`FileAction`\s will be reported;

		``"phony"``
			Only :class:`PhonyAction`\s will be reported;

		``"filephony"``
			Only :class:`FileAction`\s and :class:`PhonyAction`\s will be
			reported;

		a class or tuple of classes
			Only actions that are instances of those classes will be reported.
		"""
		def __get__(self):
			return self._showaction
		def __set__(self, value):
			if value == "none":
				self._showaction = None
			elif value == "file":
				self._showaction = FileAction
			elif value == "phony":
				self._showaction = PhonyAction
			elif value == "filephony":
				self._showaction = (PhonyAction, FileAction)
			elif value == "all":
				self._showaction = Action
			elif isinstance(value, Action):
				self._showaction = value
			elif value:
				self._showaction = Action
			else:
				self._showaction = None

	class showstep(misc.propclass):
		"""
		This property specifies for which actions tranformation steps should be
		reported during the build process. For allowed values on setting see
		:prop:`showaction`.
		"""
		def __get__(self):
			return self._showstep
		def __set__(self, value):
			if value == "none":
				self._showstep = None
			elif value == "file":
				self._showstep = FileAction
			elif value == "phony":
				self._showstep = PhonyAction
			elif value == "filephony":
				self._showstep = (PhonyAction, FileAction)
			elif value == "all":
				self._showstep = Action
			elif isinstance(value, Action):
				self._showstep = value
			elif value:
				self._showstep = Action
			else:
				self._showstep = None

	class shownote(misc.propclass):
		"""
		This property specifies which for which actions tranformation notes
		(which are similar to step, but not that important, e.g. when an
		information that is already there gets reused) be reported during the
		build process. For allowed values on setting see :prop:`showaction`.
		"""
		def __get__(self):
			return self._shownote
		def __set__(self, value):
			if value == "none":
				self._shownote = None
			elif value == "file":
				self._shownote = FileAction
			elif value == "phony":
				self._shownote = PhonyAction
			elif value == "filephony":
				self._shownote = (PhonyAction, FileAction)
			elif value == "all":
				self._shownote = Action
			elif isinstance(value, Action):
				self._shownote = value
			elif value:
				self._shownote = Action
			else:
				self._shownote = None

	class showregistration(misc.propclass):
		"""
		This property specifies for which actions registration (i.e. call to the
		:meth:`add` should be reported. For allowed values on setting see
		:prop:`showaction`.
		"""
		def __get__(self):
			return self._showregistration
		def __set__(self, value):
			if value == "none":
				self._showregistration = None
			elif value == "file":
				self._showregistration = FileAction
			elif value == "phony":
				self._showregistration = PhonyAction
			elif value == "filephony":
				self._showregistration = (PhonyAction, FileAction)
			elif value == "all":
				self._showregistration = Action
			else:
				self._showregistration = value

	def _getenvbool(self, name, default):
		return bool(int(os.environ.get(name, default)))

	def strtimedelta(self, delta):
		"""
		Return a nicely formatted and colored string for the
		:class:`datetime.timedelta` value :obj:`delta`. :obj:`delta`
		may also be :const:`None` in with case ``"0"`` will be returned.
		"""
		if delta is None:
			text = "0"
		else:
			rest = delta.seconds

			(rest, secs) = divmod(rest, 60)
			(rest, mins) = divmod(rest, 60)
			rest += delta.days*24

			secs += delta.microseconds/1000000.
			if rest:
				text = f"{rest:d}:{mins:02d}:{secs:06.3f}h"
			elif mins:
				text = f"{mins:02d}:{secs:06.3f}m"
			else:
				text = f"{secs:.3f}s"
		return s4time(text)

	def strdatetime(self, dt):
		"""
		Return a nicely formatted and colored string for the
		:class:`datetime.datetime` value :obj:`dt`.
		"""
		return s4time(dt.strftime("%Y-%m-%d %H:%M:%S.%f"))

	def strcounter(self, counter):
		"""
		Return a nicely formatted and colored string for the counter value
		:obj:`counter`.
		"""
		return s4counter(f"{counter}.")

	def strerror(self, text):
		"""
		Return a nicely formatted and colored string for the error text
		:obj:`text`.
		"""
		return s4error(text)

	def strkey(self, key):
		"""
		Return a nicely formatted and colored string for the action key
		:obj:`key`.
		"""
		s = str(key)
		if isinstance(key, url.URL) and key.islocal():
			if self.here is None:
				self.here = url.here()
			if self.home is None:
				self.home = url.home()
			test = str(key.relative(self.here))
			if len(test) < len(s):
				s = test
			test = f"~/{key.relative(self.home)}"
			if len(test) < len(s):
				s = test
		return s4key(s)

	def straction(self, action):
		"""
		Return a nicely formatted and colored string for the action
		:obj:`action`.
		"""
		name = action.__class__.__qualname__
		if name.endswith("Action"):
			name = name[:-6]

		if action.key is not None:
			return s4action(name, "(", self.strkey(action.key), ")")
		else:
			return s4action(name)

	def strdata(self, data):
		if data is nodata:
			return "nodata"
		elif isinstance(data, (int, float)):
			return s4data(repr(data))
		elif data is None:
			return s4data("None")
		elif isinstance(data, bytes):
			return s4data(f"bytes ({len(data):,}b)")
		elif isinstance(data, str):
			return s4data(f"chars ({len(data):,}c)")
		else:
			return s4data(f"{misc.format_class(data)} @ {id(data):#x}")

	def __setitem__(self, key, target):
		"""
		Add the action :obj:`target` to :obj:`self` as a target and register it
		under the key :obj:`key`.
		"""
		if isinstance(key, url.URL) and key.islocal():
			key = key.abs(scheme="file")

		if key in self:
			self.warn(RedefinedTargetWarning(key), 5)
		target.key = key
		super().__setitem__(key, target)

	def add(self, target, key=None):
		"""
		Add the action :obj:`target` as a target to :obj:`self`. If :obj:`key`
		is not :const:`None`, :obj:`target` will be registered under this key,
		otherwise it will be registered under its own key (i.e. ``target.key``).
		"""
		if key is None: # Use the key from the target
			key = target.getkey()

		self[key] = target

		self.stepsexecuted += 1
		if self.showregistration is not None and isinstance(target, self.showregistration):
			self.writestacklevel(0, self.strcounter(self.stepsexecuted), " Registered ", self.strkey(key))

		return target

	def _candidates(self, key):
		"""
		Return candidates for alternative forms of :obj:`key`. This is a
		generator, so when the first suitable candidate is found, the rest of the
		candidates won't have to be created at all.
		"""
		yield key
		key2 = key
		if isinstance(key, str):
			key2 = url.URL(key)
			yield key2
		if isinstance(key2, url.URL):
			key2 = key2.abs(scheme="file")
			yield key2
			key2 = key2.real(scheme="file")
			yield key2

	def __getitem__(self, key):
		"""
		Return the target with the key :obj:`key`. If an key can't be found, it
		will be wrapped in a :class:`ll.url.URL` object and retried. If
		:obj:`key` still can't be found a :exc:`UndefinedTargetError` will be
		raised.
		"""
		for key2 in self._candidates(key):
			try:
				return super().__getitem__(key2)
			except KeyError:
				pass
		raise UndefinedTargetError(key)

	def has_key(self, key):
		"""
		Return whether the target with the key :obj:`key` exists in the project.
		"""
		return key in self

	def __contains__(self, key):
		"""
		Return whether the target with the key :obj:`key` exists in the project.
		"""
		return any(super(Project, self).__contains__(key2) for key2 in self._candidates(key))

	def create(self):
		"""
		Create all dependencies for the project. Overwrite in subclasses.

		This method should only be called once, otherwise you'll get lots of
		:exc:`RedefinedTargetWarning`\s. But you can call :meth:`clear`
		to remove all targets before calling :meth:`create`. You can also
		use the method :meth:`recreate` for that.
		"""
		self.stepsexecuted = 0
		self.starttime = datetime.datetime.utcnow()
		self.writeln("Creating targets...")

	def recreate(self):
		"""
		Calls :meth:`clear` and :meth:`create` to recreate all project
		dependencies.
		"""
		self.clear()
		self.create()

	def argparser(self):
		"""
		Return an :mod:`argparse` parser for parsing the command line arguments.
		This can be overwritten in subclasses to add more arguments.
		"""

		def action2name(action):
			if action is None:
				return "none"
			elif action is Action:
				return "all"
			elif issubclass(FileAction, action) and issubclass(PhonyAction, action):
				return "filephony"
			elif issubclass(FileAction, action):
				return "file"
			elif issubclass(PhonyAction, action):
				return "phony"
			else:
				return "all"

		actions = ("all", "file", "phony", "filephony", "none")
		p = argparse.ArgumentParser(description="build one or more targets", epilog="For more info see http://python.livinglogic.de/make.html")
		p.add_argument("targets", metavar="target", help="Target to be built", nargs="*")
		p.add_argument("-x", "--ignoreerrors", dest="ignoreerrors", help="Ignore errors? (default: %(default)s)", action=misc.FlagAction, default=self.ignoreerrors)
		p.add_argument("-c", "--color", dest="color", help="Use colored output? (default: %(default)s)", action=misc.FlagAction, default=self.color)
		p.add_argument("-y", "--notify", dest="notify", help="Issue notification after the build? (default: %(default)s)", action=misc.FlagAction, default=self.notify)
		p.add_argument("-a", "--showaction", dest="showaction", help="Show actions? (default: %(default)s)", choices=actions, default=action2name(self.showaction))
		p.add_argument("-s", "--showstep", dest="showstep", help="Show steps? (default: %(default)s)", choices=actions, default=action2name(self.showstep))
		p.add_argument("-n", "--shownote", dest="shownote", help="Show notes? (default: %(default)s)", choices=actions, default=action2name(self.shownote))
		p.add_argument("-r", "--showregistration", dest="showregistration", help="Show registration? (default: %(default)s)", choices=actions, default=action2name(self.showregistration))
		p.add_argument("-i", "--showidle", dest="showidle", help="Show actions that didn't produce data? (default: %(default)s)", action=misc.FlagAction, default=self.showidle)
		p.add_argument("-d", "--showdata", dest="showdata", help="Show data? (default: %(default)s)", action=misc.FlagAction, default=self.showdata)
		return p

	def parseargs(self, args=None):
		"""
		Use the parser returned by :meth:`argparser` to parse the argument
		sequence :obj:`args`, modify :obj:`self` accordingly and return
		the result of the parsers :meth:`parse_args` call.
		"""
		p = self.argparser()
		args = p.parse_args(args)
		self.ignoreerrors = args.ignoreerrors
		self.color = args.color
		self.notify = args.notify
		self.showaction = args.showaction
		self.showstep = args.showstep
		self.shownote = args.shownote
		self.showregistration = args.showregistration
		self.showidle = args.showidle
		self.showdata = args.showdata
		return args

	def _get(self, target, since):
		"""
		:obj:`target` must be an action registered in :obj:`self` (or the id of
		one). For this target the :meth:`Action.get` will be called with
		:obj:`since` as the argument.
		"""
		global currentproject

		if not isinstance(target, Action):
			target = self[target]

		oldproject = currentproject
		try:
			currentproject = self
			data = target.get(self, since)
		finally:
			currentproject = oldproject
		return data

	def get(self, target):
		"""
		Get up-to-date output data from the target :obj:`target` (which must be
		an action registered with :obj:`self` (or the id of one). During the call
		the global variable ``currentproject`` will be set to :obj:`self`.
		"""
		return self._get(target, bigbang)

	def build(self, *targets):
		"""
		Rebuild all targets in :obj:`targets`. Items in :obj:`targets` must be
		actions registered with :obj:`self` (or their ids).
		"""
		global currentproject

		self.starttime = datetime.datetime.utcnow()

		format = "{:,}".format

		with url.Context():
			self.stack = []
			self.importstack = []
			self.actionscalled = 0
			self.actionsfailed = 0
			self.stepsexecuted = 0
			self.bytesread = 0
			self.filesread = 0
			self.byteswritten = 0
			self.fileswritten = 0

			self.buildno += 1 # increment build number so that actions that stored the old one can detect a new build round

			success = False
			try:
				if self.notify:
					self.notifystart()
				for target in targets:
					data = self._get(target, bigcrunch)

				if self.showsummary:
					self.write(
						"built project ",
						s4action(self.name),
						": ",
						s4data(format(len(self))),
						" registered targets; ",
						s4data(format(self.actionscalled)),
						" actions called; ",
						s4data(format(self.stepsexecuted)),
						" steps executed; ",
						s4data(format(self.filesread)),
						" files/",
						s4data(format(self.bytesread)),
						" bytes read; ",
						s4data(format(self.fileswritten)),
						" files/",
						s4data(format(self.byteswritten)),
						" bytes written; ",
						s4data(format(self.actionsfailed)),
						" actions failed",
					)
					if self.showtime:
						self.write(" [t+", self.strtimedelta(datetime.datetime.utcnow()-self.starttime), "]")
					self.writeln()
				success = True
			finally:
				if self.notify:
					self.notifyfinish(datetime.datetime.utcnow()-self.starttime, success)

	def buildwithargs(self, args=None):
		"""
		For calling make scripts from the command line. :obj:`args` defaults to
		``sys.argv``. Any positional arguments in the command line will be treated
		as target ids. If there are no positional arguments, a list of all
		registered :class:`PhonyAction` objects will be output.
		"""
		args = self.parseargs(args)

		if args.targets:
			self.build(*args.targets)
		else:
			self.writeln("Available phony targets are:")
			self.writephonytargets()

	def write(self, *texts):
		"""
		All screen output is done through this method. This makes it possible
		to redirect the output (e.g. to logfiles) in subclasses.
		"""
		astyle.stderr.write(*texts)

	def writeln(self, *texts):
		"""
		All screen output is done through this method. This makes it possible to
		redirect the output (e.g. to logfiles) in subclasses.
		"""
		astyle.stderr.writeln(*texts)
		astyle.stderr.flush()

	def writeerror(self, *texts):
		"""
		Output an error.
		"""
		self.write(*texts)

	def notifystart(self):
		misc.notifystart()

	def notifyfinish(self, duration, success):
		msgs = []
		if self.stepsexecuted:
			msgs.append(f"{self.stepsexecuted:,} steps")
		if self.fileswritten:
			msgs.append(f"{self.fileswritten:,} files")
		if self.byteswritten:
			msgs.append(f"{self.byteswritten:,} bytes")
		if not msgs:
			msgs.append("nothing to do")

		misc.notifyfinish(
			self.name,
			f"{'finished' if success else 'failed'} after {self.strtimedelta(duration)}",
			"; ".join(msgs),
		)

	def warn(self, warning, stacklevel):
		"""
		Issue a warning through the Python warnings framework
		"""
		warnings.warn(warning, stacklevel=stacklevel)

	def writestacklevel(self, level, *texts):
		"""
		Output :obj:`texts` indented :obj:`level` levels.
		"""
		self.write(s4indent(level*self.indent), *texts)
		if self.showtime and self.starttime is not None:
			self.write(" [t+", self.strtimedelta(datetime.datetime.utcnow() - self.starttime), "]")
		self.writeln()

	def writestack(self, *texts):
		"""
		Output :obj:`texts` indented properly for the current nesting of
		action execution.
		"""
		count = misc.count(level for level in self.stack if level.reportable)
		self.writestacklevel(count, *texts)

	def _writependinglevels(self):
		for (i, level) in enumerate(level for level in self.stack if level.reportable):
			if not level.reported:
				args = ["Started  ", self.straction(level.action)]
				if self.showtimestamps:
					args.append(" (since ")
					args.append(self.strdatetime(level.since))
					args.append(")")
				self.writestacklevel(i, *args)
				level.reported = True

	def writestep(self, action, *texts):
		"""
		Output :obj:`texts` as the description of the data transformation
		done by the action :obj:`arction`.
		"""
		self.stepsexecuted += 1
		if self.showstep is not None and isinstance(action, self.showstep):
			if not self.showidle:
				self._writependinglevels()
			self.writestack(self.strcounter(self.stepsexecuted), " ", *texts)

	def writenote(self, action, *texts):
		"""
		Output :obj:`texts` as the note for the data transformation done by
		the action :obj:`action`.
		"""
		self.stepsexecuted += 1
		if self.shownote is not None and isinstance(action, self.shownote):
			if not self.showidle:
				self._writependinglevels()
			self.writestack(self.strcounter(self.stepsexecuted), " ", *texts)

	def writecreatedone(self):
		"""
		Can be called at the end of an overwritten :meth:`create` to report
		the number of registered targets.
		"""
		self.writestacklevel(0, "done: ", s4data(str(len(self))), " registered targets")

	def writephonytargets(self):
		"""
		Show a list of all :class:`PhonyAction` objects in the project and
		their documentation.
		"""
		phonies = []
		maxlen = 0
		for key in self:
			if isinstance(key, str):
				maxlen = max(maxlen, len(key))
				phonies.append(self[key])
		phonies.sort(key=operator.attrgetter("key"))
		for phony in phonies:
			text = astyle.Text(self.straction(phony))
			if phony.doc:
				text.append(" ", s4indent("."*(maxlen+3-len(phony.key))), " ", phony.doc)
			self.writeln(text)

	def findpaths(self, target, source):
		"""
		Find dependency paths leading from the action :obj:`target` to the action
		:obj:`source`.
		"""
		return target.findpaths(source)


# This will be set to the project in :meth:`build` and :meth:`get`
currentproject = None
