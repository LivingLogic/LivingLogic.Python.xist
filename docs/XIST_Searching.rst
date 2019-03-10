Iterating through XIST trees
============================

There are three related methods available for iterating through an XML tree and
finding nodes in the tree: The methods :meth:`~ll.xist.xsc.Node.walk`,
:meth:`~ll.xist.xsc.Node.walknodes` and :meth:`~ll.xist.xsc.Node.walkpaths`.

The :meth:`~ll.xist.xsc.Node.walk` method
-----------------------------------------

The method :meth:`~ll.xist.xsc.Node.walk` is a generator. When called without
any arguments it visits each node in the tree once. Furthermore without
arguments parent nodes are yielded before their children, and no attribute nodes
are yielded. (This can however be changed by passing certain arguments to
:meth:`~ll.xist.xsc.Node.walk`.)

What :meth:`~ll.xist.xsc.Node.walk` outputs is a :class:`~ll.xist.xsc.Cursor`
object (in fact :meth:`~ll.xist.xsc.Node.walk` always yields the same cursor
object, but the attributes will be updated during the traversal).
A :class:`~ll.xist.xsc.Cursor` object has the following attributes:

:attr:`root`
	The node where traversal has been started (i.e. the object for which the
	:meth:`~ll.xist.xsc.Node.walk` method has been called).

:attr:`node`
	The current node being traversed.

:attr:`path`
	A list of nodes that contains the path through the tree from the root to the
	current node (i.e. ``path[0]`` is :attr:`root` and ``path[-1]`` is
	:attr:`node`).

:attr:`index`
	A path of indices (e.g. ``[0, 1]`` if the current node is the second child of
	the first child of the root). Inside attributes the index path will contain
	the name of the attribute (or a (attribute name, namespace name) tuple inside
	a global attribute).

:attr:`event`
	A string that specifies which event is currently being handled. Possible
	values are: ``"enterelementnode"``, ``"leaveelementnode"``,
	``"enterattrnode"``, ``"leaveattrnode"``, ``"textnode"``, ``"commentnode"``,
	``"doctypenode"``, ``"procinstnode"``, ``"entitynode"`` and ``"nullnode"``.

The following example shows the basic usage of the :meth:`~ll.xist.xsc.Node.walk`
method:

.. sourcecode:: pycon
	:caption: Using the :meth:`walk` method

	>>> from ll.xist.ns import html
	>>> e = html.ul(html.li(i) for i in range(3))
	>>> for cursor in e.walk():
	... 	print(f"{cursor.event} {cursor.node!r}")
	... 
	enterelementnode <ll.xist.ns.html.ul element object (3 children/no attrs) at 0x43fbb0>
	enterelementnode <ll.xist.ns.html.li element object (1 child/no attrs) at 0x452750>
	textnode <ll.xist.xsc.Text content='0' at 0x5b1670>
	enterelementnode <ll.xist.ns.html.li element object (1 child/no attrs) at 0x452830>
	textnode <ll.xist.xsc.Text content='1' at 0x5b16e8>
	enterelementnode <ll.xist.ns.html.li element object (1 child/no attrs) at 0x5b30d0>
	textnode <ll.xist.xsc.Text content='2' at 0x5b1760>

The :attr:`path` attribute can be used like this:

.. sourcecode:: pycon
	:caption: Using the :attr:`path` attribute

	>>> from ll.xist.ns import html
	>>> e = html.ul(html.li(i) for i in range(3))
	>>> for cursor in e.walk():
	... 	print([f"{n.__class__.__module__}.{n.__class__.__qualname__}" for n in cursor.path])
	...
	['ll.xist.ns.html.ul']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li', 'll.xist.xsc.Text']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li', 'll.xist.xsc.Text']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li', 'll.xist.xsc.Text']

The following example shows how the :attr:`index` attribute works:

.. sourcecode:: pycon
	:caption: Using the :attr:`index` attribute

	>>> from ll.xist.ns import html
	>>> e = html.ul(html.li(i) for i in range(3))
	>>> for cursor in e.walk():
	... 	print(f"{cursor.index} {cursor.node!r}")
	...
	[] <ll.xist.ns.html.ul element object (5 children/no attrs) at 0x4b7bb0>
	[0] <ll.xist.ns.html.li element object (1 child/no attrs) at 0x4ca750>
	[0, 0] <ll.xist.xsc.Text content='0' at 0x629670>
	[1] <ll.xist.ns.html.li element object (1 child/no attrs) at 0x4ca830>
	[1, 0] <ll.xist.xsc.Text content='1' at 0x6296e8>
	[2] <ll.xist.ns.html.li element object (1 child/no attrs) at 0x62b0d0>
	[2, 0] <ll.xist.xsc.Text content='2' at 0x629760>


