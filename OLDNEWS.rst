The following list of changes is for modules and packages that where merged
into XIST (starting with XIST 3.2) or into the former core package (starting
with XIST 2.12).


Changes in the new core package
###############################

Changes in 1.11.1 (released 01/11/2008)
=======================================

*	Added missing source file ``_xml_codec_include.c`` to the source
	distributions.


Changes in 1.11 (released 01/07/2008)
=====================================

*	``root:`` URLs are now treated as local files for purposes of file i/o.

*	:class:`ll.make.ModuleAction` no longer supports modules that fiddle with
	``sys.modules``.

*	The function :func:`ll.misc.tokenizepi` can be used to split a string
	according to the processing instruction tags in the string (this formerly
	was part of :mod:`ll.xist.xsc`).

*	:mod:`ll.make` has been changed interally to store modification timestamp,
	which should fix the implementation of :class:`PhonyAction` and makes it
	possible to use :class:`PhonyAction` objects as inputs to other actions.

*	:mod:`ll.make` has a new action :class:`ImportAction`. This action doesn't
	take any input. It imports a module specified by name, e.g.
	``make.ImportAction("cStringIO")`` (Note that you should not import one
	module via :class:`ModuleAction` and :class:`ImportAction` (or a normal
	import) as this will return two different module objects).

*	Make actions don't have the input actions as a constructor parameter any
	longer. The input action can now only be set via :meth:`__div__`.

*	:mod:`ll.make` has been updated to support the actions required by XIST 3.0.

*	The functions :func:`misc.item`, :func:`misc.first`, :func:`misc.last` and
	:func:`misc.count` have been reimplemented in C and should be faster now
	(especally :func:`item` for negative indexes).

*	:class:`misc.Namespace` is gone and has been replaced with :class:`misc.Pool`
	which works similar to the pools use by XIST (in fact XISTs pool class is
	a subclass of :class:`misc.Pool`).

*	The module :mod:`xml_codec` has been added. It contains a complete codec
	for encoding and decoding XML.


Changes in 1.10.1 (released 07/20/2007)
=======================================

*	Fix option handling in :mod:`ll.daemon` (values from the optionparser where
	never used).


Changes in 1.10 (released 06/21/2007)
=====================================

*	:mod:`ll.daemon` now uses :mod:`optparse` to parse the command line options.
	Start options ``restart`` and ``run`` have been added.


Changes in 1.9.1 (released 04/03/2007)
======================================

*	Fixed a bug in :class:`ll.url.SshConnection`, which was missing a call to
	:func:`urllib.url2pathname`.


Changes in 1.9 (released 03/30/2007)
====================================

*	:class:`ll.url.Context` no longer relies on automatic cleanup for closing
	connections. Instead when a :class:`Context` object is used in a ``with``
	block, all connections will be closed at the end of the block. This should
	finally fix the problem with hanging threads at the end of the program.

*	A script ``ucp.py`` has been added that can be used to copy stuff around::

		$ ucp -v http://www.python.org ssh://root@www.example.net/~joe/public_html/index.html -u joe -g users


Changes in 1.8 (released 03/12/2007)
====================================

*	In calls to :class:`ll.url.URL` methods that get forwarded to a connection
	it's now possible to pass keyword arguments for the connection constructor
	directly to the called method, i.e. you can do::

		>>> u = url.URL("ssh://root@www.example.com/etc/passwd")
		>>> u.size(identity="/root/.ssh/id_rsa")
		1550


Changes in 1.7.5 (released 03/09/2007)
======================================

*	:class:`ll.url.Resource` now has a method :meth:`encoding` that returns
	``None`` (for "encoding unknown").


Changes in 1.7.4 (released 03/08/2007)
======================================

*	:class:`ll.url.SshConnection` objects now supports the :var:`identity`
	parameter. This can be used to specify the filename to be used as the
	identity file (private key) for authentication.


Changes in 1.7.3 (released 02/22/2007)
======================================

*	:class:`ll.url.SshConnection` now has a new method :meth:`close` which can
	be used to shut down the communication channel. As a :class:`SshConnection`
	no longer stores a reference to the context, this means that ssh
	connections are shut down immediately after the end of the context in which
	they are stored. This avoids a problem with hanging threads.


Changes in 1.7.2 (released 02/02/2007)
======================================

*	Fixed a bug in :func:`ll.url._import`.


Changes in 1.7.1 (released 01/24/2007)
======================================

*	:mod:`ll.astyle` has been updated to the current trunk version of
	IPython__.

	__ http://ipython.scipy.org/

*	As the :mod:`new` module is deprecated, use :mod:`types` instead.


Changes in 1.7 (released 11/23/2006)
====================================

*	Fixed a bug in the user switching in :class:`ll.daemon.Daemon`.

*	Added a new action class :class:`GetAttrAction` to :mod:`ll.make`. This
	action gets an attribute of its input object.


Changes in 1.6.1 (released 11/22/2006)
======================================

*	:class:`ll.make.ModuleAction` now puts a real filename into the modules
	``__file__`` attribute, so that source code can be displayed in stacktraces.

*	:mod:`ll.astyle` has been fixed to work with the current trunk version of
	IPython__.

	__ http://ipython.scipy.org/


Changes in 1.6 (released 11/08/2006)
====================================

*	:mod:`ll.url` now supports ssh URLs which are files on remote hosts.
	This requires `py.execnet`_. Most of the file data and metadata handling
	has been rewritten to support the requirements of ssh URLs.

	.. _py.execnet: http://codespeak.net/py/current/doc/execnet.html

*	:class:`ll.make.ModeAction` and :class:`ll.make.OwnerAction` are subclasses
	of :class:`ll.make.ExternalAction` now. This means they will execute even
	in "infoonly" mode.

*	Fixed a bug in :meth:`ll.make.JoinAction.get`.

*	Remove the pid file for :meth:`ll.sisyphus.Job` when a
	:class:`KeyboardInterrupt` happens and we're running on Python 2.5.

