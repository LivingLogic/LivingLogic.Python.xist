Migrating to version 3.7
========================

Changes to the make module
--------------------------

*	The division operator is no longer implemented, so instead of::

		t1 = make.FileAction(key=url.URL("foo.txt"))
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
	``int4``, ``int8``, ``rgb4``, ``rgba4``, ``rgb8``, and ``rgba8`` have been
	dropped. The new methods ``r``, ``g``, ``b`` and ``a`` return the 8 bit
	component values.

*	The class methods ``fromhsva`` and ``fromhlsa`` have been renamed to
	``fromhsv`` and ``fromhls``.

*	The property ``css`` has been dropped instead the CSS string is returned
	by ``__str__``.

*	Dividing color now does a scalar division. Blending colors is now done with
	the modulo operator.

Removal of XPIT
---------------

*	The XPIT tamplating language has been removed. You should replace all your
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

*	The :var:`targetroot` parameter for :meth:`ll.make.XISTConvertAction.__init__`
	has been renamed to :var:`root`.

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
the attribute value into an :class:`specials.url` PI.


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
to a namespace (in the XML sense) simpy if their ``xmlns`` attribute have the
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
*	``item`` to ``li`` or ``dd`` (depending on whether it's inside an :class:`ol`,
	:class:`ul` or :class:`dl`);
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

:meth:`xsc.Namespace.tokenize` no longer has an :var:`encoding` argument, but
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
``xsc.Frag(node.walk(...)`` or ``node.walk(...)[0]`` instead.

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
to make a namespace available for parsing the rest of the XML file) you will
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

The argument :var:`filtermode` has been renamed to :var:`inmode` and (for
:meth:`walk`) :var:`walkmode` has been renamed to :var:`outmode`.


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
functionality, you may now use slices on XFind operators, and materilize the
result, i.e. replace ``xfind.slice(foo, 1, -1)`` with ``list(foo[1:-1])``, if
``foo`` is an XFind operator. Otherwise you can use ``list(foo)[1:-1]``.


Migrating to version 2.7
========================

Changes to :mod:`ll.xist.xfind`
-------------------------------

The functions :func:`xfind.first` and :func:`xfind.last` now use
:func:`xfind.item`, so they will raise an :exc:`IndexError` when no default
value is passed. To get the old behaviour, simply pass ``None`` as the default.


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
:var:`tidy` argument will be used. There are no other visible changes to the API
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

:var:`handler`
	This argument is no longer available, if you need a special handler, you
	have to subclass :class:`ll.xist.parsers.Parser` and call its parsing
	methods.

:var:`parser`
	This argument has been renamed to :var:`saxparser` and is *not* a SAX2
	parser instance any longer, but a callable that will create a SAX2 parser.

:var:`sysid`
	:var:`sysid` is now available for all parsing functions not just
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

The three arguments :var:`elementmode`, :var:`entitymode` and
:var:`procinstmode` for the publishing methods have been combined into
:var:`prefixmode`, which is used for elements only.

Changed namespaces
------------------

The character reference classes from :mod:`ll.xist.ns.html` have been moved to a
separate namespace :mod:`ll.xist.ns.chars`.

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

Many :class:`Attrs` methods have gained an additional parameter :var:`xml`,
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

:class:`ll.xist.htmlspecials.autoimg` will no longer touches existing ``width``
or ``height`` attributes, so e.g. setting the width to twice the image size via
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

But one minor difference remains: when :var:`skiproot` is set to true in the new
:meth:`find` method, the attributes of the root element will *not* be traversed.
With the old method they would be traversed.

:class:`doc` changes
--------------------

:class:`programlisting` has been renamed to :class:`prog`.

Namespace changes
-----------------

Namespaces can no longer be instantiated. Instead you have to derive a class
from :class:`Namespace`. The :var:`xmlprefix` argument from the constructor
becomes a class attribute :attr:`xmlname` and the argument :var:`xmlname`
becomes :attr:`xmlurl`.

Adding element classes to the namespace is now done with the :class:`Namespace`
classmethod :meth:`update`. If you want the turn a namespace into a module, you
can use the classmethod :meth:`makemod` instead of :meth:`update`, i.e. replace::

	xmlns = xsc.Namespace("foo", "http://www.foo.com/", vars()

with::
	
	class xmlns(xsc.Namespace):
		xmlname = "foo"
		xmlurl = "http://www.foo.com/"
	xmlns.makemod(vars())


Migrating to version 2.1
========================

The method :meth:`withSep` has been renamed to :meth:`withsep`.

The argument :var:`defaultEncoding` for the various parsing functions has been
renamed to :var:`encoding`.


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