Changing which parts of the tree are traversed
----------------------------------------------

The :meth:`~ll.xist.xsc.Node.walk` method has a few additional parameters that
specify which part of the tree should be traversed and in which order:

:obj:`entercontent` (default ``True``)
	Should the content of an element be entered? Note that when you call
	:meth:`~ll.xist.xsc.Node.walk` with :obj:`entercontent` being false,
	:meth:`~ll.xist.xsc.Node.walk` will only yield the root node itself.

:obj:`enterattrs` (default ``False``)
	Should the attributes of an element be entered? The following example shows
	the usage of :obj:`enterattrs`:

	.. sourcecode:: pycon
		:caption: Using the :obj:`enterattrs` paameter

		>>> from ll.xist.ns import html
		>>> e = html.ul(html.li(i, class_=f"li-{i}") for i in range(3))
		>>> for cursor in e.walk(enterattrs=True):
		... 	indent = "\t"*(len(cursor.path)-1)
		... 	print(f"{indent}{cursor.node!r}")
		... 
		<ll.xist.ns.html.ul element object (3 children/no attrs) at 0x51e790>
			<ll.xist.ns.html.li element object (1 child/1 attr) at 0x51e8b0>
				<ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x532f30>
				<ll.xist.xsc.Text content='0' at 0x67e6c0>
			<ll.xist.ns.html.li element object (1 child/1 attr) at 0x67f8b0>
				<ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x671720>
				<ll.xist.xsc.Text content='1' at 0x67e7b0>
			<ll.xist.ns.html.li element object (1 child/1 attr) at 0x67f930>
				<ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x671630>
				<ll.xist.xsc.Text content='2' at 0x67e990>

When both :obj:`entercontent` and :obj:`enterattrs` are true, the attributes
will always be entered before the content. Setting :obj:`enterattrs` to true
will only visit the attribute nodes themselves, but not their content.

:obj:`enterattr` (default ``False``)
	Should the content of the attributes of an element be entered? (This is only
	relevant if :obj:`enterattrs` is true.) The following example shows the usage
	of the :obj:`enterattr` parameter:

	.. sourcecode:: pycon
		:caption: Using the :obj:`enterattr` paameter

		>>> from ll.xist.ns import html
		>>> e = html.ul(html.li(i, class_=f"li-{i}") for i in range(3))
		>>> for cursor in e.walk(enterattrs=True, enterattr=True):
		... 	indent = "\t"*(len(cursor.path)-1)
		... 	print(f"{indent}{cursor.node!r}")
		... 
		<ll.xist.ns.html.ul element object (3 children/no attrs) at 0x4c1790>
			<ll.xist.ns.html.li element object (1 child/1 attr) at 0x4c18b0>
				<ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x4d5f30>
					<ll.xist.xsc.Text content='li-0' at 0x621788>
				<ll.xist.xsc.Text content='0' at 0x621710>
			<ll.xist.ns.html.li element object (1 child/1 attr) at 0x6228b0>
				<ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x614720>
					<ll.xist.xsc.Text content='li-1' at 0x621968>
				<ll.xist.xsc.Text content='1' at 0x621800>
			<ll.xist.ns.html.li element object (1 child/1 attr) at 0x622930>
				<ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x614630>
					<ll.xist.xsc.Text content='li-2' at 0x621ad0>
				<ll.xist.xsc.Text content='2' at 0x6219e0>


Changing traversal order
------------------------

The default traversal order is "top down". The following :meth:`~ll.xist.xsc.Node.walk`
parameters can be used to change that into "bottom up" order or into visiting
each element or attribute both on the way down *and* up:

:attr:`enterelementnode` (default ``True``)
	Should the generator yield the cursor before it enters an element (i.e.
	before it visits the attributes and content of the element)? The cursor
	attribute :obj:`event` will have the value ``"enterelementnode"`` in this
	case.

