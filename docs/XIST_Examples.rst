.. _XIST_Examples:

XIST examples
=============


Creating HTML
-------------

You can create and output HTML like this:

.. sourcecode:: python

	from ll.xist import xsc
	from ll.xist.ns import html, xml, meta

	node = xsc.Frag(
		xml.XML(),
		html.DocTypeXHTML10transitional(),
		html.html(
			html.head(
				meta.contenttype(),
				html.title("Example page")
			),
			html.body(
				html.h1("Welcome to the example page"),
				html.p(
					"This example page has a link to the ",
					html.a("Python home page", href="http://www.python.org/"),
					"."
				)
			)
		)
	)

You can also use :keyword:`with` blocks (and the unary ``+`` operator) to
generate the same HTML:

.. sourcecode:: python

	from ll.xist import xsc
	from ll.xist.ns import html, xml, meta

	with xsc.build():
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
						with html.a():
							with xsc.addattr("href"):
								+xsc.Text(""http://www.python.org/"")
							+xsc.Text("Python home page")
						+xsc.Text(".")


Printing HTML
-------------

When you have an XIST tree you can print it with the :meth:`string` method like this:

.. sourcecode:: python

	from ll.xist import xsc
	from ll.xist.ns import html, xml, meta

	node = xsc.Frag(
		xml.XML(),
		html.DocTypeXHTML10transitional(),
		html.html(
			html.head(
				meta.contenttype(),
				html.title("Example page")
			),
			html.body(
				html.h1("Welcome to the example page"),
				html.p(
					"This example page has a link to the ",
					html.a("Python home page", href="http://www.python.org/"),
					"."
				)
			)
		)
	)

	print(node.string(encoding="us-ascii"))


When you want to save this into a file, use the :meth:`bytes` method instead of
:meth:`string`:

.. sourcecode:: python

	with open("example.xml", "wb") as f:
		f.write(node.bytes(encoding="us-ascii"))


Defining new elements
---------------------

You can define new elements and how they should be converted to HTML
(or other XML vocabularies) like this:

.. sourcecode:: python

	from ll.xist import xsc
	from ll.xist.ns import html, xml, meta

	class cheeseshoplink(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class name(xsc.TextAttr): pass

		def convert(self, converter):
			e = html.a(
				self.attrs.name,
				href=("http://cheeseshop.python.org/pypi/", self.attrs.name)
			)
			return e.convert(converter)

	names = ["ll-xist", "cx_Oracle", "PIL"]

	node = xsc.Frag(
		xml.XML(),
		html.DocTypeXHTML10transitional(),
		html.html(
			html.head(
				meta.contenttype(),
				html.title("Cheeseshop links")
			),
			html.body(
				html.h1("Cheeseshop links"),
				html.ul(html.li(cheeseshoplink(name=name)) for name in names)
			)
		)
	)

	print(node.conv().string(encoding="us-ascii"))


Parsing HTML
------------

Parsing HTML is done like this:

.. sourcecode:: python

	from ll.xist import parse
	from ll.xist.ns import html

	node = parse.tree(
		parse.URL("http://www.python.org/"),
		parse.Tidy(),
		parse.NS(html),
		parse.Node()
	)


Finding and counting nodes
--------------------------

The following example shows you how to output the URLs of all images
inside links on Python's homepage:

.. sourcecode:: pycon

	>>> from ll.xist import parse
	>>> from ll.xist.ns import html
	>>> node = parse.tree(
	... 	parse.URL("http://www.python.org/"),
	... 	parse.Expat(ns=True),
	... 	parse.Node()
	... )
	>>> for img in node.walknodes(html.a/html.img):
	...    print(img.attrs.src)
	... 
	http://www.python.org/images/python-logo.gif
	http://www.python.org/images/trans.gif
	http://www.python.org/images/trans.gif
	http://www.python.org/images/success/nasa.jpg

If you want to output both the links and the image URLs, do the following:

.. sourcecode:: pycon

	>>> from ll.xist import parse, xfind
	>>> from ll.xist.ns import html
	>>> node = parse.tree(
	... 	parse.URL("http://www.python.org/"),
	... 	parse.Expat(ns=True),
	... 	parse.Node()
	... )
	>>> for path in node.walkpaths(html.a/html.img):
	...    print(path[-2].attrs.href, path[-1].attrs.src)
	http://www.python.org/ http://www.python.org/images/python-logo.gif
	http://www.python.org/#left%2dhand%2dnavigation http://www.python.org/images/trans.gif
	http://www.python.org/#content%2dbody http://www.python.org/images/trans.gif
	http://www.python.org/about/success/usa http://www.python.org/images/success/nasa.jpg

If you want to count the number of links on the page you can do the following:

	>>> from ll import misc
	>>> from ll.xist import parse
	>>> from ll.xist.ns import html
	>>> node = parse.tree(
	... 	parse.URL("http://www.python.org/"),
	... 	parse.Expat(ns=True),
	... 	parse.Node()
	... )
	>>> misc.count(node.walk(html.a))
	83


Replacing text
--------------

This example demonstrates how to make a copy of an XML tree with some
text replacements:

.. sourcecode:: python

	from ll.xist import xsc, parse

	def p2p(node, converter):
		if isinstance(node, xsc.Text):
			node = node.replace("Python", "Parrot")
			node = node.replace("python", "parrot")
		return node

	node = parse.tree(
		parse.URL("http://www.python.org/"),
		parse.Expat(ns=True),
		parse.Node()
	)

	node = node.mapped(p2p)
	node.write(open("parrot_index.html", "wb"))


Converting HTML to XIST code
----------------------------

The class :class:`ll.xist.present.CodePresenter` makes it possible to output an
XIST tree as usable Python source code:

.. sourcecode:: pycon

	>>> from ll.xist import parse, present
	>>> node = parse.tree(
	... 	parse.URL("http://www.python.org/"),
	... 	parse.Expat(ns=True),
	... 	parse.Node()
	... )
	>>> print(present.CodePresenter(node))
	ll.xist.xsc.Frag(
		ll.xist.ns.html.html(
			ll.xist.ns.html.head(
				ll.xist.ns.html.meta(
					http_equiv='content-type',
					content='text/html; charset=utf-8'
				),
				ll.xist.ns.html.title(
					'Python Programming Language -- Official Website'
				),
				ll.xist.ns.html.meta(
					name='keywords',
					content='python programming language object oriented web free source'
				),
				[... Many lines deleted ...]
							u'\n\tCopyright \xa9 1990-2007, ',
							ll.xist.ns.html.a(
								'Python Software Foundation',
								href='http://www.python.org/psf'
							),
							ll.xist.ns.html.br(),
							ll.xist.ns.html.a(
								'Legal Statements',
								href='http://www.python.org/about/legal'
							),
							'\n      ',
							id='footer'
						),
						'\n\n\n    ',
						id='body-main'
					),
					'\n  ',
					id='content-body'
				),
				'\n'
			),
			lang='en'
		)
	)