*	Fixed a longstanding bug in :meth:`ll.sisyphus.Job` which resulted in the
	pid file not being written in certain situations.

*	:class:`ll.daemon.Daemon` now allows to switch the group too.


Changes in 1.5 (released 09/24/2006)
====================================

*	:class:`ll.make.XISTTextAction` is compatible to XIST 2.15 now.

*	The functions :func:`ll.url.Dirname` and :func:`ll.url.Filename` have been
	removed (use :func:`ll.url.Dir` and :func:`ll.url.File` instead).

*	The methods :meth:`ll.url.URL.isLocal` and :meth:`ll.url.URL.asFilename`
	have been removed (use :meth:`ll.url.URL.islocal` and :meth:`ll.url.URL.local`
	instead).


Changes in 1.4 (released 08/23/2006)
====================================

*	A new module has been added: :mod:`ll.daemon` can be used on UNIX to fork a
	daemon running.


Changes in 1.3.2 (released 07/25/2006)
======================================

*	:class:`ll.make.ModuleAction` now normalizes line feeds, so that this
	action can now be used directly on Windows too.


Changes in 1.3.1 (released 07/06/2006)
======================================

*	An option ``showinfoonly`` has been added to :class:`ll.make.Project`
	(defaulting to ``False``). This option determines whether actions that run
	in ``infoonly`` mode are reported or not.


Changes in 1.3 (released 06/28/2006)
====================================

*	:mod:`ll.make` has been rewritten. Now there's no longer a distinction
	between :class:`Target`\s and :class:`Action`\s. Actions can be chained more
	easily and creating an action and registering it with the project are two
	separate steps. Actions can no longer be shared, as each action stores its
	own input actions (but output actions are not stored). "Ids" have been
	renamed to "keys" (and :class:`DBID`/:class:`OracleID` to
	:class:`DBKey`/:class:`OracleKey`). :class:`ImportAction` has been renamed
	to :class:`ModuleAction` and can now turn any string into a module.

*	In :mod:`ll.url` modification dates for local files now include
	microseconds (if the OS supports it).

*	A class :class:`Queue` has been added to :mod:`ll.misc` which provides FIFO
	queues.

*	A decorator :func:`withdoc` has been added to :mod:`ll.misc` that sets the
	docstring on the function it decorates.

*	:mod:`setuptools` is now supported for installation.


Changes in 1.2 (released 12/13/2005)
====================================

*	``None`` is now allowed as a proper data object in :mod:`ll.make` actions.