:attr:`leaveelementnode` (default ``False``)
	Should the generator yield the cursor after it has visited an element? The
	cursor attribute :attr:`event` will have the value ``"leaveelementnode"`` in
	this case. Passing ``enterelementnode=False, leaveelementnode=True`` to
	:meth:`~ll.xist.xsc.Node.walk` will change "top down" traversal into
	"bottom up".

:attr:`enterattrnode` (default ``True``)
	Should the generator yield the cursor before it enters an attribute?
	The cursor attribute :attr:`event` will have the value ``"enterattrnode"``
	in this case. Note that the attribute will only be entered when
	:attr:`enterattr` is true and it will only be visited if :attr:`enterattrs`
	is true.

:attr:`leaveattrnode` (default ``False``)
	Should the generator yield the cursor after it has visited an attribute?
	The cursor attribute :attr:`event` will have the value ``"leaveattrnode"``
	in this case. Note that the attribute will only be entered when
	:attr:`enterattr` is true and it will only be visited if :attr:`enterattrs`
	is true.

Passing ``True`` for all these parameters gives us the following output:

.. sourcecode:: pycon
	:caption: Full tree traversal

	>>> from ll.xist.ns import html
	>>> e = html.ul(html.li(i, class_=f"li-{i}") for i in range(3))
	>>> for cursor in e.walk(entercontent=True, enterattrs=True, enterattr=True,
	... 	 enterelementnode=True, leaveelementnode=True,
	... 	 enterattrnode=True, leaveattrnode=True):
	... 	indent = "\t"*(len(cursor.path)-1)
	... 	print(f"{indent}{cursor.event} {cursor.index} {cursor.node!r}")
	... 
	enterelementnode [] <ll.xist.ns.html.ul element object (3 children/no attrs) at 0x4cbe50>
		enterelementnode [0] <ll.xist.ns.html.li element object (1 child/1 attr) at 0x4de850>
			enterattrnode [0, 'class'] <ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x4f2f90>
				textnode [0, 'class', 0] <ll.xist.xsc.Text content='li-0' at 0x63f800>
			leaveattrnode [0, 'class'] <ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x4f2f90>
			textnode [0, 0] <ll.xist.xsc.Text content='0' at 0x63f788>
		leaveelementnode [0] <ll.xist.ns.html.li element object (1 child/1 attr) at 0x4de850>
		enterelementnode [1] <ll.xist.ns.html.li element object (1 child/1 attr) at 0x63e870>
			enterattrnode [1, 'class'] <ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x631780>
				textnode [1, 'class', 0] <ll.xist.xsc.Text content='li-1' at 0x63f9e0>
			leaveattrnode [1, 'class'] <ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x631780>
			textnode [1, 0] <ll.xist.xsc.Text content='1' at 0x63f878>
		leaveelementnode [1] <ll.xist.ns.html.li element object (1 child/1 attr) at 0x63e870>
		enterelementnode [2] <ll.xist.ns.html.li element object (1 child/1 attr) at 0x63e8f0>
			enterattrnode [2, 'class'] <ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x631690>
				textnode [2, 'class', 0] <ll.xist.xsc.Text content='li-2' at 0x63fb48>
			leaveattrnode [2, 'class'] <ll.xist.ns.html.coreattrs.class_ attr object (1 child) at 0x631690>
			textnode [2, 0] <ll.xist.xsc.Text content='2' at 0x63fa58>
		leaveelementnode [2] <ll.xist.ns.html.li element object (1 child/1 attr) at 0x63e8f0>
	leaveelementnode [] <ll.xist.ns.html.ul element object (3 children/no attrs) at 0x4cbe50>


Skipping parts of the tree
--------------------------

It is possible to change the cursor attributes that specify the traversal order
during the traversal to skip certain parts of the tree. In the following example
the content of :class:`~ll.xist.ns.html.li` elements is skipped if they have a
``class`` attribute:

.. sourcecode:: pycon
	:caption: Skipping parts of the tree

	>>> from ll.xist.ns import html
	>>> e = html.ul(html.li(i, class_=None if i%2 else f"li-{i}") for i in range(3))
	>>> for cursor in e.walk():
	... 	if isinstance(cursor.node, html.li) and "class_" in cursor.node.attrs:
	... 		cursor.entercontent = False
	... 	indent = "\t"*(len(cursor.path)-1)
	... 	print(f"{indent}{cursor.event} {cursor.node!r}")
	... 
	enterelementnode <ll.xist.ns.html.ul element object (3 children/no attrs) at 0x495790>
		enterelementnode <ll.xist.ns.html.li element object (1 child/1 attr) at 0x4958d0>
		enterelementnode <ll.xist.ns.html.li element object (1 child/no attrs) at 0x5f6130>
			textnode <ll.xist.xsc.Text content='1' at 0x5f4760>
		enterelementnode <ll.xist.ns.html.li element object (1 child/1 attr) at 0x5f6570>

