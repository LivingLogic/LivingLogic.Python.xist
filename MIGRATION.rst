Migrating to version 5.18
=========================

Changes to ``ul4``
------------------

*	The UL4 exception :class:`ll.ul4c.Error` has been renamed to
	:class:`LocationError`.

*	The UL4 function ``type`` now returns the Python class name for date, color,
	template exception objects.


Migrating to version 5.17
=========================

Changes to ``rul4``
-------------------

The function ``import`` has been split into ``load`` for loading the content of
a file and ``compile`` for compiling a string, so::

	<?code template = import("/home/user/template/foo.ul4")?>

has to be replaced with::

	<?code template = compile(load("/home/user/template/foo.ul4"))?>


Migrating to version 5.16
=========================

Changes to :mod:`orasql`
------------------------

Some methods in :mod:`orasql` have been renamed: Iterating methods no longer
have ``iter`` in their name (e.g. :meth:`itertables` is now simply called
:meth:`tables`). The ``ddl`` part of some method names has been changed to
``sql`` (e.g. :meth:`createddl` is now called :meth:`createsql`).


Migrating to version 5.15
=========================

Changes to PySQL
----------------

*	The function ``load`` has been replaced by two functions ``loadstr`` for
	loading strings and ``loadbytes`` for loading bytes, i.e. replace::

		load('foo.txt', 'utf-8', 'replace')

	with::

		loadstr('foo.txt', 'utf-8', 'replace')

	and::

		load('foo.png')

	with::

		loadbytes('foo.png')

*	PySQL no longer supports the ``-- !!!`` command terminator. Use the
	``raiseexceptions`` command instead to specify error handling.


Migrating to version 5.14
=========================

Changes to UL4
--------------

*	The boolean parameter ``keepws`` for :class:`ul4c.Template` has been renamed
	to ``whitespace`` and requires a string value now. Pass ``whitespace="keep"``
	for the old ``keepws=True`` and ``whitespace="strip"`` for the old
	``keepws=False``.

*	The ``rul4`` option :option:`--keepws` has been renamed to
	:option:`--whitespace` and defaults to ``smart`` now. So instead of the old
	``--keepws=1`` pass ``--whitespace=keep`` and for ``--keepws=0`` pass
	``--whitespace=strip``.

*	Rendering an UL4 template from inside a UL4 template is now again done via
	the ``<?render?>`` tag. So inside a template you have to replace the code::

		<?code template.render(foo, bar)?>

	with::

		<?render template(foo, bar)?>

*	Closures in UL4 templates no longer see the state of the variables at the
	time when the local template was defined, but at the time when it is called.
	This is similar to most other languages that support closures.

	To emulate the old behaviour pass the variables you want to "freeze" to a
	locally defined template and define the original template there.

Changes to ``pysql``
--------------------

*	SQL commands must be terminated with a ``-- @@@`` (or ``-- !!!``) comment
	line now, i.e. now the comment *after* the command determines whether
	exceptions will be ignored, instead of the comment before the command.


Migrating to version 5.13
=========================

Changes to UL4
--------------

*	Locally defined UL4 templates no longer see themselves among the variables
	of the parent template.

Changes to ``sisyphus``
-----------------------

*	The option :option:`setproctitle` for sisyphus jobs has been renamed to
	:option:`proctitle`. 

*	The default for the name parameter in :meth:`tasks` for sisyphus jobs has
	changed from ``str`` to ``None``, i.e. it defaults to unnamed tasks now.


Migrating to version 5.12
=========================

Changes to ``ul4on``
--------------------

*	The UL4ON serialization format has been reimplemented to be more
	human-readable and robust. The new format is incompatible to the old.
	If you update your XIST installation to 5.12 you should update the
	corresponding UL4ON versions for Java/Javascript too.


Migrating to version 5.10
=========================

Changes to ``misc``
-------------------

*	The functions :func:`misc.gzip` and :func:`misc.gunzip` have been removed
	as Python 3.2 has the functions :func:`gzip.compress` and
	:func:`gzip.uncompress`, which do the same.


Migrating to version 5.9
========================

Changes to ``db2ul4``
---------------------

*	The script ``db2ul4`` has been renamed to ``rul4``.


Changes to ``ll.url``
---------------------

*	The argument ``pattern`` of the URL methods :meth:`listdir`, :meth:`files`,
	:meth:`dirs`, :meth:`walk`, :meth:`walkfiles` and :meth:`walkdirs` has been
	renamed to ``include``.

*	The method :meth:`walk` has been renamed to :meth:`walkall`.


Migrating to version 5.7
========================

Changes to ``ll.oradd``
-----------------------

*	The ``file`` command has been renamed to ``scp``.

Changes to ``ll.orasql``
------------------------

*	The methods :meth:`ll.orasql.Record.keys` and :meth:`ll.orasql.Record.values`
	return iterators now. :meth:`ll.orasql.Record.iterkeys` and
	:meth:`ll.orasql.Record.itervalues` have been removed.


Migrating to version 5.6
========================

Changes to ``ll.oradd``
-----------------------

*	Support for ``"keys"`` and ``"sqls"`` has been removed from :mod:`ll.oradd`.
	So ::

		{
			"type": "procedure",
			"name": "procname",
			"args": {
				"proc_id": "p_10",
				"proc_date": "sysdate",
				"keys": {"proc_id": "int"},
				"sqls": ["proc_date"]
			}
		}

	has to be replaced with ::

		{
			"type": "procedure",
			"name": "procname",
			"args": {
				"proc_id": var("p_10", int),
				"proc_date": sql("sysdate")
			}
		}

*	UL4ON dumps are no longer supported by :mod:`ll.oradd`. They must be
	reencoded as Python ``repr`` outputs, which can be done with code that looks
	like this::

		import sys

		from ll import ul4on

		while True:
			try:
				print(repr(ul4on.load(sys.stdin)))
			except EOFError:
				break


Migrating to version 5.4
========================

Changes to ``ll.url``
---------------------

*	The ``remotepython`` parameter for ``ssh`` URLs has been renamed to ``python``.


Migrating to version 5.2
========================

Changes to ``sisyphus``
-----------------------

*	The method :meth:`prefix` for :mod:`sisyphus` jobs has been replaced with
	:meth:`task` which does something similar.

Changes to UL4
--------------

