Changes in 3.7.5 (released 04/19/2010)
--------------------------------------

*	:class:`ll.orasql.PrimaryKey` has a new method :meth:`itercolumns` that
	returns an iterator over the columns this primary key consists of.



Changes in 3.7.4 (released 03/25/2010)
--------------------------------------

*	Fixed a bug in :class:`ll.xist.ns.rss20.guid`. The ``isPermaLink`` attribute
	was a :class:`URLAttr`, but must be a :class:`TextAttr`.


Changes in 3.7.3 (released 02/27/2010)
--------------------------------------

*	Fixed a bug in the generated JSP code for the ``def`` opcode in
	:func:`ll.xist.ns.jsp.fromul4`.


Changes in 3.7.2 (released 02/26/2010)
--------------------------------------

*	Fixed two bugs in the XML codecs:

	-	An externally specified encoding wasn't honored in the incremental decoder.

	-	Fixed reset() for incremental codecs: If encoding has been changed during
		parsing in the incremental codecs it now gets reset to its proper initial
		value.

*	Fixed a bug in the handling of the UL4 opcode ``addlist`` in
	:func:`ll.xist.ns.jsp.fromul4`.

*	Added missing processing instruction class for the UL4 ``def`` tag to the
	:mod:`ll.xist.ns.ul4` namespace module.

*	The generated JSP code for the ``loadvar`` opcode now uses the Java method
	``Utils.getItem``, so that non-existent variables no longer get treated as
	``None``/``null``.


Changes in 3.7.1 (released 02/08/2010)
--------------------------------------

*	:func:`ll.xist.ns.jsp.fromul4` now outputs the correct code for calling the
	``format`` method on date objects (This requires version exp-22 of the
	UL4 Java package).


Changes in 3.7 (released 09/10/2009)
------------------------------------

*	In UL4 templates it's now possible to define locale templates via
	``<?def tmpl?>templatecode<?end def?>``.

*	Python 2.6 is required now.

*	:mod:`ll.orasql` and :mod:`ll.nightshade` are now part of the distribution.

*	:mod:`ll.make` has a new Action class: :class:`ObjectAction` simply returns
	an existing object.

*	The following classes have been removed from :mod:`ll.make`:
	:class:`EncodeAction`, :class:`DecodeAction`, :class:`EvalAction`,
	:class:`GZipAction`, :class:`GUnzipAction`,
	:class:`JavascriptMinifyAction`, :class:`XISTBytesAction`,
	:class:`XISTStringAction`, :class:`JoinAction`, :class:`UnpickleAction`,
	:class:`PickleAction`, :class:`TOXICAction`, :class:`TOXICPrettifyAction`,
	:class:`SplatAction`, :class:`UL4CompileAction`, :class:`UL4RenderAction`,
	:class:`UL4DumpAction`, :class:`UL4LoadAction`, :class:`XISTTextAction` and
	:class:`XISTConvertAction`. All of these actions can be executed by using
	:class:`CallAction` or :class:`CallAttrAction`.

*	:class:`ll.make.PipeAction` has been renamed to :class:`TransformAction`.

*	The new :class:`ll.make.PipeAction` pipes the input through an external
	command.

*	:class:`ll.make.FileAction` now automatically wraps the :var:`key` argument
	into an :class:`URL` object.

*	:class:`ll.make.FileAction` has two new methods :meth:`chmod` and
	:meth:`chown` that return a :class:`ModeAction` and :class:`OwnerAction`
	for modifying the file created by the :class:`FileAction`.

*	:class:`ll.make.Action` has three new methods: :meth:`call`, :meth:`getattr`
	and :meth:`callattr` create a :class:`CallAction`, :class:`GetAttrAction`
	or :class:`CallAttrAction` object respectively.

*	The division operator is no longer implemented for :class:`Action` objects
	in :mod:`ll.make`.

*	Two new UL4 functions have been added: ``float`` and ``iscolor``.

*	Two new scripts have been added: ``uls`` can be used to list any directory
	given as an URL. ``ucat`` can be used to output any file or directory.

*	The script ``ucp`` now changes the user and group only if a user or group is
	given.

*	A bug in the 64-bit support for :mod:`sgmlop` has been fixed.

*	Fixed a bug in the remote :meth:`stat` method for ssh URLs (it seems that
	the :class:`posix.stat_result` tuple objects can no longer be pickled).

*	There's a new function :func:`misc.itersplitat` for splitting a string at
	specified positions.

*	For ssh URLs a keyword argument ``ssh_config`` is supported now instead of
	``identity`` (This mirrors the corresponding change in the py__ library)

	__ http://codespeak.net/py/dist/


Changes in 3.6.6 (released 07/09/2009)
--------------------------------------

*	Fixed handling of empty pid files in :mod:`ll.sisyphus` (Fixes issue #11
	reported by Jarek Zgoda).


Changes in 3.6.5 (released 06/02/2009)
--------------------------------------

*	Fix UL4 templates that produce no output: As the generated Python sourcecode
	didn't contain any ``yield`` statements, the resulting function was an
	ordinary function instead of a generator.


Changes in 3.6.4 (released 03/19/2009)
--------------------------------------

*	A new UL4 method ``join`` has been added. It works like the Python string
	method join.

*	:mod:`ll.misc` has three new functions: :func:`gzip` und :func:`gunzip` can
	be used for compressing and uncompressing byte strings with gzip.
	:func:`jsmin` can be used to minify Javascript source.

*	Parsing an empty string with ``tidy=True`` in
	:func:`ll.xist.parsers.parsestring` now works again.


Changes in 3.6.3 (released 03/02/2009)
--------------------------------------

*	The xfind operators ``attrhasvalue``,  ``attrhasvalue_xml``,
	``attrcontains``, ``attrcontains_xml``, ``attrstartswith``,
	``attrstartswith_xml``, ``attrendswith``, ``attrendswith_xml``, ``hasid``
	and ``hasclass`` now support multiple values. The operator matches the
	node if it matches with any of the given values.

*	A new function ``reversed`` is now available in UL4 templates. It returns
	an iterator that will output the items of any sequence in reverse order.


Changes in 3.6.2 (released 02/16/2009)
--------------------------------------

*	Inside UL4 templates rendering other templates can now be done with the new
	``render`` method. This method returns the template output as a string.
	Passing parameters can be done via keyword arguments or with the ``**``
	syntax like when using the ``render`` tag.

*	A new version of the ``int`` function has been added to UL4: When called with
	two arguments, the first must be a string, and the second is treated as the
	base for the conversion.


Changes in 3.6.1 (released 01/27/2009)
--------------------------------------

*	Generating the Python source from an UL4 template is now 20-25% faster.

*	Fixed a buffer overrun in the C portions of the url module.

*	Added a class :class:`addattr` to :mod:`ll.xist.xsc`. This can be used
	to extend XML attributes via ``with`` blocks.

*	Added the function :func:`ll.xist.ns.jsp.fromul4` which can turn an UL4
	template into JSP source code.


Changes in 3.6 (released 12/31/2008)
------------------------------------

*	The following :class:`Color` class methods have been dropped: ``fromrgba``,
	``fromrgba4``, ``fromrgba8``, ``fromint4``, ``fromint8``.

*	The following :class:`Color` properties have been dropped: ``r4``, ``g4``,
	``b4``, ``a4``, ``r8``, ``g8``, ``b8``, ``a8``, ``r``, ``g``, ``b``,  ``a``
	``int4``, ``int8``, ``rgb4``, ``rgba4``, ``rgb8``, and ``rgba8`` have been
	dropped. The new methods ``r``, ``g``, ``b`` and ``a`` return the 8 bit
	component values.

*	The class methods ``fromhsva`` and ``fromhlsa`` have been renamed to
	``fromhsv`` and ``fromhls``.

*	The property ``css`` has been dropped. Instead the CSS string is returned
	by ``__str__``.

*	Dividing color now does a scalar division. Blending colors is now done with
	the modulo operator.

*	Support for color objects has been added to UL4.

*	The XPIT templating language and :class:`ll.make.XPITAction` have been
	removed.

*	Fixed a bug in :meth:`ll.make.CacheAction.get`: The action must return real
	data when called with ``bigbang`` as the timestamp.

*	:class:`ll.make.UL4RenderAction` has been fixed.


Changes in 3.5 (released 12/05/2008)
------------------------------------

*	A new function ``json`` has been added to UL4: This function returns a
	JSON dump of the object passed in (this requires either :mod:`simplejson`
	or Python 2.6).

*	The UL4 function ``csvescape`` has been renamed to ``csv``.

*	A new option :option:`--showregistration`/:option:`-r` has been added to
	make scripts.

*	:mod:`ll.make` now supports Growl__ notifications on Mac OS X. To activate
	it set the ``LL_MAKE_GROWL`` environment variable to ``1`` or use the ``-g``
	or ``--growl`` options.

	__ http://growl.info/

*	:mod:`ll.make` has a new action class :class:`JavascriptMinifyAction` for
	minimizing Javascript source.

*	:class:`ll.color.Color` has been rewritten to create immutable objects
	with the components being 8 bit values (i.e. 0-255) instead of floating
	point values between 0 and 1. An alpha component has been added.

*	A ``strong`` element has been added to the :mod:`ll.xist.ns.doc`
	namespace.


Changes in 3.4.4 (released 09/16/2008)
--------------------------------------

*	Fixed a bug in :meth:`ll.make.JoinAction.execute`.


Changes in 3.4.3 (released 09/09/2008)
--------------------------------------

*	:func:`css.applystylesheets` could no longer handle style declarations
	containing comments. This has been fixed now.


Changes in 3.4.2 (released 09/03/2008)
--------------------------------------

*	Parsing didn't work when :var:`tidy` was set to true and a :var:`base`
	argument was given. This has been fixed now.


Changes in 3.4.1 (released 08/29/2008)
--------------------------------------

*	Bugs with thread local storage have been fixed so using :class:`xsc.Pool`,
	:class:`xsc.build` and URL contexts in ``with`` blocks in multithreaded
	applications should work now.


Changes in 3.4 (released 08/19/2008)
------------------------------------

*	Templates can no longer be passed as a separate dictionary to UL4 templates
	but are passed as variables like other data objects too.

*	Strings in UL4 have gained a new method ``capitalize``.

*	Printing XML escaped strings in UL4 has now gained its own tag and opcode.
	``<?printx foo?>`` is equivalent to ``<?print xmlescape(foo)?>``.

*	Exception handling in UL4 has been rewritten to allow proper error reporting
	when calling nested templates.

*	UL4 has gained a new function ``zip``. It can be called with two or three
	arguments and does what :func:`itertools.zip` does.

*	UL4 has gained another new function: ``type`` returns the type of its
	argument as a string.

*	UL4 now supports tuple unpacking in ``<?for?>`` tags with three variables.

*	UL4 has a new tag for comments: ``<?note This is comment?>``.

*	A new script ``db2ul4.py`` has been added that can render UL4 templates with
	database content.

*	In UL4s ``<?render?>`` tags it's now possible to pass along a complete
	argument dictionary via the ``**arg`` syntax just like in Python. This syntax
	can even be used multiple times in the call. This syntax is available in
	dictionary literals too, i.e. ``{1:2, 3:4}`` and ``{**{1:2}, **{3:4}}`` are
	equivalent.

*	A new UL4 function ``get`` has been added that works similar to the
	dictionary method ``get``, but works with global variables.

*	The missing processing instruction :class:`render` has been added to
	:mod:`ll.xist.ns.ul4`.

*	:mod:`xml_codec` now partially works, even if the C module is missing. As
	long as you explicitly specify an encoding on parsing and publishing it
	should work.