This works for the following attributes:

*	:attr:`entercontent`
*	:attr:`enterattrs`
*	:attr:`enterattr`
*	:attr:`enterelementnode`
*	:attr:`leaveelementnode`
*	:attr:`enterattrnode`
*	:attr:`leaveattrnode`

After the :meth:`~ll.xist.xsc.Node.walk` generator has been reentered and the
modified attribute has been taken into account all those attributes wil be
reset to their initial value (i.e. the value that has been passed to
:meth:`~ll.xist.xsc.Node.walk`).


The methods :meth:`~ll.xist.xsc.Node.walknodes` and :meth:`~ll.xist.xsc.Node.walkpaths`
---------------------------------------------------------------------------------------

In addition to :meth:`~ll.xist.xsc.Node.walk` two other methods are available:
:meth:`~ll.xist.xsc.Node.walknodes` and :meth:`~ll.xist.xsc.Node.walkpaths`.

These generators don't produce a cursor object like :meth:`~ll.xist.xsc.Node.walk`
does. :meth:`~ll.xist.xsc.Node.walknodes` produces the node itself as the
following example demonstrates:

.. sourcecode:: pycon
	:caption: Using :meth:`~ll.xist.xsc.Node.walknodes`

	>>> from ll.xist.ns import html
	>>> e = html.ul(html.li(i) for i in range(3))
	>>> for node in e.walknodes():
	... 	print(repr(node))
	...
	<ll.xist.ns.html.ul element object (3 children/no attrs) at 0x43fbb0>
	<ll.xist.ns.html.li element object (1 child/no attrs) at 0x452750>
	<ll.xist.xsc.Text content='0' at 0x5b1670>
	<ll.xist.ns.html.li element object (1 child/no attrs) at 0x452830>
	<ll.xist.xsc.Text content='1' at 0x5b16e8>
	<ll.xist.ns.html.li element object (1 child/no attrs) at 0x5b30d0>
	<ll.xist.xsc.Text content='2' at 0x5b1760>

:meth:`~ll.xist.xsc.Node.walkpaths` produces the path. This is a copy of the
path, so it won't be changed once :meth:`~ll.xist.xsc.Node.walkpaths` is
reentered:

.. sourcecode:: pycon
	:caption: Using :meth:`~ll.xist.xsc.Node.walkpaths`

	>>> from ll.xist.ns import html
	>>> e = html.ul(html.li(i) for i in range(3))
	>>> for path in e.walkpaths():
	... 	print([f"{n.__class__.__module__}.{n.__class__.__qualname__}" for n in path])
	...
	['ll.xist.ns.html.ul']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li', 'll.xist.xsc.Text']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li', 'll.xist.xsc.Text']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li']
	['ll.xist.ns.html.ul', 'll.xist.ns.html.li', 'll.xist.xsc.Text']


Filtering the output of the tree traversal
------------------------------------------

All three tree traversal methods provide an additional argument (``*selectors``)
that can be used to filter which nodes/paths are produced. This argument can be
specified multiple times (which also means that all other arguments must be
passed as keyword arguments).


Passing a node class
~~~~~~~~~~~~~~~~~~~~

In the simplest case you can pass a :class:`~ll.xist.xsc.Node` subclass to get
only instances of that class. The following example prints all the links on the
Python home page:

.. sourcecode:: python
	:caption: Finding all links on the Python home page

	from ll.xist import xsc, parse
	from ll.xist.ns import xml, html

	doc = parse.tree(
		parse.URL("http://www.python.org"),
		parse.Expat(ns=True),
		parse.Node(pool=xsc.Pool(xml, html, chars))
	)

	for node in doc.walknodes(html.a):
		print(node.attrs.href)

This gives the output:

.. sourcecode:: text

	http://www.python.org/
	http://www.python.org/#left%2Dhand%2Dnavigation
	http://www.python.org/#content%2Dbody
	http://www.python.org/search
	http://www.python.org/about/
	http://www.python.org/news/
	http://www.python.org/doc/
	http://www.python.org/download/
	http://www.python.org/getit/
	http://www.python.org/community/
	...