*	The names of methods that should be callable for custom objects in UL4
	templates must be added to the ``ul4attrs`` attributes.

Changes to ``oradd``
--------------------

*	Committing the transactions in ``oradd`` can now be done after each record
	with the new option ``--commit``. ``--rollback`` has been removed, so you
	have to replace ``--rollback=1`` with ``--commit=never``.

Changes to ``misc``
-------------------

*	The default argument for the functions :func:`misc.first` and
	:func:`misc.last` now defaults to ``None``. I.e. for empty iterators the
	default value will always be returned instead of generating an exception.
	To simulate the old behaviour use a unique guard object as the default.

*	Renamed the attributes ``scriptname`` and ``shortscriptname`` of the
	:obj:`misc.sysinfo` object to ``script_name`` and ``short_script_name``.


Migrating to version 5.1
========================

Changes to ``db2ul4``
---------------------

*	The ``query`` method for database connections has changed: Instead of a
	query and a parameter dictionary, you have to pass in positional arguments
	that alternate between fragments of the SQL query and parameters. I.e.::

		db.query("select * from table where x=:x and y=:y", x=23, y=42)

	becomes::

		db.query("select * from table where x=", 23, " and y=", 42)

	This makes ``db2ul4`` independent from the parameter format of the database
	driver.


Migrating to version 5.0
========================

Changes to XIST
---------------

*	Accessing attributes via :meth:`__getattr__`, :meth:`__setattr__` and
	:meth:`__delattr__` now requires the XML name of the attribute instead of
	the Python name. If you only have the Python name,  you can convert it to
	the XML name with the method :meth:`Attrs._pyname2xmlname`.

*	For all methods that existed in Python/XML pairs (e.g. :meth:`withnames` and
	:meth:`withnames_xml` in :class:`xsc.Attrs` or :meth:`elementclass` and
	:meth:`elementclass_xml` in :class:`xsc.Pool` etc.) there is only one version
	now: A method without the ``_xml`` suffix in the name, that accepts the
	XML version of the name.

*	Validation is now off by default, to turn it on pass ``validate=True`` to
	:func:`parse.tree` or :func:`parse.itertree` for parsing, or to the publisher
	object or the :meth:`bytes`, :meth:`iterbytes`, :meth:`string` or
	:meth:`iterstring` methods for publishing.


Migrating to version 4.10
=========================

Changes to UL4
--------------

*	The UL4 tag ``<?render?>`` have been removed. To update your code replace
	``<?render r.render()?>`` with ``<?exe r.render()?>``.

*	The UL4 functions ``vars`` and ``get`` have been removed.

*	The automatic UL4 variable ``stack`` has been removed too.


Migrating to version 4.7
========================

Changes to UL4
--------------

