Transforming XIST trees
=======================

Apart from the :meth:`~ll.xist.xsc.Node.convert` method, XIST provides several
tools for manipulating an XML tree.


The :meth:`withsep` method
--------------------------

The method :meth:`~ll.xist.xscFrag.withsep` can be used to put a separator node
between the child nodes of an :class:`~ll.xist.xsc.Element` or
or a :class:`~ll.xist.xsc.Frag`:

.. sourcecode:: pycon

	>>> from ll.xist import xsc
	>>> from ll.xist.ns import html
	>>> node = html.div(range(10))
	>>> print(node.withsep(", ").string())
	<div>0, 1, 2, 3, 4, 5, 6, 7, 8, 9</div>


The :meth:`shuffled` method
---------------------------

The method :meth:`~ll.xist.xsc.Frag.shuffled` returns a shuffled version of the
:class:`~ll.xist.xsc.Element` or :class:`~ll.xist.xsc.Frag`:

.. sourcecode:: pycon

	>>> from ll.xist import xsc
	>>> from ll.xist.ns import html
	>>> node = html.div(range(10))
	>>> print(node.shuffled().withsep(", ").string())
	<div>8, 1, 3, 6, 7, 5, 2, 9, 4, 0</div>


The :meth:`reversed` method
---------------------------

The method :meth:`~ll.xist.xsc.Frag.reversed` returns a reversed version of an
element or fragment:

.. sourcecode:: pycon

	>>> from ll.xist import xsc
	>>> from ll.xist.ns import html
	>>> node = html.div(range(10))
	>>> print(node.reversed().withsep(",").string())
	<div>9,8,7,6,5,4,3,2,1,0</div>


The :meth:`mapped` method
-------------------------

The method :meth:`~ll.xist.xsc.Node.mapped` recursively walks the tree and
generates a new tree, where all the nodes are mapped through a function.
An example: To replace ``Python`` with ``Parrot`` in every text node on the
`Python home page`_, do the following:

.. sourcecode:: python

	from ll.xist import xsc, parse

	def p2p(node, converter):
		if isinstance(node, xsc.Text):
			node = node.replace("Python", "Parrot")
			node = node.replace("python", "parrot")
		return node

	node = parse.tree(
		parse.URL("http://www.python.org"),
		parse.Tidy(),
		parse.NS(html),
		parse.Node(pool=xsc.Pool(xml, html)),
	)
	node = node.mapped(p2p)
	node.write(open("parrot_index.html", "wb"))

The function must either return a new node, in which case this new node will
be used instead of the old one, or return the old node to tell
:meth:`~ll.xist.xsc.Node.mapped` that it should recursively continue with the
content of the node.

.. _Python home page: http://www.python.org/