Passing multiple selector arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also pass multiple classes to search for nodes that are an instance
of any of the classes.

The following example will print all header element on the Python home page:

.. sourcecode:: python
	:caption: Finding all headers on the Python home page

	from ll.xist import xsc, parse
	from ll.xist.ns import xml, html, chars

	doc = parse.tree(
		parse.URL("http://www.python.org"),
		parse.Expat(ns=True),
		parse.Node(pool=xsc.Pool(xml, html, chars))
	)

	for node in doc.walknodes(html.h1, html.h2, html.h3, html.h4, html.h5, html.h6):
		print(node.string())

This will output:

.. sourcecode:: text

	<h1 id="logoheader">
	  <a accesskey="1" href="http://www.python.org/" id="logolink">
	    <img alt="homepage" border="0" id="logo" src="http://www.python.org/images/python-logo.gif" />
	  </a>
	</h1>
	<h4><a href="http://www.python.org/about/help/">Help</a></h4>
	<h4><a href="http://pypi.python.org/pypi" title="Repository of Python Software">Package Index</a></h4>
	<h4><a href="http://www.python.org/download/releases/2.7.3/">Quick Links (2.7.3)</a></h4>
	<h4><a href="http://www.python.org/download/releases/3.3.0/">Quick Links (3.3.0)</a></h4>
	<h4><a href="http://www.python.org/community/jobs/" title="Employers and Job Openings">Python Jobs</a></h4>
	<h4><a href="http://www.python.org/community/merchandise/" title="T-shirts &amp; more; a portion goes to the PSF">Python Merchandise</a></h4>
	<h4><a href="http://wiki.python.org/moin/" style="margin-top: 1.5em">Python Wiki</a></h4>
	<h4><a href="http://blog.python.org/" style="margin-top: 1.5em">Python Insider Blog</a></h4>
	<h4><a href="http://wiki.python.org/moin/Python2orPython3" style="margin-top: 1.5em">Python 2 or 3?</a></h4>
	<h4><a href="http://www.python.org/psf/donations/" style="color: #D58228; margin-top: 1.5em">Help Fund Python</a></h4>
	<h4><a href="http://wiki.python.org/moin/Languages">Non-English Resources</a></h4>
	<h1 class="pageheading">Python Programming Language – Official Website</h1>
	<h4>Support the Python Community</h4>
	<h4><a href="http://wiki.python.org/moin/Python2orPython3">Python 3</a> Poll</h4>
	<h4>NASA uses Python...</h4>
	<h4>What they are saying...</h4>
	<h4>Using Python For...</h4>
	<h2 class="news">Python 3.3.0 released</h2>
	<h2 class="news">Third rc for Python 3.3.0 released</h2>
	<h2 class="news">Python Software Foundation announces Distinguished Service Award</h2>
	<h2 class="news">ConFoo conference in Canada, February 25th - March 13th</h2>
	<h2 class="news">Second rc for Python 3.3.0 released</h2>
	<h2 class="news">First rc for Python 3.3.0 released</h2>
	<h2 class="news">Fifth annual pyArkansas conference to be held</h2>


Passing a callable
~~~~~~~~~~~~~~~~~~

It is also possible to pass a function to :meth:`~ll.xist.xsc.Node.walk`.
This function will be called for each visited node and gets passed the path to
the visited node. If the function returns true, the node will be output.

The following example will find all external links on the Python home page:

.. sourcecode:: python
	:caption: Finding external links on the Python home page

	from ll.xist import xsc, parse
	from ll.xist.ns import xml, html, chars

	doc = parse.tree(
		parse.URL("http://www.python.org"),
		parse.Expat(ns=True),
		parse.Node(pool=xsc.Pool(xml, html, chars))
	)

	def isextlink(path):
		return isinstance(path[-1], html.a) and not str(path[-1].attrs.href).startswith("http://www.python.org")

	for node in doc.walknodes(isextlink):
		print(node.attrs.href)

This gives the output:

.. sourcecode:: text

	http://docs.python.org/devguide/
	http://pypi.python.org/pypi
	http://docs.python.org/2/
	http://docs.python.org/3/
	http://wiki.python.org/moin/
	http://blog.python.org/
	http://wiki.python.org/moin/Python2orPython3
	http://wiki.python.org/moin/Languages
	http://wiki.python.org/moin/Languages
	...