*	Compiling a UL4 template to a Java ``CompiledTemplate`` is no longer
	supported (i.e. ``template.javasource(interpreted=False)`` no longer works.
	Use ``template.javasource()`` instead (which creates Java sourcecode for
	an ``InterpretedTemplate``).


Migrating to version 4.6
========================

Changes to :mod:`ll.xist`
-------------------------

*	The :meth:`walk` method has been changed to return a :class:`Cursor` object
	instead of the path, so you have to replace::

		for path in doc.walk(...):
			# use path

	with::

		for cursor in doc.walk(...):
			# use cursor.path

*	Furthermore walk filters have been removed. Determining whether an XIST tree
	is traversed top down or bottom up can instead by specified via distinct
	parameters to the :meth:`walk` method. Replace::

		for path in doc.walk((xfind.entercontent, xfind.enterattrs, True)):
			...

	with::

		for cursor in doc.walk(entercontent=True, enterattrs=True, startelementnode=False, endelementnode=True):
			...

	If you want to enter an element only when a condition is true, you can do
	that by modifying the appropriate cursor attribute inside your loop::

		for cursor in doc.walk(entercontent=True, enterattrs=True):
			if isinstance(cursor.node, html.script, html.textarea):
				cursor.entercontent = False
			...

*	:func:`ll.xist.parse.itertree` now returns :class:`Cursor` objects too,
	instead of path lists.

*	Slicing XIST elements now returns a sliced element, instead of a slice from
	the content :class:`Frag`::

		>>> from ll.xist.ns import html
		>>> html.ul(html.li(i) for i in range(5))[1:3].string()
		'<ul><li>1</li><li>2</li></ul>'

	To get a slice from the content simply use::

		>>> html.ul(html.li(i) for i in range(5)).content[1:3].string()
		'<li>1</li><li>2</li>'


Migrating to version 4.4
========================

Changes to the required Python version
--------------------------------------

Python 3.3 is required now.


Migrating to version 4.2
========================

Changes to :mod:`ll.ul4c`
-------------------------

*	The UL4 method ``join`` no longer calls ``str`` on the items in the argument
	list. Replace ``sep.join(iterable)`` with ``sep.join(str(i) for i in iterable)``
	when you have an argument list that contains non-strings.


Migrating to version 4.1
========================

Changes to :mod:`ll.make`
-------------------------

*	The support for Growl notifications in :mod:`ll.make` on the Mac has been
	replaced by support for Mountain Lions Notification Center.

	The option has been renamed from :option:`--growl` to :option:`--notify`.

	For this to work you need to have terminal-notifier__ installed in its
	standard location (``/Applications/terminal-notifier.app``).

	__ https://github.com/alloy/terminal-notifier


Migrating to version 4.0
========================

Changes to the required Python version
--------------------------------------

Python 3.2 is required now.

Changes to UL4
--------------

*	Date constants in UL4 have changed again. They are now written like this:
	``@(2012-04-12)`` or ``@(2012-04-12T12:34:56)``.

*	The function ``json`` has been renamed to ``asjson``.

*	The ``<?render?>`` tag in UL4 now looks like a method call instead of a
	function call. I.e. ``<?render t(a=17, b=23)?>`` has changed to
	``<?render t.render(a=17, b=23)?>``.

Changes to scripts
------------------

*	The scripts ``oracreate``, ``oradrop``, ``oradelete``, ``oradiff``,
	``oramerge``, ``oragrant``, ``orafind`` and ``uhpp`` no longer have an
	:option:`-e`/:option:`--encoding` option. They always use Pythons output
	encoding.

*	The options :option:`-i`/:option:`--inputencoding` and
	:option:`-o`/:option:`--outputencoding` of the script ``db2ul4`` have been
	replaced with an option :option:`-e`/:option:`--encoding` for the encoding
	of the template files. For printing the result Pythons output encoding is
	used.

*	The options :option:`--inputencoding`,/:option:`--inputerrors` and
	:option:`--outputencoding`/:option:`--outputerrors` of
	:class:`ll.sisyphus.Job` have been replaced with option
	:option:`--encoding`/:option:`--errors` for the encoding of the log files.



Migrating to version 3.25
=========================

Changes to XIST
---------------

*	The :meth:`compact` method has been renamed to :meth:`compacted` to avoid
	collisions with the ``compact`` attribute in HTML elements.


Migrating to version 3.24
=========================

Changes to :mod:`ll.xist.ns.ul4`
--------------------------------

*	:class:`ll.xist.ns.ul4.attr_if` is now an :class:`ll.xist.xsc.AttrElement`
	subclass. Change your code from::

		html.div(id=(ul4.attr_if("foo"), "bar"))

	to::

		html.div(id=ul4.attr_if("bar", cond="foo"))

*	:class:`ll.xist.ns.ul4.attr_ifnn` has been removed. Replace it with the
	equivalent :class:`attr_if` call.


Migrating to version 3.23
=========================

Changes to :mod:`ll.ul4c`
-------------------------

*	The module global functions :func:`ll.ul4c.compile`, :func:`ll.ul4c.load` and
	:func:`ll.ul4c.loads` have been removed. Instead of them the :class:`Template`
	constructor and the class methods :meth:`load` and :meth:`loads` can be used.


Migrating to version 3.20
=========================

Changes to :mod:`ll.orasql`
---------------------------

*	The :obj:`schema` argument used by various methods in :mod:`ll.orasql` has
	been replaced by a :obj:`owner` argument that can be :const:`None` (for the
	current user), the constant :const:`ALL` for all users (which uses the
	``DBA_*`` variant of various meta data views if possible or the ``ALL_*``
	variants otherwise) and a specific user name.


Migrating to version 3.19
=========================

Changes to :mod:`ll.orasql`
---------------------------

*	:mod:`ll.orasql` now requires cx_Oracle 5.1 (i.e. ``UNICODE`` mode is no
	longer used).

*	If the :obj:`readlobs` option is false for :mod:`ll.orasql` cursors, the
	CLOBs/BLOBs returned will be wrapped into something that behaves like a
	Python file. The original :class:`LOB` object is available as the ``value``
	attribute of the returned wrapper object::

		db = orasql.connect("user/pwd@db")
		c = db.cursor()
		c.execute("select theclob from thetable")
		row = c.fetchone()
		print row[0].value.read()


Migrating to version 3.18
=========================

Changes to ``db2ul4``
---------------------

*	The variables available in UL4 templates used by ``db2ul4`` have changed.
	Instead of a ``connect`` object, there are now three objects for each
	supported database (i.e. ``oracle``, ``sqlite`` and ``mysql``). To update
	your template replace::

		connect["oracle:user/pwd@db"]

	with::

		oracle["user/pwd@db"]

Changes to scripts
------------------

*	The script ``doc2txt`` now reads from ``stdin`` and writes to ``stdout``
	instead of requiring file names on the command line.


Migrating to version 3.17
=========================

Changes to :mod:`ll.misc`
-------------------------

*	:func:`ll.misc.javastring` has been renamed to :func:`ll.misc.javaexpr`.

*	The UL4 method ``format`` is now a function instead.


Migrating to version 3.16
=========================

Changes to :mod:`ll.misc`
-------------------------

*	:func:`ll.misc.flag` is gone. If the function is still required, here is
	the source::

		def flag(value):
			if value in ("1", "true", "yes"):
				return True
			elif value in ("0", "false", "no"):
				return False
			raise ValueError("unknown flag value")


Migrating to version 3.15
=========================

Changes to :mod:`ll.xist.ns.jsp`
--------------------------------

*	:func:`ll.xist.ns.jsp.javastring` has been move to :mod:`ll.misc`.


Migrating to version 3.14
=========================

Changes to :mod:`ll.ul4c`
-------------------------

*	Date constants now need a ``@`` as a prefix. I.e. chance ``2010-11-03T`` to
	``@2010-11-03T`` etc.

*	The :obj:`function` argument for :meth:`ul4c.Template.pythonsource` is gone.
	The output will always be a full function.


Migrating to version 3.12
=========================

Changes to :mod:`ll.sisyphus`
-----------------------------

*	The maximum allowed runtime for jobs is now a hard limit. Previously a
	running job that exceeded the maximum allowed runtime would only be killed
	when the next job was started. Now the job will kill itself immediately after
	``maxtime`` seconds. This means you *might* have to adjust your ``maxtime``
	setting.

*	The default location of log files has changed again. Now ``~/ll.sisyphus/``
	is used as the base directory instead of ``~/ll.sisyphus/log/``.


Migrating to version 3.11
=========================

Changes to :mod:`ll.sisyphus`
-----------------------------

*	The method :meth:`logLoop` is gone. Replace::

		self.logLoop("done")

	with::

		return "done"

*	The method :meth:`logProgress` is gone. Replace::

		self.logProgress("parsing XML file")

	with::

		self.log("parsing XML file")

	You might also add tags to the logging call via::

		self.log.xml("parsing XML")

	(This adds the tag ``"xml"`` to the log line.)

*	The method :meth:`logError` is gone. Replace::

		self.logError("Can't parse XML file")

	with::

		self.log.error("Can't parse XML file")

	If the object passed to ``self.log`` is an exception, the logging call will
	add the ``exc`` tag automatically.

*	:class:`sisyphus.Job` no longer has a constructor. Configuration is now done
	via class attributes. Replace::

		class TransmogrifyStuff(sisyphus.Job):
			def __init__(self, connectstring):
				sisyphus.Job.__init__(self, 30, "ACME_TransmogrifyStuff", raiseerrors=True)

	with::

		class TransmogrifyStuff(sisyphus.Job):
			projectname = "ACME.MyProject"
			jobname = "TransmogrifyStuff"
			maxtime = 30

*	The default location of run/log files has changed. Now ``~/ll.sisyphus/log``
	is used for log files and ``~/ll.sisyphus/run`` is used for run files.


Migrating to version 3.10
=========================

Changes to the required Python version
--------------------------------------

Python 2.7 is required now.

Changes to :mod:`ll.make`
-------------------------

*	:mod:`ll.make` uses :mod:`argparse` now.

*	:meth:`ll.make.Project.optionparser` has been renamed to :meth:`argparser`
	and returns a :class:`argparse.ArgumentParser` object now.

*	:meth:`ll.make.Project.parseoptions` has been renamed to :meth:`parseargs`
	and returns a :class:`argparse.Namespace` object now.

Changes to :mod:`ll.daemon`
---------------------------

*	:mod:`ll.daemon` uses :mod:`argparse` now. :meth:`ll.daemon.Daemon.optionparser`
	has been renamed to :meth:`argparser`.


Migrating to version 3.9
========================

Changes to :mod:`ll.xist.ns.html`
---------------------------------

*	:class:`ll.xist.ns.html.html` will no longer change the ``lang`` and
	``xml:lang`` attributes. This functionality has been moved to the new element
	:class:`ll.xist.ns.htmlspecials.html`. Furthermore this new element will not
	change an attribute if this attribute has already been set.

	So if you need the functionality replace any use of
	:class:`ll.xist.ns.html.html` with :class:`ll.xist.ns.htmlspecials.html`.

*	:class:`ll.xist.ns.html.title` no longer does any manipulation of its content.

	If you needed this functionality, you can copy it from the old ``title``
	element and put it into your own element class.


Migrating to version 3.8
========================

Changes to parsing
------------------

*	The parsing infrastructure has been completely rewritten to be more modular
	and to support iterative parsing (similar to `ElementTree`__). Now parsing
	XML is done in a pipeline approach.

	__ http://effbot.org/zone/element-iterparse.htm

	Previously parsing a string looked like this::

		>>> from ll.xist import xsc, parsers
		>>> from ll.xist.ns import html
		>>> source = "<a href='http://www.python.org/'>Python</a>"
		>>> doc = parsers.parsestring(source, pool=xsc.Pool(html))

	Now this is done the following way::

		>>> from ll.xist import xsc, parse
		>>> from ll.xist.ns import html
		>>> source = "<a href='http://www.python.org/'>Python</a>"
		>>> doc = parse.tree(
		... 	parse.String(source)
		... 	parse.Expat()
		... 	parse.NS(html)
		... 	parse.Node(pool=xsc.Pool(html))
		... )

	For more info see the module :mod:`ll.xist.parse`.

*	Something that no longer works is parsing XML where elements from different
	namespaces use the same namespace prefix. You will either have to rewrite
	your XML or implement a new class for the parsing pipeline that handles
	namespaces prefixes *and* instantiating XIST classes (i.e. a combination
	of what :class:`ll.xist.parse.NS` and :class:`ll.xist.parse.Node` do).

*	The module :mod:`ll.xist.parsers` has been renamed to :mod:`parse`.

*	The module :mod:`ll.xist.presenters` has been renamed to :mod:`present`.

*	The classes :class:`ll.xist.converters.Converter` and
	:class:`ll.xist.publishers.Publisher` have been moved to :mod:`ll.xist.xsc`.
	The modules :mod:`ll.xist.converters` and :mod:`ll.xist.publishers` no longer
	exist.

Changes to XISTs walk filters
-----------------------------

*	The walk methods :meth:`walknode` and :meth:`walkpath` have been renamed to
	:meth:`walknodes` and :meth:`walkpaths`. The class :class:`WalkFilter` has
	been moved to :mod:`ll.xist.xfind`.

Changes to :mod:`ll.url`
------------------------

*	:class:`ll.url.Path` has been simplified: Path segments are strings instead
	of tuples. If you need the path parameters (i.e. part after ``;`` in a path
	segment) you have to split the segment yourself.

*	:meth:`ll.url.URL.import_` is gone. As a replacement :func:`misc.module` can
	be used, i.e. replace::

		>>> from ll import url
		>>> u = url.File("foo.py")
		>>> m = u.import_(mode="always")

	with::

		>>> from ll import url, misc
		>>> u = url.File("foo.py")
		>>> m = misc.module(u.openread().read(), u.local())

	However, note that :meth:`ll.url.URL.import_` has been reintroduced in 3.8.1
	based on :func:`misc.import`. This means that the mode argument is no longer
	supported.

*	ssh URLs now required to standalone :mod:`execnet` package__. The
	``ssh_config`` parameter for ssh URLs is gone.

	__ http://codespeak.net/execnet/

Changes to :mod:`ll.make`
-------------------------

*	The two classes :class:`ll.make.PoolAction` and
	:class:`ll.make.XISTPoolAction` have been dropped. To update your code,
	replace::

		make.XISTPoolAction(html)

	with::

		make.ObjectAction(xsc.Pool).call(html)

*	The class :class:`XISTParseAction` has been removed. This action can be
	replaced by a combination of :class:`ObjectAction`, :class:`CallAction` and
	:class:`CallAttrAction` using the new parsing infrastructure.

Other changes
-------------

*	:class:`ll.xist.ns.specials.z` has been moved to the :mod:`ll.xist.ns.doc`
	module.


Migrating to version 3.7
========================

Changes to the make module
--------------------------

*	The division operator for actions is no longer implemented, so instead of::

		t1 = make.FileAction(key=url.URL("file:foo.txt"))
		t2 = t1 /
		     make.DecodeAction("iso-8859-1") /
		     make.EncodeAction("utf-8") /
		     make.FileAction(key=url.URL("bar.txt"))

	you now have to write something like the following::

		t1 = make.FileAction("file:foo.txt")
		t2 = t1.callattr("decode", "iso-8859-1")
		t2 = t2.callattr("encode", "utf-8")
		t2 = make.FileAction("file:bar.txt", t2)

*	Also the following classes have been removed from :mod:`ll.make`:
	:class:`EncodeAction`, :class:`DecodeAction`, :class:`EvalAction`,
	:class:`GZipAction`, :class:`GUnzipAction`,
	:class:`JavascriptMinifyAction`, :class:`XISTBytesAction`,
	:class:`XISTStringAction`, :class:`JoinAction`, :class:`UnpickleAction`,
	:class:`PickleAction`, :class:`TOXICAction`, :class:`TOXICPrettifyAction`,
	:class:`SplatAction`, :class:`UL4CompileAction`, :class:`UL4RenderAction`,
	:class:`UL4DumpAction`, :class:`UL4LoadAction`, :class:`XISTTextAction` and
	:class:`XISTConvertAction`. All of these actions can be executed by using
	:class:`CallAction` or :class:`CallAttrAction`.


Migrating to version 3.6
========================

Changes to the color module
---------------------------

*	The following :class:`Color` class methods have been dropped: ``fromrgba``,
	``fromrgba4``, ``fromrgba8``, ``fromint4``, ``fromint8``.

*	The following :class:`Color` properties have been dropped: ``r4``, ``g4``,
	``b4``, ``a4``, ``r8``, ``g8``, ``b8``, ``a8``, ``r``, ``g``, ``b``,  ``a``
	``int4``, ``int8``, ``rgb4``, ``rgba4``, ``rgb8``, and ``rgba8``. The new
	methods ``r``, ``g``, ``b`` and ``a`` return the 8 bit component values.

*	The class methods ``fromhsva`` and ``fromhlsa`` have been renamed to
	``fromhsv`` and ``fromhls``.

*	The property ``css`` has been dropped. The CSS string is returned by
	``__str__`` now.

*	Dividing colors now does a scalar division. Blending colors is now done with
	the modulo operator.

Removal of XPIT
---------------

*	The XPIT templating language has been removed. You should replace all your
	XPIT templates with UL4 templates.


Migrating to version 3.5
========================

Changes to UL4
--------------

*	The UL4 function ``csvescape`` has been renamed to ``csv``.

Changes to the color module
---------------------------

*	:class:`ll.color.Color` has been rewritten to create immutable objects
	with the components being 8 bit values (i.e. 0-255) instead of floating
	point values between 0 and 1.


Migrating to version 3.4
========================

Changes to the make module
--------------------------

*	:class:`ll.make.CallMethAction` has been renamed to :class:`CallAttrAction`.

*	:class:`ll.make.XISTPublishAction` has been renamed to :class:`XISTBytesAction`.

Changes to UL4
--------------

*	The templates available to the ``<?render?>`` tag are no longer passed as a
	separate argument to the render methods, but can be part of the normal
	variables.

Changes to XIST
---------------

*	Building trees with ``with`` blocks has changed slightly. Unchanged code will
	lead to the following exception::

		File "/usr/local/lib/python2.5/site-packages/ll/xist/xsc.py", line 1285, in __enter__
			threadlocalnodehandler.handler.enter(self)
		AttributeError: 'NoneType' object has no attribute 'enter'

	To fix this, change your code from::

		with html.html() as node:
			with html.head():
				+html.title("Foo")
			with html.body():
				+html.p("The foo page!")

	to::

		with xsc.build():
			with html.html() as node:
				with html.head():
					+html.title("Foo")
				with html.body():
					+html.p("The foo page!")

	(i.e. wrap the outermost ``with`` block in another ``with xsc.build()``
	block.)


Migrating to version 3.3
========================

Changes to the make module
--------------------------

*	:class:`ll.make.ImportAction` has been dropped as now the module object can
	be used directly (e.g. as the input for an :class:`XISTPoolAction` object).

*	The constructor of most action classes now accept the input action as a
	parameter again. This means that you might have to change the calls.
	Usually it's safest to use keyword arguments. I.e. change::

		make.FileAction(url.File("foo.txt"))

	to::

		make.FileAction(key=url.File("foo.txt"))

*	The :obj:`targetroot` parameter for :meth:`ll.make.XISTConvertAction.__init__`
	has been renamed to :obj:`root`.

Changes to TOXIC
----------------

*	TOXIC has been split into a compiler and an XIST namespace module. Instead
	of calling the function :func:`ll.xist.ns.toxic.xml2ora` you now have to use
	:func:`ll.toxicc.compile`. (However using TOXIC with :mod:`ll.make` hasn't
	changed).

Changes to XIST
---------------

*	The default parser for XIST is expat now. To switch back to sgmlop simply
	pass an :class:`SGMLOPParser` object to the parsing functions::

		>>> from ll.xist import parsers
		>>> node = parsers.parsestring("<a>", parser=parsers.SGMLOPParser())


Migrating to version 3.2.6
==========================

Changes to escaping
-------------------

The functions :mod:`ll.xist.helpers.escapetext` and
:mod:`ll.xist.helpers.escapeattr` have been merged into :mod:`ll.misc.xmlescape`
and all the characters ``<``, ``>``, ``&``, ``"`` and ``'`` are escaped now.


Migrating to version 3.1
========================

Changes to URL handling
-----------------------

URLs containing processing instructions will no longer be transformed in
any way. If you need the old behaviour you can wrap the initial part of
the attribute value into a :class:`specials.url` PI.


Migrating to version 3.0
========================

Changes to tree traversal
-------------------------
You can no longer apply xfind expression directly to nodes, so instead of::

	for node in root//html.p:
		print node

you have to write::

	for node in root.walknode(html.p):
		print node

If you want the search anchored at the root node, you can do the following::

	for node in root.walknode(root/html.p):
		print node

This will yield :class:`html.p` elements only if they are immediate children of
the ``root`` node.

Passing a callable to the :meth:`walk` method now creates a
:class:`ll.xist.xfind.CallableSelector`. If you want the old tree traversal
logic back, you have to put your code into the :meth:`filterpath` method of a
:class:`WalkFilter` object.

Many of the XFind operators have been renamed (and all have been rewritten).
See the :mod:`xfind` documentation for more info.

The death of namespace modules
------------------------------

It's no longer possible to turn modules into namespaces. Element classes belong
to a namespace (in the XML sense) simply if their ``xmlns`` attribute have the
same value. So a module definition like this::

	from ll.xist import xsc

	class foo(xsc.Element):
		def convert(self, converter):
			return xsc.Text("foo")

	class xmlns(xsc.Namespace):
		xmlname = "foo"
		xmlurl = "http://xmlns.example.org/foo"
	xmlns.makemod(vars())

has to be changed into this::

	from ll.xist import xsc

	class foo(xsc.Element):
		xmlns = "http://xmlns.example.org/foo"

		def convert(self, converter):
			return xsc.Text("foo")

Renamed :mod:`doc` classes
--------------------------

Many classes in the :mod:`ll.xist.ns.doc` module have been renamed. The
following names have changed:

*	``function`` to ``func``;
*	``method`` to ``meth``;
*	``module`` to ``mod``;
*	``property`` to ``prop``;
*	``title`` to ``h``;
*	``par`` to ``p``;
*	``olist`` to ``ol``;
*	``ulist`` to ``ul``;
*	``dlist`` to ``dl``;
*	``item`` to ``li`` or ``dd`` (depending on whether it's inside an
	:class:`ol`, :class:`ul` or :class:`dl`);
*	``term`` to ``dt``;
*	``link`` to ``a``.


Migrating to version 2.15
=========================

Changes to plain text conversion
--------------------------------

The node method :meth:`asText` has been moved to the :mod:`html` namespace,
so you have to replace::

	print node.asText()

with::

	from ll.xist.ns import html
	print html.astext(node)

Changes to :class:`htmlspecials.pixel`
--------------------------------------

If you've been using the ``color`` attribute for :class:`htmlspecials.pixel`,
you have to add a ``#`` in from of the value, as it is a CSS color value now.
(And if've you've been using ``color`` and a CSS padding of a different color:
This will no longer work).


Migrating to version 2.14
=========================

Changes to presenters
---------------------

Presenters work differently now. Instead of::

	print node.asrepr(presenters.CodePresenter)

simply do the following::

	print presenters.CodePresenter(node)


Migrating to version 2.13
=========================

Changes to :mod:`ll.xist.xsc`
-----------------------------

:meth:`xsc.Namespace.tokenize` no longer has an :obj:`encoding` argument, but
operates on a unicode string directly. You can either use the result of a
:meth:`asString` call or decode the result of an :meth:`asBytes` call yourself.


Migrating to version 2.11
=========================

Changes to :mod:`ll.xist.xsc`
-----------------------------

The function :func:`ToNode` has been renamed to :func:`tonode`.

:class:`ll.xist.Context` no longer subclasses :class:`list`. If you need a stack
for your context, simply add the list as an attribute of the context object.

Code rearrangements
-------------------

The iterator stuff from :mod:`ll.xist.xfind` has been moved to the :mod:`ll`
package/module, i.e. you have to use :func:`ll.first` instead of
:func:`ll.xist.xfind.first`.

Changes to the :meth:`walk` method
----------------------------------

The :meth:`walk` method has changed again. There are no inmodes and outmodes any
longer. Instead input and output are :class:`Cursor` objects. If you're using
your own :meth:`walk` filters, you have to update them. For different output
modes you can use the methods :meth:`walknode`, :meth:`walkpath` or
:meth:`walkindex` instead of using the cursor yielded by :meth:`walk`.

The node methods :meth:`find` and :meth:`findfirst` have been removed. Use
``xsc.Frag(node.walk(...))`` or ``node.walk(...)[0]`` instead.

Changes to publishing
---------------------

Publishing has changed: If you've used the method :meth:`repr` before to get a
string representation of an XML tree, you have to use :meth:`asrepr` instead now
(:meth:`repr` is a generator which will produce the string in pieces).

Changes to the :mod:`xfind` module
----------------------------------

The functions :func:`item`, :func:`first`, :func:`last`, :func:`count` and
:func:`iterone` as well as the class :class:`Iterator` have been moved to the
:mod:`ll` module.


Migrating to version 2.10
=========================

Changes to publishing
---------------------

Publishing has been changed from using a stream API to using a iterator API. If
you've been using :meth:`Publisher.write` or :meth:`Publisher.writetext` (in
your own :meth:`publish` methods) you must update your code by replacing
``publisher.write(foo)`` with ``yield publisher.encode(foo)`` and
``publisher.writetext(foo)`` with ``yield publisher.encodetext(foo)``.