*	A new processing instruction class :class:`ll.xist.AttrProcInst` has been
	introduced. When an :class:`AttrProcInst` node is the first node in an
	attribute, it takes over publishing of the attribute. In all other cases
	the processing instruction disappears completely. UL4 uses this to implement
	"conditional attributes" (via the new classes :class:`attr_if` and
	:class:`attr_ifnn`).

*	Building trees with ``with`` blocks has changed slightly. Nodes used in
	``with`` blocks and with ``+`` are now passed to a ``with`` handler instead
	of building the tree directly. This fixes a problem when nested
	:meth:`convert` calls use ``with`` blocks.

*	The element :class:`ll.xist.ns.form.memo` has been renamed to
	:class:`textarea` and :class:`ll.xist.ns.form.edit` has been renamed to
	:class:`text`. Classes :class:`ll.xist.ns.form.button` and
	:class:`ll.xist.ns.form.file` have been added.

*	Iterating through the inputs in :mod:`ll.make` actions has been fixed (i.e.
	the additional inputs will be output too). :meth:`ll.make.Project.findpaths`
	has been fixed to work with non-:class:`ll.make.Action` inputs. (This means
	that now you *have* to pass a real registered target action to
	:meth:`findpaths` not just its key).

*	:mod:`ll.make` has gained a new action: :class:`XISTStringAction` publishes
	an XIST node as a unicode string. :class:`XISTPublishAction` has been renamed
	to :class:`XISTBytesAction`.

*	Fixed a bug in the caching logic in :meth:`ll.make.CacheAction`.

*	:class:`ll.make.CallMethAction` has been renamed to :class:`CallAttrAction`
	because it can be used to e.g. call functions in a module too.