:mod:`~ll.xist.xfind` selectors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The selector arguments for the walk methods get converted into a so called
:mod:`~ll.xist.xfind` selector. :mod:`~ll.xist.xfind` selectors look somewhat
like XPath expressions, but are implemented as pure Python expressions
(overloading various Python operators).

Every subclass of :class:`~ll.xist.xsc.Node` can be used as an xfind selector
and combined with other :mod:`~ll.xist.xfind` selector to create more complex
ones. For example searching for links that contain images works as follows:

.. sourcecode:: python
	:caption: Searching for :class:`~ll.xist.ns.html.img` inside :class:`~ll.xist.ns.html.a` with an :mod:`~ll.xist.xfind` expression

	for path in doc.walkpaths(html.a/html.img):
		print(path[-2].attrs.href, path[-1].attrs.src)

The output looks like this:

.. sourcecode:: text

	http://www.python.org/ http://www.python.org/images/python-logo.gif
	http://www.python.org/#left%2Dhand%2Dnavigation http://www.python.org/images/trans.gif
	http://www.python.org/#content%2Dbody http://www.python.org/images/trans.gif
	http://www.python.org/psf/donations/ http://www.python.org/images/donate.png
	http://wiki.python.org/moin/Languages http://www.python.org/images/worldmap.jpg
	http://www.python.org/about/success/usa/ http://www.python.org/images/success/nasa.jpg

If the :class:`~ll.xist.ns.html.img` elements are not immediate children of the
:class:`~ll.xist.ns.html.a` elements, the :mod:`~ll.xist.xfind` selector above
won't output them. In this case you can use a "decendant selector" instead of a
"child selector". To do this simply replace ``html.a/html.img`` with
``html.a//html.img``.

Apart from the ``/`` and ``//`` operators you can also use the ``|`` and
``&`` operators to combine :mod:`~ll.xist.xfind` selector:

.. sourcecode:: python

	from ll.xist import xsc, parse, xfind
	from ll.xist.ns import xml, html

	doc = parse.tree(
		parse.URL("http://www.python.org"),
		parse.Expat(ns=True),
		parse.Node(pool=xsc.Pool(xml, html, chars))
	)

	for node in doc.walknodes((html.a | html.area) & xfind.hasattr("href")):
		print(node.attrs.href)

Here's another example that finds all elements that have an ``id`` attribute:

.. sourcecode:: python

	from ll.xist import xsc, parse, xfind
	from ll.xist.ns import xml, html, chars

	doc = parse.tree(
		parse.URL("http://www.python.org"),
		parse.Expat(ns=True),
		parse.Node(pool=xsc.Pool(xml, html, chars))
	)

	for node in doc.walknodes(xfind.hasattr("id")):
		print(node.attrs.id)

The output looks like this:

.. sourcecode:: text

	screen-switcher-stylesheet
	logoheader
	logolink
	logo
	skiptonav
	skiptocontent
	utility-menu
	searchbox
	searchform
	...

For more examples refer to the documentation of the :mod:`~ll.xist.xfind`
module.


CSS selectors
~~~~~~~~~~~~~

It's also possible to use CSS selectors as selectors for the
:meth:`~ll.xist.xsc.Node.walk` method. The module :mod:`ll.xist.css` provides a
function :func:`~ll.xist.css.selector` that turns a CSS selector expression
into an :mod:`~ll.xist.xfind` selector:

.. sourcecode:: python
	:caption: Using CSS selectors as :mod:`~ll.xist.xfind` selectors

	from ll.xist import xsc, parse, css
	from ll.xist.ns import xml, html, chars

	doc = parse.tree(
		parse.URL("http://www.python.org"),
		parse.Expat(ns=True),
		parse.Node(pool=xsc.Pool(xml, html, chars))
	)

	for cursor in doc.walk(css.selector("div#menu ul.level-one li > a")):
		print(cursor.node.attrs.href)

This outputs all the first level links in the navigation:

.. sourcecode:: text

	http://www.python.org/about/
	http://www.python.org/news/
	http://www.python.org/doc/
	http://www.python.org/download/
	http://www.python.org/getit/
	http://www.python.org/community/
	http://www.python.org/psf/
	http://docs.python.org/devguide/

Most of the `CSS 3 selectors`__ are supported.

__ http://www.w3.org/TR/css3-selectors/

For more examples see the documentation of the :mod:`~ll.xist.css` module.