Changes to the test suite
-------------------------

The test suite now uses py.test__, so if you want to run it you'll need py.test.

__ http://codespeak.net/py/current/doc/test.html

Changes to :mod:`ll.xist.ns.code`
---------------------------------

The code in a :class:`ll.xist.ns.code.pyexec` object is no longer executed at
construction time, but at conversion time. So if you relied on this fact (e.g.
to make a namespace available for parsing of the rest of the XML file) you will
have to change your code.

Removed namespaces
------------------

The namespace modules :mod:`ll.xist.ns.css` and :mod:`ll.xist.ns.cssspecials`
have been removed.


Migrating to version 2.9
========================

Changes to exceptions
---------------------

All exception classes have been moved from :mod:`ll.xist.errors` to
:mod:`ll.xist.xsc`.

Changes to XML name handling
----------------------------

The class attribute :attr:`xmlname` no longer gets replaced with a tuple
containing both the Python and the XML name. If you want to get the Python name,
use ``foo.__class__.__name__``.

Changes to the methods :meth:`walk`, :meth:`find` and :meth:`findfirst`
-----------------------------------------------------------------------

The argument :obj:`filtermode` has been renamed to :obj:`inmode` and (for
:meth:`walk`) :obj:`walkmode` has been renamed to :obj:`outmode`.