*	The properties ``showaction``, ``showstep`` and ``shownote`` of
	:class:`ll.make.Project` object can now be assigned booleans as well (which
	results in *all* or *no* actions being shown.

*	The version number for :mod:`cssutils` has been bumped to 0.9.5.1.


Changes in 3.3.2 (released 07/15/2008)
--------------------------------------

*	Dictionaries in UL4 have gained a new method ``get``.

*	The version number for :mod:`cssutils` has been bumped again (to 0.9.5rc2
	or a later 0.9.5 version).

*	Fixed a bug in the parsing of slice expressions in UL4.

*	:mod:`ll.make` has gained a new :class:`UL4RenderAction` action.

*	Fixed a bug in the formatting for the ``getslice2`` opcode for UL4.


Changes in 3.3.1 (released 07/14/2008)
--------------------------------------

*	Fixed a bug in the implementation of the "not" operator in UL4.

*	When the UL4 compiler encounters unclosed blocks, it will now include the
	start location of the block in the error message.


Changes in 3.3 (released 07/11/2008)
------------------------------------

*	XIST has gained its fourth templating language: ``UL4`` the
	"Universal Layout Language". This templating language is similar in
	capabilities to `Djangos templating language`__. However ``UL4`` templates
	are compiled to a bytecode format, which makes it possible to implement
	template renderers in other languages and makes the template code "secure"
	(i.e.template code can't open or delete files).

	__ http://www.djangoproject.com/documentation/templates/

*	:mod:`ll.make` has gained new actions: :class:`GZipAction`,
	:class:`GUnzipAction`, :class:`CallFuncAction`,  :class:`CallMethAction`,
	:class:`UL4CompileAction`, :class:`UL4DumpAction` and :class:`UL4LoadAction`.

*	The version number for :mod:`cssutils` has been bumped to 0.9.5rc1.

*	Nodes of type :class:`ll.xist.xsc.Comment` and :class:`ll.xist.xsc.DocType`
	inside of attributes are now simply ignored when publishing instead of
	generating an exception.

*	All actions in :mod:`ll.make` no longer check whether their inputs are
	action objects. Non-action objects are simply treated as ancient input data.
	This also means that most action classes have an :var:`input` parameter in
	their constructor again, as this input could now be a constant.

*	Most attributes of action objects in :mod:`ll.make` can now be action objects
	themselves, so for example the name of the encoding to be used in an
	:class:`EncodeAction` can be the output of another action.

*	:class:`ll.make.ImportAction` has been dropped as now the module object can
	be used directly (e.g. as the input for an :class:`XISTPoolAction` object).

*	:func:`ll.misc.xmlescape` now escapes ``'`` as ``&#39;`` for IE compatibility.

*	Functions :func:`ll.misc.xmlescape_text` and :func:`ll.misc.xmlescape_attr`
	have been added that implement the functionality from XIST 3.2.5 and earlier.

*	The default parser for XIST is expat now. To switch back to sgmlop simply
	pass an :class:`SGMLOPParser` object to the parsing functions::

		>>> from ll.xist import parsers
		>>> node = parsers.parsestring("<a>", parser=parsers.SGMLOPParser())

*	TOXIC has been split into a compiler module :mod:`ll.toxicc` and an XIST
	namespace :mod:`ll.xist.ns.toxic`. TOXIC now supports output for
	SQL Server. The function :func:`xml2ora` as been renamed to :func:`compile`
	(and has a new :var:`mode` argument for specifying the database type).

*	The :var:`targetroot` parameter for :meth:`ll.make.XISTConvertAction.__init__`
	has been renamed to :var:`root`.


Changes in 3.2.7 (released 05/16/2008)
--------------------------------------

*	Added the missing file ``_misc_include.c`` to the distribution archives.


Changes in 3.2.6 (released 05/07/2008)
--------------------------------------

*	A new action class :class:`EvalAction` has been added to :mod:`ll.make`.

*	:func:`ll.xist.helpers.escapetext` and :func:`ll.xist.helpers.escapeattr`
	have been merged into one function that escapes all special characters
	(including ``'`` and ``"``) and has been renamed/moved to
	:func:`ll.misc.xmlescape`.

*	Python versions of all the functions in the module :mod:`ll.misc` have been
	added. Those versions will be used in case the C module is not available.


Changes in 3.2.5 (released 04/11/2008)
--------------------------------------

*	A refcounting bug in the attribute parsing code of :mod:`sgmlop` has been
	fixed.

*	The helper function :func:`cssescapereplace` has been removed, as it's no
	longer needed.

*	Pure Python versions of :func:`helpers.excapetext` and
	:func:`helpers.escapeattr` have been added, in case the C module is not
	available.


Changes in 3.2.4 (released 04/02/2008)
--------------------------------------

*	The following functions have been added to :mod:`ll.xist.css`:
	:func:`parsestring`, :func:`parsestream`, :func:`parsefile`, :func:`parseurl`
	and :func:`write`. They parse CSS resources and are similar to the XML/HTML
	parsing functions in that they apply the specified base URL to all URLs in
	the style sheet.

*	:mod:`cssutils` 0.9.5b2 is required now.

*	:func:`ll.xist.css.iterrules` and :func:`ll.xist.css.applystylesheets` now
	support specifying whether the preferred stylesheets or an alternate
	stylesheet group should be used.

*	:meth:`ll.xist.xsc.ProcInst.__mul__` and
	:meth:`ll.xist.xsc.ProcInst.__rmul__` now return a fragment containing
	the node repeated a number of times instead of one processing instruction
	node containing repeated content.

*	The constructor for :class:`ll.xist.parsers.ExpatParser` now takes two
	additional arguments:

	:var:`xmldecl`
		If this is true the XML declaration will appear in the resulting XIST
		tree.

	:var:`doctype`
		If this is true the doctype declaration will appear in the resulting
		XIST tree (however any internal DTD subset will be dropped).


Changes in 3.2.3 (released 03/04/2008)
--------------------------------------

*	:mod:`cssutils` 0.9.5 is used now. This simplifies the implementation of
	:func:`css.selector`.

*	A function :func:`ll.xist.css.geturls` has been added. This returns a list of
	all the URLs in a :mod:`cssutils` stylesheet.

*	:func:`toxic.xml2ora` now treats unknown processing instructions as text.
	This makes it possible to e.g. output an XML header via toxic.

*	The pseudo-elements in :mod:`ll.xist.ns.jsp` are no longer in a namespace,
	so they will always be published without any prefixes.


Changes in 3.2.2 (released 02/25/2008)
--------------------------------------

*	A new method :meth:`replaceurls` has been added to
	:class:`ll.xist.xsc.StyleAttr`. With this method all URLs in a ``style``
	attribute can be replaced.

*	Fixed a bug in :meth:`ll.xist.parsers.SGMLOPParser.begin`: The encoding
	wasn't passed properly to the XML decoder.

*	:meth:`ll.xist.xsc.ProcInst.publish` now calls the :meth:`checkvalid`
	method too.


Changes in 3.2.1 (released 02/05/2008)
--------------------------------------

*	It's now possible to force the publisher to output certain ``xmlns``
	attributes via the :var:`showxmlns` argument to the :class:`Publisher`
	constructor.


Changes in 3.2 (released 02/01/2008)
------------------------------------

*	The core package has been moved into XIST, installing XIST now only requires
	*one* package.

*	:mod:`ll.toxic` has been moved into XIST and is now available as
	:mod:`ll.xist.ns.toxic`.

*	When a :class:`ll.make.XISTParseAction` object is executed the content of
	the pool will now be extended by the content of the pool from the
	:class:`XISTPoolAction` instead of being replaced.

*	:class:`ll.make.Pool` and :class:`ll.xist.xsc.Pool` no longer use a
	:class:`WeakValueDictionary`, but a simple :class:`dict`. This means they
	can now store *any* object. A method :meth:`clear` has been added, which
	removes all registered objects.

*	Fixed a bug in :func:`ll.xist.css.iterrules` that surfaced when a
	:var:`base` argument was given.

*	Fixed a second bug in :func:`ll.xist.css.iterrules` where the ``href`` of a
	:class:`link` element wasn't applied to the URLs in the stylesheet.


Changes in 3.1 (released 01/18/2008)
------------------------------------

*	Fixed the problem that the source distibution didn't include header files.

*	If an :class:`URLAttr` attribute contains a processing instruction XIST
	will no longer transform the URL in any way.

*	Fixed a parser bug where attributes were dropped when the attribute value
	was empty.

*	Putting a module into a :class:`Pool` object now copies the ``xmlns``
	attribute too. This makes it possible to use :class:`Pool` objects as
	conversion targets.


Changes in 2.9 (released 01/07/2008)
------------------------------------

*	Namespaces have been greatly simplified. There are no namespace modules any
	longer. An element class can be assigned a namespace by setting the
	``xmlns`` class attribute to the namespace name. Global attributes can be
	assigned a namespace by setting the ``xmlns`` attribute on the attribute
	class itself (*not* on the :class:`Attrs` class). The classes
	:class:`Prefixes` and :class:`NSPool` are gone too. Instead a new class
	:class:`Pool` is used to specify which classes should be used for parsing.

*	Dependency on PyXML_ has finally been dropped. XIST now uses its own XML
	parsing API. Two parsers are available: One based on expat_ and one based on
	a custom version of sgmlop_.

	.. _PyXML: http://pyxml.sf.net/
	.. _expat: http://expat.sourceforge.net/
	.. _sgmlop: http://effbot.org/zone/sgmlop-index.htm

*	Tree traversal has been rewritten again. XFind expressions involving
	multiple uses of ``//`` now work correctly. The method :meth:`walk` now
	doesn't yield :class:`Cursor` objects, but simple path lists (actually it's
	always the same list, if you want distinct lists use :meth:`walkpath`).
	Applying XFind expressions to nodes directly is no longer supported, you
	have to call :meth:`walk`, :meth:`walknode` or :meth:`walkpath` with the
	XFind expression instead. Many XFind operators have been renamed and/or
	reimplemented (see the documentation for the :mod:`xfind` module for more
	information).

*	The methods :meth:`__getitem__`, :meth:`__setitem__` and :meth:`__delitem__`
	for :class:`Frag` and :class:`Element` now support the new walk filters, so
	you can do:

	*	``del node[html.p]`` to delete all :class:`html.p` child elements of
		``node``;
	*	``del node[html.p[2]]`` to delete only the third :class:`html.p`;
	*	``node[xfind.hasclass("note")] = html.p("There was a note here!")`` to
		replace several child nodes with a new one;
	*	``for c in node[xfind.empty]: print c.bytes()`` to print all empty
		(element) children of ``node``;
	*	``del node[node[0]]`` to delete the first child node (which is silly,
		but illustrates that you can pass a node to get/replace/delete that
		node);

*	A new module :mod:`ll.xist.css` has been added which contains CSS related
	functionality: The generator function :func:`iterrules` can be passed an
	XIST tree and it will produce all CSS rules defined in any
	:class:`html.link` or :class:`html.style` elements or imported by them
	(via the CSS rule ``@import``). This requires the :mod:`cssutils` package.

*	The function :func:`applystylesheets` modifies the XIST tree passed in by
	removing all CSS (from :class:`html.link` and :class:`html.style` elements
	and their ``@import``\ed stylesheets) and putting the styles into ``style``
	attributes of the affected elements instead.

*	The function :func:`selector` return a tree walk filter from a CSS selector
	passed as a string.

*	Constructing trees can now be done with ``with`` blocks. Code looks like
	this::
	
		with xsc.Frag() as node:
			+xml.XML()
			+html.DocTypeXHTML10transitional()
			with html.html():
				with html.head():
					+meta.contenttype()
					+html.title("Example page")
				with html.body():
					+html.h1("Welcome to the example page")
					with html.p():
						+xsc.Text("This example page has a link to the ")
						+html.a("Python home page", href="http://www.python.org/")
						+xsc.Text(".")
	
		print node.conv().bytes(encoding="us-ascii")

	Also the function :func:`xsc.append` has been renamed to :func:`add` and
	supports ``with`` blocks now instead of XPython__.

	__ http://codespeak.net/svn/user/hpk/talks/xpython-talk.txt

*	A subset of ReST__ is supported now for docstrings when using the
	:mod:`ll.xist.ns.doc` module. The module attribute :attr:`__docformat__`
	is now honored (Set it to ``"xist"`` to get XIST docstrings).

	__ http://docutils.sourceforge.net/rst.html

*	Many classes in the :mod:`ll.xist.ns.doc` have been renamed to more
	familiar names (from HTML, XHTML 2 or ReST).

*	The ``media`` attribute of :class:`html.link` and :class:`html.style` now
	has a method :meth:`hasmedia`.

*	The node method :meth:`asBytes` has been renamed to :meth:`bytes` and
	:meth:`bytes` has been renamed to :meth:`iterbytes`.

*	The node method :meth:`asString` has been renamed to :meth:`string` and a
	new method :meth:`iterstring` has been added.

*	:class:`ll.xist.ns.xml.XML10` is gone now. Use :class:`ll.xist.ns.xml.XML`
	instead.

*	:func:`xsc.tonode` now will raise an exception when it can't handle an
	argument instead of issuing a warning.

*	A class attribute :attr:`empty` inside element classes will now no longer
	get converted into :attr:`model`.

*	:class:`ll.xist.ns.doc.pyref` now copes better with decorated methods.

*	The deprecated :class:`Element` methods :meth:`hasAttr`, :meth:`hasattr`,
	:meth:`isallowedattr`, :meth:`getAttr`, :meth:`getattr`,
	:meth:`setDefaultAttr`, :meth:`setdefaultattr`, :meth:`attrkeys`,
	:meth:`attrvalues`, :meth:`attritems`, :meth:`iterattrkeys`,
	:meth:`iterattrvalues`, :meth:`iterattritems`, :meth:`allowedattrkeys`,
	:meth:`allowedattrvalues`, :meth:`allowedattritems`,
	:meth:`iterallowedattrkeys`, :meth:`iterallowedattrvalues`,
	:meth:`iterallowedattritems` and :meth:`copyDefaultAttrs` have been removed.
	The deprecated :class:`Attrs` method :meth:`copydefaults` has been removed
	too.

*	The namespace module :mod:`ll.xist.ns.cond` has been removed.

*	When calling the function :func:`ll.xist.parsers.parseURL` the arguments
	:var:`headers` and :var:`data` are now passed along to the parser's method
	only if they are specified. This makes it possible to pass ssh URLs to
	:func:`ll.xist.parsers.parseURL`.

*	The methods :meth:`withnames` and :meth:`withoutnames` have been split into
	two that take Python names and two that take XML names. Multiple arguments
	are used now (instead of one argument that must be a sequence). Passing a
	namespace to remove all attributes from the namespace is no longer
	supported.

*	The :class:`Attrs` methods :meth:`updatenew` and :meth:`updatexisting` have
	been removed.


Changes in 2.15.5 (released 07/17/2007)
---------------------------------------

*	The Python quotes example no longer contains the XML source or the
	generated HTML.


Changes in 2.15.4 (released 07/16/2007)
---------------------------------------

*	The Python quotes example now always parses the file from the original URL.

*	The Python quotes and the media example now print the result to ``stdout``.


Changes in 2.15.3 (released 07/16/2007)
---------------------------------------

*	Use a consistent license (MIT) everywhere. This should make XIST Debian
	compatible.

*	Change the Python quotes example, so that it works even if there's no
	:file:`python-quotes.xml` in the current directory.


Changes in 2.15.2 (released 01/24/2007)
---------------------------------------

*	Fixed a bug in :meth:`presenters.CodePresenter.__str__`.

*	Fixed base URL handling for tidy parsing.

*	Updated examples.

*	Updated :func:`xiter` and :func:`xattrs` implementations for :class:`Node`
	and :class:`Namespace` to conform to the newest version of IPython.


Changes in 2.15.1 (released 09/25/2006)
---------------------------------------

*	Fixed a few bugs in the :mod:`sgmlop` function declarations.

*	Readded the spacer pixel.


Changes in 2.15 (released 09/24/2006)
-------------------------------------

*	XIST has been made compatible with Python 2.5: Code has been updated
	to use the proper C API for memory management and :pep:`353` support has
	been added. XIST now includes its own fixed version of :mod:`sgmlop`.

*	The :class:`ll.xist.xsc.Attrs` methods :meth:`with` and :meth:`without` have
	been renamed to :meth:`withnames` and :meth:`withoutnames` for Python 2.5
	compatibility.

*	:class:`ll.xist.ns.htmlspecials.pixel` no longer handles colors via
	different GIFs. It uses the ``background-color`` in the ``style`` attribute
	instead. The same change has been implemented for
	:class:`ll.xist.ns.htmlspecials.autopixel`. It's now possible to overwrite
	the default ``src`` attribute value of ``root:px/spc.gif`` either via the
	XML attribute or via the converter context.

*	The node method :meth:`asText` has been made a function, moved into the
	:mod:`html` namespace and renamed to :func:`astext`. Furthermore elinks_ is
	used for plain text formatting now instead of w3m_.

	.. _elinks: http://elinks.or.cz/
	.. _w3m: http://w3m.sf.net/


Changes in 2.14.2 (released 07/04/2006)
---------------------------------------

*	Fixed a bug in the :meth:`presentAttr` method of
	:class:`ll.xist.presenters.TreePresenter`.


Changes in 2.14.1 (released 06/29/2006)
---------------------------------------

*	Fixed a bug in the :meth:`presentEntity` method of
	:class:`ll.xist.presenters.CodePresenter`.

*	Updated installation instructions.


Changes in 2.14 (released 06/28/2006)
-------------------------------------

*	Namespaces for RSS 0.91, RSS 2.0 and Atom 1.0 have been added.

*	A new namespace :mod:`ll.xist.ns.detox` has been added that is similar to
	:mod:`ll.toxic` but can be used to generate Python code instead of
	PL/SQL code. Using :mod:`detox` templates is about 50 times faster than
	using XIST trees directly and about 10 times faster than Kid__.

	__ http://kid.lesscode.org/

*	Presenters are now compatible to IPython__ :mod:`ipipe` module. This means
	that you can browse XIST trees interactively if you have IPython installed.
	:class:`NormalPresenter` and the :class:`Node` methods :meth:`repr` and
	:meth:`asrepr` have been removed.

	__ http://ipython.scipy.org/

*	A new processing instruction :class:`ll.xist.ns.specials.url` has been added
	that does the same URL transformation as :class:`ll.xist.xsc.URLAttr` does.

*	On publishing :class:`ll.xist.ns.html.html` now only adds a ``lang`` and
	``xml:lang`` attribute, if neither of them exists.

*	:mod:`setuptools` is now supported for installation.


Changes in 2.13 (released 10/31/2005)
-------------------------------------

*	:meth:`ll.xist.xsc.Namespace.tokenize` requires a :class:`unicode` object
	as input now. This makes it possible to use encodings that are not ASCII
	compatible (such as UTF-16). The :var:`encoding` argument is gone.

*	:meth:`ll.xist.xsc.Node.asString` uses the :var:`encoding` argument to
	determine which characters have to be output as character references
	now. (You'll still get a unicode object as the result.)

*	A new processing instruction class :class:`ll.xist.ns.specials.literal` has
	been added, that will output its content literally when published. This can
	be used for embedding preformatted XML (e.g. from a database) into an XIST
	tree.


Changes in 2.12 (released 10/13/2005)
-------------------------------------

*	Namespaces for `Relax NG`_ and Kid_ have been added.

	.. _Relax NG: http://www.relaxng.org/
	.. _Kid: http://kid.lesscode.org/

*	XIST requires version 1.0 of the core package now.

*	The class name for the DocBook DTD class has been fixed.


Changes in 2.11 (released 07/29/2005)
-------------------------------------

*	A script :file:`xml2xsc.py` has been added, that can be used to parse an
	XML file and generate a rudimentary XIST namespace from it.

*	A :class:`DocType` for XHTML 1.1 has been added (suggested by Elvelind
	Grandin).

*	Line number information is now added when parsing HTML.

*	The :meth:`sorted` method now supports the same arguments (:var:`cmp`,
	:var:`key` and :var:`reverse`) as :meth:`list.sort` and :func:`sorted`
	in Python 2.4.

*	The :meth:`walk` doesn't yield the node directly, but yields a :class:`Cursor`
	object now, with has several ways of referencing the node.

*	New methods :meth:`walknode`, :meth:`walkpath` and :meth:`walkindex` have
	been added.

*	Presenters use an iterator API instead of a stream API now. Dumping an
	XML tree presentation to the terminal can now start immediately instead
	of having to wait for the complete string to be formatted.

*	Fixed a bug with element/attribute names that contained a ``.`` character.
	(This broke :mod:`ll.xist.ns.fo`.)

*	Fixed a bug with ``xmlns`` attributes in nested elements. When an element
	ended the parser restored the wrong prefix mapping.

*	The :dir:`python-quotes` demo has been updated to use the current version of
	AMK's XML file.

*	Removed iterator stuff from :mod:`ll.xist.xfind`, as this is now part of the
	:mod:`ll` package/module.

*	The function :func:`ToNode` has been renamed to :func:`tonode`.

*	:class:`ll.xist.Context` no longer subclasses :class:`list`.

*	:class:`ll.xist.ns.doc.explain` will now try to output the objects in the
	order in which they appear in the Python source.

*	The node methods :meth:`find` and :meth:`findfirst` have been removed.

*	:mod:`ll.xist.ns.cond` now uses a sandbox dictionary in a converter context
	for evaluating expression.


Changes in 2.10 (released 05/20/2005)
-------------------------------------

*	The content of the processing instruction :class:`ll.xist.ns.code.pyexec`
	will not be executed at construction time, but at conversion time. The code
	in :class:`ll.xist.ns.code.pyexec` or :class:`ll.xist.ns.code.pyeval` will
	no longer be executed in the :mod:`ll.xist.sandbox` module (which has been
	removed), but in a sandbox dictionary in the converter context of the
	:mod:`ll.xist.ns.code` namespace.

*	The tests have been ported to `py.test`_.

	.. _py.test: http://codespeak.net/py/current/doc/test.html

*	The method :meth:`mapped` is now callable without arguments. In this case a
	converter will be created on the fly. You can pass constructor arguments for
	this converter to :meth:`mapped` as keyword arguments.

*	The publishing API has changed again:
	:meth:`ll.xist.publishers.Publisher.publish` no longer accepts an argument
	:var:`stream` to which the byte strings are written, but it is a generator
	now. The publisher methods :meth:`write` and :meth:`writetext` have been
	renamed to :meth:`encode` and :meth:`encodetext` and return the encoded
	byte string, instead of writing it directly to the stream. There's a new
	generator method :meth:`bytes` for nodes now, which can be passed the same
	arguments as :meth:`asBytes`. These changes should help when using XIST in
	WSGI applications.

*	The iterator returned from :meth:`Element.__getitem__`,
	:meth:`Frag.__getitem__` and the :meth:`walk` method now supports
	:meth:`__getitem__` itself, so you can write ``table[html.tr][0]`` to get
	the first row from a table or ``page.walk(xsc.FindTypeAll(html.td))[-1]``
	to get the last table cell from a complete HTML page.

*	Several bugs in the namespaces :mod:`ll.xist.ns.meta`, :mod:`ll.xist.ns.form`
	and :mod:`ll.xist.ns.specials` have been fixed.

*	The namespace modules :mod:`ll.xist.ns.css` and :mod:`ll.xist.ns.cssspecials`
	have been removed.


Changes in 2.9 (released 04/21/2005)
------------------------------------

*	XIST trees can now be pickled. The only restriction is that global
	attributes must come from a namespace that has been turned into a module via
	:meth:`makemod`, so that this module can be imported on unpickling.

*	Two arguments of the :meth:`walk` method have been renamed: :var:`filtermode`
	has been renamed to :var:`inmode` and :var:`walkmode` has been renamed to
	:var:`outmode`. For these modes two new values are supported:

	:const:`ll.xist.xsc.walkindex`
		The value passed to the filter function or yielded from the iterator is
		a list containing child indizes and attribute names that specify the path
		to the node in question.

	:const:`ll.xist.xsc.walkrootindex`
		The filter function will be called with two arguments: The first is the
		root node of the tree (i.e. the node for which :meth:`walk` has been
		called), the second one is an index path (just like for
		``ll.xist.xsc.walkindex``). If used as an :var:`outmode` a tuple with
		these two values will be yielded.

* Attribute mappings now support :meth:`__getitem__`, :meth:`__setitem__` and
	:meth:`__delitem__` with list arguments, i.e. you can do::

		>>> from ll.xist.ns import html
		>>> e = html.a("gurk", href=("hinz", "kunz"))
		>>> print e.attrs[["href", 0]]
		hinz
		>>> e.attrs[["href", 0]] = "hurz"
		>>> print e["href"]
		hurzkunz
		>>> del e.attrs[["href", 0]]
		>>> print e["href"]
		kunz

	XML attributes can now be accessed as Python attributes, i.e.::

		>>> from ll.xist.ns import html
		>>> e = html.a("spam", href="eggs")
		>>> print e.attrs.href
		eggs

	(Don't confuse this with ``e.Attrs.href`` which is the attribute class.)

*	:class:`Frag` and :class:`Element` now support :class:`Node` subclasses as
	arguments to their :meth:`__getitem__` method: An iterator for all children
	of the specified type will be returned.

*	The encoding used for parsing now defaults to :const:`None`. When reading
	from an URL and no default encoding has been specified the one from the
	``Content-Type`` header will be used. If this still doesn't result in a
	usable encoding, ``"utf-8"`` will be used when parsing XML and
	``"iso-8859-1"`` will be used when parsing broken HTML.

*	All error and warning classes from :mod:`ll.xist.errors` have been merged
	into :mod:`ll.xist.xsc`. This avoids import problems with circular imports.

*	The attributes :attr:`showLocation` and :attr:`showPath` of
	:class:`ll.xist.presenters.TreePresenter` have been lowercased and
	presenters are properly reset after they've done their job.

*	The class attribute :attr:`xmlname` will no longer be turned into a list
	containing the Python and the XML name, but will be the XML name only.
	You can get the Python name of :class:`foo` from ``foo.__class__.__name__``.

*	:class:`DeprecationWarning`\s for :attr:`name` and :attr:`attrHandlers` have
	finally been removed.

*	Instances of :class:`ll.xist.xsc.Entity` subclasses can now be compared.
	:meth:`__eq__` simply checks if the objects are instances of the same class.


Changes in 2.8.1 (released 03/22/2005)
--------------------------------------

*	Added a note about the package init file to the installation documentation.


Changes in 2.8 (released 01/03/2005)
------------------------------------

*	XIST requires Python 2.4 now.

*	:class:`ll.xist.ns.specials.x` has been renamed to
	:class:`ll.xist.ns.specials.ignore`.

*	:func:`ll.xist.utils.findAttr` has been renamed to
	:func:`ll.xist.utils.findattr`.

*	:class:`ll.xist.xfind.item` no longer handles slices.

*	XFind has been enhanced to support item and slice operators, i.e. if
	``foo`` is an XFind operator, ``foo[0]`` is an operator that will produce
	the first node from ``foo`` (if there is one). Negative values and slices
	are supported too.

*	Operators can be chained via division: ``html.a/html.b`` is an operator
	that can be passed around and applied to a node.

*	XIST requires the new core module and makes use of the new
	"cooperative displayhook" functionality defined there: If you install the
	displayhook you can tweak or replace ``ll.xist.presenters.hookpresenter``
	to change the output.


Changes in 2.7 (released 11/24/2004)
------------------------------------

*	The transparent pixel used by :class:`ll.xist.ns.htmlspecials.pixel` has
	been renamed to :file:`spc.gif` to avoid problems with IE.

*	Removed a debug print in :class:`ll.xist.xfind.Finder.__getitem__`.

*	:mod:`ll.xist.xfind` now has a new function :func:`item`, that can be used
	to get a certain item or slice from an iterator. :func:`xfind.first` and
	:func:`xfind.last` have been changed to use :func:`xfind.item`, so you now
	have to pass a default value to get the old behaviour.

*	Obsolete options in :mod:`ll.xist.options` have been removed (and
	:data:`reprEncoding` has been renamed to :data:`reprencoding`).


Changes in 2.6.2 (released 06/06/2005)
--------------------------------------

*	Fixed a bug in :meth:`ll.xist.parsers.Parser.parse`.


Changes in 2.6.1 (released 11/02/2004)
--------------------------------------

*	Fixed a bug in :meth:`ll.xist.xfind.Finder.__floordiv__`.

*	Restricted characters as defined in `XML 1.1`__ will now be published as
	character references.

	__  http://www.w3.org/TR/2004/REC-xml11-20040204/#NT-RestrictedChar


Changes in 2.6 (released 10/26/2004)
------------------------------------

*	:func:`ToNode` now tries iterating through the value passed in, so it's now
	possible to pass iterators and generators (and generator expressions in
	Python 2.4) to :class:`Frag` and :class:`Element` constructors.

*	A new API named XFind has been added for iterating through XML trees.
	XFind expressions look somewhat like XPath expressions but are pure Python
	expressions. For example finding all images inside links in an HTML page
	can be done like this::

		from ll.xist import parsers, xfind
		from ll.xist.ns import html
		node = parsers.parseURL("http://www.python.org/", tidy=True)
		for img in node//html.a/html.img:
			print img["src"]

*	The module :mod:`ll.xist.xfind` contains several operators that can be used
	in XFind expressions.

*	Parsing broken HTML is now done with the HTML parser from libxml2_. The
	parsing functions no longer accept options for tidy, only the boolean value
	of the :var:`tidy` argument is used.

	.. _libxml2: http://www.xmlsoft.org/

*	The publishing API has been simplified: Publication can now be done with
	a call to :meth:`ll.xist.publishers.Publisher.publish`, passing in a
	:class:`ll.xist.xsc.Node`. Writing strings to the publisher output is
	now done with :meth:`ll.xist.publishers.Publisher.write`. The methods
	:meth:`beginPublication` and :meth:`endPublication` have been
	removed.

*	The presentation API has been simplified in the same way: You'll get a
	presentation by calling: ``string = presenter.present(node)``. The methods
	:meth:`beginPresentation` and :meth:`endPresentation` have been removed.

*	The parser now has the option to ignore illegal elements, attributes,
	processing instructions and entities. The default behaviour is to raise an
	exception, but this can now be reconfigured via Python's warning framework.

*	The classmethod :meth:`tokenize` from :mod:`ll.toxic` has been moved to
	:class:`ll.xist.xsc.Namespace`, so it's now possible to tokenize an XML
	string for other processing instructions as well.

*	A new class :class:`ll.xist.xsc.NSPool` has been added. An :class:`NSPool`
	contains a pool of namespaces from which the parser selects the appropriate
	namespace once an ``xmlns`` attribute is encountered.</item>

*	The script :file:`xscmake.py` (which has been unmaintained for a while now)
	has been removed.</item>

*	Elements :class:`hostname`, :class:`tty`, :class:`prompt` and :class:`input`
	were added to :mod:`ll.xist.ns.doc`.

*	The method :meth:`ll.xist.xsc.Attrs.set` now returns the new attribute
	object.

*	The :meth:`visit` method has been removed.

*	:meth:`ll.xist.xsc.FindOld` has been removed.

*	:class:`ll.xist.ns.xml.header` has been renamed to
	:class:`ll.xist.ns.xml.declaration`.


Changes in 2.5 (released 06/30/2004)
------------------------------------

*	Specifying content models for elements has seen major enhancements. The
	boolean class attribute :attr:`empty` has been replaced by an object
	:attr:`model` whose :meth:`checkvalid` method will be called for validating
	the element content.

*	A new module :mod:`ll.xist.sims` has been added that provides a simple
	schema validation. Schema violations will be reported via Pythons
	warning framework.

*	All namespace modules have been updated to use :mod:`sims` information.
	The SVG module has been updated to SVG 1.1. The docbook module has been
	updated to DocBook 4.3.

*	It's possible to switch off validation during parsing and publishing.

*	:class:`ll.xist.xsc.Frag` and :class:`ll.xist.xsc.Element` both have a
	:meth:`__call__` method with the same arguments as their constructors.
	Those methods will append content nodes (and set attributes for
	:class:`ll.xist.xsc.Element`) and return :var:`self`, so they can be used
	when creating an object tree. This makes it possible to put the attributes
	close to the tag name, instead of putting them at the end after the content.

	Instead of::

		node = html.table(
			html.tr(
				html.td("foo"),
				html.td("bar"),
			),
			html.tr(
				html.td("spam"),
				html.td("eggs")
			),
			class_="example"

	you can now use the following::

		node = html.table(class_="example")(
			html.tr(
				html.td("foo"),
				html.td("bar"),
			),
			html.tr(
				html.td("spam"),
				html.td("eggs")
			)
		)

*	Experimental support for Holger Krekel's XPython_ has been added. Code
	might look like this::

		from ll.xist import xsc, converters
		from ll.xist.ns import html, meta

		import random

		c = converters.Converter()
		<c>:
			<html.html()>:
				<html.head()>:
					<meta.contenttype()>: pass
					<html.title()>:
						xsc.append("The title")
				<html.body(class_="foo")>:
					<html.h1()>:
						flag = random.choice((0, 1))
						if flag:
							xsc.append("The foo page", class_="foo")
						else:
							xsc.append("The bar page", class_="bar")
					<html.p()>:
						if flag:
							xsc.append("The foo content")
						else:
							xsc.append("The bar content")

		print c.lastnode.asBytes()

	.. _XPython: http://codespeak.net/svn/user/hpk/talks/xpython-talk.txt

*	Creating global attributes has been simplified. Passing an instance of
	:class:`ll.xist.xsc.Namespace.Attrs` to an :class:`Element` constructor
	now does the right thing::

		from ll.xist.ns import html, xml
		node = html.html(
			html.head(),
			xml.Attrs(lang="de"),
			lang="en",
		)

*	Creating skeleton implementations of XIST namespaces is no longer done
	via XML conversion (i.e. the namespace module :mod:`ll.xist.ns.xndl`),
	but through the new module :mod:`ll.xist.xnd`. The script :file:`dtdxsc.py`
	will automatically generate :mod:`sims` information.

*	:class:`ll.xist.xsc.CharRef` now inherits from :class:`ll.xist.xsc.Text`
	too, so you don't have to special case :class:`CharRef`\s any more. When
	publishing, :class:`CharRef`\s will be handled like :class:`Text` nodes.

*	:class:`ll.xist.ns.meta.contenttype` now has an attribute ``mimetype``
	(defaulting to ``"text/html"``) for specifying the MIME type.

*	:class:`ll.xist.ns.htmlspecials.caps` has been removed.

*	Registering elements in namespace classes has been rewritten to use a
	cache now.

*	Pretty printing has been changed: Whitespace will only be added now if
	there are no text nodes in element content.

*	Two mailing lists are now available: One for discussion about XIST and
	one for XIST announcements.


Changes in 2.4.1 (released 01/05/2004)
--------------------------------------

*	Changed the xmlname of :class:`ll.xist.ns.jsp.directive_page` back again
	(it's ``directive.page`` only for the XML form, which we don't use anyway.)

*	Drop the default value for
	:class:`ll.xist.ns.jsp.directive_page.Attrs.language`, as this attribute can
	only be used once.

*	If an :class:`ll.xist.xsc.Prefixes` object has a prefix mapping for a
	namespace it will return this prefix too, if asked for a prefix for a
	subclass of this namespace.


Changes in 2.4 (released 01/02/2004)
------------------------------------

*	The class :class:`ll.xist.parsers.Handler` has been renamed to :class:`Parser`
	and has been made reusable, i.e. it is possible to instantiate a parser once
	and use it multiple times for parsing. All the classes derived from
	:class:`xml.sax.xmlreader.InputSource` have been dropped and the methods
	for parsing strings, URLs and files have been implemented as methods of
	the parser. Most of the arguments that had to be passed to the various
	parsing functions are passed to the parser constructor now. The basic
	parsing functionality is implemented by parsing streams instead of
	:class:`InputSource` objects.

*	Similar to the changes for parsing, publishers have been changed to be
	reusable and most arguments to the publishing functions are available as
	arguments to the publisher constructor.

*	Now converter contexts are no longer bound to an element class, but to the
	context class defined by the element class, i.e. the attribute ``Context``
	of the argument for :meth:`Converter.__getitem__` will be used as the
	dictionary key. This makes it possible to use a class and it subclasses
	interchangeably (as long as the base class defines its own :class:`Context`
	class and the subclasses don't overwrite it).

*	Added a find functor :class:`FindTypeAllAttrs` that searches content and
	attributes.

*	Fixed the XML name for :class:`ll.xist.ns.jsp.directive_page`.

*	All character references in :mod:`ll.xist.ns.ihtml` that exist in
	:mod:`ll.xist.ns.chars` too have been removed.


Changes in 2.3 (released 12/08/2003)
------------------------------------

*	It's now possible to parse XML without generating location information for
	each node, by passing ``loc=False`` to the constructor of the
	:class:`Handler`.

*	The :class:`HTMLParser` no longer complains about global attributes or
	``xmlns``.

*	XIST now supports uTidylib_ in addition to mxTidy. uTidylib is found
	it is preferred over mxTidy.

	.. _uTidylib: http://utidylib.sf.net/

*	It's possible now to pass arguments to tidy simple by passing an argument
	dictionary for the :var:`tidy` argument in the parsing functions.

*	The methods :meth:`parsed` and :meth:`checkvalid` have been separated.

*	:class:`ll.xist.ns.htmlspecials.pixel` and
	:class:`ll.xist.ns.htmlspecials.autopixel` now check whether their
	:attr:`color` attribute is ok.

*	The base URL is now set correctly when parsing from an URL even if the
	original URL does a redirect. (This requires :mod:`ll.url` version 0.11.3).

*	Namespace handling has been rewritten again, to be more standards compliant:
	Now there is no prefixes for entities and processing instructions any longer.
	Prefix mappings can be created much simpler, and they no longer contain any
	namespace stack for parsing, as this is now done by the parser itself.
	:class:`xsc.NamespaceAttrMixIn` is gone too.

*	The processing instructions :class:`exec_` and :class:`eval_` from
	:mod:`ll.xist.ns.code` have been renamed to :class:`pyexec` and
	:class:`pyeval` and :class:`import_` has been removed.

*	:class:`CharRef`\s from :mod:`ll.xist.ns.html` have been moved to a new
	module named :mod:`ll.xist.ns.chars`.

*	The method names :meth:`beginPublication`, :meth:`endPublication` and
	:meth:`doPublication` have been lowercased.


Changes in 2.2 (released 07/31/2003)
------------------------------------

*	Namespace handling has been completely rewritten. Namespaces are now
	classes derived from :class:`ll.xist.xsc.Namespace`. Defining element
	classes can be done inside or outside the namespace class. If the element
	classes are defined outside the namespace class, they can be moved inside
	the namespace with a simple attribute assignment::

		class foo(xsc.Element):
			empty = False

		class xmlns(xsc.Namespace):
			xmlname = "foo"
			xmlurl = "http://www.foo.com/ns/foo"

		xmlns.foo = foo

*	The methods :meth:`elementkeys`, :meth:`iterelementkeys`,
	:meth:`elementvalues`, :meth:`iterelementvalues`, :meth:`elementitems` and
	:meth:`iterelementitems` can be used for iterating through the element
	classes and their names. You can use the method :meth:`element` to get an
	element class with a certain name::

		>>> from ll.xist.ns import html
		>>> html.element("div")
		<element class ll.xist.ns.html/div at 0x824363c>

*	For processing instructions, entities and character references similar
	methods are available.

*	The method :meth:`update` can be used to add many element classes to a
	namespace at once, simply by passing a dictionary with those classes
	(use ``vars()`` to add everything that's defined inside your module).
	The method :meth:`updatenew` does the same, but copies only those
	attributes that don't exist in the namespace, :meth:`updateexisting`
	copies only those that do exist. You can turn a namespace into a module
	with :meth:`makemod`::

		from ll.xist import xsc

		class foo(xsc.Element):
			empty = False

		class xmlns(xsc.Namespace):
			xmlname = "foo"
			xmlurl = "http://www.foo.com/ns/foo"
		xmlns.makemod(vars())

*	Put the above code into :file:`foo.py` and you can do the following::

		>>> import foo
		>>> foo
		<namespace foo/xmlns name=u'foo' url=u'http://www.foo.com/ns/foo' with 1 elements from 'foo.py' at 0x81bfc14>

*	:func:`getns` has been dropped, so you always have to pass in a
	:class:`Namespace` class where a namespace is required.

*	For the :class:`ll.xist.ns.jsp.directive_page` element automatic generation
	of the correct ``charset`` option in the ``contentType`` attribute is only
	done when there is a ``contentType`` attribute, as ``contentType`` is
	optional.

*	The converter has a new property :func:`node`. :var:`node` can't be passed
	to :meth:`conv` but will be set to :var:`self` by :meth:`conv`
	automatically. This makes it possible to access the "document root" during
	conversion.

*	:class:`ll.xist.ns.htmlspecials.autoimg` no longer touches existing width
	and height attributes. This means that %-formatting of the existing
	attributes is no longer done.

*	Added a new class :class:`ll.xist.ns.htmlspecials.autopixel` that works
	like :class:`ll.xist.ns.htmlspecials.pixel` but inherits the size for the
	image specified via the ``src`` attribute.

*	:class:`Frag` and :class:`Element` now support extended slices.

*	:class:`Frag` and :class:`Element` now support the methods :meth:`extend`
	and :meth:`__iadd__`.

*	For walking the tree the method :meth:`walk` has been completely rewritten
	and a new method :meth:`visit` has been added. For more info see the
	docstrings.

*	:class:`Node` now has two new methods :meth:`copy` and :meth:`deepcopy` and
	supports the :mod:`copy` module from the Python standard library.

*	Calling :meth:`mapped` through :meth:`conv` has been removed. You again
	have to call :meth:`mapped` directly and pass a node and a converter.

*	The HTML handling of the :class:`HTMLParser` has been improved (it now
	uses code from :mod:`xml.sax.drivers2.drv_sgmlop_html` (which is part of 
	PyXML__.

	__ http://pyxml.sf.net/

*	The core functionality found in the script :file:`dtd2xsc.py` has been
	moved to a class method :meth:`ll.xist.ns.xndl.fromdtd` in the
	:mod:`ll.xist.ns.xndl` namespace.

*	:class:`ll.xist.parsers.ExpatParser` is now a real subclass instead of an
	alias for :class:`xml.sax.expatreader.ExpatParser` It reports unknown
	entity references to the application (if loading of external entities is
	switched off, which is done by :class:`ll.xist.parsers.Handler` and only
	outside of attributes).

*	Namespaces have been added for Zope's TAL and METAL specifications.

*	A namespace has been added for `XSL-FO`_.

	.. _XSL-FO: http://www.w3.org/Style/XSL/


Changes in 2.1.4 (released 06/13/2003)
--------------------------------------

*	Remove the checks for attributes in attributes and moved the publication
	code for the full element into a separate method. This allows JSP tag
	library namespaces to simply overwrite :meth:`publish` to publish the
	element even inside attributes. (This is the same fix as in release 1.5.10).


Changes in 2.1.3 (released 05/07/2003)
--------------------------------------

*	The methods :meth:`sorted`, :meth:`reversed` and :meth:`shuffled` have been
	rewritten so they no longer use ``sys.maxint``. This change fixes those
	methods for 64 bit platforms (reported by Giles Frances Hall)


Changes in 2.1.2 (released 02/27/2003)
--------------------------------------

*	:class:`ll.xist.ns.struts_config11.plug_in` now allows content (as the DTD
	states). (This is the same fix as in release 1.5.8.)


Changes in 2.1.1 (released 02/11/2003)
--------------------------------------

*	Added a few elements and attributes to :mod:`ll.xist.ns.doc`:
	:class:`username`, which is used for the name of a user account,
	:class:`xref`, which is used for internal cross references and the attribute
	``id`` for :class:`section`, which specifies the target for an :class:`xref`.


Changes in 2.1 (released 12/09/2002)
------------------------------------

*	Added a new namespace module :mod:`ll.xist.ns.xndl` that contains the
	"XIST namespace definition language", i.e. elements that describe an
	XIST namespace and can be used by various scripts to generate skeleton
	namespace modules. The first of these script is the DTD to namespace
	converter :file:`dtd2xsc.py`.

*	Added a new namespace module :mod:`ll.xist.ns.tld` that contains the
	definition for Java Server Pages Tag Library descriptors and a script
	:file:`tld2xsc.py` that uses this namespace to generate namespace modules
	from ``tld`` files.

*	:class:`Attr` now supports the method :meth:`filtered`. This is used by
	:meth:`without` now. The arguments for :meth:`without` have changed,
	because handling global attributes was too "magic". A new method :meth:`with`
	has been added, with does the opposite of :meth:`without`, i.e. it removes
	all attributes that are not specified as parameters.

*	The Python name of each :class:`Node` subclass is now available as the class
	attribute :attr:`pyname`.

*	To continue the great renaming :meth:`withSep` has been renamed to
	:meth:`withsep`.

*	The namespace name for the :mod:`ll.xist.ns.struts_html` module has been
	fixed.

*	The argument :var:`defaultEncoding` for the various parsing functions has
	been renamed to :var:`encoding`.


Changes in 2.0.8 (released 11/20/2002)
--------------------------------------

*	:func:`ll.xist.ns.doc.getDoc` has been renamed to :func:`getdoc`.

*	The CSS parser was dropping the ``%`` from percentage values. This has
	been fixed.


Changes in 2.0.7 (released 11/12/2002)

*	:meth:`xsc.Element.__nonzero__` can no longer fall back to
	:meth:`xsc.Frag.__nonzero__`. (this is the same fix as in 1.5.7).


Changes in 2.0.6 (released 11/11/2002)
--------------------------------------

*	Performance optimizations.


Changes in 2.0.5 (released 11/11/2002)
--------------------------------------

*	Fixed a bug in :class:`ll.xist.ns.specials.autoimg`: Attributes were not
	converted before the size check was done (this is the same fix as in 1.5.5).


Changes in 2.0.4 (released 11/08/2002)
--------------------------------------

*	Fixed a regression bug in :class:`ll.xist.ns.jsp.directive` and several
	documentation issues.


Changes in 2.0.3 (released 10/30/2002)
--------------------------------------

*	Fixed a few bugs in :class:`HTMLParser`.

*	Added DocBook conversion for several elements in :mod:`ll.xist.ns.doc`.

*	Now the :file:`__init__.py` file for the :mod:`ll` package is included.


Changes in 2.0.2 (released 10/21/2002)
--------------------------------------

*	Fixed a bug in :meth:`Frag.__rmul__` (by reusing :meth:`__mul__`).

*	Fixed a bug with the backwards compatible prefix mapping: Defining element
	classes in ``exec`` processing instructions didn't work, because the
	prefixes object used for parsing wouldn't be updated when the namespace
	object is defined inside the processing instruction. Now using the default
	for the :var:`prefixes` argument in calls to the parsing functions uses one
	global shared :class:`Prefixes` instances where all the namespaces that are
	newly defined will be registered too.


Changes in 2.0.1 (released 10/17/2002)
--------------------------------------

*	Fixed :file:`xscmake.py` by removing the prefix handling.
	:class:`OldPrefixes` will always be used for parsing now.


Changes in 2.0 (released 10/16/2002)
------------------------------------

*	XIST now requires at least Python 2.2.1.

*	Attribute handling has been largely rewritten. Instead of a class attribute
	:attr:`attrHandlers`, the attributes are now defined through a nested class
	named :class:`Attrs` inside the element. This class must be derived from
	:class:`ll.xist.Element.Attrs` (or one of its subclasses if you want to
	inherit attributes from this class). Defining attributes is done through
	classes nested inside this attributes class and derived from any of the
	known attribute classes (like :class:`TextAttr`, :class:`URLAttr` etc.).
	The class name will be the attribute name (and can be overwritten with a
	class attribute :attr:`xmlname`. This makes it possible to have docstrings
	for attributes. Furthermore it's possible to define an attribute default
	value via the class attribute :attr:`default`, allowed values for the
	attribute via :attr:`values`, which is a list of allowed values, and
	whether the attribute is required or not via :attr:`required`.

*	XIST now has real namespace support. The new class
	:class:`ll.xist.xsc.Prefixes` can be used to define a mapping between
	prefixes and namespace names. This can be used for parsing and publishing.
	Namespace support is even available for entities and processing instruction.

*	Global attributes are supported now. Namespace modules for the ``xml`` and
	``xlink`` namespaces have been added (and :class:`ll.xist.xsc.XML` was
	moved to :mod:`ll.xist.ns.xml`).

*	A new namespace module for SVG 1.0 has been added: :mod:`ll.xist.ns.svg`.

*	The HTML specific parts of :mod:`ll.xist.ns.specials` have been split off
	into a separate module :mod:`ll.xist.ns.htmlspecials`.

*	Comparison of attributes with strings has been removed. You have to use
	:meth:`__unicode__` or :meth:`__str__` now before comparing.

*	The :class:`HTMLParser` now removes unknown attributes instead of
	complaining.

*	There is a new parser class :class:`BadEntityParser`, which is a SAX2
	parser that recognizes the character entities defined in HTML and tries to
	pass on unknown or malformed entities to the handler literally.

*	To give all nodes a chance to do something after they have been parsed (e.g.
	to prepend the base URL for :class:`URLAttr` nodes), the parser now calls
	the method :meth:`parsed` immediately after node creation. This is used for
	the new class :class:`StyleAttr`, which uses the :class:`CSSTokenizer`, to
	prepend the base URL to all URLs found in a style attribute.

*	The pixel images have been moved to the directory :dir:`px` to make image
	URLs shorter.


Changes in 1.6.1 (released 08/25/2003)
--------------------------------------

*	Updated to work with newer versions of :mod:`ll.ansistyle`.

*	Updated the namespaces :mod:`ll.xist.ns.struts_html` and
	:mod:`ll.xist.ns.struts_config11` to the state of Struts 1.1 final.


Changes in 1.6 (released 07/02/2003)
------------------------------------

*	Removed the default value for the ``className`` attribute in
	:class:`ll.xist.ns.struts_config11.action`.

*	Added an attribute ``type`` to
	:class:`ll.xist.ns.struts_config11.action_mapping`.


Changes in 1.5.13 (released 07/01/2003)
---------------------------------------

*	Implemented :meth:`ll.xist.xsc.Namespace.__eq__`, so that replacing a
	namespace in the registry really works.

*	Added an attribute ``target`` to :class:`ll.xist.ns.html.area`.


Changes in 1.5.12 (released 06/17/2003)
---------------------------------------

*	Fixed a bug in the new :mod:`ll.xist.ns.jsp`.


Changes in 1.5.11 (released 06/13/2003)
---------------------------------------

*	Updated :mod:`ll.xist.ns.jsp` to JSP 1.2.


Changes in 1.5.10 (released 06/13/2003)
---------------------------------------

*	Remove the checks for attributes in attributes and moved the publication
	code for the full element into a separate method. This allows JSP tag
	library namespaces to simply overwrite :meth:`publish` to publish the
	element even inside attributes.


Changes in 1.5.9 (released 04/30/2003)
--------------------------------------

*	Reregistering a namespace now properly overwrites the old version in
	``xsc.namespaceRegistry``.


Changes in 1.5.8 (released 02/27/2003)
--------------------------------------

*	:class:`ll.xist.ns.struts_config11.plug_in` now allows content (as the
	DTD states).


Changes in 1.5.7 (released 11/12/2002)
--------------------------------------

*	:meth:`xsc.Element.__nonzero__` can no longer fall back to
	:meth:`xsc.Frag.__nonzero__`.


Changes in 1.5.6 (released 11/11/2002)
--------------------------------------

*	Performance optimizations.


Changes in 1.5.5 (released 11/11/2002)
--------------------------------------

*	Fixed a bug in :class:`ll.xist.ns.specials.autoimg`: Attributes were not
	converted before the size check was done.


Changes in 1.5.4 (released 09/30/2002)
--------------------------------------

*	:file:`xscmake.py` now tries to strip off a trailing ``xsc`` from the
	filename before it falls back to the extension ``html`` (The builtin
	extension mapping is still tried first).


Changes in 1.5.3 (released 09/25/2002)
--------------------------------------

*	Added new processing instruction class :class:`ll.xist.ns.php.expression`
	that generates a PHP ``print`` statement from its content.


Changes in 1.5.2 (released 09/19/2002)
--------------------------------------

*	Removed the ``value`` magic from :class:`ll.xist.ns.form.checkbox` as this
	conflicted with dynamic ``value`` values.


Changes in 1.5.1 (released 09/17/2002)
--------------------------------------

*	Comparison of attributes with strings has been removed. You have to use
	:meth:`__unicode__` or :meth:`__str__` instead.

*	The :class:`HTMLParser` now removes unknown attributes instead of
	complaining.

*	There is a new parser class :class:`BadEntityParser`, which is a SAX2
	parser that recognizes the character entities defined in HTML and tries to
	pass on unknown or malformed entities to the handler literally.

*	To give all nodes a chance to do something after they have been parsed (e.g.
	to prepend the base URL for :class:`URLAttr` nodes), the parser now calls
	the method :meth:`parsed()` immediately after node creation. This is used
	for the new class :class:`StyleAttr`, which uses the :class:`CSSTokenizer`,
	to prepend the base url to all urls found in a style attribute.

*	The :class:`HTMLParser` now removes unknown attributes instead of
	complaining.

*	There is a new parser class :class:`BadEntityParser`, which is a SAX2
	parser that recognizes the character entities defined in HTML and tries to
	pass on unknown or malformed entities to the handler literally.

*	To give all nodes a chance to do something after they have been parsed (e.g.
	to prepend the base URL for :class:`URLAttr` nodes), the parser now calls
	the method :meth:`parsed` immediately after node creation. This is used for
	the new class :class:`StyleAttr`, which uses the :class:`CSSTokenizer`, to
	prepend to base URL to all URLs found in a style attribute.


Changes in 1.4.3 (released 04/29/2002)
--------------------------------------

*	New namespace module :mod:`xist.ns.struts_config11` allows to parse and
	modify Struts_ configuration files conforming to the `Struts 1.1 DTD`_.

	.. _Struts: http://jakarta.apache.org/struts/
	.. _Struts 1.1 DTD: http://jakarta.apache.org/struts/dtds/struts-config_1_1.dtd


Changes in 1.4.2 (released 03/22/2002)
--------------------------------------

*	Updated :file:`xscmake.py` to be compatible with the new :mod:`url` module.

*	:class:`xist.ns.jsp.directive_page` now automatically sets the
	``contentType`` on publishing.


Changes in 1.4.1 (released 03/21/2002)
--------------------------------------

*	Removed :class:`TidyURLInputSource`. Now it's possible to pass a :var:`tidy`
	flag to the remaining functions :func:`parseString`, :func:`parseFile` and
	:func:`parseURL` to specify whether the source should be tidied.

*	To prevent an element from being registered in a :class:`Namespace` the
	class attribute :attr:`register` can be used now. This makes it possible
	to have a name for the element even when it's not registered.

*	:mod:`xist.ns.form` elements now have all the attributes that the
	corresponding elements from :mod:`xist.ns.html` have.

*	Removed the old :mod:`xist.url` from the Windows distribution.


Changes in 1.4 (released 03/18/2002)
------------------------------------

*	Reimplemented URL handling again. Now the new global module :mod:`url` is
	used for that.


Changes in 1.3.1 (released 03/14/2002)
--------------------------------------

*	Added a method :meth:`pretty` to :class:`Node` for generating a pretty
	printable version of the node.

*	``xsc.Node.name`` no longer is a class method, but a class attribute, that
	will be set at class instantiation time by the meta class.


Changes in 1.3 (released 02/12/2002)
------------------------------------

*	Ported to Python 2.2. :class:`Node` is now derived from :class:`object`,
	:class:`Frag` from :class:`list` and there's a new class :class:`Attrs`
	which is derived from :class:`dict` for the attribute mappings. All
	presenters have been adapted to work with :class:`Attrs`. In addition to
	the usual dictionary methods and operators :class:`Attrs` has a
	method :meth:`without` that returns a copy of the :class:`Attrs` instance
	with some specified attributes removed.

*	All the node classes now have a new method :meth:`walk` that generates all
	nodes in the tree using the new generator feature of Python 2.2.

*	Also a new method :meth:`walkPath` has been added that works the same as
	:meth:`walk` but yields the complete path to each node as a list.

*	Added a class :class:`block` to :mod:`xist.ns.jsp`. The content of the
	:class:`block` instance will simply be enclosed in a ``{}`` block.
	:mod:`xist.ns.php` got such a class too.

*	Added a new module :mod:`xist.ns.ihtml` for i-mode HTML.

*	Added new modules :mod:`xist.ns.css` and :mod:`xist.ns.cssspecials` for
	generating CSS.

*	Now the various attributes of the :class:`Converter` object are collected in
	a :class:`ConverterState` object and it's possible to push and pop those
	states, i.e. it's now easy to temporarily modify a converter object during
	a :meth:`convert` call and revert back to a previous state afterwards.

*	:func:`parseURL` and :func:`parseTidyURL` now have an additional parameter
	:var:`headers` which is a list of string pairs specifying additional
	headers to be passed in with the request.

*	:func:`parseString` has an additional parameter :var:`systemId` which will
	be the system id of the :class:`InputSource`.

*	The distribution now includes the makefile and the XML source files so now
	the distribution can rebuild ifself.

*	Various other small bugfixes and enhancements.


Changes in 1.2.5 (released 12/03/2001)
--------------------------------------

*	Added a new element :class:`contentscripttype` to :mod:`xist.ns.meta` that
	generates a ``<meta http-equiv="Content-Script-Type" ...>`` element.

*	:func:`xist.ns.doc.explain` now generates anchor elements for the class,
	function and method description, so now the links on the XIST webpages
	work.

*	Docstrings and documentation has been reworked. Now :class:`xist.ns.doc.pyref`
	no longer implies a font change. Use the classes :class:`xist.ns.doc.module`,
	:class:`xist.ns.doc.class`, :class:`xist.ns.doc.method`,
	:class:`xist.ns.doc.function` and :class:`xist.ns.doc.arg` to mark up your
	Python identifiers.

*	Added the attributes ``type`` and ``key`` to
	:class:`xist.ns.struts_config.data_source`.


Changes in 1.2.4 (released 11/23/2001)
--------------------------------------

*	Added the deprecated attributes ``start`` to :class:`xist.ns.html.ol` and
	``value`` to :class:`xist.ns.html.li`.


Changes in 1.2.3 (released 11/22/2001)
--------------------------------------

*	Added missing :meth:`asPlainString` methods to :class:`Comment` and
	:class:`DocType`.


Changes in 1.2.2 (released 11/16/2001)
--------------------------------------

*	:meth:`xist.url.URL.fileSize` and :meth:`xist.url.URL.imageSize` now use
	the warning framework to report errors.

*	There is a new presenter named :class:`CodePresenter` that dumps the tree
	as Python source code.

*	The filenames of the pixel images used by :class:`xist.ns.specials.pixel`
	have changed. These images are now included.


Changes in 1.2.1 (released 10/08/2001)
--------------------------------------

*	URLs that are completely dynamic will now be left in peace when parsing or
	publishing.


Changes in 1.2 (released 10/03/2001)
------------------------------------

*	:class:`xist.ns.meta.keywords` and :class:`xist.ns.meta.description` no
	longer call :meth:`asPlainString` on their content. This makes it possible
	to e.g. generate the keywords via JSP::

		>>> from xist import parsers
		>>> from xist.ns import meta, jsp
		>>> s = '<keywords>' + \
		...     '<?jsp:expression "foo"?>' + \
		...     '</keywords>'
		>>> e = parsers.parseString(s)
		>>> print e.conv().asBytes()
		<meta name="keywords" content="<%= "foo" %>" />

*	When an element occurs inside an attribute during publishing, there won't
	be an exception raised any more. Instead the content of the element will be
	published. This fixes problems with abbreviation entities inside attributes.

*	:class:`xist.parsers.TidyURLInputSource` now uses the new experimental
	eGenix mx Extension package, which includes a Python port of tidy.

*	:meth:`__repr__` now uses the new class :class:`presenters.PlainPresenter`
	which gives a little more info than the default :meth:`__repr__`.

*	URL handling has been changed again. Upto now, :class:`URLAttr` had an
	additional instance attribute ``base``, which was the "base" file/URL from
	which the attribute was parsed. Now the base URL will be directly
	incorporated into the URL. You can pass the base URL to all the parsing
	functions. Similar to that when publishing you can specify a base URL. All
	URLs in the tree will be output relative to this base URL. Joining URLs is
	now done via :meth:`__div__` and no longer via :meth:`__add__`. This makes
	it more consistent with :mod:`fileutils`. The plan is to make URLs string
	like immutable objects and to merge them with :class:`fileutils.Filename`.

*	:class:`xist.ns.specials.php` has been moved to its own module
	(:mod:`xist.ns.php`). This module provided additional convenience
	processing instructions (just like :mod:`xist.ns.jsp` does).


Changes in 1.1.3 (released 09/17/2001)
--------------------------------------

*	The global namespace registry now keeps a sequential list of all registered
	namespaces, which will be used by the parser when searching for names. This
	gives a predictable search order even without using :class:`Namespaces`
	and its :meth:`pushNamespace` method: modules imported last will be searched
	first.

*	Processing instructions are now allowed inside attributes when publishing.

*	:mod:`xist.ns.docbooklite` has been renamed to :mod:`xist.ns.doc`. It can
	now generate HTML and Docbook output and has improved a lot. The XIST
	web pages now use this for automatic documentation generation. The doc
	example has been removed.

*	:class:`xist.url.URL` now has a new method :meth:`info` that returns the
	headers for the file/URL.

*	:class:`xist.url.URL` now has a methods :meth:`fileSize` and
	:meth:`imageSize` too.

*	:class:`xist.ns.jsp.directive_page` now has new attribute ``session``.


Changes in 1.1.2 (released 08/21/2001)
--------------------------------------

*	:meth:`__repr__` now uses the new class :class:`presenters.PlainPresenter`
	which gives a little more info than the default :meth:`__repr__`.


Changes in 1.1.1 (released 08/01/2001)
--------------------------------------

*	Small bugfix in :func:`presenters.strProcInst`.
*	Fixed :class:`xist.ns.struts_html.option` to allow content.


Changes in 1.1 (released 07/19/2001)
------------------------------------

*	Sequences in constructor arguments for :class:`Frag` and :class:`Element`
	are again expanded and it's again possible to pass dictionaries in an
	:class:`Element` constructor to specify attributes. As sequences are always
	unpacked, the method :meth:`extend` is gone. This works for :meth:`append`
	and :meth:`insert` too.

*	:class:`Node` and :class:`Frag` implement :meth:`__mul__` and
	:meth:`__rmul__`, so you can do stuff like::

		html.br()*5

	This returns a :class:`Frag` with five times to same node.

*	Arguments for the converter constructor can be passed to
	:meth:`xist.xsc.Node.conv` now, so it's possible to do stuff like this::

		from xist.ns import code
		print code.Eval("return converter.lang").conv(lang="en").asBytes()

	which will print ``en``.

*	The option :var:`XHTML` for the publishers has been changed to lowercase.

*	:class:`xist.ns.html.html` will automatically generate a ``lang`` and
	``xml:lang`` attribute when the converter has a language set.


Changes in 1.0 (released 06/18/2001)
------------------------------------

*	New module for WML 1.3.

*	The publishing interface has changed internally and publishing should be
	faster now.

*	Publishers now support a new parameter: :var:`usePrefix`, which specifies
	if namespace prefixes should be output for the element names.

*	Part of the implementation of the publishing stuff has been moved to C, so
	now you'll need a C compiler to install XIST.

*	When publishing ``"``, it will now only be replaced with ``&quot;`` inside
	attributes.

*	All the :meth:`asHTML` methods now have an additional argument
	:var:`converter`. This makes it possible to implement different processing
	modes or stages for new elements. All currently implemented elements and
	entities ignore this argument, but pass it on in the call to their
	childrens' :meth:`asHTML` method. As the name :meth:`asHTML` no longer
	makes sense, :meth:`asHTML` has been renamed to :meth:`convert`.

*	There is now a tool :file:`dtd2xsc.py` in the :dir:`scripts` directory that
	creates a skeleton XIST module from a DTD (this requires xmlproc from the
	PyXML package).

*	New preliminary module for DocBook 4.12. (Incomplete: :meth:`convert`
	methods and Unicode character entities are missing; any volunteers for
	implementing 375 classes?)

*	New module :file:`ruby.py` that implements the `W3C Ruby draft`_.

	.. _W3C Ruby draft: http://www.w3.org/TR/ruby/xhtml11-ruby-1.mod

*	:file:`sql.py` has been removed from XIST, but is available as a
	separate module.

*	The parsing interface has been changed. Parsing is now done with the
	functions :func:`parseFile`, :func:`parseString`, :func:`parseURL` and
	:func:`parseTidyURL` in the module :mod:`parsers`. It's now possible to
	specify which parser should be used for parsing by passing a SAX2 parser
	instance to any of these functions. XIST now includes a rudimentary
	SAX2 driver for :class:`sgmlop` and a rudimentary HTML parser that
	emits SAX2 events.

*	The python-quotes example has been updated to work with expat.

*	Added a new example: media.

*	All abbreviation entities have been moved to a new module :file:`abbr.py`.

*	All the modules that provide new elements and entitites have been moved
	to a subpackage :mod:`ns`.

*	:class:`Frag` and :class:`Element` now have new methods :meth:`sorted`,
	:meth:`reversed`, :meth:`filtered` and :meth:`shuffled` that return sorted,
	reversed, filtered and shuffled versions of the :class:`Frag`/:class:`Element`
	object.

*	New namespace modules :file:`ns/jsp.py` and :file:`ns/struts_html.py` have
	been added that allow you to use JSP_ and Struts_ tags with XIST.

	.. _JSP: http://java.sun.com/products/jsp/
	.. _Struts: http://jakarta.apache.org/struts/

*	A new method :meth:`asText` was added, that returns the node as a formatted
	plain ASCII text (this requires that w3m__ is installed.)

	__ http://w3m.sf.net/

*	:file:`make.py` has been renamed to :file:`xscmake.py` and moved to the
	:dir:`scripts` directory, it will be installed as a callable script with
	``python setup.py install_scripts``.

*	:file:`xscmake.py` has a new option :option:`--files`/:option:`-f`.
	The argument is a file containing a list of filenames (one name per line)
	that should be converted.

*	:file:`xscmake.py` has a new option :option:`--parser`/:option:`-r` for
	specifying which parser to use. Allowed values are ``sgmlop`` and ``expat``.

*	:file:`xscmake.py` has a new option :option:`--namespace`/:option:`-n`
	that can be used for appending :class:`Namespace` objects to the
	:class:`Namespaces` object used by :file:`xscmake.py`::

		xscmake.py -n html -n spam eggs.xsc

	With this call the parser will find element classes from the module with
	the prefix name ``spam`` before those from ``html`` and those before
	anything else.

*	:class:`xist.url.URL` no longer has an attribute :attr:`ext`. :attr:`file`
	and :attr:`ext` are merged.

*	The special treatment of sequences as constructor arguments to :class:`Frag`
	and :class:`Element` has been removed, so XIST will no longer remove one
	level of nesting. If you still want that, use a ``*`` argument.

*	:class:`Frag` and :class:`Element` now have a new method :meth:`mapped`,
	that recursively maps the nodes through a function. This is like
	:meth:`convert` but via an external function.

*	Attribute handling has been improved thanks to a suggestion by Hartmut
	Goebel: :meth:`Element.__getitem__` now always works as long as the
	attribute name is legal. If the attribute is not set, an empty attribute
	will be returned. All empty attributes will be considered as being not set
	and so :meth:`hasAttr` returns ``0`` for them, and :meth:`publish` doesn't
	publish them. This simplifies several very common cases:

	*	Copying an attribute from one element to another works regardless of
		whether the attribute is set or not;

	*	Testing for an attributes presence can now be done much simpler:
		``if element["attrname"]`` instead of ``if element.hasAttr("attrname")``
		(which still works, and should be a little faster);

	*	When you construct an XIST tree and the presence or absence of an
		attribute is tied to a condition, you can construct the attribute in
		advance and use it afterwards in the tree construction::

			if condition:
				align = "right"
			else:
				align = None
			node = html.div("spam", align=align)

		So, when the ``condition`` is false, the node will not have the
		attribute ``align`` set.

*	:class:`xist.ns.cond.If` (and :class:`xist.ns.cond.ElIf`) can now be used
	to test for attributes of the converter. I.e. it's possible to write the
	following XML::

		<if lang="en">Title
		<elif lang="de">Überschrift
		</if>

*	URL handling has be completely changed and is much, much simpler now. There
	are no more path markers. To specify an URL that is relative to the current
	directory use the scheme ``root`` (e.g. ``root:main.css``).


Changes in 0.4.7 (released 11/24/2000)
--------------------------------------

*	Fixed a bug in the entity handling.

*	Added a few deprecated elements and attributes to the :mod:`html` module.

*	Improved the publishing of attributes. Now all attribute values will be
	published. For boolean attributes no value will be published for ``XHTML==0``
	and the attribute name will be used for ``XHTML==1`` or ``XHTML==2``.

*	:meth:`Element.compact` now works (better) ;).

*	Incorparated many bug fixes from Hartmut Goebel.

*	Implemented :meth:`xsc.Element.copyDefaultAttrs`, which copies unset
	attributes over from a dictionary (simplifies implementing
	:class:`specials.plaintable` and :class:`specials.plainbody`).

*	:meth:`providers.Provider.pushNamespace` now handles multiple arguments
	which may be :class:`Namespace` objects or modules (in which case,
	``module.namespace`` will be pushed).

*	:meth:`providers.Providers.popNamespace` can now pop multiple namespaces
	at once.

*	:class:`providers.TidyURIProvider` now uses :func:`os.popen3` for piping
	the file through tidy, so now there will be no more temporary files. The
	call to tidy now includes options that hopefully make the output more
	suited to XIST.

*	Incorparated a new :file:`url.py` by Hartmut Goebel, that fixes many problem
	(e.g. optimizing ``http://server/foo/bar/../../baz.gif`` now works.)

*	:file:`make.py` includes a new option :option:`--path` for adding
	directories to :data:`sys.path`.


Changes in 0.4.6 (released 11/03/2000)
--------------------------------------

*	Now uses :class:`sgmlop.XMLParser` instead of :class:`sgmlop.SGMLParser`,
	so case is preserved.

*	Fixed another regression from the URL to string conversion change.


Changes in 0.4.5 (released 11/01/2000)
--------------------------------------

*	Converting URLs to nodes is now done in :func:`ToNode`, so :class:`URL`
	objects can be used everywhere.

*	Fixed a few bugs in :meth:`Text._strtext` and :meth:`URLAttr._str`.


Changes in 0.4.4 (releases 10/27/2000)
--------------------------------------

*	Now testing if characters can be encoded with the specified encoding is
	done directy. This means, that escaping unencodable characters now works
	even with exotic encodings (tested with `JapaneseCodecs 1.0.1`__.

	__ http://pseudo.grad.sccs.chukyo-u.ac.jp/~kajiyama/python/

*	The :class:`URLAttr` constructor now can handle a single parameter of the
	type :class:`URL`.

*	The URL to string conversion function have changed: :meth:`URL.asString`
	returns the URL with path markers, :meth:`URL.asPlainString` returns the
	URL without path markers.

*	Added the ``i18n`` attribute to the :class:`font` element.

*	Fixed the clashes between the class names for the elements and entities
	:class:`sub` and :class:`sup` in :file:`html.py`.

*	Several small enhancements and bug fixes contributed by Hartmut Goebel.


Changes in 0.4.3 (released 10/19/2000)
--------------------------------------

*	Now processing instruction classes are registered in the same way as
	elements and entities are.

*	The leaf nodes (:class:`Text`, :class:`Comment`, :class:`ProcInst`) are now
	considered immutable. This means that their :meth:`asHTML` method can
	simply return :var:`self`, because now those nodes can be shared between
	trees. Functionality for manipulation the objects is provided by a mixin
	class very similar to :class:`UserString`. All this results in a speedup
	of about 10% for the python-quotes example.

*	Small optimizations in the :meth:`asHTML` methods of :class:`Element` and
	:class:`Frag` optimized away many calls to :meth:`append`, :meth:`extend`
	and :meth:`ToNode` and result in a speedup of about 30% for the
	python-quotes example. One consequence of this is that :class:`Null`
	objects will no longer be ignored.


Changes in 0.4.2 (released 09/24/2000)
--------------------------------------

*	New elements :class:`keywords` and :class:`description` in :file:`meta.py`.

*	Fixed a bug in :meth:`Namespace.register`, now setting ``name=None`` to
	prevent an element from being registered works again.


Changes in 0.4.1 (released 09/21/2000)
--------------------------------------

*	A new module named :file:`meta.py` has been created, that simplifies
	generating meta tags.

*	Various small bugfixes.


Changes in 0.4 (released 09/19/2000)
------------------------------------

*	XIST now requires at least Python 2.0b1.

*	A new bugfixed version of the sgmlop source is available from the
	`FTP site`_.

	.. _FTP site: ftp://ftp.livinglogic.de/pub/livinglogic/xist/

*	XIST now completely supports Unicode. For output any encoding known to
	Python can be used, so now you can output your HTML in ASCII, Latin-1,
	UTF-8, UTF-16, ...

*	All publishers have been updated to support Unicode. The publishing
	interface has been streamlined (:var:`encoding` and :var:`XHTML` parameters
	are now attributes of the publisher).

*	:meth:`asString` will now always return a Unicode string. If you want a byte
	string use :meth:`asBytes` instead, where the encoding can be specified as
	an argument.

*	There an additional publisher class :class:`FilePublisher`, which can be
	used for publishing to a file (or anything else that has a :meth:`write`
	and a :meth:`writelines` method, and is supported by the stream writer
	available through :func:`codecs.lookup`).

*	Element and attribute names are no longer converted to lowercase. If you
	have an attribute name which clashes with a Python keyword (e.g. ``class``)
	append an underscore (``_``), which will be removed before accessing the
	attribute. This is the "official" Python method for handling these cases.

*	Elements and entities are no longer registered one by one. Now you can
	build :class:`Namespace` objects which are used for searching and there are
	:meth:`pushNamespace` and :meth:`popNamespace` functions in :mod:`XSC.xsc`.
	For more info, see the source.

*	Image size calculation has been removed from :class:`html.img` and
	:class:`html.input`. Use :class:`specials.autoimg` and
	:class:`specials.autoinput` for that.

*	:meth:`__getitem__`, :meth:`__setitem__` and :meth:`__delitem` of
	:class:`Frag` and :class:`Element` now accepts a list as an argument. The
	method will be applied recursively, i.e. ``e[[0, 1, "foo", 2]`` is the
	same as ``e[0][1]["foo"][2]``.

*	The deprecated module :file:`db.py` no longer exists. Useful functions and
	elements from :file:`db.py` have been moved to :file:`sql.py` and
	:file:`form.py` respectively.

*	When using :func:`xsc.make` the encoding and XHTML parameters to use can
	now be specified on the command line (e.g. ``--encoding utf-8 --xhtml 2``)

*	Handling of multiline ``<?xsc-eval?>`` and ``<?xsc-exec?>`` has been
	enhanced, although XIST will not be able to guess the correct indentation
	in all cases. As a workarround simply add a Python comment to the beginning.
	So the following won't work::

		<?xsc-exec
			for i in xrange(10):
				do(i)
		?>

	But this will::

		<?xsc-exec
			#
			for i in xrange(10):
				do(i)
		?>

*	Make functionality has been moved to :file:`make.py`, as certain modules
	can't be used as the main script, because reimporting them in processing
	instructions won't work. Now you can simply call::

		make.py --import xist.html --import spam eggs.xsc

*	There is a new module :file:`cond.py`, that contains elements that can be
	used for conditionals::

		<?xsc-exec a=42?>
		<if cond="a==21">
			<b>foo</b>
		<elif cond="a==42"/>
			<i>bar</i>
		<else/>
			baz
		</if>


Changes in 0.3.9 (released 08/10/2000)
--------------------------------------

*	sgmlop will now be found either via ``import sgmlop`` or via
	``from xml.parsers import sgmlop``.


Changes in 0.3.8 (released 07/14/2000)
--------------------------------------

*	Fixed a bug in :meth:`URLAttr.publish`, which prevented :class:`URLAttr`
	from working at all.


Changes in 0.3.7 (released 07/06/2000)
--------------------------------------

*	Fixed a bug in :class:`html.img` and :class:`html.input`. Now image size
	calculation works again.


*	Changes in 0.3.6 (released 07/04/2000)

*	Fixed a bug in :meth:`Node._matches`, which resulted in a non working
	:meth:`find`.


Changes in 0.3.5 (released 07/02/2000)
--------------------------------------

*	The documentation example has been enhanced. Now documenting methods works.

*	When the member :attr:`elementname`: in the element class is set before
	calling :func:`registerElement`, this element name will be used for the
	element. This allows custom names even when using
	:func:`registerAllElements`.

*	Comparison of scheme and server in URLs is done case insensitive (as
	:rfc:`2068` requires.)

*	Image size calculation is now done in :meth:`asString` and not in
	:meth:`asHTML`.	This allows to write faster code. Old method::

		e = html.div(html.img(...),gurk.hurz()).asHTML().asString()

	New method::

		e = html.div(html.img(...),gurk.hurz().asHTML()).asString()

*	Image size calculation is now done for ``<nput type="image">``. The ``size``
	attribute is set to the image width.

*	Manipulating the path in an URL is now done via the usual
	:meth:`__setitem__`/:meth:`__getitem__` stuff, which keeps the path in a
	consistent state::

		>>> from xist.URL import URL
		>>> u = URL("/foo/*/../bar/baz.gif")
		>>> del u[1]
		>>> u
		URL(scheme='server', path=['bar'], file='baz', ext='gif')

*	:meth:`findNodes` (which has been shortened to :meth:`find`) has an
	additional argument :var:`test`, which can be a test function that will be
	called when the node passes all other tests.

*	:meth:`asString` no longer generates a string directly, but uses the new
	method :meth:`publish`, which has an additional argument :var:`publisher`,
	to which the strings to be output are passed.


Changes in 0.3.4 (released 05/31/2000)
--------------------------------------

*	Location information is now copied over in :meth:`clone`, :meth:`asHTML`
	and :meth:`compact` where appropriate, so you know even in the HTML tree
	where something came from.

*	``xsc.repransi`` can now have three values:

	0
		coloring is off
	1
		coloring is on for a dark background
	2
		coloring is on for a light background

*	All ``repransi`` variables are now arrays with two strings, the first for
	dark, the second for light.


Changes in 0.3.3 (released 05/30/2000)
--------------------------------------

*	The workaround for the trailing CDATA bug in sgmlop has been removed, so
	now you'll need a newer version of sgmlop (included in PyXML 0.5.5.1).


Changes before 0.3.3
--------------------

*	These changes predate written history.