*	:mod:`ll.xpit` now supports conditionals (i.e. the new processing
	instruction targets ``if``, ``elif``, ``else`` and ``endif``. Now there
	*must* be a space after the target name.


Changes in 1.1.1 (released 11/15/2005)
======================================

*	Fixed a bug in :meth:`ll.make.Project.buildwithargs`.


Changes in 1.1 (released 10/31/2005)
====================================

*	:class:`ll.make.TOXICAction` no longer takes an :var:`encoding` argument in
	the constructor, but works on unicode strings directly.

*	Two new actions (:class:`DecodeAction` and :class:`EncodeAction`) have been
	added to :mod:`ll.make`.


Changes in 1.0.2 (released 10/24/2005)
======================================

*	Fixed a bug in :meth:`ll.make.Project.destroy` that broke the
	:meth:`recreate` method.


Changes in 1.0.1 (released 10/18/2005)
======================================

*	Fixed a bug in :meth:`ll.make.Project.__contains__.`


Changes in 1.0 (released 10/13/2005)
====================================

*	This package now contains the following modules, that have been distributed
	as separate packages previously: :mod:`ansistyle`, :mod:`color`,
	:mod:`make`, :mod:`misc` (which contains the stuff from the old :mod:`ll`
	package), :mod:`sisyphus`, :mod:`url` and :mod:`xpit`.

*	:class:`ll.misc.Iterator` now has a method :meth:`get` that will return a
	default value when the iterator doesn't have the appropriate item.

*	In :mod:`ll.make` the output has been fixed: The ``showactionfull`` flag is
	checked before the ``showaction`` flag and target id's will always be
	output in this mode.


Changes in the old core package
###############################

Changes in ll-core 0.3 (released 05/24/2005)
============================================

*	Functions will now no longer be turned into :func:`staticmethod` objects
	automatically when used in a :class:`Namespace`.

*	The iterator tools from :mod:`ll.xist.xfind` (:func:`item`, :func:`first`,
	:func:`last`, :func:`count` and :class:`Iterator`) have been move here,
	as they are in no way specific to XIST.

*	A test suite has been added.

*	The wrapper function returned by :func:`notimplemented` will now have an
	attribute :attr:`__wrapped__` that points back to the original function.


Changes in ll-core 0.2.1 (released 01/21/2005)
==============================================

*	:meth:`__getitem__` now raises a KeyError if the attribute doesn't exist.


Changes in ll-core 0.2 (released 01/11/2005)
============================================

*	:class:`Namespace` now has a :meth:`__getitem__` method, so a
	:class:`Namespace` class can be used in a call to the :func:`eval` function.


Changes in ll-core 0.1 (released 01/03/2005)

*	Initial release


Changes in ll-ansistyle
#######################

Changes in ll-ansistyle 1.1 (released 06/28/2005)
=================================================

*	The methods :meth:`pushcolor` and :meth:`popcolor` have been resurrected.
	Without them switching to a new color and back would have to be done in a
	single call to :meth:`feed`.


Changes in ll-ansistyle 1.0 (released 06/08/2005)
=================================================

*	:mod:`ll.ansistyle` has been completely reimplemented to use an iterator
	interface instead of a stream interface.

*	Support for underlined and blinking text has been added.

*	A py.test_ based test suite has been added.

	.. _py.test: http://codespeak.net/py/current/doc/test.html


Changes in ll-ansistyle 0.6.1 (released 03/22/2005)
===================================================

*	Added a note about the package init file to the installation documentation.


Changes in ll-ansistyle 0.6 (released 01/03/2005)
=================================================

*	:mod:`ansistyle` requires the core module and Python 2.4 now.


Changes in ll-ansistyle 0.5 (released 05/21/2004)
=================================================

*	:class:`Text` has been derived from :class:`list` directly, so it inherits
	all list methods.

*	The method :meth:`getcolor` has been dropped. The class attribute :attr:`color`
	is used now instead.


Changes in ll-ansistyle 0.4 (released 07/31/2003)
=================================================

*	The names of the methods :meth:`pushColor`, :meth:`popColor`,
	:meth:`getColor` and :meth:`escapeChar` have been changed to lowercase.

*	:mod:`ansistyle` requires Python 2.3 now.


Changes in ll-ansistyle 0.3.1 (released 11/14/2002)
===================================================

*	Added source code encodings to all Python files.


Changes in ll-ansistyle 0.3 (released 08/27/2002)
=================================================

*	:mod:`ansistyle` has been moved to the :mod:`ll` package.


Changes in ll-ansistyle 0.2.2 (released 02/12/2002)
===================================================

*	Fixed a bug in :meth:`Text.insert`.


Changes in ll-ansistyle 0.2.1 (released 04/11/2001)
===================================================

*	ansistyle now compiles under Windows with Visual C++. A binary distribution
	archive is available from the FTP directory.


Changes in ll-ansistyle 0.2 (released 04/02/2001)
=================================================

*	ansistyle now supports background colors. You can specify the background
	color via the bits 4-7 of the color, i.e. for the background color
	b = 0,...,7, and the foreground color f=0,...,15 the color value is
	``(b<<4)|f``.


Changes in ll-ansistyle 0.1.1 (released 03/21/2001)
===================================================

*	Fixed a minor bug in :meth:`ansistyle.Text.__repr__`


Changes in ll-ansistyle 0.1 (released 02/18/2001)
=================================================

*	Initial release


Changes in ll-color
###################

Changes in ll-color 0.3.1 (released 03/22/2005)
===============================================

*	Added a note about the package init file to the installation documentation.


Changes in ll-color 0.3 (released 01/21/2005)
=============================================

*	Two new methods (:meth:`abslum` and :meth:`rellum`) have been added that
	return a color with modified luminosity.


Changes in ll-color 0.2 (released 01/03/2005)
=============================================

*	:mod:`color` requires the core module and Python 2.4 now.

*	Various bug fixes.


Changes in ll-color 0.1.1 (released 05/07/2004)
===============================================

*	Fixed a bug in the :prop:`css` property.


Changes in ll-color 0.1 (released 05/07/2004)
=============================================

*	Initial release.


Changes in ll-make
##################

Changes in ll-make 1.1.2 (released 10/04/2005)
==============================================

*	Fixed a bug in the handling of color environment variables.


Changes in ll-make 1.1.1 (released 09/02/2005)
==============================================

*	Specifying colors via environment variables now works.

*	It's possible to specify a default for the ``show...`` options via
	environment variables.

*	:class:`CacheAction` now drops the data in its :meth:`clear` method.


Changes in ll-make 1.1 (released 09/01/2005)
============================================

*	New action classes have been added: :class:`PickleAction`,
	:class:`UnpickleAction`, :class:`NullAction` and :class:`CacheAction`.

*	During calls to :meth:`Target.clear` and :meth:`Target.dirty` the action
	methods with the same name are now called.


Changes in ll-make 1.0 (released 08/29/2005)
============================================

*	:class:`Target` objects may now cache the objects that they create, so it can
	be reused for different outputs.

*	The :class:`Action` chain has been split into four chains that will be used
	in different situations. Each target has an internal and external
	representation (e.g. the Python ``str`` object (the internal representation),
	that is the content of a file (the external representation). The read chain
	creates the internal representation from the external one, the write chain
	creates the external representation from the internal one. The convert chain
	converts between different internal representations. The use chain is called
	when external and internal representation exist and are up to date.

*	The internal representation of a target is now available via the method
	:meth:`getdata`.

*	Importing Python modules is now done via an :class:`ImportAction`.

*	:class:`ImportAction` and :class:`UseModuleAction` can be used to
	automatically track module dependencies.

*	During build operations the currently "running" project is available as
	``ll.make.currentproject``.

*	Two new action classes are available: :class:`SelectMainAction` and
	:class:`JoinOrderedAction`, which can be used to select the input
	data at the start of a convert chain.


Changes in ll-make 0.26 (released 05/29/2005)
=============================================

*	Uses :mod:`ansistyle` 1.1 now.

*	Introduced a new :class:`Action` class named :class:`ChainedAction` that
	consists of a list of other actions. Each :class:`Target` now only has one
	action to update this target, but this action might be a
	:class:`ChainedAction`. :class:`Action` objects can be added (which results
	in a :class:`ChainedAction`).


Changes in ll-make 0.25 (released 05/20/2005)
=============================================

*	:mod:`make` is compatible with XIST 2.10 now.


Changes in ll-make 0.24 (released 04/11/2005)
=============================================

*	:class:`XPITAction` now works if there is no namespace available. In this
	case only the global namespace will be passed to the expressions.


Changes in ll-make 0.23.1 (released 03/22/2005)
===============================================

*	Added a note about the package init file to the installation documentation.


Changes in ll-make 0.23 (released 02/14/2005)
=============================================

*	Actions can now be displayed during the make process in two ways: a short
	name (this uses the method :meth:`desc`) and a longer description (using the
	method :meth:`fulldesc`). You can activate the full description via the
	command line option :option:`-vf` and deactivate it with :option:`-vF`.
	In interactive mode you can use the attribute :attr:`showactionsfull`.


Changes in ll-make 0.22 (released 01/21/2005)
=============================================

*	:class:`XPITAction` will now pass the project, target and action to the
	embedded Python expression as global variables.


Changes in ll-make 0.21 (released 01/19/2005)
=============================================

*	An action class :class:`XPITAction` has been added for use with
	:mod:`ll.xpit`.

*	Setting a project dirty (so that out-of-dateness will be rechecked)
	has been factored into a separate method.


Changes in ll-make 0.20 (released 01/03/2005)
=============================================

*	:mod:`make` requires the core module and Python 2.4 now.


Changes in ll-make 0.19.1 (released 11/26/2004)
===============================================

*	Fixed print of tracebacks when :attr:`ignoreerrors` is true.


Changes in ll-make 0.19 (released 10/29/2004)
=============================================

*	:mod:`ll.make` is compatible with XIST 2.6 now (and incompatible with
	XIST 2.5).


Changes in ll-make 0.18.2 (released 10/12/2004)
===============================================

*	Retry with absolute and real URLs in :meth:`__candidates` even if the
	argument is already an :class:`ll.url.URL` object. This works around an
	URL normalization bug under Windows.


Changes in ll-make 0.18.1 (released 08/27/2004)
===============================================

*	``Target.actions`` is now a list instead of a tuple.


Changes in ll-make 0.18 (released 07/06/2004)
=============================================

*	Added a new action class :class:`TOXICPrettifyAction` that uses the new
	:func:`prettify` function introduced in :mod:`ll.toxic` version 0.3.


Changes in ll-make 0.17 (released 06/02/2004)
=============================================

*	Renamed :class:`OracleTarget` to :class:`DBTarget`.

*	Reporting :class:`PhonyTarget` objects has been moved to a separate method
	named :meth:`reportphonytargets`.


Changes in ll-make 0.16 (released 05/31/2004)
=============================================

*	The method :meth:`buildWithArgs` has been dropped. Use :meth:`buildwithargs`
	now.

*	Argument parsing has been made extensible. The method :meth:`optionparser`
	must return an instance of :class:`optparse.OptionParser`. The method
	:meth:`parseoptions` parses the argument sequence passed in (defaults to
	``sys.argv[1:]`` and returns a tuple with ``(values, args)`` (just like
	:meth:`optparse.OptionParser.parse_args` does).

*	The arguments :var:`ignoreerrors`, :var:`color`, :var:`maxinputreport`
	have been removed from the :class:`Project` constructor. If you really need
	different values for these, simply change the attributes after creating the
	:class:`Project` object.

*	:meth:`Project.__getitem__` and :meth:`Project.__contains__` now recognize
	database ids.


Changes in ll-make 0.15.1 (released 05/25/2004)
===============================================

*	Fixed formatting bugs in :class:`OracleReadResource`.


Changes in ll-make 0.15 (released 05/25/2004)
=============================================

*	There's a new option :option:`-vl` that reports the recursion level as an
	indentation during the build process. This makes it easier to see, what
	depends on what. The indentation per level can be specified with the
	environment variable ``LL_MAKE_INDENT``.

*	The environment variable ``MAKE_REPRANSI`` has been renamed to
	``LL_MAKE_REPRANSI``.


Changes in ll-make 0.14.2 (released 05/25/2004)
===============================================

*	If a target has prerequisites, the time to rebuild those will be reported
	in the progress report too (if time reporting is on (via the option
	:option:`-vt`)).

*	Fix a bug in :class:`XISTPublishAction`.


Changes in ll-make 0.14.1 (released 05/21/2004)
===============================================

*	The default color for output has been removed.

*	In the progress report URLs relative to the home directory are now tried too
	to find the shortest URL for display.

*	Fix a bug in :class:`JoinedReadAction` and various other bugs.


Changes in ll-make 0.14 (released 05/20/2004)
=============================================

*	Actions have been made much more atomic and flexible. For each target a
	chain of actions will be executed. The first action loads the file. The next
	actions transform the content, after that an action will save the result to a
	file. Finally other actions can modify this file (what has formerly been
	known as "secondary actions").

	For example: to transform an XIST file now you need a :class:`ReadAction`, a
	:class:`XISTParseAction`, a :class:`XISTConvertAction`, a
	:class:`XISTPublishAction` and a :class:`WriteAction`. The base :class:`URL`s
	for parsing and publishing have been moved from :class:`XISTTarget` to
	:class:`XISTParseAction` and :class:`XISTPublishAction`.

*	:class:`DBID` has been rewritten. For Oracle :class:`DBID` objects it's
	possible to read and write functions and procedures via a file-like
	interface.

*	Support for `Apache FOP`_ and ll-toxic_ has been added.

	.. _Apache FOP: http://xml.apache.org/fop/index.html
	.. _ll-toxic: http://www.livinglogic.de/Python/toxic/

*	The :class:`Target` methods :meth:`sources` and :meth:`targets` have been
	renamed to :meth:`inputs` and :meth:`outputs` (related methods have been
	renamed too).

*	The options for selecting the verbosity of the progress report have been
	combined into one option :option:`-v`.

*	The progress report tries to shorten URLs by displaying relative URLs
	(relative to the current directory) if those are shorter (which they usually
	are).


Changes in ll-make 0.13.1 (released 05/05/2004)
===============================================

* Fixed a small bug in :meth:`Project.__contains__`.


Changes in ll-make 0.13 (released 01/12/2004)
=============================================

*	Now after the build the import cache ``ll.url.importcache`` will be restored
	to the state before the call. This fixes a bug, where a module that was
	loaded from another module (not as a :class:`PythonTarget`), didn't get
	cleared from the import cache.


Changes in ll-make 0.12 (released 01/02/2004)
=============================================

*	Adapted to XIST 2.4. :class:`XISTTarget` now has two attributes ``parser``
	and ``publisher`` which will be used by :class:`XISTAction` for parsing and
	publishing targets.

*	Changed the assertions that check that :class:`XISTAction`,
	:class:`CopyAction` and :class:`SplatAction` have only one source into
	exceptions.

*	:meth:`Project.__getitem__` and related methods will now only try absolute
	file paths, if the URL really is local.

*	Dropped the deprecated project method :meth:`has`.

*	For parsing the command line option :mod:`optparse` is used now instead of
	:mod:`getopt`.


Changes in ll-make 0.11.7 (released 12/15/2003)
===============================================

*	When building a target fails, the file will now only be removed if it exists.


Changes in ll-make 0.11.6 (released 12/08/2003)
===============================================

*	Remove the module from the import cache in :meth:`PythonTarget.clear`, so
	that the module will be reloaded when :meth:`Project.recreate` is used.

*	Made compatible with XIST 2.3.


Changes in ll-make 0.11.5 (released 12/06/2003)
===============================================

*	Now when a project is rebuilt, all loaded Python modules will be removed
	from the import cache before rebuilding commences. This should fix
	intermodule dependencies.


Changes in ll-make 0.11.4 (released 12/06/2003)
===============================================

*	Added methods :meth:`itersources`, :meth:`itertargets`,
	:meth:`itersourcedeps` and :meth:`itertargetdeps` to the :class:`Target`
	class.


Changes in ll-make 0.11.3 (released 11/22/2003)
===============================================

*	:meth:`__getitem__` and :meth:`__contains__` of the :class:`Project` class
	now first try with an absolute filename and then with the real filename
	(i.e. all links resolved).


Changes in ll-make 0.11.2 (released 08/06/2003)
===============================================

*	A few of the :class:`Project` attributes have been renamed to avoid name
	clashes when a class was derived from :class:`Project` and
	:class:`ll.sisyphus.Job`.


Changes in ll-make 0.11.1 (released 08/01/2003)
===============================================

*	Fixed a bug in :meth:`Project.build`: Timestamps were not cleared on the
	second call to :meth:`build` when the first one had failed.

*	Timestamp handling was broken. Timestamps from the filesystem were in UTC,
	but the timestamp set after calls to :meth:`Target.update` were in local
	time. This has been fixed now.


Changes in ll-make 0.11 (released 07/31/2003)
=============================================

*	Calling the XIST conversion in :class:`XISTAction` has been moved from
	:meth:`execute` to a new method :meth:`convert` to be easier to customize.

*	:mod:`make` requires Python 2.3 now.


Changes in ll-make 0.10 (released 07/02/2003)
=============================================

*	Targets will now be removed when building them fails.


Changes in ll-make 0.9.5 (released 05/02/2003)
==============================================

*	:meth:`Project.__getitem__` now retries with a canonical filename
	(i.e. the result of the :meth:`real`) before giving up.


Changes in ll-make 0.9.4 (released 04/24/2003)
==============================================

*	All primary actions now make sure that the output file is removed when an
	error happens. The next call to a make script will again try to generate
	the output instead of silently skipping the half finished (but seemingly up
	to date) file.


Changes in ll-make 0.9.3 (released 04/23/2003)
==============================================

*	Use the enhanced :meth:`import_` method from :mod:`ll.url` 0.7.

*	Add a ``doc`` attribute to :class:`PhonyTarget` which can be used in help
	messages (e.g. when :meth:`buildWithArgs` is called without arguments).


Changes in ll-make 0.9.2 (released 04/15/2003)
==============================================

*	Fixed a small bug in the deprecated :meth:`Project.has`.


Changes in ll-make 0.9.1 (released 03/11/2003)
==============================================

*	Fixed a small bug in :meth:`Target.lastmodified`.


Changes in ll-make 0.9 (released 03/10/2003)
============================================

*	Generating a :class:`Publisher` in an :class:`XISTAction` has been moved to
	a separate method :meth:`publisher`.

*	Each target can now be assigned a sequence of actions. There are new action
	classes :class:`ModeAction` and :class:`OwnerAction` that change the access
	permissions or owner of a file that has been created by a previous action
	in an action sequence.

*	Updated the timestamp functionality so that with Python 2.3 the
	:mod:`datetime` module will be used for timestamps.


Changes in ll-make 0.8 (released 03/03/2003)
============================================

*	The project method :meth:`has` has been deprecated. Use :meth:`has_key` or
	the new :meth:`__contains__` for that. This means that all dictionary access
	method try strings, URLs and absolute URLs now.

*	Populating a project can now be done in the overwritable method
	:meth:`create`. There is a new method :meth:`clear` which removes all
	targets from the project. Use the method :meth:`recreate` to recreate
	a project, i.e. call :meth:`clear` and :meth:`create`.


Changes in ll-make 0.7 (released 02/26/2003)
============================================

*	Made compatible with XIST 1.5 again: ``prefixes`` is only passed to the
	parser, when it is not :const:`None`.

*	:meth:`has` and :meth:`has_key` have been changed to do the same as
	:meth:`__getitem__`, i.e. retry with an URL or absolute URL in case of
	an error.

*	:meth:`build` can now be called multiple times and will reset timestamp
	information on all subsequent calls. This makes it possible to rerun a
	build process without having to recreate the project with its targets
	and dependencies (provided that no targets have to be added or removed).


Changes in ll-make 0.6.1 (released 02/14/2003)
==============================================

*	:class:`XISTTarget` has new attributes :attr:`parser`, :attr:`handler` and
	:attr:`prefixes` that can be specified in the constructor and will be used
	for parsing.


Changes in ll-make 0.6 (released 11/20/2002)
============================================

*	:meth:`Project.__getitem__` now raises an :class:`UndefinedTargetError`
	exception with the original key if retrying with an :class:`URL` object
	fails.

*	The methods :meth:`Target.sources` and :meth:`Target.targets` have been
	changed to return the :class:`Target` objects instead of the :class:`Dep`
	objects. The old functionality is still available as
	:meth:`Target.sourcedeps` and :meth:`Target.targetdeps`. The same has been
	done for the method :meth:`Target.newerSources` (and the method name has
	been made lowercase).


Changes in ll-make 0.5 (released 11/13/2002)
============================================

*	:class:`Project` is derived from :class:`dict` now.

*	Calling :meth:`Project.buildWithArgs` with an empty argument list now
	lists all :class:`PhonyTarget` objects.


Changes in ll-make 0.4.2 (released 11/11/2002)
==============================================

*	Added a new target class :class:`JavaPropAction`, for Java property files.

*	Added a :meth:`__len__` to the :class:`Project` class.


Changes in ll-make 0.4.1 (released 10/25/2002)
==============================================

*	Added a new action class :class:`SplatAction`, that can be used for
	replacing strings in files.

*	Speed up dependency creation by adding slot declarations.


Changes in ll-make 0.4 (released 08/27/2002)
============================================

*	Adapted to XIST 2.0.


Changes in ll-make 0.3.2 (released 06/16/2002)
==============================================

*	Work around a problem with unicode objects in ``sys.path``. This workaround
	will disappear as soon as Python 2.3 is released.

*	Use the method :meth:`doPublication` for publishing nodes. (This requires
	XIST 1.4.4.)


Changes in ll-make 0.3.1 (released 03/28/2002)
==============================================

*	Added a warning when the id of a new target already exists in the project,
	i.e. when the target is redefined.

*	Added a warning for file modification timestamps from the future.


Changes in ll-make 0.3 (released 03/18/2002)
============================================

*	Now :class:`url.URL` is used everywhere instead of
	:class:`fileutils.Filename`


Changes in ll-make 0.2.3 (released 02/22/2002)
==============================================

*	Added a new class :class:`DBID` that can be used as an id for database
	content.

*	Ported to Python 2.2


Changes in ll-make 0.2.2 (released 01/25/2001)
==============================================

*	Verbosity can now be specified via several :class:`Project` constructor
	arguments.

*	:meth:`Action.converter` now sets the attribute ``makeaction`` on the
	returned :class:`Converter` object.


Changes in ll-make 0.2.1 (released 10/03/2001)
==============================================

*	Support for the :var:`root` paramenter for the :meth:`convert` method in
	:class:`XISTAction`.


Changes in ll-make 0.2 (released 10/02/2001)
============================================

*	Dependencies now have a type (a subclass of :class:`Dep`). This allows to
	mark certain dependencies as "special".

*	:meth:`Project.build` can now be called with a :class:`Target` or a
	filename as a string.


Changes in ll-make 0.1 (released 07/27/2001)
============================================

*	Initial release.


Changes in ll-sisyphus
######################


Changes in ll-sisyphus 0.10.1 (released 03/22/2005)
===================================================

*	Added a note about the package init file to the installation documentation.


Changes in ll-sisyphus 0.10 (released 01/03/2005)
=================================================

*	:mod:`sisyphus` requires the core module and Python 2.4 now.


Changes in ll-sisyphus 0.9.1 (released 04/28/2004)
==================================================

*	Fixed a bug related to logging empty strings.


Changes in ll-sisyphus 0.9 (released 11/13/2003)
================================================

*	Lowercased the constructor arguments :var:`maxRuntime`, :var:`raiseErrors`
	and :var:`printKills`.

*	When the job is started it checks whether it's predecessor is still running
	(i.e. it checks whether the pid from the run file really exists).

*	Added a method :meth:`logErrorOnly` that writes to the error log only (this
	is used when the message about a job still running is written to the error
	log, so the progress log from the previous job execution won't be disturbed).

*	The loop log now contains the exception value in case of an error.


Changes in ll-sisyphus 0.8 (released 07/31/2003)
================================================

*	:mod:`sisyphus` now uses and requires Python 2.3.

*	The logging methods can now log everything. If the logged object is not a
	string, :mod:`pprint` is used for formatting.

*	The number of seconds is now properly formatted with hours, minutes and
	seconds in the logfiles.

*	A few methods have been lowercased.

*	When a job fails the method :meth:`failed` is called now. This gives the
	job the change to clean up.


Changes in ll-sisyphus 0.7 (released 03/11/2003)
================================================

*	:mod:`sisyphus` now uses the :mod:`ll.url` module, :mod:`ll.fileutils`
	is no longer required.


Changes in ll-sisyphus 0.6.2 (released 12/03/2002)
==================================================

*	error reports are now logged to the process log too.


Changes in ll-sisyphus 0.6.1 (released 09/10/2002)
==================================================

*	The :class:`Job` constructor has a new argument :var:`printKills` which
	specifies whether killing a previous job should be printed (i.e. mailed
	from cron).


Changes in ll-sisyphus 0.6 (released 08/27/2002)
================================================

*	:mod:`sisyphus` has been moved to the :mod:`ll` package.


Changes in ll-sisyphus 0.5.3 (released 05/07/2002)
==================================================

*	Derive :class:`Job` from :class:`object` to be able to use new style classes
	in mixins in subclasses.


Changes in ll-sisyphus 0.5.2 (released 07/19/2001)
==================================================

*	Made compatible with fileutils 0.2.


Changes in ll-sisyphus 0.5.1 (released 04/12/2001)
==================================================

*	Fixed a severe bug (missing call to :func:`os.path.expanduser`), that
	prevented :class:`Job` from working.


Changes in ll-sisyphus 0.5 (released 03/29/2001)
================================================

*	The :class:`Job` constructor has a new parameter :var:`raiseErrors`. When
	set to true exceptions will not only be written to the logfile but raised,
	which results in a output to the terminal and an email from the cron daemon.


Changes in ll-sisyphus 0.4 (released 03/26/2001)
================================================

*	The class :class:`LogFile` has been moved to a seperate module named
	:mod:`fileutils`.


Changes in ll-sisyphus 0.3 (released 02/16/2001)
================================================

*	Initial public release


Changes in ll-url
#################


Changes in ll-url 0.15.1 (released 03/22/2005)
==============================================

*	Added a note about the package init file to the installation documentation.


Changes in ll-url 0.15 (released 02/24/2005)
============================================

*	The :prop:`mimetype` property of :class:`ReadResource` is no longer a tuple,
	but a plain string.

*	:class:`ReadResource` has a new property :prop:`encoding`, which is the
	character encoding of the resource.

*	A bug in the ``lastmodified`` property of :class:`WriteResource` has been
	fixed.


Changes in ll-url 0.14.2 (released 02/22/2005)
==============================================

*	``url.URL("file:foo/").local()`` will now always end in a directory
	separator. This didn't work on Windows before.


Changes in ll-url 0.14.1 (released 01/13/2005)
==============================================

*	On Windows ``url.File("c:\\foo").abs()`` generated ``URL('file:///C|/foo')``.
	Now the result will always be ``URL('file:/C|/foo')``. The same fix has been
	made for :meth:`real` and the constructor.


Changes in ll-url 0.14 (released 01/03/2005)
============================================

*	:mod:`url` requires the core module and Python 2.4 now.


Changes in ll-url 0.13 (released 11/25/2004)
============================================

*	The helper function :func:`_unescape` will now interpret ``%u`` escapes
	(produced by Microsoft software). The patch has been contributed by
	Artiom Morozov.


Changes in ll-url 0.12.1 (released 11/03/2004)
==============================================

*	Fixed a bug in the C helper function :func:`_unescape` (forget to clear
	the exception).

*	Dropped the system default encoding from the list of encodings that will be
	tried when UTF-8 fails in :func:`_unescape`.


Changes in ll-url 0.12 (released 01/12/2004)
============================================

*	:func:`removefromimportcache` has been dropped, now you can assign the
	import cache directly (as the module level attribute :attr:`importcache`.
	Removing modules from the import cache can now be done via
	``url.importcache.remove(mod)``.


Changes in ll-url 0.11.7 (released 12/23/2003)
==============================================

*	Fixed a bug in :meth:`Path.real` that only surfaced on Windows.


Changes in ll-url 0.11.6 (released 12/06/2003)
==============================================

*	Added a function :func:`removefromimportcache`.


Changes in ll-url 0.11.5 (released 11/22/2003)
==============================================

*	Fixed a bug with the :var:`scheme` argument of the methods :meth:`real`
	and :meth:`abs`.


Changes in ll-url 0.11.4 (released 11/19/2003)
==============================================

*	:attr:`realurl` has been renamed to :attr:`finalurl` and now works for
	local URLs too (it will be the same as the original URL).


Changes in ll-url 0.11.3 (released 11/17/2003)
==============================================

*	Added an attribute :attr:`realurl` to :class:`ReadResource` which contains
	the real URL (which might be different from the URL passed to the
	constructor, because of a redirect).


Changes in ll-url 0.11.2 (released 11/17/2003)
==============================================

*	URLs that have an authority part but a relative path will be properly
	formatted, i.e. the leading ``/`` will be included.


Changes in ll-url 0.11.1 (released 08/13/2003)
==============================================

*	The :class:`URL` method :meth:`rename` has been fixed.

*	A bug has been fixed that created relative paths for HTTP URLs that didn't
	have a trailing ``/``.


Changes in ll-url 0.11 (released 08/04/2003)
============================================

*	A method :meth:`withoutfrag` has been added. :meth:`withFragment` has been
	renamed to :meth:`withfrag` and the property :attr:`fragment` has been
	renamed to :attr:`frag`.


Changes in ll-url 0.10 (released 07/31/2003)
============================================

*	:mod:`url` requires Python 2.3 now.

*	The method :mod:`insert` has been fixed.


Changes in ll-url 0.9.1 (released 07/17/2003)
=============================================

*	Fixed a bug that drops the filename in :meth:`relative` when both URLs have
	the same filenames but a different query.

*	The fragment is now properly escaped when the URL is regenerated.


Changes in ll-url 0.9 (released 07/09/2003)
===========================================

*	:meth:`withExt` and friends have been lowercased.

*	The :attr:`path` has been changed from a string to an object of the new
	class :class:`Path`. This new class provides many of the path related
	functionality of URLs.

*	The method :meth:`URL.import_` no longer uses the import machinery (from
	the :mod:`imp` module), but :func:`execfile`. This has the following
	consequences:

	-	You can only import files with the extension ``.py``.

	-	The imported module no longer retains deleted attributes of the
		previous version.

	-	The file will be compiled even if a bytecode file exists.


Changes in ll-url 0.8 (released 06/04/2003)
===========================================

*	Added methods :meth:`abs` and :meth:`__rdiv__` to :class:`URL`.

*	The method :meth:`real` now has an argument :var:`scheme` that specifies
	which scheme should the use for the resulting URL.

*	Now the query part of an :class:`URL` will be parsed into the attribute
	:attr:`query_parts` (which is a dictionary). If the query can't be parsed,
	:attr:`query_parts` will be ``False``, but :attr:`query` will still contain
	the complete query part.


Changes in ll-url 0.7.1 (released 05/01/2003)
=============================================

*	Made :meth:`clearimportcache` a class method.


Changes in ll-url 0.7 (released 04/23/2003)
===========================================

*	Introduced :meth:`local` as a synonym for :meth:`asFilename`, :func:`Dir`
	as a synonym for :func:`Dirname` and :func:`File` as a synonym for
	:func:`Filename`.

*	Added functions :func:`first`, :func:`firstdir` and :func:`firstfile`,
	that returns the first URL from a list that exists, is a directory or
	a file.

*	The method :meth:`import_` uses a cache now. Different caching strategies
	can be chosen through the :var:`mode` parameter.


Changes in ll-url 0.6.2 (released 03/07/2002)
=============================================

*	The method :meth:`real` checked whether the referenced file really is a
	directory. This has the problem that the directory/file must exist. Now
	the directoryness of the URL itself is used.


Changes in ll-url 0.6.1 (released 03/06/2002)
=============================================

*	Fixed a bug in :meth:`chown`: Attributes are not available for
	:func:`pwd.getpwnam()` and :func:`grp.getgrnam()` results under Python 2.2.
	Use the tuple entry instead.

*	Added methods :meth:`mtime`, :meth:`atime` and :meth:`size` to :class:`URL`.


Changes in ll-url 0.6 (released 03/05/2002)
===========================================

*	Now all arguments for :meth:`walk` default to :const:`False`.

*	Added new convenience methods :meth:`walkfiles` and :meth:`walkdirs`.

*	An :class:`URL` can now be iterated. This is equivalent to
	``walk(dirsbefore=True, files=True)``.

*	Many functions from :mod:`os` and :mod:`os.path` have been added as
	methods to :mod:`ll.url`. This was inspired by Jason Orendorff's
	:mod:`path`__ module.

	__ http://www.jorendorff.com/articles/python/path/

*	The method :meth:`import_` is now available in the :class:`URL` class too.

*	When Python 2.3 is used timestamp will now be :class:`datetime.datetime`
	objects and :mod:`mx.DateTime` is no longer required. With Python 2.2
	:mod:`mx.DateTime` will still be used.


Changes in ll-url 0.5.1 (released 01/07/2002)
=============================================

*	Added a :file:`LICENSE` file.


Changes in ll-url 0.5 (released 11/14/2002)
===========================================

*	:class:`WriteResource` has been largely rewritten to elminate the overhead
	of calls the :meth:`write`. Access to properties might be a little slower
	now, because :class:`WriteResource` has been optimized for maximum writing
	speed.

*	Added source code encoding statements to the Python files.


Changes in ll-url 0.4.3 (released 11/11/2002)
=============================================

*	Fixed a refcounting leak in the new version of :func:`_normalizepath`.


Changes in ll-url 0.4.2 (released 11/08/2002)
=============================================

*	:func:`_normalizepath` has been reimplemented in C for performance reasons.


Changes in ll-url 0.4.1 (released 10/29/2002)
=============================================

*	:class:`ReadResource` and :class:`WriteResource` now have a method
	:meth:`import_`, that imports the file as a Python module (ignoring the
	file extension).


Changes in ll-url 0.4 (released 10/18/2002)
===========================================

*	Added a :file:`HOWTO` file.

*	Made the docstrings compatible with XIST 2.0.

*	The :prop:`imagesize` property now raises an :class:`IOError` if the PIL
	is not available.


Changes in ll-url 0.3.1 (released 09/09/2002)
=============================================

*	:class:`WriteResource` will now generate an empty file, even if
	:meth:`write` is never called. This is checked in :meth:`close`.

*	:class:`WriteResource` gained a destructor that will call :meth:`close`.


Changes in ll-url 0.3 (released 08/27/2002)
===========================================

*	:mod:`url` has been moved to the :mod:`ll` package.


Changes in ll-url 0.2 (released 06/18/2002)
===========================================

*	:func:`_escape` now always uses unicode strings. 8bit strings will be
	converted to unicode before the UTF-8 version will be encoded.

*	:func:`_unescape` now always emits unicode strings. If the UTF-8 decoding
	does not work, the system default encoding will be tried, and finally
	Latin-1 will be used.

*	:func:`_escape` and :func:`_unescape` have been rewritten in C for
	performance reasons.


Changes in ll-url 0.1.8 (released 05/07/2002)
=============================================

*	Illegal ``%`` escapes now only issue a warning and will be used literally
	when the warning framework doesn't raise an exception.


Changes in ll-url 0.1.7 (released 04/30/2002)
=============================================

*	Removed the illegal scheme handling change from 0.1.6 again. Now this has
	to be done before constructing an :class:`URL`.


Changes in ll-url 0.1.6 (released 04/26/2002)
=============================================

*	Now when the parser discovers an illegal scheme, you get another chance:
	Beginning whitespace will be stripped and it will be retried.


Changes in ll-url 0.1.5 (released 04/25/2002)
=============================================

*	Fixed a bug in :meth:`__div__`: Now ``URL("http://foo/bar")/"/baz"`` works.


Changes in ll-url 0.1.4 (released 04/15/2002)
=============================================

*	When assigning to the :attr:`url` property, the scheme will now only be set
	when it consists of legal characters. This means that parsing
	``/foo.php?x=http://www.bar.com`` won't try to set a scheme
	``/foo.php?x=http``, but will use an empty scheme.


Changes in ll-url 0.1.3 (released 04/09/2002)
=============================================

*	Make :attr:`ext` and :attr:`file` work with opaque :class:`URL`\s.

*	Forgot the make :attr:`resdata` assignable. Fixed.

*	Now the scheme to be used can be specified for the various filename
	functions.

*	Added a method :meth:`withFragment` that returns a copy of the :class:`URL`
	with a new fragment.

*	Use the :mod:`email` package instead of :mod:`rfc822`	for :func:`formatdate`.

*	No longer quote ``[`` and ``]`` to be compatible with the ezt templates from
	ViewCVS__.

	__ http://viewcvs.sf.net/

*	When joining URLs the right hand URL no longer inherits the scheme, if it
	has not scheme, but the path is absolute::

		>>> url.URL("root:foo.html")/url.URL("/cgi-bin/")
		URL('/cgi-bin/')


Changes in ll-url 0.1.2 (released 03/26/2002)
=============================================

*	Fixed a bug in :meth:`URL.__eq__` and :meth:`URL.__hash__`: ``query`` and
	``fragment`` were not used. This has been fixed.


Changes in ll-url 0.1.1 (released 03/20/2002)
=============================================

*	Fixed a bug in :attr:`ReadResource.contentlength`, which tried to convert
	the :func:`stat` result to a :class:`DateTime` object.


Changes in ll-url 0.1 (released 03/18/2002)
===========================================

*	Initial release


Changes in ll-xpit
##################


Changes in ll-xpit 0.2.1 (released 03/22/2005)
==============================================

*	Added a note about the package init file to the installation documentation.


Changes in ll-xpit 0.2 (released 01/21/2005)
============================================

*	:func:`convert` now takes both a global and a local namespace and will
	raise an exception when an unknown processing instruction target is
	encountered.


Changes in ll-xpit 0.1 (released 01/19/2005)
============================================

*	Initial release.