Migrating to version 2.8
========================

Changes to display hooks
------------------------

The way XIST uses :func:`sys.displayhook` has been enhanced. To make use of
this, you might want to update your Python startup script. For more info see the
`installation instructions`__.

__ http://www.livinglogic.de/xist/Installation.html

Changes to the :attr:`xmlns` attribute
--------------------------------------

Each element (or entity, or processing instruction) class had an attribute
:attr:`xmlns` that references the namespace module. This attribute has been
renamed to :attr:`__ns__`.

Other minor changes
-------------------

:class:`ll.xist.ns.specials.x` has been renamed to
:class:`ll.xist.ns.specials.ignore`.

:class:`ll.xist.xfind.item` no longer handles slices. If you've used that
functionality, you may now use slices on XFind operators, and materialize the
result, i.e. replace ``xfind.slice(foo, 1, -1)`` with ``list(foo[1:-1])``, if
``foo`` is an XFind operator. Otherwise you can use ``list(foo)[1:-1]``.


Migrating to version 2.7
========================

Changes to :mod:`ll.xist.xfind`
-------------------------------

The functions :func:`xfind.first` and :func:`xfind.last` now use
:func:`xfind.item`, so they will raise an :exc:`IndexError` when no default
value is passed. To get the old behaviour, simply pass :const:`None` as the default.