Using converter contexts to pass information between elements
-------------------------------------------------------------

Converter contexts can be used to pass information between elements.
The following example will generate HTML ``<h1>``, ..., ``<h6>`` elements
according to the nesting depth of a ``<section>`` element.

.. sourcecode:: python

	from ll.xist import xsc

	class section(xsc.Element):
		class Attrs(xsc.Element.Attrs):
			class title(xsc.TextAttr): pass

		class Context(xsc.Element.Context):
			def __init__(self):
				xsc.Element.Context.__init__(self)
				self.level = 1

		def convert(self, converter):
			context = converter[self]
			elementname = f"h{min(context.level, 6)}"
			node = xsc.Frag(
				getattr(converter.target, elementname)(self.attrs.title),
				self.content
			)
			context.level += 1
			node = node.convert(converter)
			context.level -= 1
			return node

	with xsc.build():
		with section(title="Python Tutorial") as document:
			with section(title="Using the Python Interpreter"):
				with section(title="Invoking the Interpreter"):
					+section(title="Argument Passing")
					+section(title="Interactive Mode")
				with section(title="The Interpreter and Its Environment"):
					+section(title="Error Handling")
					+section(title="Executable Python Scripts")
					+section(title="Source Code Encoding")
					+section(title="The Interactive Startup File")

	print(document.conv().string())

The output of this script will be:

.. sourcecode:: html

	<h1>Python Tutorial</h1>
	<h2>Using the Python Interpreter</h2>
	<h3>Invoking the Interpreter</h3>
	<h4>Argument Passing</h4>
	<h4>Interactive Mode</h4>
	<h3>The Interpreter and Its Environment</h3>
	<h4>Error Handling</h4>
	<h4>Executable Python Scripts</h4>
	<h4>Source Code Encoding</h4>
	<h4>The Interactive Startup File</h4>
	</tty>


Formatting HTML as plain text
-----------------------------

The function :func:`ll.xist.ns.html.astext` can to used to format HTML into
plain text:

.. sourcecode:: python

	from ll.xist.ns import html

	e = html.div(
		html.h1("The Zen of Python, by Tim Peters"),
		html.ul(
			html.li("Beautiful is better than ugly."),
			html.li("Explicit is better than implicit."),
			html.li("Simple is better than complex."),
			html.li("Complex is better than complicated."),
			html.li("Flat is better than nested."),
			html.li("Sparse is better than dense."),
			html.li("Readability counts."),
			html.li("Special cases aren't special enough to break the rules."),
			html.li("Although practicality beats purity."),
			html.li("Errors should never pass silently."),
			html.li("Unless explicitly silenced."),
			html.li("In the face of ambiguity, refuse the temptation to guess."),
			html.li("There should be one-- and preferably only one --obvious way to do it."),
			html.li("Although that way may not be obvious at first unless you're Dutch."),
			html.li("Now is better than never."),
			html.li("Although never is often better than *right* now."),
			html.li("If the implementation is hard to explain, it's a bad idea."),
			html.li("If the implementation is easy to explain, it may be a good idea."),
			html.li("Namespaces are one honking great idea -- let's do more of those!"),
		)
	)

	print(html.astext(e, width=40))

This will output:

.. sourcecode:: text

	The Zen of Python, by Tim Peters
	================================

	*  Beautiful is better than ugly.

	*  Explicit is better than implicit.

	*  Simple is better than complex.

	*  Complex is better than complicated.

	*  Flat is better than nested.

	*  Sparse is better than dense.

	*  Readability counts.

	*  Special cases aren't special enough
	   to break the rules.

	*  Although practicality beats purity.

	*  Errors should never pass silently.

	*  Unless explicitly silenced.

	*  In the face of ambiguity, refuse the
	   temptation to guess.

	*  There should be one-- and preferably
	   only one --obvious way to do it.

	*  Although that way may not be obvious
	   at first unless you're Dutch.

	*  Now is better than never.

	*  Although never is often better than
	   *right* now.

	*  If the implementation is hard to
	   explain, it's a bad idea.

	*  If the implementation is easy to
	   explain, it may be a good idea.

	*  Namespaces are one honking great idea
	   -- let's do more of those!
