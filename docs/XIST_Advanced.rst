Advanced topics
===============

Converter contexts
------------------

Converter contexts can be used to pass around information in recursive
calls to the :meth:`convert` and :meth:`mapped` methods.
A :class:`~ll.xist.xsc.Converter` object will be passed in all calls, so this
object is the place to store information. However if each element, procinst and
entity class decided on its own which attributes names to use, name collisions
would be inevitable. To avoid this, the following system is used.

When a class wants to store information in a converter, it has to define
a :class:`Context` class (normally derived from the :class:`Context`
class of its base class). The constructor must initialize the context object
to a initial state. You can get the context object for a certain class by
treating the converter as a dictionary with the class (or an instance) as the
key like this:

.. sourcecode:: python
	:caption: Defining and using a converter context

	from ll.xist import xsc

	class counter(xsc.Element):
		class Context(xsc.Element.Context):
			def __init__(self):
				xsc.Element.Context.__init__(self)
				self.count = 0

		def convert(self, converter):
			context = converter[self]
			node = xsc.Text(context.count)
			context.count += 1
			return node


Chaining pools and extending namespaces
---------------------------------------

When using :class:`ll.xist.xsc.Pool` objects it's possible to do some sort of
"namespace subclassing".

Registering a module in a pool not only registers the element, procinst and
entity classes in the pool for parsing, but each attribute of the module (as
long as it's weak referencable) is available as an attribute of the pool
itself:

.. sourcecode:: python
	:caption: Pool attributes

	from ll.xist import xsc
	from ll.xist.ns import html

	pool = xsc.Pool(html)
	print(pool.img)

This outputs ``<element class ll.xist.ns.html:img at 0x3eed00>``.

It's possible to chain pools together. When an attribute isn't found in
the first pool, it will be looked up in a second pool (the so called base
pool):

.. sourcecode:: python
	:caption: Pool chaining

	from ll.xist import xsc
	from ll.xist.ns import html, svg

	hpool = xsc.Pool(html)
	spool = xsc.Pool(svg, hpool)
	print(spool.img)

Here the :obj:`hpool` (containing the :mod:`html` namespace) will be used when
the attribute can't be found in :obj:`spool`. So this will again give the output
``<element class ll.xist.ns.html:img at 0x3eed00>``.

It's possible to get automatic pool chaining. If a module has an attribute
:attr:`__bases__` (which must be a sequence of modules), they will be wrapped
in a pool automatically and used as the base pools for the pool created for
the first module. This makes it possible to "overwrite" element classes in
existing namespaces. For example to replace the :class:`~ll.xist.ns.html.a`
class in :mod:`ll.xist.ns.html`, put the following into a module :mod:`html2`:

.. sourcecode:: python
	:caption: Automatic pool chaining (:file:`html2.py`)

	from ll.xist.ns import html

	__bases__ = [html]

	class a(html.a):
		xmlns = html.xmlns

		def convert(self, converter):
			node = html.a(self.content, self.attrs, target="_top")
			return node.convert(converter)

Now you can use the module in a pool:

.. sourcecode:: python
	:caption: Using a pool chain

	from ll.xist import xsc
	import html2

	pool = xsc.Pool(html2)
	print(pool.a, pool.b)

This outputs:

.. sourcecode:: pycon

	<element class html2:a at 0x113ec40> <element class ll.xist.ns.html:b at 0x1101fe0>

Note that such a chained pool can of course be used when parsing XML. The
parser will recursively search for the first class that has the appropriate
name when instantiating the tree nodes.


Conversion targets
------------------

The :obj:`converter` argument passed to the :meth:`convert` method has an
attribute :attr:`target` which is a module or pool and specifies the target
namespace to which :obj:`self` should be converted.

You can check which conversion is wanted by checking e.g. the :attr:`xmlns`
attribute. Once this is determined you can use element classes from the target
to create the required XML object tree. This makes it possible to customize
the conversion by passing a chained pool to the :meth:`convert` method that
extends an existing namespace.

The following example shows how an element be converted to two
different targets:

.. sourcecode:: python
	:caption: Using conversion targets

	from ll.xist import xsc
	from ll.xist.ns import html, fo

	class bold(xsc.Element):
		def convert(self, converter):
			if converter.target.xmlns == html.xmlns:
				node = converter.target.b(self.content)
			elif converter.target.xmlns == fo.xmlns:
				node = converter.target.inline(self.content, font_weight="bold")
			else:
				raise TypeError(f"unsupported conversion target {converter.target!r}")
			return node.convert(converter)

The default target for conversion is :mod:`ll.xist.ns.html`.
Other targets can be specified via the :obj:`target` argument in the
:class:`Converter` constructor or the :meth:`conv` method:

.. sourcecode:: pycon

	>>> from ll.xist.ns import html, fo
	>>> import foo # This is the code from above
	>>> print(foo.bold("foo").conv().string())
	<b>foo</b>
	>>> print(foo.bold("foo").conv(target=html).string())
	<b>foo</b>
	>>> print(foo.bold("foo").conv(target=fo).string())
	<inline font-weight="bold">foo</inline>


Validation and content models
-----------------------------

When generating HTML you might want to make sure that your generated code
doesn't contain any illegal element nesting (i.e. something bad like
``<p><p>foo</p></p>`` in HTML). The module :mod:`ll.xist.ns.html` does this
automatically:

.. sourcecode:: pycon

	>>> from ll.xist.ns import html
	>>> node = html.p(html.p(u"foo"))
	>>> print(node.string())
	/Users/walter/checkouts/LivingLogic.Python.xist/src/ll/xist/sims.py:222: \
	WrongElementWarning: element <ll.xist.ns.html.p element object (1 child/no attrs) at 0x270b30> \
	may not contain element <ll.xist.ns.html.p element object (1 child/no attrs) at 0x69850>
	  warnings.warn(WrongElementWarning(node, child, self.elements))
	<p><p>foo</p></p>

For your own elements you can specify the content model too. This is done by
setting the class attribute :attr:`model` inside the element class.
:attr:`model` must be an object that provides a :meth:`checkvalid` method.
This method will be called during parsing or publishing with the element as
an argument. When invalid content is detected, the Python warning framework
should be used to issue a warning.

The module :mod:`ll.xist.sims` contains several classes that provide simple
validation methods:

*	:class:`ll.xist.sims.Empty` can be used to ensure that the element doesn't
	have any content (like ``br`` and ``img`` in HTML).

*	:class:`ll.xist.sims.Any` does allow any content.

*	:class:`ll.xist.sims.NoElements` will warn about elements from the same
	namespace (elements from other namespaces will be OK).

*	:class:`ll.xist.sims.NoElementsOrText` will warn about elements from the
	same namespace and non-whitespace text content.

*	:class:`ll.xist.sims.Elements` will only allow the elements specified in
	the constructor.

*	:class:`ll.xist.sims.ElementsOrText` will only allow the elements specified
	in the constructor and text.

None of these classes will check the number of child elements or their
order.

For more info see the :mod:`ll.xist.sims` module.