Migrating to version 2.6
========================

Changes to the publishing API
-----------------------------

The top level publishing method in the publisher has been renamed from
:meth:`dopublication` to :meth:`publish`. If you're using the publishing API
directly (instead of the node methods :meth:`asBytes` and :meth:`write`), you'll
have to update your code.

The method that writes a unicode object to the output stream has been renamed
from :meth:`publish` to :meth:`write`. This is only relevant when you've
overwritten the :meth:`publish` method in your own node class (e.g. in JSP tag
library directives or similar stuff, or for special nodes that publish some text
literally).

Changes to the presentation API
-------------------------------

The presentation API has been changed too: The top level presentation method in
the presenter has been renamed from :meth:`dopresentation` to :meth:`present`.
This is only relevant if you've written your own presenter, or are using the
presentation API directly (instead of the node method :meth:`repr`).

Parsing HTML
------------

Parsing HTML is now done via libxml2's HTML parser, instead of using µTidyLib of
mxTidy. You can no longer pass arguments to tidy. Only the boolean values of the
:obj:`tidy` argument will be used. There are no other visible changes to the API
but the result of parsing might have changed.

Removed APIs and scripts
------------------------

The script ``xscmake.py`` has been removed.

The :meth:`visit` method has been removed.

:meth:`ll.xist.xsc.FindOld` has been removed.

:class:`ll.xist.ns.xml.header` has been renamed to
:class:`ll.xist.ns.xml.declaration`.


Migrating to version 2.5
========================

Changes to content model
------------------------

The boolean class attribute :attr:`empty` for element classes has been replaced
by an object :attr:`model`. :attr:`empty` is still supported, but issues a
:class:`PendingDeprecationWarning`. If you don't want to specify a proper
content model for your own elements you can replace ``empty = False`` with
``model = True`` (which is a shortcut for ``model = sims.Any()``) and
``empty = True`` with ``model = False`` (which is a shortcut for
``model = sims.Empty()``).


Migrating to version 2.4
========================

Changes to parsing
------------------

Parsing has changed internally, but the module level parsing functions in
:mod:`ll.xist.parsers` are still available (and will create a parser on the
fly), but a few arguments have changed:

:obj:`handler`
	This argument is no longer available, if you need a special handler, you
	have to subclass :class:`ll.xist.parsers.Parser` and call its parsing
	methods.

:obj:`parser`
	This argument has been renamed to :obj:`saxparser` and is *not* a SAX2
	parser instance any longer, but a callable that will create a SAX2 parser.

:obj:`sysid`
	:obj:`sysid` is now available for all parsing functions not just
	:func:`parseString`.

Changes to converter contexts
-----------------------------

:meth:`ll.xist.converters.Converter.__getitem__` now doesn't use the key passed
in, but ``key.Context`` as the real dictionary key. This has the following
consequences:

*	If you want a unique context for your own element class, you *must*
	implement a new :class:`Context` class (otherwise you'd get
	:class:`ll.xist.xsc.Element.Context`)::

		class Foo(xsc.Element):
			empty = False

			class Context(xsc.Element.Context):
				def __init_(self):
					xsc.Element.Context.__init__(self)
					...

*	Subclasses that don't overwrite :class:`Context` (as well as instances of
	those classes) can be passed to
	:meth:`ll.xist.converters.Converter.__getitem__` and the unique base class
	context object will be returned.

Changed namespaces
------------------

The character reference classes from :mod:`ll.xist.ns.ihtml` that are duplicates
of those in :mod:`ll.xist.ns.chars` have been removed, so you have to use
:mod:`ll.xist.ns.chars` for those characters in addition to
:mod:`ll.xist.ns.ihtml`


Migrating to version 2.3
========================

Changes in namespace handling
-----------------------------

Namespace handling has changed. There are no entity or processing instruction
prefixes any longer and creating a proper :class:`Prefixes` object has been
simplified. For example::

	prefixes = xsc.Prefixes()
	prefixes.addElementPrefixMapping(None, html)
	prefixes.addElementPrefixMapping("svg", svg)

can be simplified to::

	prefixes = xsc.Prefixes(html, svg=svg)

The three arguments :obj:`elementmode`, :obj:`entitymode` and
:obj:`procinstmode` for the publishing methods have been combined into
:obj:`prefixmode`, which is used for elements only.

Changed namespaces
------------------

The character reference classes from :mod:`ll.xist.ns.html` have been moved
to a separate namespace :mod:`ll.xist.ns.chars`.

The processing instructions :class:`eval_` and :class:`exec_` from the
:mod:`ll.xist.ns.code` module have been renamed to :class:`pyeval` and
:class:`pyexec`.

Changed method names
--------------------
The method names :meth:`beginPublication`, :meth:`endPublication` and
:meth:`doPublication` have been lowercased.


Migrating to version 2.2
========================

Attribute methods
-----------------

The :class:`Element` methods for accessing attributes have been deprecated. So
instead of ``node.hasattr("attr")``, you should use::

	"attr" in node.attrs

The same holds for checking whether an attribute is allowed. You can use the
following code::

	"attr" in node.Attrs

or::

	"attr" in NodeClass.Attrs

or::

	NodeClass.isallowed("attr")

Many :class:`Attrs` methods have gained an additional parameter :obj:`xml`,
which specifies whether an attribute name should be treated as the XML or the
Python name of the attribute. Make sure that you're not mixing up your arguments
in the function call. The safest method for this is using keyword arguments,
e.g.::

	node.attr.get("attr", default=42)

JSP directive page element
--------------------------

A ``contentType`` attribute is no longer generated for the
:class:`ll.xist.ns.jsp.directive_page`. You have to explicitly use an attribute
``contentType="text/html"`` to get a ``contentType`` attribute in the resulting
JSP. The ``charset`` option is generated automatically from the encoding
specified in the publisher.

:class:`autoimg` changes
------------------------

:class:`ll.xist.htmlspecials.autoimg` will no longer touch existing ``width`` or
`height`` attributes, so e.g. setting the width to twice the image size via
``width="2*%(width)s"`` no longer works. You have to implement your own version
of :class:`autoimg` if you need this.

:meth:`find` changes
--------------------

:meth:`find` has been completely rewritten to use the new tree traversal
filters. For backwards compatibility a filter functor
:class:`ll.xist.xsc.FindOld` exists that takes the same arguments as the old
:meth:`find` method. I.e. you can replace::

	node.find(
		type=html.a,
		attr={"href": None},
		searchchildren=True
	)

with::

	node.find(
		xsc.FindOld(
			type=html.a,
			attr={"href": None},
			searchchildren=True
		),
		skiproot=True
	)

But one minor difference remains: when :obj:`skiproot` is set to true in the new
:meth:`find` method, the attributes of the root element will *not* be traversed.
With the old method they would be traversed.

:class:`doc` changes
--------------------

:class:`programlisting` has been renamed to :class:`prog`.

Namespace changes
-----------------

Namespaces can no longer be instantiated. Instead you have to derive a class
from :class:`Namespace`. The :obj:`xmlprefix` argument from the constructor
becomes a class attribute :attr:`xmlname` and the argument :obj:`xmlname`
becomes :attr:`xmlurl`.

Adding element classes to the namespace is now done with the :class:`Namespace`
classmethod :meth:`update`. If you want the turn a namespace into a module, you
can use the classmethod :meth:`makemod` instead of :meth:`update`, i.e. replace::

	xmlns = xsc.Namespace("foo", "http://www.foo.com/", vars())

with::

	class xmlns(xsc.Namespace):
		xmlname = "foo"
		xmlurl = "http://www.foo.com/"
	xmlns.makemod(vars())


Migrating to version 2.1
========================

The method :meth:`withSep` has been renamed to :meth:`withsep`.

The argument :obj:`defaultEncoding` for the various parsing functions has been
renamed to :obj:`encoding`.


Migrating to version 2.0
========================

Attribute handling
------------------

The biggest change is in the way attributes are defined. In older versions you
had to define a class attribute :attr:`attrHandlers` that mapped attribute names
to attribute classes. This created problems with "illegal" attribute names (e.g.
``class`` and ``http-equiv`` in HTML), so for them an ugly workaround was
implemented. With 2.0 this is no longer neccessary. Defining attributes is done
via a class :class:`Attrs` nested inside the element class like this::

	class foo(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class bar(xsc.TextAttr)
				"The bar attribute"
				default = "spam"
				values = ("spam", "eggs")
				required = True
			class baz(xsc.URLAttr):
				"The baz attribute"

Default values, set of allowed attributes values and whether the attribute is
required can be defined via class attributes as shown above. You should
(directly or indirecty) inherit from :class:`xsc.Element.Attrs`, because this
class implements handling of global attributes. If you want to inherit some
attributes (e.g. from your base class), you can derive from the appropriate
:class:`Attrs` class. Removing an attribute you inherited can be done like
this::

	class bar(foo):
		class Attrs(foo.Attrs):
			baz = None

This removes the attribute ``baz`` inherited from :class:`foo`.

For attribute names that are no legal Python identifiers, the same method can be
used as for element classes: Define the real XML name via a class attribute.
This class attribute has been renamed from :attr:`name` to :attr:`xmlname`.

This also means that you always have to use the Python name when using
attributes now. The XML name will only be used for parsing and publishing.

XIST 2.0 tries to be as backwards compatible as possible: An existing
:attr:`attrHandlers` attribute will be converted to an :class:`Attrs` class on
the fly (and will generate a :class:`DeprecationWarning` when the class is
created). An :class:`Attrs` class will automatically generate an
:attr:`attrHandlers` attribute, so it's possible to derive from new element
classes in the old way. The only situation where this won't work, is with
attributes where the Python and XML name differ, you have to use "new style"
attributes there.

Namespace support
-----------------

XIST supports XML namespaces now and for parsing it's possible to configure
which namespaces should be available for instantiating classes from. For more
info about this refer to the documentation for the class :class:`Prefixes`.

Before 2.0 the XML name for a namespace object was pretty useless, now it can be
used as the namespace name in ``xmlns`` attributes and it will be used for that
when publishing and specifying an ``elementmode`` of ``2`` in the call to the
publishing method or the constructor of the publisher.

Namespace objects should now be named ``xmlns`` instead of ``namespace`` as
before.

Global attributes
-----------------

Global attributes are supported now, e.g. the attributes ``xml:lang`` and
``xml:space`` can be specified in an element constructor like this::

	from ll.xist import xsc
	from ll.xist.ns import html, xml

	node = html.html(
		content,
		{(xml, "lang"): "en", (xml, "space"): "preserve"},
		lang="en"
	)

Instead of the module object (which must contain a namespace object named
``xmlns``), you can also pass the namespace object itself (i.e. ``xml.xmlns``)
or the namespace name (i.e. ``"http://www.w3.org/XML/1998/namespace"``).

Namespace changes
-----------------

The classes :class:`XML` and :class:`XML10` have been moved from
:mod:`ll.xist.xsc` to :mod:`ll.xist.ns.xml`.

All the classes in :mod:`ll.xist.ns.specials` that are specific to HTML
generation have been moved to the new module :mod:`ll.xist.ns.htmlspecials`.

The module :mod:`ll.xist.ns.html` has been updated to the XHTML specification,
so there might be some changes. The new feature for specifying attribute
restrictions has been used, so e.g. you'll get warnings for missing ``alt``
attributes in :class:`img` elements. These warnings are issued via the warning
framework. Refer to the documentation for the :mod:`warnings` module to find out
how to configure the handling of these warnings.

Miscellaneous
-------------

XIST now requires at least Python 2.2.1 because the integer constants
:const:`True` and :const:`False` are used throughout the code wherever
appropriate. These constants will become instances of the new class
:class:`bool` in Python 2.3. You might want to change your code too, to use
these new constant (e.g. when setting the element class attribute
:attr:`empty`).

Using mixed case method names was a bad idea, because this conflicts with
Python's convention of using all lowercase names (without underscores). These
method names will be fixed in the next few XIST versions. The first names that
where changed were the element methods :meth:`getAttr` and :meth:`hasAttr`,
which have been renamed to :meth:`getattr` and :meth:`hasattr` respectively.
:meth:`getAttr` and :meth:`hasAttr` are still there and can be called without
generating deprecation warnings, but they will start to generate warnings in the
upcoming versions.
